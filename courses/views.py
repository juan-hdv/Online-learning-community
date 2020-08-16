import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.db import IntegrityError, Error
from django.db.models import Avg
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

from .models import User, Course, CourseCategory, CourseAdd, CourseReviews, Order, OrderItem, OrderSubitem
from .utils import paypal_getToken, paypal_createOrder, paypal_captureOrder, paypal_showDetailsOrder

''' 
 **	ERROR HANDLERS
''' 
def handler404 (request, exception):
	pagename = request.get_full_path().split("/").pop()
	response = render(request, '404.html', {
		"message": "The resource you are looking for does not exist.",
		"pagename": pagename
	})
	response.status_code = 404
	return response

''' 
 **	INDEX
''' 
def index (request):
	if request.user.is_authenticated:
		usrCurrent = User.objects.get(username=request.user.username) # Get current user object
	else:
		usrCurrent = None
	return render(request, "courses/index.html", { 
		"catalog": Course.objects.filter(active=True),
		"categories": CourseCategory.objects.order_by('name'),
		"user": usrCurrent,
	})

''' 
 **	USERS SIGNING
''' 
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

''' 
 **	COURSES
''' 
def courseReview (request, idcourse=None):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))

	usrCurrent = User.objects.get(username=request.user.username) # Get current user object
	if request.method == "GET":
		course = Course.objects.get(id=idcourse)
		# Get review from user for the current course
		ur = CourseReviews.objects.filter(course=course,user=usrCurrent)
		if ur.exists():
			ur = ur.first()
			userReview = {'text': ur.text, 'rating': ur.rating }
		else:
			userReview = {'text':'', 'rating':0}
		courseReviews = CourseReviews.objects.exclude(user=usrCurrent).filter(course=course)
		return render(request, "courses/review.html", {"course": course, "userReview": userReview, "courseReviews": courseReviews})
	elif request.method == "POST":
	    # Get form fields 
		courseId = request.POST.get('idcourse', None)
		course = Course.objects.get(id=courseId)
		if not courseId:
			return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "No id_courses"})
		userRating = request.POST.get('userrating', None)
		userReview = request.POST.get('userreview', None)
		action = request.POST.get ('buttonAction', None)

		if action in "update":
			rating, created = CourseReviews.objects.update_or_create(
				course=course, user=usrCurrent, 
				defaults={'rating': userRating, 'text': userReview}
			)
		elif action in "delete":
			# Delete rating for course and user
			try:
				CourseReviews.objects.filter(course=course, user=usrCurrent).delete()
			except IntegrityError:
				return render(request, "courses/register.html", {"message": "Integrity error.", "msgType":"alert-warning"})
		else:
			return render(request, "courses/error.html", {"msgType": "alert-danger", "message": f'Invalid operation - Unknown botton action: {action}'})
		# Recalculate course average rating
		course.avgRating = float(CourseReviews.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg'])
		course.save()
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": 'Bad request!'})

''' 
 **	ORDERS (SHOPING CART)
''' 

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

# URL showcart -- Show active orders from current user
def showCart(request):
	if request.method != "GET":
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Only GET request allowed"})

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))

	# Get client
	try:
		usrCurrent = User.objects.get(username=request.user.username) # Get current user object
	except usrCurrent.DoesNotExist:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "User do not exist."})
	# Get active orders for current User
	orders = Order.objects.filter(active=True,client=usrCurrent.id)
	return render(request, "courses/cart.html", {"orders":orders})

''' 
 **	CHECKOUT
''' 
# URL dopayment
def createPaypalOrder(request):
	if not (request.is_ajax and request.method == "POST"):
		return render(request, "courses/error.html", {"message": "Operation not allowed."})

	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('login'))

	# Get clicked order-id
    # It's an Ajax request and data comes in "request.body" not in "request.POST"!!!!
	data = json.loads(request.body)
	orderid = data['orderid']
	try:
		order = Order.objects.get(id=orderid) # Get clicked order
	except order.DoesNotExist:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Order do not exist."})

	# Get the paypal Token
	response = paypal_getToken(settings.PAYPAL_URLTOKEN)
	if response.status_code != 200:
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": f"HTTP Error {response.status_code} <getting token>."})

	# Get and set Order Details
	paypalOrder = {
		'token': response.json()['access_token'],
		'details': {
			'orderid': f"{order.id}",
			'referencename': order.items.all().first().course.name,
			'referencecode': f"ACC-{order.items.all().first().course.id}",
			'totalamount': f"{order.price}",
		},
		'response':'', # paypal_getToken do not returns a response 'text'
	}
	# Create paypal Order => 201 Created
	response = paypal_createOrder (settings.PAYPAL_URLORDER, paypalOrder['token'], paypalOrder['details'])
	if response.status_code != 201: # Created
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": f"HTTP Error {response.status_code} <creating order>. Please try later."})		

	jsonResponse = response.json()
	request.session['paypalOrder'] = paypalOrder
	request.session['paypalOrder']['response'] = jsonResponse
	return JsonResponse(jsonResponse)

# URL capturepayment
def capturePaypalOrder(request):
	if not (request.is_ajax and request.method == "POST"):
		return render(request, "courses/error.html", {"message": "Operation not allowed."})

	# Get current token
	paypalOrder = request.session.get("paypalOrder",False)
	if not paypalOrder: 
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Payment failed. Nonexistent <token> or <order>.  Please restart your payment."})

	token = paypalOrder['token']
	# Personalize URL with paypal order ID
	url = next((item for item in paypalOrder['response']['links'] if item['rel'] == 'capture'), None)["href"]
	# CAPTURE funds of paypal order => 201 Created
	response = paypal_captureOrder (url, token)
	if response.status_code != 201: # Created
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": f"HTTP Error {response.status_code} <creating order>. Please try later."})
	jsonResponse = response.json()

	# If user authorized payment, the order must be marked as processed (INACTIVE)
	if jsonResponse['status'] == "COMPLETED":
		orderid = paypalOrder['details']['orderid']
		try:
			order = Order.objects.get(id=orderid) # Get clicked order
		except order.DoesNotExist:
			return render(request, "courses/error.html", {"msgType": "alert-danger", "message": "Order do not exist."})
		# Mark Order as processed
		order.active = False
		order.save()

	request.session['paypalOrder']['response'] = jsonResponse
	return JsonResponse(jsonResponse)

# URL showpayment
def showPaypalPayment(request):
	# Get current token
	paypalOrder = request.session.get("paypalOrder",False)
	if not paypalOrder: 
		return HttpResponseRedirect(reverse("index"))

	token = paypalOrder['token']
	# Personalize URL with paypal order ID
	url = settings.PAYPAL_URLSHOW.replace('<ORDERID>',paypalOrder['response']['id'])
	# Show paypal order details => 200 Ok
	response = paypal_showDetailsOrder (url, token)
	if response.status_code != 200: # Ok
		return render(request, "courses/error.html", {"msgType": "alert-danger", "message": f"HTTP Error {response.status_code} <creating order>. Please try later."})

	jsonResponse = response.json()
	request.session['paypalOrder']['response'] = jsonResponse
	paypalOrder = request.session['paypalOrder']

	# Delete session variables
	del request.session['paypalOrder']
	request.session.modified = True
	return render(request, "courses/showpayment.html", {'payment':paypalOrder})

# URL cancelpayment
def cancelPaypalPayment(request):
	return render(request, "courses/information.html", {"msgType": "alert-success", "message": f"Your payment has been successfully canceled. No charges have been applied."})



