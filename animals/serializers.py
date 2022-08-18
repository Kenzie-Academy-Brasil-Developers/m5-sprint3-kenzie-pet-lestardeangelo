import math

from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from traits.models import Trait
from traits.serializers import TraitSerializer

from .models import Animal, SexAnimal


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexAnimal.choices, default=SexAnimal.OTHER)

    age_in_human_years = serializers.SerializerMethodField()

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def get_age_in_human_years(self, obj: Animal) -> int:
        return 16 * math.log(obj.age) + 31

    def create(self, validated_data: dict) -> Animal:

        group_data = validated_data.pop("group")
        trait_data = validated_data.pop("traits")

        group, _ = Group.objects.get_or_create(**group_data)

        animal_obj: Animal = Animal.objects.create(**validated_data, group=group)

        for trait in trait_data:
            trait, _ = Trait.objects.get_or_create(**trait)
            animal_obj.traits.add(trait)

        return animal_obj

    def update(self, instance: Animal, validated_data: dict) -> Animal:
        non_editable = ("traits", "group", "sex")
        errors = {}

        for key, value in validated_data.items():
            if key in non_editable:
                errors.update({key: f"You can not update {key} property."})
                continue

            setattr(instance, key, value)

        if errors:
            raise ValidationError(errors)

        instance.save()

        return instance
