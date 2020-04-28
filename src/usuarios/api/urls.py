from django.urls import path
from usuarios.api.views import(
    api_registro_view,
    api_get_usuario,
    api_update_usuario,
    SeguidoresListAPIView,
    SeguidosListAPIView,
    api_follow_user,
    api_unfollow_user
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'usuarios'
#urls de la api, estableciendo el fragmento, metodo o clase llamado, nombre
urlpatterns = [
    path('register', api_registro_view, name='registro'),
    path('login', obtain_auth_token, name='login'),
    path('get', api_get_usuario, name='get'),
    path('update', api_update_usuario, name='update'),
    path('seguidores', SeguidoresListAPIView.as_view(), name="get_seguidores"),
    path('seguidos', SeguidosListAPIView.as_view(), name="get_seguidos"),
    path('follow', api_follow_user, name="follow_user"),
    path('unfollow/<usuario_seguidor>/<usuario_seguido>', api_unfollow_user, name="unfollow_user"),
]