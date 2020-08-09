from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError, Error
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
import json

from .models import User, Course, CourseCategory, CourseAdd, Order, OrderItem, OrderSubitem

def handler404 (request, exception):
	pagename = request.get_full_path().split("/").pop()
	response = render(request, '404.html', {
		"message": "The resource you are looking for does not exist.",
		"pagename": pagename
	})
	response.status_code = 404
	return response

def index (request):
	if request.user.is_authenticated:
		return render(request, "courses/index.html", { 
			"catalog": Course.objects.filter(active=True),
			"categories": CourseCategory.objects.order_by('name'),
			"message": "Hellooooooooooo"
		})
	else:
		return HttpResponseRedirect(reverse('login'))

def loginView(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		usr = authenticate(request, username=username, password=password)
		if usr is not None:
			login(request, usr)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "courses/login.html", {"message": "Invalid credentials.", "msgType":"alert-danger"})
	else:
		return render(request, "courses/login.html")

def logoutView(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))

def registerView(request):
	if request.method == "POST":
		# get fields username, password, first name, last name, email address
		username = request.POST['username']
		email = request.POST['email']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "courses/register.html", {"message": "Passwords must match.","msgType":"alert-warning"})

		try:
			usr = User.objects.create_user(username, email, password)
			usr.first_name = firstname
			usr.last_name = lastname
			usr.save()
		except IntegrityError:
			return render(request, "courses/register.html", {"message": "Username already taken.", "msgType":"alert-warning"})
		
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request, "courses/register.html")

# createOrder - A course and a lists of it's adds
def addToCart(request):
	if request.method != "POST":
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Only POST request allowed"})

    # Get form fields 
	courseId = request.POST.get('idcourse', None)
	if not courseId:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "No id_courses"})
	# Get selectd Adds 
	addsList = request.POST.getlist('courseAdds',None)

	# Get the selected course
	try:
		course = Course.objects.get(pk=courseId)
	except KeyError:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Key error."})
	except course.DoesNotExist:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Course do not exist."})

	productQ = 1
	usrCurrent = User.objects.get(username=request.user.username) # Get current user object

	# Create a new order for current user
	order  = Order() 
	order.client = usrCurrent
	order.price = 0
	order.active = True
	order.save()
	
	# # Create new order item
	ordItem = OrderItem()
	ordItem.course = course
	ordItem.quantity = productQ
	ordItem.price = course.price
	ordItem.order = order
	ordItem.save()

	# Relate products with items (Adds)
	extrapricesAdds = 0
	for a in addsList:
		params = a.split("-") # This field has this format: <id>-<extraprices>
		addExtraprice = float(params[1])
		addId = int(params[0])
		extrapricesAdds += addExtraprice
		# Create new subitem of order item
		ordSubitem = OrderSubitem()
		try:
			ordSubitem.add = CourseAdd.objects.get(id=addId)
		except KeyError:
			return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "CourseAdd Key error."})
		except CourseAdd.DoesNotExist:
			return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "CourseAdd do not exist."})
		ordSubitem.extraprice = addExtraprice
		ordSubitem.item = ordItem
		ordSubitem.save()

	# Update order info
	order.price = (course.price + extrapricesAdds) * productQ 
	order.save()

	return HttpResponseRedirect(reverse("index"))

# deleteFromCart - Delete a current order id | Cascade delete Items adn Subitems
def deleteFromCart(request):
	if request.method != "POST":
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Only POST request allowed"})

    # get form fields 
	orderId = request.POST.get('idorder', None)
	if not orderId:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "No id_order"})

	# Delete order with idorder and cascade delete Items adn Subitems
	try:
		Order.objects.filter(pk=orderId).delete()
	except IntegrityError:
		return render(request, "courses/register.html", {"message": "Integrity error.", "msgType":"alert-warning"})

	return HttpResponseRedirect(reverse("showcart"))

# Show active orders from current user
def showCart(request):
	if request.method != "GET":
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Only GET request allowed"})
	# Get client
	try:
		usrCurrent = User.objects.get(username=request.user.username) # Get current user object
	except usrCurrent.DoesNotExist:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "User do not exist."})
	# Get active orders for current User
	orders = Order.objects.filter(active=True,client=usrCurrent.id)
	return render(request, "courses/cart.html", {"orders":orders})
