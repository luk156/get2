from django.db import models

# Create your models here.

STATI_MEZZI=( ('disponbile','Disponibile'), ('indisponibile','Non Disponibile'), )


class Mezzo(models.Model):
	targa=models.CharField('Targa', max_length=7)
	marca=models.CharField('Marca costrutrice', max_length=20)
	modello=models.CharField('Modello', max_length=20)
	stato=models.CharField('Stato', max_length=40, choices=STATI_MEZZI, default='disponibile')