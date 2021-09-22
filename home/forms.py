from django import forms
from django.db.models.fields import DateField
from django.forms import ModelForm
from home.models import *
from core import settings
class EmpresaForms(ModelForm):
    class Meta:
        model = Empresa
        fields = ['razon_social',"ruc", 'direccion','telefono', 'correo']


class AgenciaForms(ModelForm):
    class Meta:
        model = Agencia
        fields = ['nombre',"direccion", 'provincia','canton', 'correo']
        

class SecretariaForms(ModelForm):
    class Meta:
        model = Secretaria
        fields = ['user']
        
class UserForms(ModelForm):
    class Meta:
        model = User
        fields = ['first_name',"last_name","email","password","username"]

    def clean_email(self):
        try:
         
            sc = User.objects.get(email=self.cleaned_data["email"], 
                last_name="Cliente"
                )
            if sc is not None:
                raise forms.ValidationError("Cliente con este correo ya registrado")
            else:
                pass            
        except User.DoesNotExist: 
            pass
        return self.cleaned_data["email"]


        
        
class UserFormsUpdate(ModelForm):
    class Meta:
        model = User
        fields = ['first_name',"last_name","email","username"]
        
        
class PlanesInternetForms(ModelForm):
    class Meta:
        model = PlanesInternet
        fields = ['tipo_plan',"nombre","precio","ancho_bando","comparticion","observaciones","detalles","agencia"]




class ContratoForm(ModelForm):
    fecha_contrato= forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)   
    class Meta:
        model = Contrato
        fields = ['cliente',"plan_internet","tecnico","costo_instalacion","fecha_contrato"]


class RegistrosPagosForm(ModelForm):
    fecha_pago= forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)  
    class Meta:
        model = RegistrosPagos
        fields = ['cliente',"fecha_pago","valor"]


class AgendamientoForm(ModelForm):
    fecha_instalacion= forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)   
    class Meta:
        model = Agendamiento        
        fields = ["user",'tipo_agendamiento',"fecha_instalacion","cliente","costo_adicional","detalles_agendamiento","estado_agendamiento","direccion","tecnico"]


class PasswordForms(ModelForm):
    class Meta:
        model = User
        fields = ["password"]

        labels = {
           
            'password' : 'Nueva contraseña',
          
        }
        widgets = {
          
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':''}),
        }