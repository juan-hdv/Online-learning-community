# cs50-2020-capstone
CS50W Capstone project
Arts and Crafts Courses

### Author/Date

      Juan Gabriel MEJÍA / 2020-08-16

## INTRODUCTION
### Description

An skillshare.com / Udemy.com like online learning community and selling online courses, that will allow users to browse course catalog, filter courses by categories, search for courses, see courses details, add/delete courses to/from a shopping cart, include course adds to orders, give rates and reviews, check ratings and reviews from other users and, finally, checkout orders in the shopping cart.

### Technologies
Python, Django, JavaScript - ECMAScript 6 (ES6), HTML, and CSS.

## PROJECT DETAILS
### General implemented requirements

0. Authentication: allow user to login and logout the site.
1. Show course catalog.
2. Filter courses by multiple categories.
3. Filter courses by a filter string. Filter string is searched into the course’s titles and descriptions.
4. Show course details and prepare an order with course adds. Some of the adds are charged, some others are free.
5. Add an order to the shopping cart. An Order includes course, selected adds (some free some charged), items prices and total price.
6. Show orders in the shopping cart and an icon with the number of selected courses (if any).
7. Give course ratings/reviews and show course ratings average/reviews.
8. Authorization: Make course catalog available for non-signed in users and shopping cart available only for signed in users.
9. Paypal payment integration.

### Project personal experience

It has been hard work and at the same time very enriching.

Thanks to the development of the Capstone project, I have learned and deepened especially in:

#### Django
- The models: handle the inherited abstract User model; the need to make methods within the model classes; the aggregation functions; using "related_name" for one to many relationships (foreign) and for many to many relatioships (QuerySets and entry_set); using class META to define constrains.
- Exporting settings variables for templates.
- Defining a urls (routes) for GET method with parameters and at the same time for POST methods without parameters.
- REST call to external APIs through requests.
- Use of custom HTTP error pages.
- Creating personalized template Tags.

#### Python
- Operations on strings.
- Dictionaries and Sets operations.
- Find / deccode strings Base64 (Interesting).

#### Javascript
- Use of operations on the DOM and manage events.
- Use of FETCH to call own and external APIs.

#### HTML
- Intensive use of Boostrap.
- Use of cloudflare font-awesome icons.
- Using modal dialogs (Bootstrap).

#### CSS:
- Use of the SCSS language.

### Difficulties

I have encountered great difficulties especially in the integration with Paypal, particularly due to the lack of good  documentation. I've wasted lot of time on outdated documents.

### Project files and directories
* courses/:  Aplication directory (Application name: courses)
	* media/: Courses images (*.jpg)
	* migrations/:  Migrations files (* .py)
	* static/
		* courses/:  Static files for the courses application
			* css/:
				* colors.scs:  	Some colors codes references from htmlcolorcodes.com
				* main.css:  	Style sheet
				* main.scss: 	Sass file that compiles to main.css
				* main.css.map: Map file create by the scss compiler.
			* js/:
				* main.js:  Javascript code for: Filtering by categories and by filter string; configuring an Order with course adds; rating and write reviews.
				* paypal.js: Javascriot code for paypal API integration for order payments. JS Fetch is used for server services calls.
			* favicon.ico: small icon associated with the website
	* templates/
		* courses/:  Templates for courses application
			* cart:	list orders, items and subitems; display a modal dialog with order contents, allowing to choose course adds; allow payments (payàl button).
			* error.html: general error template.
			* index.html:  list course catalog and allows filtering.
			* error.html: general error template.
			* information.html: general information template.
			* login.html: login page
			* layout.html: root template from which every other template inherits.
			* register.html: new user registraton form.
			* showpayment.html:  show successful payment results and a modal dialog with datails.
		* 404.html: Personalized 404 http error page. Work only in production mode and debug=false.
	* templatetags/: Template tags used in django templates.
			* range.py: generate a range from < start > to < end > for iterating through a for loop.
	* admin.py: For registering models to be accessed from /admin. All the models in models.py are registered.
	* apps.py: registered apps for the current project
	* context_processors: export som settings variables definitions to be used in templates: FILTER_INITIAL_NAME,PAYPAL_CLIENTID.
	* models.py: app models.
		* User(AbstractUser): A User can create many Orders / A user can write reviews for many courses in CourseReview (ratings/reviews)
		* Course: A Course have one CourseProvider
		* CourseProvider: A CourseProvider can proved many Courses.
		* CourseCategory: A CourseCategory is associated with many Courses / A Course have ono or many CourseCategory's
		* CourseAdd: A CourseAdd belongs to one Course / A Course have cero o many CourseAdd's
		* CourseReviews: A course review/rating is written by a User for a Course
		* Order: An Order is associated with on User / A User is asociated with cero o many Order's
		* OrderItem: An OrderItem is part of only one Order, and is assoated with one Course
		* OrderSubitem:	An OrderSubitem is part of only one OrderItem, and is assoated with one Course Add
	* test.py: file for tests
	* urls.py: html app routes
	* utils.py: Paypal REST API calls and some utility functions (encode/decode BASE64).
	* views.py: app controllers responding to routes
		* Errors:
			* handler404
		* Catalog
			* index
		User athentocation:
			* loginView
			* logoutView
			* registerView
		* Coourses Reviews and Rating:
			* courseReview
		* Shopping Cart:
			* addToCart
			* deleteFromCart
			* showCart
		* Payment Checkout:
			* createPaypalOrder
			* capturePaypalOrder
			* showPaypalPayment
			* cancelPaypalPayment
* project5/   The project directory
	* asgi.py: ASGI config for project5 project.
	* setting.py: project setting file (Django settings). Defines som Paypal variables in development environment, then to be moved to env variables in production: PAYPAL_CLIENTID, PAYPAL_SECRET, PAYPAL_URLTOKEN, PAYPAL_URLORDER, PAYPAL_URLSHOW,
	* urls.py: html project routes
	* wsgi.py: WSGI config for project4 project.
* db.sqlite3: The databse file.
* manage.py:  Django's command-line utility for administrative tasks
* README.md: This file.

## RUNNING APP in Ubuntu
### Create an Enviroment

 Before running a project, an Environment must be set for Python 3 and requirements.txt must be then installed
 For example to create an environment called: /env-py3.9

 First create directory:
 	mkdir env-py3.9

 Then set environment:
 	python3 -m venv env-py3.9

Finally, activate envirinment:
	source env-py3.9/bin/activate

Now is time time install Python packages - If requirements.txt is present:
	pip install requests

	I have created an environment called: /env-py3.9

### Prepare environment
	> source active.sh

	# Where active.sh is a file with 2 lines:
	source env-py3.9/bin/activate
	cd env-py3.9/pr*5*/pr*5
