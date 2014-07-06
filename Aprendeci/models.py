from django.db import models

class Grafo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    grafoPadre = models.ForeignKey("self", blank=True, null=True)

    def numeroDeConceptos(self):
        return 5

    def __str__(self):
        return self.nombre

class Concepto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True, editable=False)
    imagen = models.ImageField(upload_to="img/icons/conceptos")
    requisitos = models.ManyToManyField("self", symmetrical=False, blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    grafo = models.ForeignKey(Grafo, blank=True)

    def __str__(self):
        return self.nombre