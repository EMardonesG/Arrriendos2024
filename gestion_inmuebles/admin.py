from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import TipoInmueble, Comuna, Region, TipoUsuario, PerfilUsuario, Inmueble, Solicitud

class TipoInmuebleAdmin(admin.ModelAdmin):
    list_display = ('tipo_inmueble',)
    search_fields = ('tipo_inmueble',)
admin.site.register(TipoInmueble, TipoInmuebleAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('region',)
    search_fields = ('region',)
admin.site.register(Region, RegionAdmin)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('comuna', 'region')
    search_fields = ('comuna',)
    list_filter = ('region',)
admin.site.register(Comuna, ComunaAdmin)

class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('tipo_usuario',)
    search_fields = ('tipo_usuario',)
admin.site.register(TipoUsuario, TipoUsuarioAdmin)

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'apellido', 'tipo_usuario')
    search_fields = ('nombre', 'apellido', 'correo')
    list_filter = ('tipo_usuario',)
admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)

class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre_inmueble', 'tipo_inmueble', 'comuna', 'region', 'propietario', 'numero_hab', 'numero_banos', 'm2_construido', 'precio', 'fecha_publicacion')
    search_fields = ('nombre_inmueble', 'descripcion', 'direccion', 'precio')
    list_filter = ('tipo_inmueble', 'comuna', 'region')

    def save_model(self, request, obj, form, change):
        if obj.tipo_inmueble_id == 1:  # Only allow arrendadores for "arriendo" type
            if not hasattr(request.user, 'perfilusuario') or request.user.perfilusuario.tipo_usuario.tipo_usuario != 'arrendador':
                raise PermissionDenied("Solo los arrendadores pueden crear inmuebles para arriendo.")
        super().save_model(request, obj, form, change)

admin.site.register(Inmueble, InmuebleAdmin)

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('arrendatario', 'inmueble', 'fecha_solicitud', 'estado')
    search_fields = ('arrendatario__nombre', 'arrendatario__apellido', 'inmueble__nombre_inmueble')
    list_filter = ('estado',)

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.arrendatario != request.user.perfilusuario:
                return False
        return True

admin.site.register(Solicitud, SolicitudAdmin)
