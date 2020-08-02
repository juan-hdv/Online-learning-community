from django.contrib import admin
# Register your models here.
from .models import User, Course, CourseCategory, CourseAdd, Order, OrderItem, OrderSubitem

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(CourseAdd)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderSubitem)
