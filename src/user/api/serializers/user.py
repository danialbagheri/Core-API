from django.core.exceptions import ValidationError
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from user.models import User
from user.services import EmailSubscriptionValidator


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            're_password',
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        re_password = validated_data.pop('re_password')
        if password != re_password:
            raise ValidationError('Invalid Password Repeat.')
        new_user = super().create(validated_data)
        new_user.set_password(password)
        new_user.save()
        return new_user


class UserRetrieveSerializer(DjoserUserSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = DjoserUserSerializer.Meta.fields + ('mobile_number',)
        read_only_fields = DjoserUserSerializer.Meta.read_only_fields

    # @staticmethod
    # def get_is_subscribed(user: User):
    #     if user.is_subscribed is not None:
    #         return user.is_subscribed
    #
    #     is_subscribed = EmailSubscriptionValidator(user.email).validate()
    #     user.is_subscribed = is_subscribed
    #     user.save(update_fields=['is_subscribed'])
    #     return is_subscribed
