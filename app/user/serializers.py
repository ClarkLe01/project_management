from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'avatar', 'password')   # noqa: 501
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }
