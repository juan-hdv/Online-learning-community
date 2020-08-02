from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	# More fields?
	def __str__(self):
		return f"{self.username} ({self.email})"

# Course catalog
class Course(models.Model):
	# When a course must no appear in the catalog, set active = False (do not delete it)
	name = models.CharField(max_length=128)
	description = models.CharField(max_length=512)
	image = models.CharField(max_length=256) # image name
	price = models.FloatField(default=0.0)
	maxFreeAdds = models.IntegerField(default=0)
	active = models.BooleanField(default=False)

	def __str__(self):
		return f"[{self.name}] maxFreeAddsfree({self.maxFreeAdds}) (${self.price}) active[{self.active}]"

# Course category
class CourseCategory(models.Model):
	name = models.CharField(max_length=64)
	courses = models.ManyToManyField(Course,related_name="categories") # One Category relates to Many Courses / One course to many Categories

	def __str__(self):
		return f"{self.name}"

# Course adds. Free or Charged
class CourseAdd(models.Model):
	name = models.CharField(max_length=128)
	free = models.BooleanField(default=False) # If true add is fre of charge and extraprice is 0
	extraprice = models.FloatField(default=0.0)
	course = models.ForeignKey(Course, on_delete=models.PROTECT) # One course have many possible Adds / One add is related with only one course
	active = models.BooleanField(default=False)

	def __str__(self):
		return f"[{self.name}] --{self.free}--(${self.extraprice}) active[{self.active}]"

# Order
class Order(models.Model):
	datetime = models.DateTimeField(auto_now=False, auto_now_add=True) # default=timezone.now
	client = models.OneToOneField(User,on_delete=models.CASCADE)
	price = models.FloatField(default=0.0)
	active = models.BooleanField(default=False) # An inactive order is one already payed and served 

	def __str__(self):
		return f"[{self.datetime}] {self.client.username} {self.price} active[{self.active}]"

# Order Item - Name and code of the ordered Course
class OrderItem(models.Model):
	# productcod = ForeignKey(Course, on_delete=models.CASCADE) # One Order relates to Many products (Courses)
	quantity = models.IntegerField(default=0)
	price = models.FloatField(default=0.0) # Total order due amount
	order = models.ForeignKey(Order, on_delete=models.CASCADE) # One Order relates to Many order-Items / On items relates to One order
	
	def __str__(self):
		return f"[{self.productcod.id}] ({self.quantity}) (${self.price}) Ord[{order.id}]"

# Order Subitem - Name and code of the ordered Product Ingredient or add for a Course
class OrderSubitem(models.Model):
	addcod = models.ForeignKey(CourseAdd, on_delete=models.CASCADE) # One Course Add relates to Many order Subitems / One subitem relates to one add
	extraprice = models.FloatField(default=0.0)
	item = models.ForeignKey(OrderItem, on_delete=models.CASCADE) # One orden Subitem relates to ine Orden item / One order-Item relates to Many order-Subitems

	def __str__(self):
		return f"[{self.addcod.id}] (${self.extraprice}) Parent({item.productcod.name})"
