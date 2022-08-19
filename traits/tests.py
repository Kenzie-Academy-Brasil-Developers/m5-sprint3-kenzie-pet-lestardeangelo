from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Trait

class TraitTestCase(TestCase):
    @classmethod

    def setUpTestData(cls) -> None:
        cls.correct_trait = {
            "name": "peludo"
        }

        cls.incorrect_trait = {}

    def test_trait_properties(self):
        trait = Trait.objects.create(**self.correct_trait)

        self.assertEqual(trait.name, self.correct_trait['name'])

    def test_create_trait_without_name(self):
        trait = Trait(**self.incorrect_trait)

        with self.assertRaises(ValidationError):
            trait.full_clean()