from functools import cache

from animals.models import Animal
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Group

# Create your tests here.

class GroupTestCase(TestCase):
    @classmethod

    def setUpTestData(cls) -> None:
        cls.correct_group_data = {
            "name": "cão",
            "scientific_name": "canis familiaris"
        }

        cls.group_data_without_name = {
            "scientific_name": "canis familiaris"
        }

        cls.group_data_without_specific_name = {
            "scientific_name": "canis familiaris"
        }

        cls.group = Group.objects.create(**cls.correct_group_data)

    def test_group_properties(self) -> None: 

        self.assertEqual(self.group.name, self.correct_group_data['name'])
        self.assertEqual(self.group.scientific_name, self.correct_group_data['scientific_name'])

    def test_create_group_without_name(self) -> None: 
        group = Group(**self.group_data_without_name)

        with self.assertRaises(ValidationError):
            group.full_clean()

    def test_create_group_without_scientific_name(self) -> None: 
        group = Group(**self.group_data_without_specific_name)


        with self.assertRaises(ValidationError):
            group.full_clean()


    def test_group_may_contain_multiple_animals(self):
        animals = [Animal.objects.create(**{
            "name": "Beethoven",
            "age": 1,
            "weight": 30,
            "sex": "Macho",
            "group": self.group
        }) for _ in range(20)]

        for animal in animals:
            self.assertIs(animal.group, self.group)