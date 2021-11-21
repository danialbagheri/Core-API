from rest_framework import serializers

from web.models import Configuration


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'
        lookup_field = 'key'
