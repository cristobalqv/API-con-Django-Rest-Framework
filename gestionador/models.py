from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    descripcion = models.TextField()
    autores = models.ManyToManyField('Autor', related_name='libros')
    copias_totales = models.PositiveIntegerField()
    copias_disponibles = models.PositiveIntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.copias_disponibles < 0:
            raise ValidationError("Las copias disponibles no pueden ser negativas.")

    def save(self, *args, **kwargs):
        print(f"Guardando libro: {self.titulo} con {self.copias_disponibles} copias disponibles")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo



class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    biografia = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'



class Prestamo(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'libro'],
                condition=models.Q(estado='ACTIVO'),
                name='unique_active_loan'
            )
        ]

    ESTADO_PRESTAMO = [
        ('ACTIVO', 'activo'),
        ('ATRASADO', 'atrasado'),
        ('DEVUELTO', 'devuelto'),
        ('PERDIDO', 'perdido')
    ]

    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    libro = models.ForeignKey(Libro, on_delete=models.PROTECT)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateTimeField()
    fecha_devolucion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PRESTAMO, default='ACTIVO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):  # Corregido de __Str__ a __str__
        return f'Usuario: {self.usuario}. Libro: {self.libro}. Estado del prestamo: {self.estado}'