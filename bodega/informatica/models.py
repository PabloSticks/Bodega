from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    id_rol = models.IntegerField(choices=[(1, 'Administrador'), (2, 'Pañol')])
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    estado = models.BooleanField(default=True)  # Activo o inactivo
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    
class AsignarMaterial(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.docente.nombre} - {self.material.nombre}"

