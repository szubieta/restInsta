from rest_framework import serializers

from usuarios.models import Usuario, UsuarioSeguido

#serializador para el registro, es distinto al de usuarios ya que aqui pasaremos la contraseña
class RegistroSerializer(serializers.ModelSerializer):
    #password2 es el campo de comprobacion de repetir contraseña
    password2 = serializers.CharField(style = {'input_type' : 'password'}, write_only = True)
    #metadatos del serializador 
    class Meta:
        model = Usuario
        fields = ['email', 'username', 'nombre', 'apellido1', 'apellido2', 'fecha_nacimiento', 
        'telefono', 'password', 'password2', 'genero', 'imagen']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    #sobreescribimos el metodo para guardar los objetos
    def save(self):
        #creamos el objeto
        user = Usuario(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            nombre = self.validated_data['nombre'],
            apellido1 = self.validated_data['apellido1'],
            apellido2 = self.validated_data['apellido2'],
            fecha_nacimiento = self.validated_data['fecha_nacimiento'],
            telefono = self.validated_data['telefono'],
            genero = self.validated_data['genero'],
            imagen = self.validated_data['imagen'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        #comprobamos si las constraeñas coinciden
        if password!=password2:
            raise serializers.ValidationError({'password' : 'passwords no coinciden'})
        #la añadimos y guardamos el objeto
        user.set_password(password)
        user.save()
        return user
#serializador de las relaciones de seguimiento
class UsuarioSeguidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioSeguido
        fields = ['usuario_seguidor', 'usuario_seguido', 'fecha_seguido']

#serializador de usuarios
class UsuarioSerializer(serializers.ModelSerializer):
    #llamadas a los serializadores para obtener las relaciones de seguimiento
    imagen = serializers.SerializerMethodField('get_user_image')
    
    class Meta:
        model = Usuario
        fields = ['pk', 'email', 'username', 'nombre', 'apellido1', 'apellido2', 'fecha_nacimiento', 
        'telefono', 'descripcion', 'genero', 'imagen', 'n_seguidores', 'n_seguidos', 'n_publicaciones']

    def get_user_image(self, usuario):
        if usuario.imagen:
            return self.context.get('request').build_absolute_uri(usuario.imagen.url)
        else:
            return ""


class UpdateUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['pk', 'email', 'username', 'nombre', 'fecha_nacimiento', 'telefono', 'descripcion', 'imagen']
