from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import random

User = get_user_model()

def get_random_digit(leng=4):
    t = str(random.randint(0000, (10 ** leng) - 1)).format('0' + str(leng) + 'd')
    return get_random_digit(leng) if len(t) < leng else t


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.first_name = user.first_name.capitalize()
        user.last_name = user.last_name.capitalize()
        if not user.email:
            user.email = None

        password = validated_data.get('password', "")
        user.set_password(password)
        verification_token = get_random_digit()
        user.verification_token = verification_token
        user.save()
        return user


class RegisterViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    http_method_names = ['post']

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def destroy(self, request, pk=None, **kwargs):
        request.user.is_active = False
        request.user.save()

        return Response(status=204)
