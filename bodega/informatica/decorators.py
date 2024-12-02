from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def administrador_required(view_func):
    def wrapper(request, *args, **kwargs):
        usuario_rol = request.session.get('usuario_rol')
        if usuario_rol == 1:  # Verifica si es administrador
            return view_func(request, *args, **kwargs)
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return wrapper

def panol_required(view_func):
    def wrapper(request, *args, **kwargs):
        usuario_rol = request.session.get('usuario_rol')
        if usuario_rol == 2:  # Verifica si es pañol
            return view_func(request, *args, **kwargs)
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return wrapper
