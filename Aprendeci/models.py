from django.contrib.auth.models import User
from django.db import models


class Grafo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    grafoPadre = models.ForeignKey("self", blank=True, null=True)

    # Devuelve el numero de conceptos pertenecientes a este grafo
    def numero_de_conceptos(self):
        numConceptos = self.concepto_set.all().count()
        for grafo in self.grafo_set.all():
            numConceptos += grafo.concepto_set.all().count()
        return numConceptos

    # Devuelve la lista de conceptos pertenecientes a este grafo
    def obtener_conceptos(self, incluir_indirectos):
        conceptos = set()

        for concepto in self.concepto_set.all():
            conceptos.add(concepto)

        if incluir_indirectos:
            for grafo in self.grafo_set.all():
                for concepto in grafo.obtener_conceptos(True):
                    conceptos.add(concepto)

        return conceptos

    # Devuelve la lista de grafos que tienen como padre
    def obtener_grafos(self):
        grafos = set()

        for grafo in Grafo.objects.all():
            if grafo.grafoPadre == self:
                grafos.add(grafo)

        return grafos

    # Devuelve la lista de grafos que podrian incluirse en este
    def obtener_grafos_posibles(self):
        grafos = set()

        for grafo in Grafo.objects.all():
            if grafo != self and grafo.grafoPadre != self and grafo.grafoPadre != self.grafoPadre and grafo !=  self.grafoPadre:
                grafos.add(grafo)

        return grafos

    # Indica si el grafo pertenece al curso recibido
    def pertenece_al_curso(self, cursoId):
        curso = Curso.objects.get(pk=cursoId)
        if self == curso.grafo:
            return True
        else:
            if not self.grafoPadre is None:
                return self.grafoPadre.pertenece_al_curso(cursoId)
            else:
                return False

    # Indica si algun concepto del grafo tiene relacion
    def esta_relacionado_con(self, grafoId):
        grafo = Grafo.objects.get(pk=grafoId)
        for concepto in self.concepto_set.all():
            for conceptoExterno in grafo.concepto_set.all():
                if conceptoExterno.requisitos.filter(pk=concepto.pk).count() > 0:
                    return True

        return False

    def __str__(self):
        return self.nombre


class Concepto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
    imagen = models.ImageField(upload_to="img/icons/conceptos", default="img/icons/conceptos/defecto.png")
    requisitos = models.ManyToManyField("self", symmetrical=False, blank=True)
    porcentajeBase = models.IntegerField(default=60)
    color = models.CharField(max_length=6)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    grafo = models.ForeignKey(Grafo, blank=True)

    def pertenece_al_curso(self, cursoId):
        return self.grafo.pertenece_al_curso(cursoId)

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
        conceptos = curso.grafo.obtener_conceptos(True)
        for c in conceptos:
            calificacion = Calificaciones(estudiante=self, concepto=c, calificacion=0)
            calificacion.save()

    def __str__(self):
        return self.usuario.first_name + " " + self.usuario.last_name


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
    profesor = models.ForeignKey(Profesor, related_name='profesor')
    estudiantes = models.ManyToManyField(Estudiante, related_name='estudiantes')

    def numero_de_estudiantes(self):
        return self.estudiantes.count()

    def estudiantes_aprobados(self, conceptos, aprobados):
        for con in self.grafo.concepto_set.all():
            numEst = 0

            for est in self.estudiantes.all():
                calificacion = Calificaciones.objects.filter(estudiante=est, concepto=con).first()

                if calificacion is None:
                    calificacion = Calificaciones(estudiante=est, concepto=con, calificacion=0)
                    calificacion.save()
                else:
                    if calificacion.calificacion >= con.porcentajeBase:
                        numEst += 1

            conceptos.append(con.nombre)
            aprobados.append(numEst)

    def tiene_estudiante(self, estudiante):
        if estudiante.estudiante in self.estudiantes.all():
            return True

        return False

    def __str__(self):
        return self.nombre