# Generated by Django 1.11.3 on 2017-09-06 07:39
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_fsm
import model_utils.fields
from django.db import migrations, models

import waldur_core.core.fields
import waldur_core.core.models
import waldur_core.logging.loggers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('structure', '0001_squashed_0036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('uuid', waldur_core.core.fields.UUIDField()),
                (
                    'state',
                    models.CharField(
                        choices=[
                            ('DRAFT', 'Draft'),
                            ('SENT', 'Sent'),
                            ('PAID', 'Paid'),
                            ('MARKED_AS_PAID', 'Marked as paid'),
                            ('CANCELLED', 'Cancelled'),
                            ('REFUNDED', 'Refunded'),
                            ('PARTIALLY_REFUNDED', 'Partially refunded'),
                            ('MARKED_AS_REFUNDED', 'Marked as refunded'),
                            ('UNPAID', 'Unpaid'),
                            ('PAYMENT_PENDING', 'Payment pending'),
                        ],
                        default='DRAFT',
                        max_length=30,
                    ),
                ),
                ('invoice_date', models.DateField()),
                ('end_date', models.DateField()),
                (
                    'pdf',
                    models.FileField(
                        blank=True, null=True, upload_to='paypal-invoices'
                    ),
                ),
                ('number', models.CharField(max_length=30)),
                (
                    'tax_percent',
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=4,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                    ),
                ),
                ('backend_id', models.CharField(blank=True, max_length=128)),
                (
                    'issuer_details',
                    waldur_core.core.fields.JSONField(
                        blank=True,
                        default={},
                        help_text='Stores data about invoice issuer',
                    ),
                ),
                (
                    'payment_details',
                    waldur_core.core.fields.JSONField(
                        blank=True,
                        default={},
                        help_text='Stores data about customer payment details',
                    ),
                ),
                (
                    'month',
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ]
                    ),
                ),
                ('year', models.PositiveSmallIntegerField()),
                (
                    'customer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='paypal_invoices',
                        to='structure.Customer',
                    ),
                ),
            ],
            options={
                'ordering': ['-invoice_date'],
            },
            bases=(
                waldur_core.logging.loggers.LoggableMixin,
                models.Model,
                waldur_core.core.models.BackendModelMixin,
            ),
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity', models.PositiveIntegerField(default=0)),
                (
                    'unit_of_measure',
                    models.CharField(
                        choices=[
                            ('QUANTITY', 'Quantity'),
                            ('HOURS', 'Hours'),
                            ('AMOUNT', 'Amount'),
                        ],
                        default='HOURS',
                        max_length=30,
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateTimeField(null=True)),
                ('end', models.DateTimeField(null=True)),
                (
                    'invoice',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='items',
                        to='waldur_paypal.Invoice',
                    ),
                ),
            ],
            options={
                'ordering': ['invoice', '-start'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                ('uuid', waldur_core.core.fields.UUIDField()),
                ('error_message', models.TextField(blank=True)),
                (
                    'state',
                    django_fsm.FSMIntegerField(
                        choices=[
                            (0, 'Initial'),
                            (1, 'Created'),
                            (2, 'Approved'),
                            (4, 'Erred'),
                        ],
                        default=0,
                    ),
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('backend_id', models.CharField(max_length=255, null=True)),
                ('token', models.CharField(max_length=255, null=True)),
                ('approval_url', models.URLField()),
                (
                    'customer',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='structure.Customer',
                    ),
                ),
            ],
            options={
                'ordering': ['-modified'],
            },
            bases=(waldur_core.logging.loggers.LoggableMixin, models.Model),
        ),
    ]
