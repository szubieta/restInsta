from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuarios.models import Usuario, UsuarioSeguido

#clase que muestra los modelos en la pagina del administrador de django
class UsuarioAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'nombre', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
#y las añadimos a la pagina
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(UsuarioSeguido)
