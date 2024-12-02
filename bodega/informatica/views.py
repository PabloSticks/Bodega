from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario, Docente, Material, AsignacionMaterial
from .decorators import administrador_required, panol_required

def user_login(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        password = request.POST.get('password')

        try:
            user = Usuario.objects.get(nombre=nombre)
            if check_password(password, user.password):
                request.session['usuario_id'] = user.id
                request.session['usuario_nombre'] = user.nombre
                request.session['usuario_rol'] = user.id_rol
                if user.id_rol == 1:
                    return redirect('home')
                elif user.id_rol == 2:
                    return redirect('home')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except Usuario.DoesNotExist:
            messages.error(request, 'Nombre de usuario no encontrado')

    return render(request, 'login.html')



# Vista para cerrar sesión
def user_logout(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('login')

def permission_denied_view(request, exception=None):
    return render(request, 'permission_denied.html', status=403)

## HOME 

def home(request):
    usuario_rol = request.session.get('usuario_rol')

    # Validar roles
    es_admin = usuario_rol == 1
    es_panol = usuario_rol == 2

    if es_admin:
        # Renderiza el panel del administrador
        return render(request, 'home.html', {'es_admin': es_admin, 'es_panol': False})
    elif es_panol:
        # Renderiza el panel del pañol
        return render(request, 'home.html', {'es_admin': False, 'es_panol': es_panol})
    else:
        # Si no tiene permisos, lanza un error 403
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied


## CRUD USUARIO

# Crear usuario
@administrador_required
def crear_usuarios(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        password = make_password(request.POST['password'])  # Encripta la contraseña
        id_rol = request.POST['id_rol']

        Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            password=password,
            id_rol=id_rol
        )
        return redirect('listar_usuario')  
    return render(request, 'usuarios/crear_usuarios.html')

# Listar usuarios
@administrador_required
def listar_usuarios(request):
    usuarios = Usuario.objects.filter(estado=True)  
    return render(request, 'usuarios/listar_usuarios.html', {
        'usuarios': usuarios
    })

# Actualizar usuario
@administrador_required
def actualizar_usuarios(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        usuario.nombre = request.POST['nombre']
        usuario.correo = request.POST['correo']
        usuario.password = make_password(request.POST['password'])  
        usuario.id_rol = request.POST['id_rol']
        usuario.save()
        return redirect('listar_usuario')
    return render(request, 'usuarios/actualizar_usuarios.html', {'usuario': usuario})

# Eliminar usuario
@administrador_required
def eliminar_usuarios(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuario')
    return render(request, 'usuarios/eliminar_usuarios.html', {'usuario': usuario})

## CRUD DOCENTE

# Crear Docente 
@administrador_required
def crear_docente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        estado = request.POST.get('estado') == 'on'  

        Docente.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            estado=estado
        )
        return redirect('listar_docente')  # Redirigir al listado de docentes
    return render(request, 'docentes/crear_docente.html')

# Listar Docente 
@administrador_required
def listar_docentes(request):
    docente = Docente.objects.all()  
    return render(request, 'docentes/listar_docente.html', {
        'docentes': docente
    })

# Actualizar Docente
@administrador_required
def actualizar_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        docente.nombre = request.POST['nombre']
        docente.correo = request.POST['correo']
        docente.telefono = request.POST['telefono']
        docente.estado = request.POST.get('estado') == 'on'
        docente.save()
        return redirect('listar_docente')
    return render(request, 'docentes/actualizar_docente.html', {'docente': docente})

# Eliminar Docente
@administrador_required
def eliminar_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        docente.delete()
        return redirect('listar_docente')
    return render(request, 'docentes/eliminar_docente.html', {'docente': docente})

## CRUD para materiales

# crear material 
@administrador_required
def crear_materiales(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']  # Cambiado de POST() a POST[]
        modelo = request.POST['modelo']
        stock = request.POST['stock']
        estado = request.POST.get('estado') == 'on'  # Para manejar checkboxes

        Material.objects.create(
            nombre=nombre,
            modelo=modelo,
            stock=stock,
            estado=estado
        )
        return redirect('listar_materiales')  # Redirigir al listado de materiales
    return render(request, 'materiales/crear_materiales.html')

# listar material 
@administrador_required
def listar_materiales(request):
    materiales = Material.objects.all()  
    return render(request, 'materiales/listar_materiales.html', {
        'materiales': materiales  #
    })

# actualizar material
@administrador_required
def actualizar_materiales(request, material_id):
    material = get_object_or_404(Material, id=material_id)  
    if request.method == 'POST':
        material.nombre = request.POST['nombre']
        material.modelo = request.POST['modelo']
        material.stock = request.POST['stock']
        material.estado = request.POST.get('estado') == 'on'
        material.save()
        return redirect('listar_material')
    return render(request, 'materiales/actualizar_materiales.html', {'material': material})


@administrador_required
# eliminar material
def eliminar_materiales(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.delete()
        return redirect('listar_materiales')
    return render(request, 'materiales/eliminar_materiales.html', {'materiales': material})


# ASIGNAR MATERIAL 

@panol_required
def registrar_asignacion(request):    
    if request.method == 'POST':
        docente_id = request.POST['docente']
        material_id = request.POST['material']
        cantidad = int(request.POST['cantidad'])

        docente = Docente.objects.get(id=docente_id)
        material = Material.objects.get(id=material_id)

        if material.stock >= cantidad:  # Validar que hay suficiente stock
            material.stock -= cantidad  
            material.save()

            AsignacionMaterial.objects.create(
                docente=docente,
                material=material,
                cantidad=cantidad
            )
            return redirect('listar_asignaciones')  
        else:
            return render(request, 'asignaciones/error_stock.html')  

    docentes = Docente.objects.all()
    materiales = Material.objects.all()
    return render(request, 'asignaciones/registrar_asignacion.html', {
        'docentes': docentes,
        'materiales': materiales
    })

@panol_required
def listar_asignaciones(request):
    asignaciones = AsignacionMaterial.objects.all()
    return render(request, 'asignaciones/listar_asignaciones.html', {'asignaciones': asignaciones})
