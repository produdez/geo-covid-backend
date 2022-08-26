
from django.test import TestCase
from djongo import models

# Model For Testing
class SampleTestModel(models.Model):
    name = models.TextField()
    num = models.IntegerField()


class AnimalTestCase(TestCase):
    def setUp(self):
        SampleTestModel.objects.create(name="lion", num=134)
        SampleTestModel.objects.create(name="cat", num=3456)

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = SampleTestModel.objects.get(name="lion")
        cat = SampleTestModel.objects.get(name="cat")
        self.assertEqual(lion.num, 134)
        self.assertEqual(cat.num, 3456)
    def test3(self):
        """Animals that can speak are correctly identified"""
        SampleTestModel.objects.create(name="cat", num=3456)
        self.assertEqual(SampleTestModel.objects.count(), 3)
    def test4(self):
        """Animals that can speak are correctly identified"""
        SampleTestModel.objects.create(name="cat", num=3456)
        self.assertEqual(SampleTestModel.objects.count(), 3)
    def test5(self):
        """Animals that can speak are correctly identified"""
        self.assertEqual(SampleTestModel.objects.count(), 2)
