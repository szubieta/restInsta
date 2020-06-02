from rest_framework import serializers
from publicaciones.models import Publicacion, PublicacionGuardada, Comentario, MeGusta
from usuarios.models import Usuario

#serializador de comentarios, transforma en json
class ComentarioSerializer(serializers.ModelSerializer):
    #llamamos a un metodo del serializador
    usuario = serializers.SerializerMethodField('get_username')
    user_image = serializers.SerializerMethodField('get_user_image')
    #clase que almacena los metadatos
    class Meta:
        model = Comentario #modelo
        fields = ['usuario', 'user_image', 'publicacion', 'comentario', 'fecha_publicado']#y campos a mostrar

    def get_username(self, comentario): #metodo que devuelve el nombre de usuario en vez del id
        username = comentario.usuario.username
        return username

    def get_publicacion(self, comentario):
        publicacion = comentario.publicacion.pk
        return publicacion

    def get_user_image(self, publicacion):
        usuario = Usuario.objects.get(username = publicacion.usuario)
        if usuario.imagen:
            return self.context['request'].build_absolute_uri(usuario.imagen.url)
        else:
            return ""

class CreateComentarioSerializer(serializers.ModelSerializer):
    
    usuario = serializers.SerializerMethodField('get_username')

    class Meta:
        model = Comentario
        fields = ['usuario', 'publicacion', 'comentario', 'fecha_publicado']

    def get_username(self, megusta):#metodo que devuelve el nombre de usuario en vez del id
        username = megusta.usuario.username
        return username

#serializador de me gustas, transforma en json
class MeGustaSerializer(serializers.ModelSerializer):
    #llamamos a un metodo del serializador
    usuario = serializers.SerializerMethodField('get_username')
    
    class Meta:
        model = MeGusta
        fields = ['usuario', 'publicacion', 'fecha_publicado']

    def get_username(self, megusta):#metodo que devuelve el nombre de usuario en vez del id
        username = megusta.usuario.username
        return username

class PublicacionGuardadaSerializer(serializers.ModelSerializer):
    #llamamos a un metodo del serializador
    usuario = serializers.SerializerMethodField('get_username')
    
    class Meta:
        model = PublicacionGuardada
        fields = ['usuario', 'publicacion', 'fecha_guardado']

    def get_username(self, megusta):#metodo que devuelve el nombre de usuario en vez del id
        username = megusta.usuario.username
        return username
    
#serializador de me publicaciones, transforma en json
class PublicacionSerializer(serializers.ModelSerializer):

    usuario = serializers.SerializerMethodField('get_username')#llamamos a un metodo del serializador
    user_image = serializers.SerializerMethodField('get_user_image')
    megustas = MeGustaSerializer(many = True)#llamamos al serializador de me gustas que devuelve en forma de array los me gustas de esa publicacion


    class Meta:
        model = Publicacion
        fields = ['id', 'usuario', 'user_image', 'descripcion', 'fecha_publicado', 'localizacion', 'n_likes', 'n_comentarios', 'es_imagen', 'imagen', 'video', 'megustas']

    def get_username(self, publicacion):#metodo que devuelve el nombre de usuario en vez del id
        username = publicacion.usuario.username
        return username

    def get_user_image(self, publicacion):
        usuario = Usuario.objects.get(username = publicacion.usuario)
        if usuario.imagen:
            return self.context['request'].build_absolute_uri(usuario.imagen.url)
        else:
            return ""

class CreatePublicacionSerializer(serializers.ModelSerializer):

    usuario = serializers.SerializerMethodField('get_username')#llamamos a un metodo del serializador

    class Meta:
        model = Publicacion
        fields = ['descripcion', 'fecha_publicado', 'localizacion', 'n_likes', 'n_comentarios', 'es_imagen', 'imagen', 'video', 'usuario']

    def get_username(self, publicacion):#metodo que devuelve el nombre de usuario en vez del id
        username = publicacion.usuario.username
        return username