from django.urls import path
from . import views

handler403 = 'informatica.views.permission_denied'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    
    path('listar_usuario/', views.listar_usuarios, name='listar_usuario'),
    path('crear_usuario/', views.crear_usuarios, name='crear_usuario'),
    path('actualizar_usuario/<int:user_id>/', views.actualizar_usuarios, name='actualizar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuarios, name='eliminar_usuario'),

    path('crear_docente/', views.crear_docente, name='crear_docente'),
    path('listar_docente/', views.listar_docentes, name='listar_docente'),
    path('actualizar_docente/<int:docente_id>/', views.actualizar_docente, name='actualizar_docente'),
    path('eliminar_docente/<int:docente_id>/', views.eliminar_docente, name='eliminar_docente'),

    path('crear_materiales/', views.crear_materiales, name='crear_materiales'),
    path('listar_materiales/', views.listar_materiales, name='listar_materiales'),
    path('actualizar_materiales/<int:material_id>/', views.actualizar_materiales, name='actualizar_materiales'),
    path('eliminar_materiales/<int:material_id>/', views.eliminar_materiales, name='eliminar_materiales'),

    path('registrar_asignacion/', views.registrar_asignacion, name='registrar_asignacion'),
    path('listar_asignaciones/', views.listar_asignaciones, name='listar_asignaciones'),
]


