from django.test import TestCase
from animals.models import Animal
from traits.models import Trait
from groups.models import Group
from django.core.exceptions import ValidationError


class AnimalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        
        cls.animal_data = {
            "name": "odin",
            "age": 2,
            "weight": 30,
            "sex": "Macho",
        }

        cls.animal_data_2 = {
            "name": "thor",
            "age": 4,
            "weight": 20,
            "sex": "Invalido",
        }

        cls.group_data = {
            "name": "cão", 
            "scientific_name": "canis familiaris"
        }

        cls.traits_data_1 = {
            "name": "peludo"
        }

        cls.traits_data_2 = {
            "name": "médio porte"
        }

        cls.trait_1 = Trait.objects.create(**cls.traits_data_1)
        cls.trait_2 = Trait.objects.create(**cls.traits_data_2)
        cls.group = Group.objects.create(**cls.group_data)
        cls.animal = Animal.objects.create(**cls.animal_data, group=cls.group)
        cls.animal_2 = Animal.objects.create(**cls.animal_data_2, group=cls.group)

    def test_animal_fields(self):
        print("Test for animal fields")

        self.assertEqual(self.animal_data["name"], self.animal.name)
        self.assertEqual(self.animal_data["age"], self.animal.age)
        self.assertEqual(self.animal_data["weight"], self.animal.weight)
        self.assertEqual(self.animal_data["sex"], self.animal.sex)
    

    def test_animal_fields_parameters(self):
        print("Test for animal fields parameters")

        animal_test_1 = Animal.objects.get(id = 1)
        name_max_length = animal_test_1._meta.get_field('name').max_length
        sex_max_length = animal_test_1._meta.get_field('sex').max_length 
        weight_max_digits = animal_test_1._meta.get_field('weight').max_digits

        self.assertEqual(name_max_length, 50) 
        self.assertEqual(sex_max_length, 15) 
        self.assertEqual(weight_max_digits, 6)

    def test_animal_sex_invalid_choice(self):
        print("Test for animal sex invalid choice")

        self.assertRaises(ValidationError, self.animal_2.full_clean)
    
    def test_animal_may_contain_several_traits(self):
        print("Test for animal may contain several traits")
        self.animal.traits.set([self.trait_1, self.trait_2])

        self.assertEquals(self.animal.traits.count(), 2)
        self.assertIn(self.trait_1 and self.trait_2, self.animal.traits.all())