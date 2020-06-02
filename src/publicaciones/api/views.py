from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView 
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import F, Q, Subquery


from usuarios.models import Usuario, UsuarioSeguido
from usuarios.api.serializers import UsuarioSerializer
from publicaciones.models import Publicacion, PublicacionGuardada, MeGusta, Comentario
from publicaciones.api.serializers import PublicacionSerializer, MeGustaSerializer, CreatePublicacionSerializer, ComentarioSerializer, CreateComentarioSerializer, PublicacionGuardadaSerializer

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
        serializer = CreatePublicacionSerializer(publicacion, data = request.data)#serializamos los datos
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
            Publicacion.objects.filter(pk = serializer.validated_data['publicacion'].pk).update(n_publicaciones = F('n_publicaciones')-1)
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
        serializer = CreatePublicacionSerializer(publicacion, data = request.data)
        data = {}#array en el que devolvemos datos
        if serializer.is_valid():#si los datos enviados son validos, se guarda
            serializer.save()
            Usuario.objects.filter(pk = usuario.pk).update(n_publicaciones = F('n_publicaciones')+1)
            #devolvemos respuestas
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
#vista basada en una Clase, esta vista devuelve una lista con todas las publicaciones
#de forma paginada, es decir, mostrando x elementos en cada página, esto se define en src/settings.py.REST_FRAMEWORK
class PublicacionListAPIView(ListAPIView):
    queryset = Publicacion.objects.all().order_by('-n_likes')#elementos buscados
    serializer_class = PublicacionSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter,)#ademas, se puede ordenar por parametros get

#vista que permite ver las publicaciones de los seguidos
class PublicacionFeed(ListAPIView):
    def get_queryset(self):
        seguidos = UsuarioSeguido.objects.filter(Q(usuario_seguidor = self.request.user.pk) | Q(usuario_seguido = self.request.user.pk)).values('usuario_seguido')
        seguidos != Usuario.objects.get(pk = self.request.user.pk)
        return Publicacion.objects.filter(usuario__in = seguidos).order_by('-fecha_publicado')
    queryset = get_queryset#elementos buscados
    serializer_class = PublicacionSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter,)#ademas, se puede ordenar por parametros get

#vista que permite ver la feed de un usuario
class UsuarioFeed(ListAPIView):
    def get_queryset(self):
        usuario = Usuario.objects.get(username = self.kwargs['username'])
        return Publicacion.objects.filter(usuario = usuario).order_by('-fecha_publicado')
    queryset = get_queryset#elementos buscados
    serializer_class = PublicacionSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter,)#ademas, se puede ordenar por parametros get

#vista que permite ver los comentarios de una publicacion
class ComentariosPublicacion(ListAPIView):
    def get_queryset(self):
        return Comentario.objects.filter(publicacion = self.request.GET.get('id'))
    queryset = get_queryset#elementos buscados
    serializer_class = ComentarioSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter,)#ademas, se puede ordenar por parametros get

class LikesPublicacion(ListAPIView):
    def get_queryset(self):
        megustas = MeGusta.objects.filter(publicacion = self.request.GET.get('id')).order_by('-fecha_publicado')
        return Usuario.objects.filter(pk__in = Subquery(megustas.values('usuario')))
    queryset = get_queryset#elementos buscados
    serializer_class = UsuarioSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter, SearchFilter)#ademas, se puede ordenar por parametros get
    search_fields = ('username', 'nombre')

#vista que permite dar un megusta
@api_view(['POST'])
@permission_classes((IsAuthenticated,))#comprobamos si se envia un token en el header de la peticion
def api_like_publicacion(request):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        serializer = MeGustaSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            serializer.validated_data['usuario'] = request.user
            serializer.validated_data['publicacion'] = serializer.validated_data['publicacion']
            serializer.save()
            Publicacion.objects.filter(pk = serializer.validated_data['publicacion'].pk).update(n_likes = F('n_likes')+1)
            data['response'] = "Success"
            return Response(status = status.HTTP_201_CREATED, data = data)
        else:
            data['response'] = "Credenciales erroneas"
            return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#vista que permite quitar un megusta
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))#comprobamos si se envia un token en el header de la peticion
def api_unlike_publicacion(request, publicacion):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        data = {}
        data['publicacion'] = publicacion
        data['usuario'] = usuario
        return Response(status = status.HTTP_404_NOT_FOUND, data = data)
    #doble comprobacion
    try:#comprobamos si existe el objeto
        megusta = MeGusta.objects.get(publicacion = publicacion, usuario = request.user)
    except MeGusta.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        data = {}
        if(usuario.username == Token.objects.get(user = usuario.pk).user.username):
            Publicacion.objects.filter(pk = publicacion).update(n_likes = F('n_likes')-1)
            if megusta.delete():
                data['response'] = 'Success'
            else:
                data['response'] = "Failure"
            return Response(status = status.HTTP_200_OK, data = data)
        else:
            data['response'] = "Credenciales erroneas"
            return Response(status = status.HTTP_400_BAD_REQUEST, data = data)
        return Response(status = status.HTTP_400_BAD_REQUEST)


#vista que permite publicar un comentario
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_post_comment(request):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    data = {}
    if request.method == "POST":
        serializer = CreateComentarioSerializer(data = request.data)

        if serializer.is_valid():
            serializer.validated_data['usuario'] = request.user
            serializer.validated_data['publicacion'] = serializer.validated_data['publicacion']
            serializer.save()
            Publicacion.objects.filter(pk = serializer.validated_data['publicacion'].pk).update(n_comentarios = F('n_comentarios')+1)
            data['response'] = "Success"
            return Response(status = status.HTTP_201_CREATED, data = data)
        else:
            data['response'] = "Credenciales erroneas"
            return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_save_publicacion(request):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    data = {}
    if request.method == "POST":
        serializer = PublicacionGuardadaSerializer(data = request.data)

        if serializer.is_valid():
            serializer.validated_data['usuario'] = request.user
            serializer.validated_data['publicacion'] = serializer.validated_data['publicacion']
            serializer.save()
            data['response'] = "Success"
            return Response(status = status.HTTP_201_CREATED, data = data)
        else:
            data['response'] = "Credenciales erroneas"
            return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))#comprobamos si se envia un token en el header de la peticion
def api_unsave_publicacion(request, publicacion):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        data = {}
        data['publicacion'] = publicacion
        data['usuario'] = usuario
        return Response(status = status.HTTP_404_NOT_FOUND, data = data)
    #doble comprobacion
    try:#comprobamos si existe el objeto
        publicacion = PublicacionGuardada.objects.get(publicacion = publicacion, usuario = request.user)
    except PublicacionGuardada.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        data = {}
        if(usuario.username == Token.objects.get(user = usuario.pk).user.username):
            if publicacion.delete():
                data['response'] = 'Success'
            else:
                data['response'] = "Failure"
            return Response(status = status.HTTP_200_OK, data = data)
        else:
            data['response'] = "Credenciales erroneas"
            return Response(status = status.HTTP_400_BAD_REQUEST, data = data)
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))#comprobamos si se envia un token en el header de la peticion
def api_get_if_saved(request, publicacion):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        data = {}
        try:
            PublicacionGuardada.objects.get(usuario = usuario, publicacion = publicacion)
            data['response'] = "True"
            return Response(data = data)
        except PublicacionGuardada.DoesNotExist:
            data['response'] = "False"
            return Response(data = data)
