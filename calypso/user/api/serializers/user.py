from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        new_user = super().create(validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user
