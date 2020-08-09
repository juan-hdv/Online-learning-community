from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
	path("login", views.loginView, name="login"),
	path("logout", views.logoutView, name="logout"),
	path("register", views.registerView, name="register"),
	path("addtocart", views.addToCart, name="addtocart"),
	path("deletefromcart", views.deleteFromCart, name="deletefromcart"),
	path("showcart", views.showCart, name="showcart"),
]
# For accesing applicaction media files 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)