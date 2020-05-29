from django.urls import path
from publicaciones.api.views import (#importamos todas las vistas de la API
    api_detail_publicacion,
    api_update_publicacion,
    api_delete_publicacion,
    api_create_publicacion,
    PublicacionListAPIView,
    PublicacionFeed,
    ComentariosPublicacion,
    api_like_publicacion,
    api_unlike_publicacion,
    post_comment,
    UsuarioFeed,

)
#definimos el nombre de la aplicación para establecer sus urls
app_name = 'publicaciones'
#creamos las URLs, dando la direccion, el metodo al que llaman y el nombre
urlpatterns = [
    path('<slug>/', api_detail_publicacion, name="detail"),
    path('update/<slug>', api_update_publicacion, name="update"),
    path('delete/<slug>', api_delete_publicacion, name="delete"),
    path('', api_create_publicacion, name="create"), 
    path('list', PublicacionListAPIView.as_view(), name="list"),       
    path('feed', PublicacionFeed.as_view(), name="feed"),
    path('userfeed/<username>', UsuarioFeed.as_view(), name="user feed"),
    path('like', api_like_publicacion, name="like"),
    path('unlike/<publicacion>', api_unlike_publicacion, name="unlike"),
    path('comments', ComentariosPublicacion.as_view(), name="comments"),
    path('postcomment', post_comment, name="post comment"),

]