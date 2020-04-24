from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView 
from rest_framework.filters import OrderingFilter

from usuarios.models import Usuario
from publicaciones.models import Publicacion
from publicaciones.api.serializers import PublicacionSerializer

#anotacion que solo acepta peticiones get
@api_view(['GET'])
@permission_classes((IsAuthenticated,)) #comprobamos si se envia un token en el header de la peticion
def api_detail_publicacion(request, slug):
    #comprobamos si existe el objeto publicacion
    try:
        publicacion = Publicacion.objects.get(slug = slug)
    except Publicacion.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET': #doble comprobacion del metodo http
        serializer = PublicacionSerializer(publicacion) #serializamos el objeto y devolvemos sus datos
        return Response(serializer.data)


#anotacion que solo acepta peticiones get
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))#comprobamos si se envia un token en el header de la peticion
def api_update_publicacion(request, slug):
    try:#comprobamos si existe el objeto
        publicacion = Publicacion.objects.get(slug = slug)
    except Publicacion.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    usuario = request.user #creamos el usuario a partir del token enviado 
    if publicacion.usuario != usuario:#si no es el propietario no puede editar
        return Response({'response' : 'No tienes permiso para editar esta publicación'})
    #doble comprobacion
    if request.method == 'PUT':
        serializer = PublicacionSerializer(publicacion, data = request.data)#serializamos los datos
        data = {}#array en el que devolvemos datos
        if serializer.is_valid():#si los datos enviados son validos, se guarda
            serializer.save()
            data['success'] = 'success'
            return Response(data = data)#devolvemos respuesta positiva
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)#devolvemos error

#anotacion que solo acepta peticiones delete
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))#comprobamos si se envia un token en el header de la peticion
def api_delete_publicacion(request, slug):
    try:#comprobamos si existe el objeto
        publicacion = Publicacion.objects.get(slug = slug)
    except Publicacion.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    usuario = request.user#creamos el usuario a partir del token enviado 
    if publicacion.usuario != usuario:
        return Response({'response' : 'No tienes permiso para eliminar esta publicación'})
    #doble comprobacion
    if request.method == 'DELETE':
        data = {}#array en el que devolvemos datos
        if publicacion.delete():#si se ha eliminado guardamos mensaje correcto
            data['success'] = 'success'
        else:
            data ['success'] = 'failure'
        return Response(data = data)#devolvemos los datos
        
#anotacion que solo acepta peticiones post
@api_view(['POST'])
@permission_classes((IsAuthenticated,))#comprobamos si se envia un token en el header de la peticion
def api_create_publicacion(request):
    usuario = request.user
    publicacion = Publicacion(usuario = usuario)
    #doble comprobacion
    if request.method == "POST":
        serializer = PublicacionSerializer(publicacion, data = request.data)
        data = {}#array en el que devolvemos datos
        if serializer.is_valid():#si los datos enviados son validos, se guarda
            serializer.save()
            #devolvemos respuestas
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
#vista basada en una Clase, esta vista devuelve una lista con todas las publicaciones
#de forma paginada, es decir, mostrando x elementos en cada página, esto se define en src/settings.py.REST_FRAMEWORK
class PublicacionListAPIView(ListAPIView):
    queryset = Publicacion.objects.all()#elementos buscados
    serializer_class = PublicacionSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter,)#ademas, se puede ordenar por parametros get

