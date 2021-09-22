

from django.contrib.auth import authenticate
from django.http import response
from django.http.response import FileResponse,JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login
from home.models import *
from home.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
        
def logout(request):
    django_logout(request)
    return redirect('/')

def index(request):
    if(request.method == "POST"):
        email = request.POST.get("email","")
        password = request.POST.get("password","")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            print(user.last_name)
            if user.last_name =="Tecnico":
                return redirect('agendamientos')
            elif user.last_name =="Meganet":
                
                return redirect('inicio')
            elif user.last_name =="Secretaria":
                
                return redirect('contratos')
                    
        else:
            return render(request,'index.html',{"error":"Datos incorrectos"})
        
    
    return render(request, 'index.html', {})

@login_required
def inicio(request):
    try:
        adminitrador = AdministradorUser.objects.get(user=request.user)
        empresa = Empresa.objects.get(id_administrador=adminitrador)
        return render(request, 'inicio.html', {"empresa":empresa})
    except Empresa.DoesNotExist:
        return render(request, 'inicio.html', {"empresa":""})


@login_required
def nueva_empresa(request):    
    if(request.method == "POST"):
        form=EmpresaForms(request.POST)
        if form.is_valid():
            administrador=AdministradorUser.objects.get(user=request.user)
            empresa=Empresa.objects.create(id_administrador=administrador,
                                           razon_social=form.cleaned_data["razon_social"],
                                           ruc=form.cleaned_data["ruc"],
                                           direccion=form.cleaned_data["direccion"],
                                           telefono=form.cleaned_data["telefono"],
                                           correo=form.cleaned_data["correo"])
           
            return redirect('inicio')
        else:
            return render(request,'Empresas/nueva.html',{"error":form}) 
    
    return render(request,"Empresas/nueva.html")

@login_required
def editar_empresa(request,id):    
    empresa=Empresa.objects.get(id=id)
    if(request.method == "POST"):
        form=EmpresaForms(request.POST,instance=empresa)
        if form.is_valid():
            form.save()           
            return redirect('inicio')
        else:
            return render(request,'Empresas/editar.html',{"error":form}) 
    
    return render(request,"Empresas/editar.html",{"empresa":empresa})


@login_required
def eliminar_empresa(request,id): 
    empresa=Empresa.objects.get(id=id)   
    if(request.method == "POST"):
        empresa.delete()
           
        return redirect('inicio')
       
    
    return render(request,"Empresas/eliminar.html",{"empresa":empresa})


@login_required
def agencias(request):
    
    adminitrador = AdministradorUser.objects.get(user=request.user)
    try:
        
        empresa = Empresa.objects.get(id_administrador=adminitrador)
        list_agencias=Agencia.objects.all()
        return render(request, 'Agencias/inicio.html', {"list_agencias":list_agencias})
        
    except Empresa.DoesNotExist:
        return redirect("/inicio/")
        
    
    


@login_required
def nueva_agencia(request):    
    if(request.method == "POST"):
        form=AgenciaForms(request.POST)
        if form.is_valid():
            administrador=AdministradorUser.objects.get(user=request.user)
            empresa=Empresa.objects.get(id_administrador=administrador)
            agencia=Agencia.objects.create(id_empresa=empresa,
                                           nombre=form.cleaned_data["nombre"],
                                           direccion=form.cleaned_data["direccion"],
                                           provincia=form.cleaned_data["provincia"],
                                           canton=form.cleaned_data["canton"],
                                           correo=form.cleaned_data["correo"])
            messages.add_message(request, messages.SUCCESS, 'Se creo la agencia correctamente.')           
            return redirect('agencias')
        else:
            return render(request,'Agencias/nueva.html',{"error":form}) 
    
    return render(request,"Agencias/nueva.html")
from django.contrib import messages
@login_required
def editar_agencia(request,id):    
    agencia=Agencia.objects.get(id=id)
    if(request.method == "POST"):
        form=AgenciaForms(request.POST,instance=agencia)
        if form.is_valid():
            form.save()           
            messages.add_message(request, messages.SUCCESS, 'Se actualizo la agencia correctamente.')
            return redirect('agencias')
        else:
            return render(request,'Agencias/editar.html',{"error":form}) 
    
    return render(request,"Agencias/editar.html",{"agencia":agencia})


