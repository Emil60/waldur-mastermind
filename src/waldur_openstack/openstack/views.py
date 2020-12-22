import logging

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import decorators, exceptions, response
from rest_framework import serializers as rf_serializers
from rest_framework import status

from waldur_core.core import exceptions as core_exceptions
from waldur_core.core import utils as core_utils
from waldur_core.core import validators as core_validators
from waldur_core.core import views as core_views
from waldur_core.logging.loggers import event_logger
from waldur_core.structure import filters as structure_filters
from waldur_core.structure import permissions as structure_permissions
from waldur_core.structure import views as structure_views

from . import executors, filters, models, serializers

logger = logging.getLogger(__name__)


class OpenStackServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.OpenStackService.objects.all().order_by('id')
    serializer_class = serializers.ServiceSerializer

    def list(self, request, *args, **kwargs):
        """
        To create a service, issue a **POST** to */api/openstack/* as a customer owner.

        You can create service based on shared service settings. Example:

        .. code-block:: http

            POST /api/openstack/ HTTP/1.1
            Content-Type: application/json
            Accept: application/json
            Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
            Host: example.com

            {
                "name": "Common OpenStack",
                "customer": "http://example.com/api/customers/1040561ca9e046d2b74268600c7e1105/",
                "settings": "http://example.com/api/service-settings/93ba615d6111466ebe3f792669059cb4/"
            }

        Or provide your own credentials. Example:

        .. code-block:: http

            POST /api/openstack/ HTTP/1.1
            Content-Type: application/json
            Accept: application/json
            Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
            Host: example.com

            {
                "name": "My OpenStack",
                "customer": "http://example.com/api/customers/1040561ca9e046d2b74268600c7e1105/",
                "backend_url": "http://keystone.example.com:5000/v2.0",
                "username": "admin",
                "password": "secret"
            }
        """

        return super(OpenStackServiceViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        To update OpenStack service issue **PUT** or **PATCH** against */api/openstack/<service_uuid>/*
        as a customer owner. You can update service's `name` and `available_for_all` fields.

        Example of a request:

        .. code-block:: http

            PUT /api/openstack/c6526bac12b343a9a65c4cd6710666ee/ HTTP/1.1
            Content-Type: application/json
            Accept: application/json
            Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
            Host: example.com

            {
                "name": "My OpenStack2"
            }

        To remove OpenStack service, issue **DELETE** against */api/openstack/<service_uuid>/* as
        staff user or customer owner.
        """
        return super(OpenStackServiceViewSet, self).retrieve(request, *args, **kwargs)


class OpenStackServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.OpenStackServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer
    filterset_class = filters.OpenStackServiceProjectLinkFilter

    def list(self, request, *args, **kwargs):
        """
        In order to be able to provision OpenStack resources, it must first be linked to a project. To do that,
        **POST** a connection between project and a service to */api/openstack-service-project-link/*
        as stuff user or customer owner.

        Example of a request:

        .. code-block:: http

            POST /api/openstack-service-project-link/ HTTP/1.1
            Content-Type: application/json
            Accept: application/json
            Authorization: Token c84d653b9ec92c6cbac41c706593e66f567a7fa4
            Host: example.com

            {
                "project": "http://example.com/api/projects/e5f973af2eb14d2d8c38d62bcbaccb33/",
                "service": "http://example.com/api/openstack/b0e8a4cbd47c4f9ca01642b7ec033db4/"
            }

        To remove a link, issue DELETE to URL of the corresponding connection as stuff user or customer owner.
        """
        return super(OpenStackServiceProjectLinkViewSet, self).list(
            request, *args, **kwargs
        )


class FlavorViewSet(structure_views.BaseServicePropertyViewSet):
    """
    VM instance flavor is a pre-defined set of virtual hardware parameters that the instance will use:
    CPU, memory, disk size etc. VM instance flavor is not to be confused with VM template -- flavor is a set of virtual
    hardware parameters whereas template is a definition of a system to be installed on this instance.
    """

    queryset = models.Flavor.objects.all().order_by('settings', 'cores', 'ram', 'disk')
    serializer_class = serializers.FlavorSerializer
    lookup_field = 'uuid'
    filterset_class = filters.FlavorFilter


class ImageViewSet(structure_views.BaseServicePropertyViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    lookup_field = 'uuid'
    filterset_class = filters.ImageFilter


class VolumeTypeViewSet(structure_views.BaseServicePropertyViewSet):
    queryset = models.VolumeType.objects.all().order_by('settings', 'name')
    serializer_class = serializers.VolumeTypeSerializer
    lookup_field = 'uuid'
    filterset_class = filters.VolumeTypeFilter


class SecurityGroupViewSet(structure_views.BaseResourceViewSet):
    queryset = models.SecurityGroup.objects.all()
    serializer_class = serializers.SecurityGroupSerializer
    filterset_class = filters.SecurityGroupFilter
    disabled_actions = [
        'create',
        'pull',
    ]  # pull operation should be implemented in WAL-323

    def default_security_group_validator(security_group):
        if security_group.name == 'default':
            raise exceptions.ValidationError(
                {'name': _('Default security group is managed by OpenStack itself.')}
            )

    update_validators = partial_update_validators = (
        structure_views.ResourceViewSet.update_validators
        + [default_security_group_validator]
    )
    update_executor = executors.SecurityGroupUpdateExecutor
    partial_update_serializer_class = (
        update_serializer_class
    ) = serializers.SecurityGroupUpdateSerializer

    destroy_validators = structure_views.ResourceViewSet.destroy_validators + [
        default_security_group_validator
    ]
    delete_executor = executors.SecurityGroupDeleteExecutor

    @decorators.action(detail=True, methods=['POST'])
    def set_rules(self, request, uuid=None):
        """ WARNING! Auto-generated HTML form is wrong for this endpoint. List should be defined as input.

            Example:
            [
                {
                    "protocol": "tcp",
                    "from_port": 1,
                    "to_port": 10,
                    "cidr": "10.1.1.0/24"
                }
            ]
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        executors.PushSecurityGroupRulesExecutor().execute(self.get_object())
        return response.Response(
            {'status': _('Rules update was successfully scheduled.')},
            status=status.HTTP_202_ACCEPTED,
        )

    set_rules_validators = [core_validators.StateValidator(models.Tenant.States.OK)]
    set_rules_serializer_class = serializers.SecurityGroupRuleListUpdateSerializer


class FloatingIPViewSet(structure_views.BaseResourceViewSet):
    queryset = models.FloatingIP.objects.all().order_by('address')
    serializer_class = serializers.FloatingIPSerializer
    filterset_class = filters.FloatingIPFilter
    disabled_actions = ['update', 'partial_update', 'create']
    delete_executor = executors.FloatingIPDeleteExecutor
    pull_executor = executors.FloatingIPPullExecutor

    def list(self, request, *args, **kwargs):
        """
        To get a list of all available floating IPs, issue **GET** against */api/floating-ips/*.
        Floating IPs are read only. Each floating IP has fields: 'address', 'status'.

        Status *DOWN* means that floating IP is not linked to a VM, status *ACTIVE* means that it is in use.
        """

        return super(FloatingIPViewSet, self).list(request, *args, **kwargs)

    @decorators.action(detail=True, methods=['post'])
    def attach_to_port(self, request, uuid=None):
        floating_ip: models.FloatingIP = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        port: models.Port = serializer.validated_data['port']
        if port.state != models.Port.States.OK:
            raise core_exceptions.IncorrectStateException(
                _(
                    'The port [%(port)s] is expected to have [OK] state, but actual one is [%(state)s]'
                )
                % {'port': port, 'state': port.get_state_display()}
            )
        if port.tenant != floating_ip.tenant:
            raise exceptions.ValidationError(
                {
                    'detail': _(
                        'The port [%(port)s] is expected to belong to the same tenant [%(tenant)s] , but actual one is [%(actual_tenant)s]'
                    )
                    % {
                        'port': port,
                        'tenant': floating_ip.tenant,
                        'actual_tenant': port.tenant,
                    }
                }
            )

        executors.FloatingIPAttachExecutor().execute(
            floating_ip, port=core_utils.serialize_instance(port)
        )
        return response.Response(
            {'status': _('attaching was scheduled')}, status=status.HTTP_202_ACCEPTED
        )

    attach_to_port_serializer_class = serializers.FloatingIPAttachSerializer
    attach_to_port_validators = [
        core_validators.StateValidator(models.FloatingIP.States.OK)
    ]

    @decorators.action(detail=True, methods=['post'])
    def detach_from_port(self, request=None, uuid=None):
        floating_ip: models.FloatingIP = self.get_object()
        if not floating_ip.port:
            raise exceptions.ValidationError(
                {
                    'port': _('Floating IP [%(fip)s] is not attached to any port.')
                    % {'fip': floating_ip}
                }
            )
        executors.FloatingIPDetachExecutor().execute(floating_ip)
        return response.Response(
            {'status': _('detaching was scheduled')}, status=status.HTTP_202_ACCEPTED
        )

    detach_from_port_validators = [
        core_validators.StateValidator(models.FloatingIP.States.OK)
    ]


class TenantViewSet(structure_views.ImportableResourceViewSet):
    queryset = models.Tenant.objects.all()
    serializer_class = serializers.TenantSerializer
    filterset_class = structure_filters.BaseResourceFilter

    create_executor = executors.TenantCreateExecutor
    update_executor = executors.TenantUpdateExecutor
    pull_executor = executors.TenantPullExecutor

    importable_resources_backend_method = 'get_tenants_for_import'
    importable_resources_serializer_class = serializers.TenantImportableSerializer
    importable_resources_permissions = [structure_permissions.is_staff]
    import_resource_serializer_class = serializers.TenantImportSerializer
    import_resource_permissions = [structure_permissions.is_staff]
    import_resource_executor = executors.TenantImportExecutor

    def delete_permission_check(request, view, obj=None):
        if not obj:
            return
        if obj.service_project_link.service.settings.shared:
            if settings.WALDUR_OPENSTACK['MANAGER_CAN_MANAGE_TENANTS']:
                structure_permissions.is_manager(request, view, obj)
            elif settings.WALDUR_OPENSTACK['ADMIN_CAN_MANAGE_TENANTS']:
                structure_permissions.is_administrator(request, view, obj)
            else:
                structure_permissions.is_owner(request, view, obj)
        else:
            structure_permissions.is_administrator(request, view, obj)

    delete_executor = executors.TenantDeleteExecutor
    destroy_permissions = [
        delete_permission_check,
        structure_permissions.check_access_to_services_management,
    ]
    create_permissions = update_permissions = partial_update_permissions = [
        structure_permissions.check_access_to_services_management,
    ]

    @decorators.action(detail=True, methods=['post'])
    def set_quotas(self, request, uuid=None):
        """
        A quota can be set for a particular tenant. Only staff users can do that.
        In order to set quota submit **POST** request to */api/openstack-tenants/<uuid>/set_quotas/*.
        The quota values are propagated to the backend.

        The following quotas are supported. All values are expected to be integers:

        - instances - maximal number of created instances.
        - ram - maximal size of ram for allocation. In MiB_.
        - storage - maximal size of storage for allocation. In MiB_.
        - vcpu - maximal number of virtual cores for allocation.
        - security_group_count - maximal number of created security groups.
        - security_group_rule_count - maximal number of created security groups rules.
        - volumes - maximal number of created volumes.
        - snapshots - maximal number of created snapshots.

        It is possible to update quotas by one or by submitting all the fields in one request.
        Waldur will attempt to update the provided quotas. Please note, that if provided quotas are
        conflicting with the backend (e.g. requested number of instances is below of the already existing ones),
        some quotas might not be applied.

        .. _MiB: http://en.wikipedia.org/wiki/Mebibyte

        Example of a valid request (token is user specific):

        .. code-block:: http

            POST /api/openstack-tenants/c84d653b9ec92c6cbac41c706593e66f567a7fa4/set_quotas/ HTTP/1.1
            Content-Type: application/json
            Accept: application/json
            Host: example.com

            {
                "instances": 30,
                "ram": 100000,
                "storage": 1000000,
                "vcpu": 30,
                "security_group_count": 100,
                "security_group_rule_count": 100,
                "volumes": 10,
                "snapshots": 20
            }

        Response code of a successful request is **202 ACCEPTED**.
        In case tenant is in a non-stable status, the response would be **409 CONFLICT**.
        In this case REST client is advised to repeat the request after some time.
        On successful completion the task will synchronize quotas with the backend.
        """
        tenant = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        quotas = dict(serializer.validated_data)
        for quota_name, limit in quotas.items():
            tenant.set_quota_limit(quota_name, limit)
        executors.TenantPushQuotasExecutor.execute(tenant, quotas=quotas)

        return response.Response(
            {'detail': _('Quota update has been scheduled')},
            status=status.HTTP_202_ACCEPTED,
        )

    set_quotas_permissions = [structure_permissions.is_staff]
    set_quotas_validators = [core_validators.StateValidator(models.Tenant.States.OK)]
    set_quotas_serializer_class = serializers.TenantQuotaSerializer

    @decorators.action(detail=True, methods=['post'])
    def create_network(self, request, uuid=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        network = serializer.save()

        executors.NetworkCreateExecutor().execute(network)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    create_network_validators = [
        core_validators.StateValidator(models.Tenant.States.OK)
    ]
    create_network_serializer_class = serializers.NetworkSerializer

    def external_network_is_defined(tenant):
        if not tenant.external_network_id:
            raise core_exceptions.IncorrectStateException(
                _(
                    'Cannot create floating IP if tenant external network is not defined.'
                )
            )

    @decorators.action(detail=True, methods=['post'])
    def create_floating_ip(self, request, uuid=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        floating_ip = serializer.save()

        executors.FloatingIPCreateExecutor.execute(floating_ip)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    create_floating_ip_validators = [
        core_validators.StateValidator(models.Tenant.States.OK),
        external_network_is_defined,
    ]
    create_floating_ip_serializer_class = serializers.FloatingIPSerializer

    @decorators.action(detail=True, methods=['post'])
    def pull_floating_ips(self, request, uuid=None):
        tenant = self.get_object()

        executors.TenantPullFloatingIPsExecutor.execute(tenant)
        return response.Response(status=status.HTTP_202_ACCEPTED)

    pull_floating_ips_validators = [
        core_validators.StateValidator(models.Tenant.States.OK)
    ]
    pull_floating_ips_serializer_class = rf_serializers.Serializer

    @decorators.action(detail=True, methods=['post'])
    def create_security_group(self, request, uuid=None):
        """
        Example of a request:

        .. code-block:: http

            {
                "name": "Security group name",
                "description": "description",
                "rules": [
                    {
                        "protocol": "tcp",
                        "from_port": 1,
                        "to_port": 10,
                        "cidr": "10.1.1.0/24"
                    },
                    {
                        "protocol": "udp",
                        "from_port": 10,
                        "to_port": 8000,
                        "cidr": "10.1.1.0/24"
                    }
                ]
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        security_group = serializer.save()

        executors.SecurityGroupCreateExecutor().execute(security_group)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    create_security_group_validators = [
        core_validators.StateValidator(models.Tenant.States.OK)
    ]
    create_security_group_serializer_class = serializers.SecurityGroupSerializer

    @decorators.action(detail=True, methods=['post'])
    def pull_security_groups(self, request, uuid=None):
        executors.TenantPullSecurityGroupsExecutor.execute(self.get_object())
        return response.Response(
            {'status': _('Security groups pull has been scheduled.')},
            status=status.HTTP_202_ACCEPTED,
        )

    pull_security_groups_validators = [
        core_validators.StateValidator(models.Tenant.States.OK)
    ]

    @decorators.action(detail=True, methods=['post'])
    def change_password(self, request, uuid=None):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        executors.TenantChangeUserPasswordExecutor.execute(self.get_object())
        return response.Response(
            {'status': _('Password update has been scheduled.')},
            status=status.HTTP_202_ACCEPTED,
        )

    change_password_serializer_class = serializers.TenantChangePasswordSerializer
    change_password_validators = [
        core_validators.StateValidator(models.Tenant.States.OK)
    ]

    @decorators.action(detail=True, methods=['post'])
    def pull_quotas(self, request, uuid=None):
        executors.TenantPullQuotasExecutor.execute(self.get_object())
        return response.Response(
            {'status': _('Quotas pull has been scheduled.')},
            status=status.HTTP_202_ACCEPTED,
        )

    pull_quotas_validators = [core_validators.StateValidator(models.Tenant.States.OK)]


class RouterViewSet(core_views.ReadOnlyActionsViewSet):
    lookup_field = 'uuid'
    queryset = models.Router.objects.all()
    filter_backends = (DjangoFilterBackend, structure_filters.GenericRoleFilter)
    filterset_class = filters.RouterFilter
    serializer_class = serializers.RouterSerializer

    @decorators.action(detail=True, methods=['POST'])
    def set_routes(self, request, uuid=None):
        router = self.get_object()
        serializer = self.get_serializer(router, data=request.data)
        serializer.is_valid(raise_exception=True)
        old_routes = router.routes
        new_routes = serializer.validated_data['routes']
        router.routes = new_routes
        router.save(update_fields=['routes'])
        executors.RouterSetRoutesExecutor().execute(router)

        event_logger.openstack_router.info(
            'Static routes have been updated.',
            event_type='openstack_router_updated',
            event_context={
                'router': router,
                'old_routes': old_routes,
                'new_routes': new_routes,
                'tenant_backend_id': router.tenant.backend_id,
            },
        )

        logger.info(
            'Static routes have been updated for router %s from %s to %s.',
            router,
            old_routes,
            new_routes,
        )

        return response.Response(
            {'status': _('Routes update was successfully scheduled.')},
            status=status.HTTP_202_ACCEPTED,
        )

    set_routes_serializer_class = serializers.RouterSetRoutesSerializer
    set_routes_validators = [core_validators.StateValidator(models.Router.States.OK)]


class PortViewSet(structure_views.BaseResourceViewSet):
    queryset = models.Port.objects.all()
    filter_backends = (DjangoFilterBackend, structure_filters.GenericRoleFilter)
    filterset_class = filters.PortFilter
    serializer_class = serializers.PortSerializer

    disabled_actions = ['create']
    update_executor = executors.PortUpdateExecutor
    delete_executor = executors.PortDeleteExecutor


class NetworkViewSet(structure_views.BaseResourceViewSet):
    queryset = models.Network.objects.all()
    serializer_class = serializers.NetworkSerializer
    filterset_class = filters.NetworkFilter

    disabled_actions = ['create']
    update_executor = executors.NetworkUpdateExecutor
    delete_executor = executors.NetworkDeleteExecutor
    pull_executor = executors.NetworkPullExecutor

    @decorators.action(detail=True, methods=['post'])
    def create_subnet(self, request, uuid=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subnet = serializer.save()
        enable_default_gateway = serializer.validated_data['enable_default_gateway']

        executors.SubNetCreateExecutor.execute(
            subnet, enable_default_gateway=enable_default_gateway
        )
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    create_subnet_validators = [
        core_validators.StateValidator(models.Network.States.OK)
    ]
    create_subnet_serializer_class = serializers.SubNetSerializer

    @decorators.action(detail=True, methods=['post'])
    def set_mtu(self, request, uuid=None):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        network = serializer.save()
        executors.SetMtuExecutor.execute(network)
        return response.Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    set_mtu_validators = [core_validators.StateValidator(models.Network.States.OK)]
    set_mtu_serializer_class = serializers.SetMtuSerializer


class SubNetViewSet(structure_views.BaseResourceViewSet):
    queryset = models.SubNet.objects.all()
    serializer_class = serializers.SubNetSerializer
    filterset_class = filters.SubNetFilter

    disabled_actions = ['create']
    update_executor = executors.SubNetUpdateExecutor
    delete_executor = executors.SubNetDeleteExecutor
    pull_executor = executors.SubNetPullExecutor

    def get_update_executor_kwargs(self, serializer):
        return {
            'enable_default_gateway': serializer.validated_data[
                'enable_default_gateway'
            ]
        }

    @decorators.action(detail=True, methods=['post'])
    def create_port(self, request, uuid=None):
        subnet = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        port = serializer.save()
        executors.PortCreateExecutor().execute(port, subnet_id=subnet.backend_id)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    create_port_serializer_class = serializers.PortSerializer

    create_port_validators = [core_validators.StateValidator(models.SubNet.States.OK)]
