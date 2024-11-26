from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class TipoInmueble(models.Model):
    tipo_inmueble = models.CharField(
        max_length=20,
        choices=[
            ('Casa', 'Casa'),
            ('Departamento', 'Departamento'),
            ('Parcela', 'Parcela'),
        ]
    )

    def __str__(self):
        return self.tipo_inmueble


class Region(models.Model):
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.region


class Comuna(models.Model):
    comuna = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.comuna} ({self.region.region})"


class TipoUsuario(models.Model):
    tipo_usuario = models.CharField(
        max_length=20,
        choices=[
            ('arrendatario', 'Arrendatario'),
            ('arrendador', 'Arrendador'),
        ]
    )

    def __str__(self):
        return self.tipo_usuario


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    rut = models.CharField(max_length=12)  
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.tipo_usuario}"


class Inmueble(models.Model):
    propietario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='propiedades')
    tipo_inmueble = models.ForeignKey(TipoInmueble, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    nombre_inmueble = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    m2_construido = models.FloatField()
    numero_banos = models.IntegerField(default=0)
    numero_hab = models.IntegerField(default=0)
    direccion = models.CharField(max_length=200)
    numero_estacionam = models.IntegerField(default=0)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True) 
    precio = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Check if the 'propietario' is an 'arrendador' (landlord)
        if self.propietario.tipo_usuario.tipo_usuario != 'arrendador':
            raise PermissionDenied("Only 'arrendadores' can create inmuebles.")
        
        # Call the parent class's save method
        super(Inmueble, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_inmueble


class Solicitud(models.Model):
    arrendatario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='solicitudes')
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('aprobada', 'Aprobada'),
            ('rechazada', 'Rechazada'),
        ],
        default='pendiente'
    )

    def __str__(self):
        return f"Solicitud by {self.arrendatario} for {self.inmueble}"
