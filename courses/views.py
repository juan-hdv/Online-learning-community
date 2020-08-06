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
		"message":f"The resource you are looking for does not exist.",
		"pagename": pagename
	})
	response.status_code = 404
	return response

def index (request):
	if request.user.is_authenticated:
		return render(request, "courses/index.html", { 
			"catalog": Course.objects.filter(active=True),
			"categories": CourseCategory.objects.order_by('name')
		})
	else:
		return HttpResponseRedirect(reverse('login'))

def loginView(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		usr = authenticate(request, username=username, password=password)
		if usr is not None:
			'''
			request.session["loginMessage"] = ''
			request.session["orderMessage"] = ''
			'''
			login(request, usr)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "courses/login.html", {"message": "Invalid credentials.", "msgType":"alert-danger"})
	else:
		return render(request, "courses/login.html")

def logoutView(request):
	'''
	request.session["loginMessage"] = ''
	request.session["orderMessage"] = ''
	'''
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
		
		request.session["loginMessage"] = "Registration succesfull. Please login."
		return HttpResponseRedirect(reverse('index'))
	else:
		return render(request, "courses/register.html")

# Get The current Uset Order Info 
def getCurrentUserOrder(request):
	pass

# createOrder - A course and a lists of it's adds
def addToCart(request):
	if request.method != "POST":
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Only POST request allowed"})

    # get form fields 
	courseId = request.POST.get('id_course', None)
	if not courseId:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "No id_courses"})
	addsList = request.POST.getlist('courseAdds',None)

	# Get course
	try:
		course = Course.objects.get(pk=courseId)
	except KeyError:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Key error."})
	except course.DoesNotExist:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Course do not exist."})

	productQ = 1
	# Get order from current user
	usrCurrent = User.objects.get(username=request.user.username) # Get current user object
	# Get active order for current User if exists or create a new
	try:
		order = Order.objects.filter(active=True).get(client=usrCurrent.id)
	except Order.DoesNotExist:
		order  = Order() 
		order.save()

	# Include product in Order
	ordItem = OrderItem()
	ordItem.productname = course.name
	ordItem.productcod = course.id
	ordItem.quantity = productQ
	ordItem.price = course.price
	ordItem.order = order
	ordItem.save()

	# Relate products with items (Adds)
	extrapricesAdds = 0
	for a in addsList:
		params = a.split("-") # This field has this format: <id>-<extraprices>
		addId = int(params[0])
		addExtraprice = float(params[1])
		extrapricesAdds += addExtraprice

		ordSubitem = OrderSubitem()
		ordSubitem.addcod = CourseAdd.objects.get(id=addId) 
		ordSubitem.extraprice = addExtraprice
		ordSubitem.item = ordItem
		ordSubitem.save()

	# Set order info
	order.client = usrCurrent
	order.price = (course.price + extrapricesAdds) * productQ 
	order.active = True
	order.save()

	request.session["orderMessage"] = "Product added to the car."
	return HttpResponseRedirect(reverse("index"))

'''


def showCart(request):
	# Get order from current user
	order = getCurrentUserOrder (request)
	if order:
		message = "Empty cart!"
	else:
		message = ""

	return render(request, "orders/showcart.html", {"order":order, "message":message, "msgType":"alert-info"})

'''