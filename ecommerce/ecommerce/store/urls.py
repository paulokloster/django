from django.urls import include, path
# from .views import login_view
from . import views

urlpatterns = [



    path('home/', views.home, name="home"),

    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),


    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),


    # LOGIN AND REGISTRATION
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),




]
