import logging

from django.conf import settings
from django.db import transaction

from waldur_core.core import middleware
from waldur_core.core.utils import serialize_instance
from waldur_core.structure import models as structure_models
from waldur_core.structure import permissions as structure_permissions
from waldur_core.structure import signals as structure_signals
from waldur_mastermind.marketplace.models import Resource
from waldur_mastermind.marketplace_remote.utils import INVALID_RESOURCE_STATES

from . import PLUGIN_NAME, log, models, tasks

logger = logging.getLogger(__name__)


def update_remote_project_permission(sender, instance, user, **kwargs):
    if not settings.WALDUR_AUTH_SOCIAL['ENABLE_EDUTEAMS_SYNC']:
        return

    transaction.on_commit(
        lambda: tasks.update_remote_project_permissions.delay(
            serialize_instance(instance.project),
            serialize_instance(instance.user),
            instance.role,
            True,
            instance.expiration_time and instance.expiration_time.isoformat() or None,
        )
    )


def sync_permission_with_remote_project(
    sender, structure, user, role, signal, expiration_time=None, **kwargs
):
    if not settings.WALDUR_AUTH_SOCIAL['ENABLE_EDUTEAMS_SYNC']:
        return

    if user.registration_method != 'eduteams':
        return

    grant = signal == structure_signals.structure_role_granted

    transaction.on_commit(
        lambda: tasks.update_remote_project_permissions.delay(
            serialize_instance(structure),
            serialize_instance(user),
            role,
            grant,
            expiration_time and expiration_time.isoformat() or None,
        )
    )


def sync_permission_with_remote_customer(
    sender, structure, user, role, signal, expiration_time=None, **kwargs
):
    if not settings.WALDUR_AUTH_SOCIAL['ENABLE_EDUTEAMS_SYNC']:
        return

    if user.registration_method != 'eduteams':
        return

    if role != structure_models.CustomerRole.OWNER:
        # Skip support role synchronization
        return

    grant = signal == structure_signals.structure_role_granted

    transaction.on_commit(
        lambda: tasks.update_remote_customer_permissions.delay(
            serialize_instance(structure),
            serialize_instance(user),
            role,
            grant,
            expiration_time and expiration_time.isoformat() or None,
        )
    )


def create_request_when_project_is_updated(sender, instance, created=False, **kwargs):
    if created:
        return

    if not settings.WALDUR_AUTH_SOCIAL['ENABLE_EDUTEAMS_SYNC']:
        return

    user = middleware.get_current_user()

    if not user:
        return

    if not set(instance.tracker.changed()) & set(
        structure_models.PROJECT_DETAILS_FIELDS
    ):
        return

    qs = models.ProjectUpdateRequest.objects.filter(
        project=instance, state=models.ProjectUpdateRequest.States.PENDING
    )
    if qs.exists():
        qs.update(state=models.ProjectUpdateRequest.States.CANCELED)
    payload = {}
    for key in structure_models.PROJECT_DETAILS_FIELDS:
        payload[f'old_{key}'] = instance.tracker.previous(key)
        payload[f'new_{key}'] = getattr(instance, key)
        payload['created_by'] = user
    offering_ids = (
        Resource.objects.filter(project=instance, offering__type=PLUGIN_NAME)
        .exclude(state__in=INVALID_RESOURCE_STATES)
        .values_list('offering_id', flat=True)
        .distinct()
    )
    offerings = models.Offering.objects.filter(id__in=offering_ids)
    for offering in offerings:
        project_request = models.ProjectUpdateRequest.objects.create(
            project=instance,
            offering=offering,
            state=models.ProjectUpdateRequest.States.PENDING,
            **payload,
        )
        logger.info(
            "The project update request %s has been created by user %s",
            project_request,
            user,
        )
        # Auto-approve if possible
        # Code from waldur_mastermind.marketplace.permissions.user_is_service_provider_owner_or_service_provider_manager
        if structure_permissions._has_owner_access(
            user, offering.customer
        ) or offering.customer.has_user(
            user, role=structure_models.CustomerRole.SERVICE_MANAGER
        ):
            logger.info(
                "The user %s can automatically approve the request %s.",
                user,
                project_request,
            )
            project_request.approve(user, 'Auto approval')
        else:
            logger.info(
                "The user %s can not automatically approve the request %s. Manual approval is required.",
                user,
                project_request,
            )


def sync_remote_project_when_request_is_approved(
    sender, instance, created=False, **kwargs
):
    if not settings.WALDUR_AUTH_SOCIAL['ENABLE_EDUTEAMS_SYNC']:
        return

    if created:
        return

    if (
        not instance.tracker.has_changed('state')
        or instance.state != models.ProjectUpdateRequest.States.APPROVED
    ):
        return

    transaction.on_commit(
        lambda: tasks.sync_remote_project.delay(serialize_instance(instance))
    )


def delete_remote_project(sender, instance, **kwargs):
    project = instance
    transaction.on_commit(
        lambda: tasks.delete_remote_project.delay(
            serialize_instance(project),
        )
    )


def log_request_events(sender, instance, created=False, **kwargs):
    event_context = {'project': instance.project, 'offering': instance.offering}
    if created:
        log.event_logger.project_update_request.info(
            'Project update request has been created.',
            event_type='project_update_request_created',
            event_context=event_context,
        )
        return
    if not instance.tracker.has_changed('state'):
        return
    if instance.state == models.ProjectUpdateRequest.States.APPROVED:
        log.event_logger.project_update_request.info(
            'Project update request has been approved.',
            event_type='project_update_request_approved',
            event_context=event_context,
        )
    elif instance.state == models.ProjectUpdateRequest.States.REJECTED:
        log.event_logger.project_update_request.info(
            'Project update request has been rejected.',
            event_type='project_update_request_rejected',
            event_context=event_context,
        )


def trigger_order_item_callback(sender, instance, created=False, **kwargs):
    if not instance.callback_url:
        return

    if not instance.tracker.has_changed('state'):
        return

    transaction.on_commit(
        lambda: tasks.trigger_order_item_callback.delay(serialize_instance(instance))
    )


def notify_about_project_details_update(sender, instance, created=False, **kwargs):
    if created:
        return

    if (
        not instance.tracker.has_changed('state')
        or instance.state != models.ProjectUpdateRequest.States.APPROVED
    ):
        return

    transaction.on_commit(
        lambda: tasks.notify_about_project_details_update.delay(
            serialize_instance(instance)
        )
    )
