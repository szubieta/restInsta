from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView 
from rest_framework.filters import OrderingFilter
from django.db.models import F

from usuarios.models import UsuarioSeguido, Usuario
from usuarios.api.serializers import RegistroSerializer, UsuarioSerializer, UpdateUsuarioSerializer, UsuarioSeguidoSerializer

#anotacion que solo admite peticiones post
@api_view(['POST'])
def api_registro_view(request):
    #doble comprobacion
    if request.method == 'POST':
        #creamos el serializador, y si es valido se crea y guarda el objeto
        serializer = RegistroSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            usuario = serializer.save()
            #guardamos todos os datos del usuario
            data['response'] = 'Usuario registrado' 
            data['email'] = usuario.email
            data['username'] = usuario.username
            data['nombre'] = usuario.nombre
            data['apellido1'] = usuario.apellido1
            data['apellido2'] = usuario.apellido2
            data['fecha_nacimiento'] = usuario.fecha_nacimiento
            data['telefono'] = usuario.telefono
            token = Token.objects.get(user = usuario).key
            data['token'] = token
            return Response(data, status = status.HTTP_201_CREATED)#y devolvemos los datos
        else:
            data = serializer.errors
            return Response(data, status = status.HTTP_400_BAD_REQUEST)#y devolvemos los datos

#anotacion que solo admite peticiones get
@api_view(['GET'])
@permission_classes((IsAuthenticated,))#si se envia token se ejecuta
def api_get_usuario(request):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    #doble comprobacion
    if request.method == 'GET':#se serializa los datos y se devuelven
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)


#anotacion que solo admite peticiones put
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))#si se envia token se ejecuta
def api_update_usuario(request):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    #doble comprobacion
    if request.method == 'PUT':
        serializer = UpdateUsuarioSerializer(usuario, data = request.data)
        data = {}
        if serializer.is_valid():#si los datos son validos al serializador se guardan
            serializer.update(usuario, serializer.validated_data)
            data['response'] = "Actualizado correctamente"
            return Response(serializer.data)#devolvemos datos al usuario
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



class SeguidoresListAPIView(ListAPIView):
    def get_queryset(self):
        return UsuarioSeguido.objects.filter(usuario_seguido = self.request.user.pk)
    queryset = get_queryset#elementos buscados
    serializer_class = UsuarioSeguidoSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter,)#ademas, se puede ordenar por parametros get

class SeguidosListAPIView(ListAPIView):
    def get_queryset(self):
        return UsuarioSeguido.objects.filter(usuario_seguidor = self.request.user.pk)
    queryset = get_queryset#elementos buscados
    serializer_class = UsuarioSeguidoSerializer#serializador
    authentication_classes = (TokenAuthentication,)#clases de autenticacion (token)
    permission_classes = (IsAuthenticated,)#unicamente funciona si se provee el token en el header
    pagination_class = PageNumberPagination#la clase de paginacion
    filter_backends = (OrderingFilter,)#ademas, se puede ordenar por parametros get

#vista para seguir un usuario
@api_view(['POST'])
@permission_classes((IsAuthenticated,))#si se envia token se ejecuta
def api_follow_user(request):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
    except Usuario.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    #doble comprobacion
    if request.method == 'POST':
        serializer = UsuarioSeguidoSerializer(data = request.data)
        data = {}
        if serializer.is_valid():#si los datos son validos al serializador se guardan
            if(usuario.username == Token.objects.get(user = usuario.pk).user.username):
                serializer.save()
                Usuario.objects.filter(username = serializer.validated_data['usuario_seguido'].username).update(n_seguidores = F('n_seguidores')+1)
                Usuario.objects.filter(username = serializer.validated_data['usuario_seguidor'].username).update(n_seguidos = F('n_seguidos')+1)
                data['response'] = "Success"
                return Response(status = status.HTTP_201_CREATED, data = data)
            else:
                data['response'] = "Credenciales erroneas"
                return Response(status = status.HTTP_400_BAD_REQUEST, data = data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#vista para dejar de seguir a un usuario
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))#si se envia token se ejecuta
def api_unfollow_user(request, usuario_seguidor, usuario_seguido):
    try:#comprobamos que el ususario exista
        #el usuario se busca a traves del token enviado
        usuario = request.user
        
    except Usuario.DoesNotExist:
        data = {}
        data['seguidor'] = usuario_seguidor
        data['seguido'] = usuario_seguido
        return Response(status = status.HTTP_404_NOT_FOUND, data = data)
    #doble comprobacion
    try:#comprobamos si existe el objeto
            follow = UsuarioSeguido.objects.get(usuario_seguidor = usuario_seguidor, usuario_seguido = usuario_seguido)
    except UsuarioSeguido.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        data = {}
        if(usuario.username == Token.objects.get(user = usuario.pk).user.username):
            Usuario.objects.filter(pk = usuario_seguido).update(n_seguidores = F('n_seguidores')-1)
            Usuario.objects.filter(pk = usuario_seguidor).update(n_seguidos = F('n_seguidos')-1)
            if follow.delete():
                data['response'] = 'Success'
            else:
                data['response'] = "Failure"
            return Response(status = status.HTTP_200_OK, data = data)
        else:
            data['response'] = "Credenciales erroneas"
            return Response(status = status.HTTP_400_BAD_REQUEST, data = data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
