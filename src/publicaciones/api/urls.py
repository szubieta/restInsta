from django.urls import path
from publicaciones.api.views import (#importamos todas las vistas de la API
    api_detail_publicacion,
    api_update_publicacion,
    api_delete_publicacion,
    api_create_publicacion,
    PublicacionListAPIView,

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
]