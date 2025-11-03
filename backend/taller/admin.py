from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class FiltroSucursal(admin.SimpleListFilter):
    """Filtro personalizado por sucursal"""
    title = 'Sucursal'
    parameter_name = 'sucursal'

    def lookups(self, request, model_admin):
        return [(s.id_sucursal, s.nombre) for s in Sucursal.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(sucursal_id=self.value())
        return queryset

class FiltroTaller(admin.SimpleListFilter):
    """Filtro personalizado por taller"""
    title = 'Taller'
    parameter_name = 'taller'

    def lookups(self, request, model_admin):
        return [(t.id_taller, t.nombre) for t in Taller.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(taller_id=self.value())
        return queryset

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'nombre', 'apellido', 'rol', 'is_active', 'date_joined']
    list_filter = ['rol', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'nombre', 'apellido']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información PepsiCo', {
            'fields': ('nombre', 'apellido', 'telefono', 'rol')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('rol')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['patente', 'marca', 'modelo', 'año', 'tipo_vehiculo', 'operativo', 'estado_vehiculo', 'taller', 'sucursal']
    list_filter = [FiltroSucursal, FiltroTaller, 'operativo', 'tipo_vehiculo', 'estado_vehiculo', 'para_remate']
    search_fields = ['patente', 'marca', 'modelo']
    list_editable = ['operativo', 'estado_vehiculo']
    readonly_fields = ['edad']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('patente', 'marca', 'modelo', 'año', 'edad', 'tipo_vehiculo')
        }),
        ('Estado Operativo', {
            'fields': ('operativo', 'estado_vehiculo', 'kilometraje', 'vida_util')
        }),
        ('Gestión Flota', {
            'fields': ('para_remate', 'cumplimiento', 'tct', 'plan_verano')
        }),
        ('Ubicación', {
            'fields': ('usuario', 'sucursal', 'taller')
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario', 'sucursal', 'taller', 'estado_vehiculo')

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['id_tarea', 'vehiculo', 'usuario', 'estado', 'prioridad', 'fecha_asignacion', 'taller']
    list_filter = ['estado', 'prioridad', 'taller', 'fecha_asignacion']
    search_fields = ['vehiculo__patente', 'usuario__nombre', 'usuario__apellido', 'titulo']
    date_hierarchy = 'fecha_asignacion'
    list_editable = ['estado', 'prioridad']
    
    fieldsets = (
        ('Información General', {
            'fields': ('titulo', 'descripcion', 'estado', 'prioridad')
        }),
        ('Asignación', {
            'fields': ('vehiculo', 'usuario', 'taller', 'agenda')
        }),
        ('Fechas', {
            'fields': ('fecha_asignacion', 'fecha_hora_inicio', 'fecha_hora_fin')
        }),
        ('Gestión', {
            'fields': ('pausada', 'motivo_pausa')
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vehiculo', 'usuario', 'taller', 'agenda')

@admin.register(RegistroVehiculo)
class RegistroVehiculoAdmin(admin.ModelAdmin):
    list_display = ['id_registro', 'vehiculo', 'usuario', 'estado_vehiculo', 'fecha_hora', 'observaciones_short']
    list_filter = ['estado_vehiculo', 'fecha_hora', 'usuario']
    search_fields = ['vehiculo__patente', 'observaciones']
    date_hierarchy = 'fecha_hora'
    readonly_fields = ['fecha_hora']
    
    def observaciones_short(self, obj):
        return obj.observaciones[:50] + '...' if len(obj.observaciones) > 50 else obj.observaciones
    observaciones_short.short_description = 'Observaciones'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vehiculo', 'usuario', 'estado_vehiculo')

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'usuario', 'fecha_generacion']
    list_filter = ['tipo', 'fecha_generacion', 'usuario']
    search_fields = ['titulo', 'contenido']
    date_hierarchy = 'fecha_generacion'
    readonly_fields = ['fecha_generacion']

@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['id_mensaje', 'usuario', 'contenido_short', 'fecha_hora', 'leido']
    list_filter = ['leido', 'fecha_hora', 'usuario']
    search_fields = ['contenido', 'usuario__username']
    list_editable = ['leido']
    date_hierarchy = 'fecha_hora'
    
    def contenido_short(self, obj):
        return obj.contenido[:30] + '...' if len(obj.contenido) > 30 else obj.contenido
    contenido_short.short_description = 'Contenido'

# Registros simples para modelos maestros
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre_rol', 'descripcion']
    search_fields = ['nombre_rol']

@admin.register(EstadoVehiculo)
class EstadoVehiculoAdmin(admin.ModelAdmin):
    list_display = ['nombre_estado', 'descripcion']
    search_fields = ['nombre_estado']

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'region', 'direccion']
    list_filter = ['region', 'ciudad']
    search_fields = ['nombre', 'ciudad']

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'sucursal', 'capacidad', 'direccion']
    list_filter = ['sucursal', 'capacidad']
    search_fields = ['nombre', 'sucursal__nombre']

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['id_agenda', 'taller']
    list_filter = ['taller']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('taller')

@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ['nombre_ruta', 'origen', 'destino', 'distancia_km', 'sucursal']
    list_filter = ['sucursal']
    search_fields = ['nombre_ruta', 'origen', 'destino']

@admin.register(RutaVehiculo)
class RutaVehiculoAdmin(admin.ModelAdmin):
    list_display = ['ruta', 'vehiculo']
    list_filter = ['ruta']
    search_fields = ['ruta__nombre_ruta', 'vehiculo__patente']

# Personalización del sitio admin
admin.site.site_header = "PepsiCo Chile - Gestión de Talleres"
admin.site.site_title = "Administración PepsiCo Talleres"
admin.site.index_title = "Panel de Control Principal"