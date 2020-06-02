from django.urls import path
from publicaciones.api.views import (#importamos todas las vistas de la API
    api_detail_publicacion,
    api_update_publicacion,
    api_delete_publicacion,
    api_create_publicacion,
    PublicacionListAPIView,
    PublicacionFeed,
    ComentariosPublicacion,
    LikesPublicacion,
    api_like_publicacion,
    api_unlike_publicacion,
    api_post_comment,
    UsuarioFeed,
    api_save_publicacion,
    api_unsave_publicacion,
    api_get_if_saved,

)
#definimos el nombre de la aplicación para establecer sus urls
app_name = 'publicaciones'
#creamos las URLs, dando la direccion, el metodo al que llaman y el nombre
urlpatterns = [
    path('<slug>/', api_detail_publicacion, name="detail"),
    path('update/<slug>', api_update_publicacion, name="update"),
    path('delete/<slug>', api_delete_publicacion, name="delete"),
    path('upload', api_create_publicacion, name="create"), 
    path('list', PublicacionListAPIView.as_view(), name="list"),       
    path('feed', PublicacionFeed.as_view(), name="feed"),
    path('userfeed/<username>', UsuarioFeed.as_view(), name="user feed"),
    path('likelist', LikesPublicacion.as_view(), name="like list"),
    path('like', api_like_publicacion, name="like"),
    path('unlike/<publicacion>', api_unlike_publicacion, name="unlike"),
    path('comments', ComentariosPublicacion.as_view(), name="comments"),
    path('postcomment', api_post_comment, name="post comment"),
    path('save', api_save_publicacion, name="save publicacion"),
    path('unsave/<publicacion>', api_unsave_publicacion, name="unsave publicacion"),
    path('saved/<publicacion>', api_get_if_saved, name="unsave publicacion"),

]