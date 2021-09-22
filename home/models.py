from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class AdministradorUser(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.first_name
    
 
    
class Secretaria(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    agencia = models.ForeignKey("Agencia", on_delete=models.CASCADE)
    
  
    
    def __str__(self):
        return self.user.first_name
    
class Cliente(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    direccion= models.CharField(max_length=150)
    agencia = models.ForeignKey("Agencia", on_delete=models.CASCADE)
    
   
    
    def __str__(self):
        return self.user.first_name
    
    
class Tecnico(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    agencia = models.ForeignKey("Agencia", on_delete=models.CASCADE)
    
  
    
    def __str__(self):
        return self.user.first_name
    
    
class Empresa(models.Model):
    id_administrador = models.OneToOneField("AdministradorUser", on_delete=models.CASCADE)
    razon_social = models.CharField(max_length=150)
    ruc = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=150)
    correo = models.CharField(max_length=150)
    
    def __str__(self):
        return self.razon_social
    
    
class Agencia(models.Model):    
    id_empresa = models.ForeignKey("Empresa", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    provincia = models.CharField(max_length=150)
    canton = models.CharField(max_length=150)
    correo = models.CharField(max_length=150)
    
    def __str__(self):
        return self.nombre
    

class PlanesInternet(models.Model):
    tipo_plan = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150,unique=True)
    precio = models.CharField(max_length=150)
    ancho_bando = models.CharField(max_length=150)
    comparticion = models.CharField(max_length=150)    
    observaciones = models.CharField(max_length=150)    
    detalles = models.CharField(max_length=150)        
    agencia = models.ForeignKey("Agencia", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    

class Contrato(models.Model):
    cliente = models.OneToOneField("Cliente",on_delete=models.CASCADE)
    plan_internet = models.ForeignKey("PlanesInternet",on_delete=models.CASCADE)
    direccion =  models.CharField(max_length=150)
    tecnico= models.ForeignKey("Tecnico", on_delete=models.CASCADE)
    costo_instalacion = models.CharField(max_length=150)
    fecha_contrato=models.DateField(auto_now=False)    
    def __str__(self):
        return self.cliente.user.first_name
    
    
class Agendamiento(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_agendamiento = models.CharField(max_length=150)
    fecha_instalacion=models.DateField(auto_now=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    costo_adicional = models.CharField(max_length=150)
    detalles_agendamiento = models.CharField(max_length=150)
    direccion= models.CharField(max_length=150)
    estado_agendamiento = models.BooleanField(default=False)
    tecnico= models.ForeignKey("Tecnico", on_delete=models.CASCADE)
    def __str__(self):
        return self.tipo_agendamiento
    
import datetime
fecha=datetime.datetime.now().strftime ("%Y%m%d")


class RegistrosPagos(models.Model):
    cliente = models.ForeignKey("Cliente",on_delete=models.CASCADE)
    fecha_pago=models.DateField(auto_now=False)
    valor = models.CharField(max_length=150)
    create_at= models.DateTimeField(blank=False, null=False,default=datetime.date.today)
    def __str__(self):
        return self.cliente.user.first_name
    
    
    