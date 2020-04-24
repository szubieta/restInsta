from rest_framework import serializers
from publicaciones.models import Publicacion, Comentario, MeGusta

#serializador de comentarios, transforma en json
class ComentarioSerializer(serializers.ModelSerializer):
    #llamamos a un metodo del serializador
    usuario = serializers.SerializerMethodField('get_username')
    #clase que almacena los metadatos
    class Meta:
        model = Comentario #modelo
        fields = ['usuario', 'publicacion', 'comentario', 'fecha_publicado']#y campos a mostrar

    def get_username(self, comentario): #metodo que devuelve el nombre de usuario en vez del id
        username = comentario.usuario.username
        return username

    def get_publicacion(self, comentario):
        publicacion = comentario.publicacion.pk
        return publicacion

#serializador de me gustas, transforma en json
class MeGustaSerializer(serializers.ModelSerializer):
    #llamamos a un metodo del serializador
    usuario = serializers.SerializerMethodField('get_username')
    
    class Meta:
        model = Comentario
        fields = ['usuario', 'publicacion', 'fecha_publicado']

    def get_username(self, comentario):#metodo que devuelve el nombre de usuario en vez del id
        username = comentario.usuario.username
        return username
    
#serializador de me publicaciones, transforma en json
class PublicacionSerializer(serializers.ModelSerializer):

    usuario = serializers.SerializerMethodField('get_username')#llamamos a un metodo del serializador
    comentarios = ComentarioSerializer(many = True)#llamamos al serializador de comentarios que devuelve en forma de array los comentarios de esa publicacion
    megustas = MeGustaSerializer(many = True)#llamamos al serializador de me gustas que devuelve en forma de array los me gustas de esa publicacion

    class Meta:
        model = Publicacion
        fields = ['descripcion', 'fecha_publicado', 'localizacion', 'n_likes', 'n_comentarios', 'es_imagen', 'imagen', 'video', 'usuario', 'comentarios', 'megustas']

    def get_username(self, publicacion):#metodo que devuelve el nombre de usuario en vez del id
        username = publicacion.usuario.username
        return username