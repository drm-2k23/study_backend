from rest_framework import serializers
from user_custom.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Enter password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True}}




