from rest_framework import serializers
from edp_user.models import UserProfile


class UserInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    email = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE, required=True)
    status = serializers.ChoiceField(choices=UserProfile.STATUS, required=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
