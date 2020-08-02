from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index (request):
	pass



'''
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import ProductType, Product, Ingredient, Order, OrderItem, OrderSubitem

# Create a menu structure from database
class Menu():
    def __init__(self):
    	# Construct a dictionary of ProductType. Any item with 2 lists: products and ingredients
    	ptype = ProductType.objects.all()
    	self.dict = {}
    	for pt in ptype:
    		prods = Product.objects.filter(ptype=pt)
    		sorted(prods, key=lambda x: x.name.lower())
    		key = "_".join(pt.name.split(" ")) # Product Type without spaces
    		self.dict.update( { key: {"name": pt.name, "products" : prods, "ingredients" : Ingredient.objects.filter(ptype=pt) }} )


# Menú Variable
generalMenu = Menu().dict

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return render(request, "orders/index.html", { "menu": generalMenu , "message": request.session["orderMessage"], "msgType":"alert-info"})
	else:
		return render(request, "orders/login.html", {"message": request.session["loginMessage"]})

def login_view(request):
	username = request.POST["username"]
	password = request.POST["password"]
	usr = authenticate(request, username=username, password=password)
	if usr is not None:
		login(request, usr)
		request.session["loginMessage"] = ''
		request.session["orderMessage"] = ''
		request.session["currentUser"] = username
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "orders/login.html", {"loginMessage": "Invalid credentials."})

def logout_view(request):
	logout(request)
	request.session["loginMessage"] = ''
	request.session["orderMessage"] = ''
	request.session["currentUser"] = ''
	return HttpResponseRedirect(reverse("index"))

def register(request):
    return render(request, "orders/registration.html")

def saveRegistration(request):
    # get fields username, password, first name, last name, email address
	username = request.POST['username']
	email = request.POST['email']
	password = request.POST['password']
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']

	usr = User.objects.create_user(username, email, password)
	usr.last_name = firstname
	usr.last_name = lastname
	usr.save()
	request.session["loginMessage"] = "Registration succesfull. Please login."
	return HttpResponseRedirect(reverse('index'))

# Get The current Uset Order Info 
def getCurrentUserOrder(request):
	# Get client
	username = request.session["currentUser"]
	try:
		usr =User.objects.get(username=username)
	except KeyError:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "No selection."})
	except User.DoesNotExist:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "User do not exist."})

	# Get active order for current User if exists or create a new
	try:
		ordr = Order.objects.get(client=usr.id).filter(ordered=False)
		if not ordr:
			ordr  = Order() 
	except KeyError:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "No selection."})
	except Order.DoesNotExist:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "Order does not exist."})
	print (f"======>{ordr.price}--[{usr.id}]")
	return ordr

# createOrder is do not exist and add a product and ingredients
def addToCart(request):
	if request.method != "POST":
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "Only POST request allowed"})

    # get form fields 
	productId = request.POST.get('id_product', None)
	if not productId:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "No id_product"})
	productQ = request.POST.get('id_productQuantity',None)
	if not productQ:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "No id_productQuantity"})
	productQ = int (productQ)

	ingredientsList = request.POST.getlist('productIngredients',None)

	# Get product
	try:
		prod = Product.objects.get(pk=productId)
	except KeyError:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "No selection."})
	except prod.DoesNotExist:
		return render(request, "orders/error.html", {"msgType": "alert-danger", "message": "Product do not exist."})

	# Get order from current user
	ordr = getCurrentUserOrder (request)

	# Include product in Order
	ordItem = OrderItem()
	ordItem.productname = prod.name
	ordItem.productcod = prod.id
	ordItem.size = prod.size
	ordItem.quantity = productQ
	ordItem.price = prod.price * productQ
	ordItem.order = ordr.id

	# Relate products with Ingredients
	for i in ingredientsList:
		ordSubitem = OrderSubitem()
		ordSubitem.ingredientname = i.data-name
		ordSubitem.ingredientcod = i.value
		ordSubitem.extraprice = i.data-extraprice
		extrapricesIngredients += i.data-extraprice
		ordSubitem.item = ordItem.id

	# Set order info
	username = request.session["currentUser"]
	usr = User.objects.get(username=username)
	ordr.client = usr.id
	ordr.price = (prod.price * productQ) + extrapricesIngredients
	ordr.ordered = True

	# Save order info
	ordSubitem.save()
	ordItem.save()
	ordr.save()

	request.session["orderMessage"] = "Product added to the car."
	# HttpResponseRedirect(reverse("index"))

def showCart(request):
	# Get order from current user
	order = getCurrentUserOrder (request)
	if order:
		message = "Empty cart!"
	else:
		message = ""

	return render(request, "orders/showcart.html", {"order":order, "message":message, "msgType":"alert-info"})

# BORRAR
def book(request, flight_id):
	try:
		passenger_id = int(request.POST["passenger"])
		flight = Flight.objects.get(pk=flight_id)
		passenger = Passenger.objects.get(pk=passenger_id)
	except KeyError:
		return render(request, "flights/error.html", {"message": "No selection."})
	except Flight.DoesNotExist:
		return render(request, "flights/error.html", {"message": "No flight."})
	except Passenger.DoesNotExist:
		return render(request, "flights/error.html", {"message": "No passenger."})
	passenger.flights.add(flight)
	return HttpResponseRedirect(reverse("flight", args=(flight_id,)))

'''