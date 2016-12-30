from decimal import Decimal
import pytz

from django.utils import timezone
from freezegun import freeze_time
from nodeconductor.core import utils as core_utils
from nodeconductor_assembly_waldur.packages.tests import factories as packages_factories
from rest_framework import test

from .. import models


class InvoiceTotalPriceUpdateTest(test.APITestCase):

    def create_package_template(self, single_component_price=10, components_amount=1):
        template = packages_factories.PackageTemplateFactory()
        first_component = template.components.first()
        first_component.price = single_component_price
        first_component.amount = components_amount
        first_component.save()
        return template

    def test_package_creation_does_not_increase_price_from_old_package_if_it_is_cheaper(self):
        # arrange
        old_component_price = 10
        new_component_price = old_component_price + 5
        start_date = timezone.datetime(2014, 2, 14, tzinfo=pytz.UTC)
        package_change_date = timezone.datetime(2014, 2, 20, tzinfo=pytz.UTC)

        with freeze_time(start_date):
            base_template = self.create_package_template(single_component_price=old_component_price)
            old_package = packages_factories.OpenStackPackageFactory(template=base_template)
            self.assertEqual(models.OpenStackItem.objects.count(), 1)
            customer = old_package.tenant.service_project_link.project.customer

        with freeze_time(package_change_date):
            old_package.delete()

            # advanced package
            new_template = self.create_package_template(single_component_price=new_component_price)
            packages_factories.OpenStackPackageFactory(
                template=new_template,
                tenant__service_project_link__project__customer=customer,
            )

        old_components_price = models.OpenStackItem.calculate_price_for_period(
            price=old_component_price,
            start=start_date,
            end=package_change_date - timezone.timedelta(days=1)
        )

        new_components_price = models.OpenStackItem.calculate_price_for_period(
            price=new_component_price,
            start=package_change_date,
            end=core_utils.month_end(package_change_date)
        )

        expected_price = old_components_price + new_components_price

        # assert
        self.assertEqual(models.Invoice.objects.count(), 1)
        invoices_price = models.Invoice.objects.first().price
        self.assertEqual(Decimal(expected_price), invoices_price)

    def test_package_creation_increases_price_from_old_package_if_it_is_more_expensive(self):
        # arrange
        old_component_price = 10
        new_component_price = old_component_price - 5
        start_date = timezone.datetime(2014, 2, 14, tzinfo=pytz.UTC)
        package_change_date = timezone.datetime(2014, 2, 20, tzinfo=pytz.UTC)

        with freeze_time(start_date):
            base_template = self.create_package_template(single_component_price=old_component_price)
            old_package = packages_factories.OpenStackPackageFactory(template=base_template)
            self.assertEqual(models.OpenStackItem.objects.count(), 1)
            customer = old_package.tenant.service_project_link.project.customer

        with freeze_time(package_change_date):
            old_package.delete()

            # advanced package
            new_template = self.create_package_template(single_component_price=new_component_price)
            packages_factories.OpenStackPackageFactory(
                template=new_template,
                tenant__service_project_link__project__customer=customer,
            )

        old_components_price = models.OpenStackItem.calculate_price_for_period(
            price=old_component_price,
            start=start_date,
            end=package_change_date
        )

        new_components_price = models.OpenStackItem.calculate_price_for_period(
            price=new_component_price,
            start=package_change_date + timezone.timedelta(days=1),
            end=core_utils.month_end(package_change_date)
        )

        expected_price = old_components_price + new_components_price

        # assert
        self.assertEqual(models.Invoice.objects.count(), 1)
        invoices_price = models.Invoice.objects.first().price
        self.assertEqual(Decimal(expected_price), invoices_price)

    def test_package_creation_does_not_increase_price_from_old_package_if_it_is_cheaper_in_the_end_of_the_month(self):

        # arrange
        old_component_price = 10
        new_component_price = old_component_price + 5
        start_date = timezone.datetime(2014, 2, 20, tzinfo=pytz.UTC)
        package_change_date = timezone.datetime(2014, 2, 28, tzinfo=pytz.UTC)

        with freeze_time(start_date):
            base_template = self.create_package_template(single_component_price=old_component_price)
            old_package = packages_factories.OpenStackPackageFactory(template=base_template)
            self.assertEqual(models.OpenStackItem.objects.count(), 1)
            customer = old_package.tenant.service_project_link.project.customer

        with freeze_time(package_change_date):
            old_package.delete()

            # advanced package
            new_template = self.create_package_template(single_component_price=new_component_price)
            packages_factories.OpenStackPackageFactory(
                template=new_template,
                tenant__service_project_link__project__customer=customer,
            )

        old_components_price = models.OpenStackItem.calculate_price_for_period(
            price=old_component_price,
            start=start_date,
            end=package_change_date - timezone.timedelta(days=1)
        )

        new_components_price = models.OpenStackItem.calculate_price_for_period(
            price=new_component_price,
            start=package_change_date,
            end=core_utils.month_end(package_change_date)
        )

        expected_price = old_components_price + new_components_price

        # assert
        self.assertEqual(models.Invoice.objects.count(), 1)
        invoices_price = models.Invoice.objects.first().price
        self.assertEqual(Decimal(expected_price), invoices_price)

    def test_package_creation_increases_price_from_old_package_if_it_is_more_expensive_in_the_end_of_the_month(self):
        # arrange
        old_component_price = 15
        new_component_price = old_component_price - 5
        start_date = timezone.datetime(2014, 2, 20, tzinfo=pytz.UTC)
        package_change_date = timezone.datetime(2014, 2, 28, tzinfo=pytz.UTC)

        with freeze_time(start_date):
            base_template = self.create_package_template(single_component_price=old_component_price)
            old_package = packages_factories.OpenStackPackageFactory(template=base_template)
            self.assertEqual(models.OpenStackItem.objects.count(), 1)
            customer = old_package.tenant.service_project_link.project.customer

        with freeze_time(package_change_date):
            old_package.delete()

            # advanced package
            new_template = self.create_package_template(single_component_price=new_component_price)
            packages_factories.OpenStackPackageFactory(
                template=new_template,
                tenant__service_project_link__project__customer=customer,
            )

        old_components_price = models.OpenStackItem.calculate_price_for_period(
            price=old_component_price,
            start=start_date,
            end=package_change_date
        )

        new_components_price = models.OpenStackItem.calculate_price_for_period(
            price=new_component_price,
            start=package_change_date + timezone.timedelta(days=1),
            end=core_utils.month_end(package_change_date + timezone.timedelta(days=1))
        )

        expected_price = old_components_price + new_components_price

        # assert
        self.assertEqual(models.Invoice.objects.count(), 1)
        invoices_price = models.Invoice.objects.first().price
        self.assertEqual(Decimal(expected_price), invoices_price)

    def test_package_creation_does_not_increase_price_for_cheaper_1_day_long_old_package_in_the_end_of_the_month(self):

        # arrange
        old_component_price = 5
        new_component_price = old_component_price + 5
        start_date = timezone.datetime(2014, 2, 27, tzinfo=pytz.UTC)
        package_change_date = timezone.datetime(2014, 2, 28, tzinfo=pytz.UTC)

        with freeze_time(start_date):
            base_template = self.create_package_template(single_component_price=old_component_price)
            old_package = packages_factories.OpenStackPackageFactory(template=base_template)
            self.assertEqual(models.OpenStackItem.objects.count(), 1)
            customer = old_package.tenant.service_project_link.project.customer

        with freeze_time(package_change_date):
            old_package.delete()

            # advanced package
            new_template = self.create_package_template(single_component_price=new_component_price)
            packages_factories.OpenStackPackageFactory(
                template=new_template,
                tenant__service_project_link__project__customer=customer,
            )

        old_components_price = models.OpenStackItem.calculate_price_for_period(
            price=old_component_price,
            start=start_date,
            end=package_change_date - timezone.timedelta(days=1)
        )

        new_components_price = models.OpenStackItem.calculate_price_for_period(
            price=new_component_price,
            start=package_change_date,
            end=core_utils.month_end(package_change_date)
        )

        expected_price = old_components_price + new_components_price

        # assert
        self.assertEqual(models.Invoice.objects.count(), 1)
        invoices_price = models.Invoice.objects.first().price
        self.assertEqual(Decimal(expected_price), invoices_price)

    def test_package_creation_does_not_increase_price_for_cheaper_1_day_long_old_package_in_the_same_day(self):

        # arrange
        old_component_price = 10
        new_component_price = old_component_price + 5
        start_date = timezone.datetime(2014, 2, 26, tzinfo=pytz.UTC)
        package_change_date = start_date

        with freeze_time(start_date):
            base_template = self.create_package_template(single_component_price=old_component_price)
            old_package = packages_factories.OpenStackPackageFactory(template=base_template)
            self.assertEqual(models.OpenStackItem.objects.count(), 1)
            customer = old_package.tenant.service_project_link.project.customer

        with freeze_time(package_change_date):
            old_package.delete()

            # advanced package
            new_template = self.create_package_template(single_component_price=new_component_price)
            packages_factories.OpenStackPackageFactory(
                template=new_template,
                tenant__service_project_link__project__customer=customer,
            )

        old_components_price = models.OpenStackItem.calculate_price_for_period(
            price=old_component_price,
            start=start_date,
            end=package_change_date
        )

        new_components_price = models.OpenStackItem.calculate_price_for_period(
            price=new_component_price,
            start=package_change_date,
            end=core_utils.month_end(package_change_date)
        )

        expected_price = old_components_price + new_components_price

        # assert
        self.assertEqual(models.Invoice.objects.count(), 1)
        self.assertEqual(Decimal(expected_price), models.Invoice.objects.first().price)
