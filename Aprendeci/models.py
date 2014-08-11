from django.contrib.auth.models import User
from django.db import models

class Grafo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    grafoPadre = models.ForeignKey("self", blank=True, null=True)

    def numero_de_conceptos(self):
        numConceptos = self.concepto_set.all().count()
        for grafo in self.grafo_set.all():
            numConceptos += grafo.concepto_set.all().count()
        return numConceptos

    def obtener_conceptos(self):
        conceptos = set()

        for concepto in self.concepto_set.all():
            conceptos.add(concepto)

        for grafo in self.grafo_set.all():
            for concepto in grafo.obtener_conceptos():
                conceptos.add(concepto)

        return conceptos

    def __str__(self):
        return self.nombre


class Concepto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
    imagen = models.ImageField(upload_to="img/icons/conceptos")
    requisitos = models.ManyToManyField("self", symmetrical=False, blank=True)
    porcentajeBase = models.IntegerField(default=60)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    grafo = models.ForeignKey(Grafo, blank=True)

    def __str__(self):
        return self.nombre


class Recurso(models.Model):
    DOCUMENTO = 'D'
    ENLACE = 'E'
    VIDEO = 'V'
    TIPOS_RECURSO = (
        (ENLACE, 'Enlace'),
        (DOCUMENTO, 'Documento'),
        (VIDEO, 'Video'),
    )

    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
    tipo = models.CharField(max_length=1, choices=TIPOS_RECURSO)
    direccion = models.CharField(max_length=100)
    concepto = models.ForeignKey(Concepto)

    def __str__(self):
        return self.nombre


class Profesor(models.Model):
    usuario = models.OneToOneField(User)


class Estudiante(models.Model):
    usuario = models.OneToOneField(User)
    conceptos = models.ManyToManyField(Concepto, through="Calificaciones")

    def enrolarse(self, curso):
        curso.estudiantes.add(self)
        conceptos = curso.grafo.obtener_conceptos()
        for c in conceptos:
            calificacion = Calificaciones(estudiante=self, concepto=c, calificacion=0)
            calificacion.save()


class Calificaciones(models.Model):
    estudiante = models.ForeignKey(Estudiante)
    concepto = models.ForeignKey(Concepto)
    calificacion = models.IntegerField()


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    sigla = models.CharField(max_length=4)
    clave = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="img/cursos", default="img/cursos/Defecto.jpg")
    grafo = models.ForeignKey(Grafo)
    profesor = models.ForeignKey(Estudiante, related_name='profesor')
    estudiantes = models.ManyToManyField(Estudiante, related_name='estudiantes')

    def numero_de_estudiantes(self):
        return self.estudiantes.count()

    def __str__(self):
        return self.nombre