from django.contrib.auth.models import AbstractUser
from django.db.models import Q, Sum, Count
from django.db import models


class User(AbstractUser):
    # get set of active orders (those not payed yet)
    def get_activeOrders(self):
        return self.orders.filter(active=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


# Course provider
class CourseProvider(models.Model):
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


# Course catalog
class Course(models.Model):
    # When a course must no appear in the catalog, set active = False (do not delete it)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    image = models.CharField(max_length=256)  # image name
    price = models.FloatField(default=0.0)
    maxFreeAdds = models.IntegerField(default=0)
    provider = models.ForeignKey(
        CourseProvider, on_delete=models.PROTECT, default=1, blank=True
    )  # One course have one provider / One provider is related with many courses
    avgRating = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)

    def get_avgRating_int(self):
        return int(self.avgRating)

    def __str__(self):
        return f"[{self.name}] maxFreeAddsfree({self.maxFreeAdds}) (${self.price}) active[{self.active}]"


# Course category
class CourseCategory(models.Model):
    name = models.CharField(max_length=64)
    courses = models.ManyToManyField(
        Course, related_name="categories", blank=True
    )  # One Category relates to Many Courses / One course to many Categories

    def __str__(self):
        return f"{self.name}"


# Course adds. Free or Charged
class CourseAdd(models.Model):
    name = models.CharField(max_length=128)
    free = models.BooleanField(
        default=False
    )  # If true add is fre of charge and extraprice is 0
    extraprice = models.FloatField(default=0.0)
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="adds", blank=True
    )  # One add is related with only one course / One course have many possible Adds
    active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"[{self.name}] --{self.free}--(${self.extraprice}) active[{self.active}]"
        )


# Course Review
class CourseReviews(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="reviews"
    )  # One review is related with only one course / One course could have many reviews
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )  # One review is related with only one User / One User could have mave many reviews
    text = models.CharField(max_length=256, default="")
    rating = models.IntegerField(default=0)

    # Add a contraint for a composite key (course-user)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "user"], name="course-user-compositekey"
            )
        ]

    def __str__(self):
        return f"{self.course.name}--{self.user.username} ({self.rating}) [{self.text}]"


# Order
class Order(models.Model):
    datetime = models.DateTimeField(
        auto_now=False, auto_now_add=True
    )  # default=timezone.now
    client = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE
    )  # One Order is related with only one User / One User have many possible Orders
    price = models.FloatField(default=0.0)
    active = models.BooleanField(
        default=True
    )  # An inactive order is one already payed and served

    # Get a constructed order code including date
    def get_orderCode(self):
        return "{date}-{id:03d}".format(
            date=self.datetime.strftime("%Y-%m"), id=self.id
        )

    def __str__(self):
        return f"({self.id}) Dt[{self.datetime}] {self.client.username} {self.price} active[{self.active}] nItems({self.items.count()})"


# Order Item - Code of the ordered Course
class OrderItem(models.Model):
    course = models.ForeignKey(
        Course, related_name="orders", on_delete=models.CASCADE, default=1, blank=True
    )  # One OrderItem relates one Course / One course with many orderItems
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0.0)  # Total order due amount
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )  # One Order relates to Many order-Items / On items relates to One order

    # Get subitems total price, total number of subitems, and number of free subitems
    def get_subitemsPrice(self):
        response = self.subitems.all().aggregate(
            extraprices=Sum("extraprice", filter=Q(add__free=False)),
            numcharged=Count("add", filter=Q(add__free=False)),
            numfree=Count("add", filter=Q(add__free=True)),
        )
        return {
            "extraprices": response["extraprices"] or 0,
            "numcharged": response["numcharged"],
            "numfree": response["numfree"],
        }

    def __str__(self):
        return f"({self.id}) Course[{self.course.name}] Q({self.quantity}) (${self.price}) ParentOrder({self.order.id}) nSubitems({self.subitems.count()})"


# Order Subitem - Code of the ordered add for a Course
class OrderSubitem(models.Model):
    add = models.ForeignKey(
        CourseAdd, on_delete=models.CASCADE
    )  # One subitem relates to one add / One Course Add relates to Many order Subitems
    extraprice = models.FloatField(default=0.0)
    item = models.ForeignKey(
        OrderItem, related_name="subitems", on_delete=models.CASCADE
    )  # One orden Subitem relates to one Orden item / One order-Item relates to Many order-Subitems

    def __str__(self):
        return f"({self.id}) add[{self.addcod.name}] (${self.extraprice}) ParentItem({self.item.id})"
