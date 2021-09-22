from django.contrib import admin
from home.models import *
# Register your models here.


class AdministradorAdmin(admin.ModelAdmin):        
    list_display  = ("user",)
    pass


class EmpresaAdmin(admin.ModelAdmin):        
    list_display  = ("razon_social","ruc")
    pass


class SecretariaAdmin(admin.ModelAdmin):        
    list_display  = ("user","agencia")
    pass

class ContratoAdmin(admin.ModelAdmin):        
    list_display  = ("cliente","plan_internet","tecnico","costo_instalacion",)
    pass

class AgendamientoAdmin(admin.ModelAdmin):        
    list_display  = ("tipo_agendamiento","fecha_instalacion","cliente","costo_adicional","detalles_agendamiento","estado_agendamiento")
    pass


class PagosAdmin(admin.ModelAdmin):        
    list_display  = ("cliente","fecha_pago","valor","create_at")
    pass

class TecnicosAdmin(admin.ModelAdmin):        
    list_display  = ("user","agencia")
    pass


class ClientesAdmin(admin.ModelAdmin):        
    list_display  = ("user","agencia")
    pass
class PlanesAdmin(admin.ModelAdmin):        
    list_display  = ("tipo_plan","nombre","precio","ancho_bando","comparticion")
    pass



admin.site.register(AdministradorUser, AdministradorAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Secretaria, SecretariaAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Agendamiento, AgendamientoAdmin)
admin.site.register(RegistrosPagos, PagosAdmin)
admin.site.register(Tecnico, TecnicosAdmin)
admin.site.register(Cliente, ClientesAdmin)
admin.site.register(PlanesInternet, PlanesAdmin)