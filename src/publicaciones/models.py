from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
import datetime

#metodo que define la ruta de guardado de los archivos
def ruta_guardar(instance, filename, **kwargs):#pasamos la instancia del objeto, nombre de fichero y los keyword arguments
    ruta = 'publicaciones/{usuario_id}/{fecha_publicado}{filename}'.format(#establecemos la ruta en publicaciones
        usuario_id = str(instance.usuario.id),#id del usuario sacado de la instancia
        fecha_publicado = str(instance.fecha_publicado),#fecha, sacado de la instacia
        filename = filename#y elnombre del fichero
    )
    return ruta
#modelo Publicacion, hereda de la clase Model de django
class Publicacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    descripcion = models.TextField(verbose_name = 'descripción', default='')
    localizacion = models.CharField(verbose_name = 'localización', max_length = 100, default='')
    fecha_publicado = models.DateTimeField(verbose_name = 'fecha publicado', auto_now = True)
    fecha_editado = models.DateTimeField(verbose_name = 'fecha editado', auto_now_add = True)
    n_likes = models.BigIntegerField(verbose_name = 'Nº likes', default = 0)
    n_comentarios = models.BigIntegerField(verbose_name = 'Nº comentarios', default = 0)
    es_imagen = models.BooleanField(verbose_name = 'es imagen')
    imagen = models.ImageField(upload_to = ruta_guardar, null = True, blank = True)#la ruta a la que se guarda 'upload to' llama al metodo
    video = models.FileField(upload_to = ruta_guardar, null = True, blank = True)
    slug = models.SlugField(blank = True, unique = True)

    def __str__(self):
        return self.usuario.username +', '+str(self.fecha_publicado)

#modelo comentario que hereda de Model de django
class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)#claves foraneas que referencian otra clase
    publicacion = models.ForeignKey(Publicacion, related_name = 'comentarios',on_delete = models.CASCADE)
    comentario = models.CharField(verbose_name = 'comentario', max_length = 200)
    fecha_publicado = models.DateTimeField(verbose_name = 'fecha publicado', auto_now = True)

    def __str__(self):
        return self.usuario.username +" "+ self.publicacion.slug +" "+ self.comentario

#modelo megusta que hereda de la clase Model de django
class MeGusta(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, related_name = 'megustas',on_delete = models.CASCADE)
    fecha_publicado = models.DateTimeField(verbose_name = 'fecha publicado', auto_now = True)

    #sobreescribimos la clase meta para establecer una clave primaria compuesta
    class Meta:
        unique_together = ('usuario', 'publicacion',)

    def __str__(self):
        return self.usuario.username +" "+ self.publicacion.slug


#disparador que se ejecuta despues de eliminar una publicacion
@receiver(post_delete, sender = Publicacion)
def borrar(sender, instance, **kwargs):#para eliminar el fichero generado
    if not instance.imagen:
        instance.video.delete(False)
    else:
        instance.imagen.delete(False)

#disparador que se ejecuta antes de uardar una publicacion para crear el slug
#el slug es el ultimo fragmento de la url que identifica univocamente un recurso
def pre_save_publicacion_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        fecha = datetime.datetime.today()
        instance.slug = slugify(instance.usuario.username) + '-' + str(fecha.year) + '-' + str(fecha.month) + '-' + str(fecha.day) + '-' + str(fecha.hour) + '-' + str(fecha.minute)+ '-' + str(fecha.second)

pre_save.connect(pre_save_publicacion_receiver, sender = Publicacion)