@login_required
def eliminar_agencia(request,id): 
    agencia=Agencia.objects.get(id=id)   
    if(request.method == "POST"):
        agencia.delete()
        messages.add_message(request, messages.SUCCESS, 'Se elimino la agencia correctamente.')
        return redirect('agencias')
       
    
    return render(request,"Agencias/eliminar.html",{"agencia":agencia})

#planes

@login_required
def planes(request): 
    adminitrador = AdministradorUser.objects.get(user=request.user)
    try:
        empresa = Empresa.objects.get(id_administrador=adminitrador)
        #agencia = Agencia.objects.get(id_empresa=empresa.id)
        list_planes=PlanesInternet.objects.all()    
    except Empresa.DoesNotExist:
        return redirect("/inicio/")
    return render(request, 'Planes/inicio.html', {"list_planes":list_planes})
    


@login_required
def nuevo_plan(request):    
    agencias = Agencia.objects.all()
    if(request.method == "POST"):
        form=PlanesInternetForms(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo el plan correctamente.')
            return redirect('planes')
        else:
            if request.is_ajax():      
                print("error")                
                return JsonResponse(form.errors, status=400)
            return render(request,'Planes/nuevo.html',{"error":form,"agencias":agencias}) 
    
    return render(request,"Planes/nuevo.html",{"agencias":agencias})

@login_required
def editar_plan(request,id):    
    agencias = Agencia.objects.all()
    plan=PlanesInternet.objects.get(id=id)
    if(request.method == "POST"):
        form=PlanesInternetForms(request.POST,instance=plan)
        if form.is_valid():
            form.save()           
            messages.add_message(request, messages.SUCCESS, 'Se actualizo el plan correctamente.')
            return redirect('planes')
        else:
            if request.is_ajax():      
                print("error")                
                return JsonResponse(form.errors, status=400)
            return render(request,'Planes/editar.html',{"error":form,"agencias":agencias}) 
    
    return render(request,"Planes/editar.html",{"agencias":agencias,"plan":plan})


@login_required
def eliminar_plan(request,id): 
    plan=PlanesInternet.objects.get(id=id)   
    if(request.method == "POST"):
        messages.add_message(request, messages.SUCCESS, 'Se elimino el plan correctamente.')
        plan.delete()
           
        return redirect('planes')
       
    
    return render(request,"Planes/eliminar.html",{"plan":plan})


#SECRETARIAS

@login_required
def secretarias(request): 
    list_secretarias=Secretaria.objects.all()
    return render(request, 'Secretarias/inicio.html', {"list_secretarias":list_secretarias})
    


@login_required
def nueva_secretaria(request):    
    agencias = Agencia.objects.all()
    if(request.method == "POST"):
        form=UserForms(request.POST)
        if form.is_valid():  
           
            try:
                user_secretaria=User()
                user_secretaria.first_name=form.data.get("first_name")
                user_secretaria.last_name=form.data.get("last_name")
                user_secretaria.email=form.data.get("email")
                user_secretaria.set_password(form.data.get("password"))
                user_secretaria.username=form.data.get("username")
                agencia_select=request.POST.get("agencia","")
                agencia_se=Agencia.objects.get(id=agencia_select)
                user_secretaria.save()
                secretaria=Secretaria.objects.create(agencia=agencia_se,user=user_secretaria)      
            except Agencia.DoesNotExist:
                forms.ValidationError("Seleccione una agencia")
                if request.is_ajax():                      
                    return JsonResponse({"agencia":["Seleccione una agencia"]}, status=400) 
                
            messages.add_message(request, messages.SUCCESS, 'Se creo la secretaria correctamente.')
            return redirect('secretarias')
        else:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
            return render(request,'Secretarias/nueva.html',{"error":"Datos incorrectos","agencias":agencias,"tipo_usuario":"Secretaria"}) 
    
    return render(request,"Secretarias/nueva.html",{"agencias":agencias,"tipo_usuario":"Secretaria" })

@login_required
def editar_secretaria(request,id):    
    secretaria=Secretaria.objects.get(id=id)
    user=User.objects.get(id=secretaria.user.id)
    agencias=Agencia.objects.all()
    if(request.method == "POST"):
        form=UserFormsUpdate(request.POST,instance=user)
        if form.is_valid():
            form.save()           
            messages.add_message(request, messages.SUCCESS, 'Se actualizo la secretaria correctamente.')
            return redirect('secretarias')
        else:
            return render(request,'Secretarias/editar.html',{"error":form,"agencias":agencias,"secretaria":secretaria}) 
    
    return render(request,"Secretarias/editar.html",{"agencias":agencias,"secretaria":secretaria})


@login_required
def eliminar_secretaria(request,id): 
    secretaria=Secretaria.objects.get(id=id)   
    user=User.objects.get(id=secretaria.user.id)   
    if(request.method == "POST"):
        secretaria.delete()
        user.delete()
        messages.add_message(request, messages.SUCCESS, 'Se elimino la secretaria correctamente.')
        return redirect('secretarias')
       
    
    return render(request,"Secretarias/eliminar.html",{"secretaria":secretaria})


#tecnicos

@login_required
def tecnicos(request): 
    list_tecnicos=Tecnico.objects.all()
    return render(request, 'Tecnicos/inicio.html', {"list_tecnicos":list_tecnicos})
    


@login_required
def nuevo_tecnico(request):    
    agencias = Agencia.objects.all()
    if(request.method == "POST"):
        form=UserForms(request.POST)
        if form.is_valid():  
            user_tecnico=User()
            user_tecnico.first_name=form.data.get("first_name")
            user_tecnico.last_name=form.data.get("last_name")
            user_tecnico.email=form.data.get("email")
            user_tecnico.set_password(form.data.get("password"))
            user_tecnico.username=form.data.get("username")
            user_tecnico.save()
            
            agencia_select=request.POST.get("agencia","")
            agencia_se=Agencia.objects.get(id=agencia_select)
            tecnico=Tecnico.objects.create(agencia=agencia_se,user=user_tecnico)           
            messages.add_message(request, messages.SUCCESS, 'Se creo el técnico correctamente.')
            return redirect('tecnicos')
        else:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
            return render(request,'Tecnicos/nuevo.html',{"error":"Datos incorrectos","agencias":agencias,"tipo_usuario":"Tecnico"}) 
    
    return render(request,"Tecnicos/nuevo.html",{"agencias":agencias,"tipo_usuario":"Tecnico" })

@login_required
def editar_tecnico(request,id):    
    tecnico=Tecnico.objects.get(id=id)
    user=User.objects.get(id=tecnico.user.id)
    agencias=Agencia.objects.all()
    if(request.method == "POST"):
        form=UserFormsUpdate(request.POST,instance=user)
        if form.is_valid():
            form.save()           
            messages.add_message(request, messages.SUCCESS, 'Se actualizo el técnico correctamente.')
            return redirect('tecnicos')
        else:
            return render(request,'Tecnicos/editar.html',{"error":form,"agencias":agencias,"tecnico":tecnico}) 
    
    return render(request,"Tecnicos/editar.html",{"agencias":agencias,"tecnico":tecnico})


@login_required
def eliminar_tecnico(request,id): 
    tecnico=Tecnico.objects.get(id=id)   
    user=User.objects.get(id=tecnico.user.id)   
    if(request.method == "POST"):
        tecnico.delete()
        user.delete()
        messages.add_message(request, messages.SUCCESS, 'Se elimino el técnico correctamente.')
        return redirect('tecnicos')
       
    
    return render(request,"Tecnicos/eliminar.html",{"tecnico":tecnicos})




#clientes

@login_required
def clientes(request): 
    list_clientes=Cliente.objects.all()
    return render(request, 'Clientes/inicio.html', {"list_clientes":list_clientes})
    


@login_required
def nuevo_cliente(request):    
    agencias = Agencia.objects.all()
    if(request.method == "POST"):
        form=UserForms(request.POST)
        if form.is_valid():  
            user=form.save()
            agencia_select=request.POST.get("agencia","")
            agencia_se=Agencia.objects.get(id=agencia_select)
            cliente=Cliente.objects.create(agencia=agencia_se,user=user)           
            messages.add_message(request, messages.SUCCESS, 'Se creo el cliente correctamente.')
            return redirect('clientes')
        else:
            print("error")                
            
            if request.is_ajax():      
                print("error")                
                return JsonResponse(form.errors, status=400)
            return render(request,'Clientes/nuevo.html',{"error":"Datos incorrectos","agencias":agencias,"tipo_usuario":"Cliente"}) 
    
    return render(request,"Clientes/nuevo.html",{"agencias":agencias,"tipo_usuario":"Cliente" })

@login_required
def editar_cliente(request,id):    
    cliente=Cliente.objects.get(id=id)
    user=User.objects.get(id=cliente.user.id)
    agencias=Agencia.objects.all()
    if(request.method == "POST"):
        form=UserFormsUpdate(request.POST,instance=user)
        if form.is_valid():
            form.save()           
            messages.add_message(request, messages.SUCCESS, 'Se actualizo el cliente correctamente.')
            return redirect('clientes')
        else:
            return render(request,'Clientes/editar.html',{"error":form,"agencias":agencias,"cliente":cliente}) 
    
    return render(request,"Clientes/editar.html",{"agencias":agencias,"cliente":cliente})


@login_required
def eliminar_cliente(request,id): 
    cliente=Cliente.objects.get(id=id)   
    user=User.objects.get(id=cliente.user.id)   
    if(request.method == "POST"):
        cliente.delete()
        user.delete()
        messages.add_message(request, messages.SUCCESS, 'Se actualizo el cliente correctamente.')
        return redirect('clientes')
       
    
    return render(request,"Clientes/eliminar.html",{"cliente":cliente})





#contratos

@login_required
def contratos(request):     
    lista_contratos=Contrato.objects.all()     
   
    return render(request, 'Contratos/inicio.html', {"lista_contratos":lista_contratos})
    


@login_required
def nuevo_contrato(request):    
    tecnicos=Tecnico.objects.all()
    planes_internet=PlanesInternet.objects.all()

    clientes=Cliente.objects.all()
    if (request.method == "GET"):
        searchCliente=request.GET.get("q","")
        
        if searchCliente != "":
            clientes=clientes.filter(user__last_name="Cliente",user__first_name__icontains=searchCliente)
            return render(request,"Contratos/nuevo.html",{"clientes":clientes,"tecnicos":tecnicos,"planes_internet":planes_internet })
        pass

    if(request.method == "POST"):
        form=ContratoForm(request.POST)
        if form.is_valid():  
            contrato_save=form.save()                 
            url=reverse('nuevo-agendamiento') 
            messages.add_message(request, messages.SUCCESS, 'Se creo el contrato correctamente.')
            return redirect(url+ '?contrato={}'.format(contrato_save.id))
           
        else:
            if request.is_ajax():                      
                return JsonResponse(form.errors, status=400) 
            return render(request,'Contratos/nuevo.html',{"error":"Datos incorrectos","clientes":clientes,"tecnicos":tecnicos,"planes_internet":planes_internet}) 
    
    return render(request,"Contratos/nuevo.html",{"clientes":[],"tecnicos":tecnicos,"planes_internet":planes_internet })
import datetime
@login_required
def editar_contrato(request,id):    
    contrato=Contrato.objects.get(id=id)
    clientes=Cliente.objects.all()
    tecnicos=Tecnico.objects.all()
    planes_internet=PlanesInternet.objects.all()
    
    if(request.method == "POST"):
        form=request.POST
      
        print(request.POST)
        form=ContratoForm(form,instance=contrato)
        if form.is_valid():
            form.save()           
            messages.add_message(request, messages.SUCCESS, 'Se actualizo el contrato correctamente.')
            return redirect('contratos')
        else:
            if request.is_ajax():                      
                return JsonResponse(form.errors, status=400) 
            return render(request,'Contratos/editar.html',{"error":form,"contrato":contrato,"clientes":clientes,"tecnicos":tecnicos,"planes_internet":planes_internet}) 
 
    return render(request,"Contratos/editar.html",{"contrato":contrato,"clientes":clientes,"tecnicos":tecnicos,"planes_internet":planes_internet})


@login_required
def eliminar_contrato(request,id): 
    contrato=Contrato.objects.get(id=id)   
   
    if(request.method == "POST"):
        contrato.delete()
        
        messages.add_message(request, messages.SUCCESS, 'Se elimino el contrato correctamente.')
        return redirect('contratos')
       
    
    return render(request,"Contratos/eliminar.html",{"contrato":contrato})






#agendamientos

@login_required
def agendamientos(request): 
    user = request.user
    print(user.last_name)
    lista_agendamientos=[]
    if user.last_name == "Tecnico":
        tecnico= Tecnico.objects.get(user=user)
        lista_agendamientos= Agendamiento.objects.filter(tecnico=tecnico)
    else:
        lista_agendamientos= Agendamiento.objects.all()
    return render(request, 'Agendamientos/inicio.html', {"lista_agendamientos":lista_agendamientos})
    

def vcedula(texto):
    # sin ceros a la izquierda
    nocero = texto.strip("0")
    
    cedula = int(nocero,0)
    verificador = cedula%10
    numero = cedula//10
    
    # mientras tenga números
    suma = 0
    while (numero > 0):
        
        # posición impar
        posimpar = numero%10
        numero   = numero//10
        posimpar = 2*posimpar
        if (posimpar  > 9):
            posimpar = posimpar-9
        
        # posición par
        pospar = numero%10
        numero = numero//10
        
        suma = suma + posimpar + pospar
    
    decenasup = suma//10 + 1
    calculado = decenasup*10 - suma
    if (calculado  >= 10):
        calculado = calculado - 10

    if (calculado == verificador):
        validado = 1
    else:
        validado = 0
        
    return (validado)



def obtener_datos(request):
    if request.method == "POST":
        import json
        post_data = json.loads(request.body.decode("utf-8"))
        id_cliente = post_data["id"]
       
        contrato_selected = Contrato.objects.filter(
            cliente=id_cliente)
        

        print(contrato_selected[0].plan_internet.precio)

        return response.JsonResponse({
           "costo":contrato_selected[0].plan_internet.precio
           
        })


@login_required
def nuevo_agendamiento(request):  
 
  
    list_tecnicos = Tecnico.objects.all()
    contratoinst=None  
  

    clientes=Cliente.objects.all()
    if (request.method == "GET"):
        searchCliente=request.GET.get("q","")
        
        if searchCliente != "":
            clientes=clientes.filter(user__last_name="Cliente",user__first_name__icontains=searchCliente)
           
            return render(request,"Agendamientos/nuevo.html",{"contrato":contratoinst,"list_contratos":clientes,"list_tecnicos":list_tecnicos })
   
    if(request.method == "POST"):
        form=AgendamientoForm(request.POST)
        if form.is_valid():  
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Se creo el agendamiento correctamente.')           
            return redirect('agendamientos')
        else:
            if request.is_ajax():                      
                return JsonResponse(form.errors, status=400) 
            return render(request,'Agendamientos/nuevo.html',{"error":"Datos incorrectos","form":form}) 
    
    return render(request,"Agendamientos/nuevo.html",{"contrato":contratoinst,"list_contratos":[],"list_tecnicos":list_tecnicos })

@login_required
def editar_agendamiento(request,id):    
    agendamiento_ins=Agendamiento.objects.get(id=id)
    list_contratos = Cliente.objects.all()
    list_tecnicos = Tecnico.objects.all()
    constratos_ins=Cliente.objects.get(id=agendamiento_ins.cliente.id)
    agendamiento_ins.fecha_instalacion=agendamiento_ins.fecha_instalacion.strftime('%m/%d/%Y')
    if(request.method == "POST"):
        agendamiento_insta=Agendamiento.objects.get(id=id)
        form=AgendamientoForm(request.POST,instance=agendamiento_insta)
        if form.is_valid():
            print("valido")
            form.save()         
            messages.add_message(request, messages.SUCCESS, 'Se actualizo el agendamiento correctamente.')             
            return redirect('agendamientos')
        else:
            if request.is_ajax():                      
                return JsonResponse(form.errors, status=400) 
            return render(request,'Agendamientos/editar.html',{"error":form}) 
    
    return render(request,"Agendamientos/editar.html",{"agendamiento":agendamiento_ins,"contrato":constratos_ins,"list_contratos":list_contratos,"list_tecnicos":list_tecnicos})


@login_required
def eliminar_agendamiento(request,id): 
    agendamiento_isn=Agendamiento.objects.get(id=id)   
     
    if(request.method == "POST"):
        agendamiento_isn.delete()
        
        messages.add_message(request, messages.SUCCESS, 'Se elimino el agendamiento correctamente.')
        return redirect('agendamientos')
       
    
    return render(request,"Agendamientos/eliminar.html",{"agendamiento":agendamiento_isn})



#registro pagos
from reportlab.pdfgen import canvas
import io
from PIL import Image
import os
from reportlab.lib.utils import ImageReader
@login_required
def registo_pagos(request): 
    if request.method =="POST":
        buffer = io.BytesIO()
        nombre=request.POST.get("nombre","")
        valor=request.POST.get("valor","")
        fecha=request.POST.get("fecha","")
        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
       
        logo = ImageReader('https://i.ibb.co/7t7PGh3/meganet-removebg-preview.png')
        
        
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawImage(logo, 24, 750,300,50)
        p.drawString(24, 725, "Empresa:")
        p.drawString(100, 725, "Meganet")
        p.drawString(24, 700, "Cliente:")
        p.drawString(100, 700, nombre)
        p.drawString(24, 675, "Valor Cancelado:")
        p.drawString(150, 675, valor)
        p.drawString(24, 650, "Fecha:")
        p.drawString(100, 650, fecha)
        p.drawString(24, 575, "__________________")
        p.drawString(60, 560, "Cliente")
        p.drawString(170, 575, "__________________")
        p.drawString(210, 560, "Empresa")
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    lista_pagos=RegistrosPagos.objects.all()  
   
    print(lista_pagos)
    return render(request, 'RegistroPagos/inicio.html', {"lista_pagos":lista_pagos})
    

from django import forms
from django.forms import ValidationError
@login_required
def nuevo_pago(request):  
    
   
    list_clientes= Cliente.objects.all()

    fechaPago=datetime.datetime.now().strftime('%m/%d/%Y')
    print(fechaPago)
    if (request.method == "GET"):
        searchCliente=request.GET.get("q","")
        
        if searchCliente != "":
            clientes=list_clientes.filter(user__last_name="Cliente",user__first_name__icontains=searchCliente)
            
            return render(request,"RegistroPagos/nuevo.html",{"list_clientes":clientes,"fecha":fechaPago })
    if(request.method == "POST"):
        form=RegistrosPagosForm(request.POST)
        if form.is_valid(): 
            try:               
                registro = RegistrosPagos.objects.get(create_at=datetime.date.today(),cliente=form.cleaned_data["cliente"])
                if registro:                    
                    forms.ValidationError("Ya existe un pago registrado el dia de hoy")
                    print(request.is_ajax())
                    if request.is_ajax():  
                        return JsonResponse({"cliente":["Ya existe un pago registrado el dia de hoy"]}, status=400) 
                    else:
                        return JsonResponse({"cliente":["Ya existe un pago registrado el dia de hoy"]}, status=400) 

            except RegistrosPagos.DoesNotExist:
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Se creo el registro de pago correctamente.')
                return redirect('registro-pagos')
                pass
    
        else:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
            return render(request,'RegistroPagos/nuevo.html',{"error":"Datos incorrectos","form":form}) 
    
    return render(request,"RegistroPagos/nuevo.html",{"list_clientes":[],"fecha":fechaPago })

@login_required
def editar_pago(request,id):    
    pago_ins=RegistrosPagos.objects.get(id=id)
    pago_ins.fecha_pago=pago_ins.fecha_pago.strftime('%m/%d/%Y')
    lista_pagos = RegistrosPagos.objects.all()   
    list_clientes= Cliente.objects.all()
    if(request.method == "POST"):
        form=RegistrosPagosForm(request.POST,instance=pago_ins)
        if form.is_valid():
            form.save()   
            messages.add_message(request, messages.SUCCESS, 'Se actualizo el registro de pago correctamente.')        
            return redirect('registro-pagos')
        else:
            return render(request,'RegistroPagos/editar.html',{"error":form,"lista_pagos":lista_pagos,"list_clientes":list_clientes}) 
    
    return render(request,"RegistroPagos/editar.html", {"lista_pagos":lista_pagos,"list_clientes":list_clientes,"pago":pago_ins })


@login_required
def eliminar_pago(request,id): 
    pagos=RegistrosPagos.objects.get(id=id)   
     
    if(request.method == "POST"):
        pagos.delete()
        
        messages.add_message(request, messages.SUCCESS, 'Se elimino el registro de pago correctamente.')
        return redirect('registro-pagos')
       
    
    return render(request,"RegistroPagos/eliminar.html",{"pagos":pagos})


from django.contrib.auth.forms import PasswordChangeForm

@login_required   
def cambiarContraseña(request,id):
    isn=User.objects.get(id=id)
    data={
        "form":PasswordChangeForm(isn, request.POST),
        "id":isn.id
    }
    if request.method == "POST":
        form=PasswordChangeForm(isn, request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()            
            return redirect('tecnicos')
        else:
            print(form)
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
            return render(request,'cambiarpassword.html',form) 


    return render(request,"cambiarpassword.html",data)
    pass  