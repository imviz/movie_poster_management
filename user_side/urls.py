from django.urls import path
from . import views
from . views  import *
from rest_framework .routers import DefaultRouter


router=DefaultRouter()
# user update 
router.register('update',update_user,basename='update_user')
# crud operations of Post
router.register('poster',poster,basename='poster')

urlpatterns = [
               
    # for registration
    path('register/',views.user_register,name='user_register'),
    # for admin login with token 
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),  
    # for self post viewing
    path('self_post/',views.self_post,name='self_post'),
    # for other  post viewing
    path('other_post/',views.others_post,name='other_post'),
    # visibbility changing
   
    
]+router.urls
