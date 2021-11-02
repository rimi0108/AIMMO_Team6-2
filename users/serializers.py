from rest_framework import serializers
from .models import User


class TutorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'email',
                  'password')
