from django.test import TestCase

from .models import Course, CourseProvider

class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        CourseProvider.objects.create(name='Test Provider')
        Course.objects.create(name='Test Course', description='Test Description')

    def test_name_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_name_max_length(self):
        course = Course.objects.get(id=1)
        max_length = course._meta.get_field('name').max_length
        self.assertEquals(max_length, 128)

    def test_object_name_is_name(self):
        course = Course.objects.get(id=1)
        expected_object_name = f'{course.__str__()}'
        self.assertEquals(expected_object_name, str(course))

