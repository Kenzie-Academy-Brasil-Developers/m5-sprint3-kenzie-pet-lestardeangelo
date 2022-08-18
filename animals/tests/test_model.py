from animals.models import Animal
from django.core.exceptions import ValidationError
from django.test import TestCase
from groups.models import Group
from traits.models import Trait


class AnimalTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.animal_1_data = {
            "name": "Beethoven",
            "age": 1,
            "weight": 30,
            "sex": "Macho",
            "group": {"name": "cão", "scientific_name": "canis familiaris"},
            "traits": [{"name": "peludo"}, {"name": "médio porte"}],
        }

        cls.animal_2_data = {
            "name": "Beethoven",
            "age": 1,
            "weight": 30,
            "group": {"name": "cão", "scientific_name": "canis familiaris"},
            "traits": [{"name": "peludo"}, {"name": "médio porte"}],
        }

        cls.animal_3_data = {
            "name": "Beethoven",
            "age": 1,
            "weight": 30,
            "sex": "Sex Invalido",
        }

        cls.sex_default = "Não informado"

        cls.animal_1 = Animal.objects.create(**cls.animal_1_data)
        cls.animal_2 = Animal.objects.create(**cls.animal_2_data)
        cls.animal_3 = Animal(**cls.animal_3_data)

        cls.animals = [Animal.objects.create(cache=50000) for _ in range(20)]
        cls.group = Group.objects.create(name="cão", scientific_name="canis familiaris")

        cls.trait = Trait.objects.create(name="trat 1")


        def test_name_max_length(self):
            max_length = self.animal_1._meta.get_field("name").max_length
            self.assertEquals(max_length, 50)

        def test_sex_default_choice(self):
            sex_default = self.animal_2.sex

            self.assertEqual(sex_default, self.sex_default)

        def test_sex_wrong_choice(self):
            self.assertRaises(ValidationError, self.aniaml_3.full_clean)

        # test 1:n
        def test_group_may_contain_multiple_animals(self):
            # loop para verificar a quantidade de filmes que a companhia tem se é a mesma quantidade de filmes criados.
            for animal in self.animals:
                animal.group = self.group
                animal.save()

            self.assertEquals(len(self.animals), self.group.animals.count())

            # loop para verificar se o group de cada animal é o mesmo para todos.
            for animal in self.animals:
                self.assertIs(animal.group, self.group)

        def test_animal_cannot_belong_to_more_than_one_group(self):
            for animal in self.animals:
                animal.group = self.group
                animal.save()

            group_2 = Group.objects.create(
                name="cão 2", scientific_name="canis familiaris 2"
            )

            # Percorrendo o loop, estamos atualizando a instância de cada aniaml passando um novo group
            for animal in self.animals:
                animal.group = group_2
                animal.save()

            # Aqui estamos verificando se os aniamis não estão presentes no primeirao group.
            # Alem de analisamos se os animais estão presentes no segundo group.
            for animal in self.animals:
                self.assertNotIn(animal, self.group.animals.all())
                self.assertIn(animal, group_2.animals.all())

        # test n:n
        def test_trait_can_be_attached_to_multiple_animals(self):

            for animal in self.animals:
                self.trait.animals.add(animal)

            self.assertEquals(len(self.animals), self.trait.animals.count())

            for animal in self.animals:
                self.assertIn(self.trait, animal.traits.all())
