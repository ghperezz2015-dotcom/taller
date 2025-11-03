from django.contrib.auth.models import AbstractUser
from django.db import models

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Taller(models.Model):
    id_taller = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    capacidad = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre_rol

class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
    # Django AbstractUser ya tiene username, password, etc.
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class EstadoVehiculo(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    
    def __str__(self):
        return self.nombre_estado

class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    patente = models.CharField(max_length=6, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    edad = models.IntegerField()
    vida_util = models.IntegerField()
    kilometraje = models.IntegerField()
    operativo = models.CharField(max_length=1)
    tipo_vehiculo = models.CharField(max_length=50)
    para_remate = models.CharField(max_length=1)
    cumplimiento = models.CharField(max_length=50)
    tct = models.CharField(max_length=50)
    plan_verano = models.CharField(max_length=1)
    
    # Foreign Keys
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado_vehiculo = models.ForeignKey(EstadoVehiculo, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.patente

class RegistroVehiculo(models.Model):
    id_registro = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=300)
    foto = models.ImageField(upload_to='vehiculos/', blank=True, null=True)  # Cambié BFILE a ImageField
    
    # Foreign Keys
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado_vehiculo = models.ForeignKey(EstadoVehiculo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Registro {self.id_registro} - {self.vehiculo.patente}"

class Agenda(models.Model):
    id_agenda = models.AutoField(primary_key=True)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Agenda {self.id_agenda} - {self.taller.nombre}"

class Tarea(models.Model):
    id_tarea = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=50)
    prioridad = models.CharField(max_length=50)
    
    # Foreign Keys
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo

class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    contenido = models.CharField(max_length=300)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    leido = models.CharField(max_length=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Mensaje {self.id_mensaje} - {self.usuario.nombre}"

class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50)
    contenido = models.CharField(max_length=500)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.titulo

class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    nombre_ruta = models.CharField(max_length=50)
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia_km = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre_ruta

class RutaVehiculo(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['ruta', 'vehiculo']
    
    def __str__(self):
        return f"{self.vehiculo.patente} - {self.ruta.nombre_ruta}"