from django.contrib.auth import get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProfileSerializer, self).__init__(*args, **kwargs)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'patch', 'options', 'put', 'delete']

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class LoginAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        token, created = Token.objects.get_or_create(user=user)
        user_data = ProfileSerializer(instance=user, context={'request': request})
        return Response({
            'token': token.key,
            'user': user_data.data,
        })


@api_view(["GET"])
@permission_classes((AllowAny,))
def check_token(request, token):
    try:
        Token.objects.get(key=token)
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=401)
