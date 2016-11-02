from rest_framework import serializers

from . import models


class InvoiceItemSerializer(serializers.ModelSerializer):
    package = serializers.HyperlinkedRelatedField(view_name='openstack-package-detail',
                                                  lookup_field='uuid', read_only=True)

    class Meta(object):
        model = models.InvoiceItem
        fields = ('tenant_name', 'template_name', 'package', 'price', 'start', 'end')

    def to_representation(self, instance):
        ret = super(InvoiceItemSerializer, self).to_representation(instance)
        if instance.package:
            ret['tenant_name'] = instance.package.tenant.name
            ret['template_name'] = instance.package.template.name

        return ret


class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    total = serializers.DecimalField(max_digits=15, decimal_places=7)
    items = InvoiceItemSerializer(many=True)

    class Meta(object):
        model = models.Invoice
        fields = (
            'url', 'uuid', 'customer', 'total', 'items', 'state', 'year', 'month'
        )
        view_name = 'invoice-detail'
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'customer': {'lookup_field': 'uuid'},
        }
