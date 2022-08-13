from email.policy import default
from pyexpat import model
from tkinter import CASCADE
from django.db import models

class Sex(models.TextChoices):
    default = "Não informado."
    male = "Macho"
    female = "Femea"

# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=15, choices=Sex.choices, default=Sex.default)


    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="animals")

    traits = models.ManyToManyField("traits.Trait", related_name="animals")

    def __repr__(self) -> str:
        return f"<Animal {self.id} - {self.name}>"