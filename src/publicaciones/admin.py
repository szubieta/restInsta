from django.contrib import admin
from publicaciones.models import Publicacion, Comentario, MeGusta

#clase que rellena con las clases la pagina admin de django

#las clases ModelAdmin nos permite modificar la vista por defecto del admin, pudiendo mostrar más campos en la tabla
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'descripcion', 'fecha_publicado', 'fecha_editado', 'es_imagen', 'n_likes', 'n_comentarios')
    search_fields = ('usuario', 'fecha_publicado')
    readonly_fields = ('fecha_publicado', 'n_likes', 'n_comentarios')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'publicacion', 'comentario', 'fecha_publicado')
    search_fields = ('usuario', 'publicacion', 'fecha_publicado')
    readonly_fields = ('usuario', 'publicacion', 'fecha_publicado')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class MeGustaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'publicacion', 'fecha_publicado')
    search_fields = ('usuario', 'publicacion', 'fecha_publicado')
    readonly_fields = ('usuario', 'publicacion', 'fecha_publicado')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Publicacion, PublicacionAdmin)
admin.site.register(Comentario)
admin.site.register(MeGusta)
