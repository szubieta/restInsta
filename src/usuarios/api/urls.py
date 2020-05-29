from django.urls import path
from usuarios.api.views import(
    api_registro_view,
    api_get_usuario,
    api_get_userData,
    api_update_usuario,
    SeguidoresListAPIView,
    SeguidosListAPIView,
    UsuariosListAPIView,
    SeguidoresDataListAPIView,
    SeguidosDataListAPIView,
    api_follow_user,
    api_unfollow_user,
    api_get_if_follows,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'usuarios'
#urls de la api, estableciendo el fragmento, metodo o clase llamado, nombre
urlpatterns = [
    path('register', api_registro_view, name='registro'),
    path('login', obtain_auth_token, name='login'),
    path('get', api_get_usuario, name='get'),
    path('getData/<username>', api_get_userData, name="userData"),
    path('update', api_update_usuario, name='update'),
    path('users', UsuariosListAPIView.as_view(), name="get_usuarios"),
    path('seguidores/<usuario_seguido>', SeguidoresListAPIView.as_view(), name="get_seguidores"),
    path('seguidos/<usuario_seguidor>', SeguidosListAPIView.as_view(), name="get_seguidos"),
    path('seguidosData/<usuario_seguidor>', SeguidosDataListAPIView.as_view(), name="get_seguidos"),
    path('seguidoresData/<usuario_seguido>', SeguidoresDataListAPIView.as_view(), name="get_seguidos"),
    path('follow', api_follow_user, name="follow_user"),
    path('unfollow/<usuario_seguidor>/<usuario_seguido>', api_unfollow_user, name="unfollow_user"),
    path("getFollow/<usuario_seguido>", api_get_if_follows, name="get if user follows")
]