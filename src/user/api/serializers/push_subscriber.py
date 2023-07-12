from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user.models import PushSubscriber


class PushSubscriberSerializer(serializers.ModelSerializer):
    keys = serializers.DictField(write_only=True)

    class Meta:
        model = PushSubscriber
        fields = (
            'id',
            'endpoint',
            'keys',
        )

    def validate(self, attrs):
        keys = attrs['keys']
        if 'p256dh' not in keys or 'auth' not in keys:
            raise ValidationError('The keys field must contain both "p256dh" and "auth"')
        return attrs

    def create(self, validated_data):
        keys = validated_data.pop('keys')
        validated_data['p256dh'] = keys['p256dh']
        validated_data['auth'] = keys['auth']
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
        return super().create(validated_data)
