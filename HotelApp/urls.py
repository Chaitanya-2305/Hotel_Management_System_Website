from django.urls import path
from . import views
urlpatterns = [
    path('',views.loginview,name = 'loginurl'),
    path('logout/',views.logoutview,name='logouturl'),
    path('Home/',views.Homeview,name='homeurl'),
    path('Table/',views.Tableview,name='tableurl') ,
    path('Menu/',views.menuview.as_view(),name = 'menuurl'),
    path('Bookings/',views.Bookingview,name = 'bookingurl'),
    path('signup/',views.signupview,name='signupurl'),
    path('about/',views.aboutview,name='abouturl'),
    path('contact/',views.contactview,name='contacturl')
]