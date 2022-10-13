from django.urls import path
from . import views
from . views  import *
from rest_framework .routers import DefaultRouter


router=DefaultRouter()
# user update and CRUD operation of users
router.register('user',user_details,basename='user_details')
# crud operations of Post
router.register('poster',poster,basename='poster')

urlpatterns = [              
    # visibility changing
    path('change/<int:id>/',views.visibility_change,name='visibility'),
    
]+router.urls
