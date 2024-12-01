
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Usuario, Docente, Material

# Vista para el login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

# Vista para cerrar sesión
def user_logout(request):
    logout(request)
    return redirect('login')

## HOME 

@login_required
def home(request):
    return render(request, 'home.html', {'es_admin': request.user.is_superuser})


## CRUD USUARIO

# Crear usuario
@login_required
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
@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.filter(estado=True)  
    return render(request, 'usuarios/listar_usuarios.html', {
        'usuarios': usuarios
    })

# Actualizar usuario
@login_required
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
@login_required
def eliminar_usuarios(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuario')
    return render(request, 'usuarios/eliminar_usuarios.html', {'usuario': usuario})

## CRUD DOCENTE

# Crear Docente 
@login_required
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
@login_required
def listar_docentes(request):
    docente = Docente.objects.all()  
    return render(request, 'docentes/listar_docente.html', {
        'docentes': docente
    })

# Actualizar Docente
@login_required
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
@login_required 
def eliminar_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        docente.delete()
        return redirect('listar_docente')
    return render(request, 'docentes/eliminar_docente.html', {'docente': docente})

## CRUD para materiales

# crear material 
@login_required
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
@login_required
def listar_materiales(request):
    materiales = Material.objects.all()  
    return render(request, 'materiales/listar_materiales.html', {
        'materiales': materiales  #
    })

# actualizar material
@login_required 
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


@login_required
# eliminar material
def eliminar_materiales(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.delete()
        return redirect('listar_materiales')
    return render(request, 'materiales/eliminar_materiales.html', {'materiales': material})
