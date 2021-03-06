from os import name
from django.urls import path
from .views import *

urlpatterns = [
    path('show',showall,name='showall'),
    path('contact/',contactsss,name='contact'),
    path('carts/',cart,name='cartss'),
    path('check/',check,name='check'),
    path('cheakout/',checkout,name='checkout'),
    path('shop/',shop,name='shop'),
    path('details/',details,name='details'),
    path('view/<int:pk>',view,name='view'),
    path('delete/<int:pk>',delete,name='delete'),
    path('edit/<int:pk>',edit,name='edit'),
    path('register/',registerview,name='register'),
    path('login/',loginview,name='login'),
    path('logout/',logoutUSer,name='logout'),
    path('forgotpwd/',forgotpwd,name='forgotpwd'),
    path('otpcheck/',otpcheck),
    path('newpassword/',newpwd),
    path('carts/<int:id>',carts,name='cart'),
    path('viewcart/',viewcart,name='viewcart'),
    path('deletecart/<int:pk>',deletecart,name='deletecart'),
    path('cat/',c,name='c'),
    path('categ/<str:name>', categ, name='categg'),
    path('add_to_cart/<int:id>',add_to_cart),
    path('plus/<int:id>',plus,name='plus'),
    path('minus/<int:id>',minus,name='minus'),
    path('home/', home, name='home'),
    path('s/',search,name='search'),
    path('success' , success , name='success'),
    path('pcat/',pcat,name='pcat'),
    path('pcatt/',pcatt,name='pcatt'),
    path('pcattt/',pcattt,name='pcattt'),
    path('pcatttt/',pcatttt,name='pcatttt'),
    path('col/',col,name='col'),
    path('colo/',colo,name='colo'),
    path('color/',color,name='color'),
    path('col0rr/',colorr,name='colorr'),
    path('size/',size,name='size'),
    path('sizes/',sizes,name='sizes'),
    path('sizess/',sizess,name='sizess'),
    path('sizesss/',sizesss,name='sizesss'),
    path('sort/',sort,name='sort'),
    path('profile/',prof,name='profile'),
    path('editprofile/',editprof,name='editprofile'),
    path('ms/',ms,name='ms'),
]
