from tokenize import group

from django.db import models


class SexAnimal(models.TextChoices):
    MACHO = "Macho"
    FEMEA = "Femea"
    OTHER = "Não informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, choices=SexAnimal.choices, default=SexAnimal.OTHER
    )

    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="animals")
    traits = models.ManyToManyField("traits.trait", related_name="animals")

    def __repr__(self) -> str:
        return f"Animal {self.id} - {self.name}"
