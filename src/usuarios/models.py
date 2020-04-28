from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


#clase que nos permite manejar y administrar los objetos usuario heredando de la clase que nos da django para crear el modelo personalizado
class MiUsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombre, apellido1, fecha_nacimiento, telefono, genero, password = None):#metodo llamado para crear un usuario
        #comprobaciones de todos los campos necesarios
        if not email:
            raise ValueError("Debe haber un email")
        if not username:
            raise ValueError("Debe haber un nombre de usuario")
        if not nombre:
            raise ValueError("Debe haber un nombre")
        if not apellido1:
            raise ValueError("Debe haber un apellido")
        if not fecha_nacimiento:
            raise ValueError("Debe haber fecha de nacimiento")
        if not telefono:
            raise ValueError("Debe haber un telefono")
        if not genero:
            raise ValueError("Debe especificarse el genero")
        #rellenamos el objeto con los datos
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            nombre = nombre, 
            apellido1 = apellido1, 
            fecha_nacimiento = fecha_nacimiento, 
            telefono = telefono, 
            genero = genero,
        )
        user.set_password(password)#guardamos la contraseña
        user.save(using = self._db)#usando el sgdb de la app
        return user

    def create_superuser(self, email, username, nombre, apellido1, fecha_nacimiento, telefono, genero, password):#metodo llamado para crear un superusuario
        user = self.create_user(#llamamos recursivamente al metodo anteriormente creado
            email = self.normalize_email(email),
            username = username,
            nombre = nombre, 
            apellido1 = apellido1, 
            fecha_nacimiento = fecha_nacimiento, 
            telefono = telefono, 
            genero = genero,
            password = password,
        )
        #establecemos los campos booleanos de permisos a true
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db)
        return user

def ruta_guardar(instance, filename, **kwargs):
    ruta = 'usuarios/{usuario_id}-{filename}'.format(
        usuario_id = str(instance.id),
        filename = filename
    )
    return ruta

#esta clase extiende y sustituye al modelo de usuarios por defecto de django, esto lo hacemos para añadir más campos a la clase
#reutilizando la seguridad implementada del framework así tendremos un modelo de usuario que se ajuste a las necesidades de nuestra aplicación
class Usuario(AbstractBaseUser):
    #campos obligatorios al extender de la clase
    email = models.EmailField(verbose_name = 'email', max_length = 100, unique = True)
    username = models.CharField(verbose_name ='username', max_length = 30, unique = True)
    date_joined = models.DateTimeField(verbose_name = 'date joined', auto_now_add = True)
    last_login = models.DateTimeField(verbose_name = 'last login', auto_now = True)
    is_admin = models.BooleanField(verbose_name = 'is admin', default = False)
    is_active = models.BooleanField(verbose_name = 'is active', default = True)
    is_staff = models.BooleanField(verbose_name = 'is staff', default = False)
    is_superuser = models.BooleanField(verbose_name = 'is superuser', default = False)
    #campos extras que añadimos
    nombre = models.CharField(verbose_name = 'nombre', max_length = 20)
    apellido1 = models.CharField(verbose_name = 'apellido1', max_length = 30)
    apellido2 = models.CharField(verbose_name = 'apellido2', max_length = 30)
    fecha_nacimiento = models.DateField(verbose_name = 'fecha nacimiento')
    telefono_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El telefono debe introducirse con el formato: '+999999999' ")
    telefono = models.CharField(verbose_name = 'telefono', validators=[telefono_regex], max_length = 17)
    descripcion = models.TextField(verbose_name = 'descripcion', default = '');
    n_seguidores = models.IntegerField(verbose_name = 'seguidores', default = 0)
    n_seguidos = models.IntegerField(verbose_name = 'seguidos', default = 0)
    imagen = models.ImageField(upload_to = ruta_guardar, null = True, blank = True)

    class Genero(models.TextChoices):#clase interna que funciona como un Enum
        MASCULINO = 'M', _('Masculino')
        FEMENINO = 'F', _('Femenino')
        OTRO = 'O', _('Otro')
    genero = models.CharField(max_length=1, choices=Genero.choices, default=Genero.OTRO)

    USERNAME_FIELD = 'email' #campo por el que haremos el login
    REQUIRED_FIELDS = ['username', 'nombre', 'apellido1', 'fecha_nacimiento', 'telefono', 'genero']#campos requeridos al crear el objeto

    objects = MiUsuarioManager()#establecemos el manager a la calse

    def __str__(self):#lo que devuelve al msotrar un objeto de esta clase
        return self.username
    
    def has_perm(self, perm, obj=None):#metodo necesario de django para sabe si tiene permisos o no
        return self.is_admin

    def has_module_perms(self, app_label):#metodo necesario de django para sabe si tiene permisos o no sobre los módulos
        return True

#disparador que se ejecuta despues de guardar un objeto
@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def crear_token(sender, instance = None, created = False, **kwargs):
    if created:#si el objeto se crea correctamente se crea un token con ese usuario
        Token.objects.create(user = instance)

#clase usuarioseguido, establece relaciones de seguimiento entre usuarios
class UsuarioSeguido(models.Model):
    usuario_seguidor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'seguidos')
    usuario_seguido = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'seguidores')
    fecha_seguido = models.DateTimeField(verbose_name = 'fecha seguido', auto_now = True)
    #metadatos para establecer una clave primaria compuesta
    class Meta:
        unique_together = ('usuario_seguidor', 'usuario_seguido',)

    def __str__(self):
        return self.usuario_seguidor.username +" "+ self.usuario_seguido.username