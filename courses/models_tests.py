# Python
from django.test import TestCase
from datetime import date
from .models import (
    Course, CourseProvider, User, 
    CourseAdd, OrderItem, OrderSubitem, CourseCategory, CourseReviews, Order
)

class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        provider = CourseProvider.objects.create(name='Test Provider')
        Course.objects.create(name='Test Course', description='Test Description', image='test_image.jpg', price=100.0, maxFreeAdds=5, provider=provider, avgRating=4.5, active=True)

    def test_name_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_image_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'image')

    def test_price_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')

    def test_maxFreeAdds_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('maxFreeAdds').verbose_name
        self.assertEquals(field_label, 'maxFreeAdds')

    def test_provider_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('provider').verbose_name
        self.assertEquals(field_label, 'provider')

    def test_avgRating_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('avgRating').verbose_name
        self.assertEquals(field_label, 'avgRating')

    def test_active_label(self):
        course = Course.objects.get(id=1)
        field_label = course._meta.get_field('active').verbose_name
        self.assertEquals(field_label, 'active')

    def test_get_avgRating_int(self):
        course = Course.objects.get(id=1)
        self.assertEquals(course.get_avgRating_int(), 4)

    def test_object_name_is_str(self):
        course = Course.objects.get(id=1)
        expected_object_name = f'[{course.name}] maxFreeAddsfree({course.maxFreeAdds}) (${course.price}) active[{course.active}]'
        self.assertEquals(expected_object_name, str(course))


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='12345')

    def test_user_creation(self):
        user = User.objects.get(id=1)
        self.assertEquals(user.username, 'testuser')

class CourseProviderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CourseProvider.objects.create(name='Test Provider')

    def test_course_provider_creation(self):
        provider = CourseProvider.objects.get(id=1)
        self.assertEquals(provider.name, 'Test Provider')


class CourseCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CourseCategory.objects.create(name='Test Category')

    def test_name_label(self):
        category = CourseCategory.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

class CourseReviewsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        provider = CourseProvider.objects.create(name='Test Provider')
        course = Course.objects.create(name='Test Course', description='Test Description', image='test_image.jpg', price=100.0, maxFreeAdds=5, provider=provider, avgRating=4.5, active=True)
        user = User.objects.create_user(username='testuser', password='12345')
        CourseReviews.objects.create(course=course, user=user, text="Test Content", rating=4.5)

    def test_title_label(self):
        review = CourseReviews.objects.get(id=1)
        field_label = review._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        Order.objects.create(datetime='2020-01-01 00:00:00', client=user, price=100.0)

    def test_get_orderCode(self):
        order = Order.objects.get(id=1)
        today = date.today()
        self.assertEquals(order.get_orderCode(), f"{today.strftime('%Y-%m')}-001")



