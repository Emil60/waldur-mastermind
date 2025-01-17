from django.core.management.base import BaseCommand

from waldur_core.structure import models as structure_models
from waldur_core.structure.utils import move_project


class Command(BaseCommand):
    help = "Move Waldur project to a different organization."

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--project',
            dest='project_uuid',
            required=True,
            help='UUID of a project to move.',
        )
        parser.add_argument(
            '-c',
            '--customer',
            dest='customer_uuid',
            required=True,
            help='Target organization UUID',
        )

    def handle(self, project_uuid, customer_uuid, *args, **options):
        try:
            project = structure_models.Project.available_objects.get(uuid=project_uuid)
        except structure_models.Project.DoesNotExist:
            self.stdout.write(self.style.ERROR('Project is not found.'))
            return
        except ValueError:
            self.stdout.write(self.style.ERROR('Project UUID is not valid.'))
            return

        try:
            customer = structure_models.Customer.objects.get(uuid=customer_uuid)
        except structure_models.Customer.DoesNotExist:
            self.stdout.write(self.style.ERROR('Organization is not found.'))
            return
        except ValueError:
            self.stdout.write(self.style.ERROR('Organization UUID is not valid.'))
            return

        move_project(project, customer)
        self.stdout.write(
            self.style.SUCCESS('Project has been moved to another organization.')
        )
