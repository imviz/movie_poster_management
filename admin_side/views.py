from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from user_side.models import Account,PostManagement
from rest_framework  import status
from  user_side.serializer import AccountSerializer,PosterSerializer
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import  TokenObtainPairView
from rest_framework.decorators import permission_classes


    
# for admin CRUD operations of user
class user_details(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=Account.objects.filter(is_admin=False)
    serializer_class=AccountSerializer
    
# for admin CRUD operation of poster
class poster(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset=PostManagement.objects.all()
    serializer_class=PosterSerializer
    
 
    
#visibility changing of post  
@api_view(['PATCH'])    
@permission_classes([IsAdminUser])
def visibility_change(request,id): 
    data=request.data   
    print(data,'data')
    x=list(data['select'])     
    print(type(x))
    print(x)
    x=(map(int,x))    
    post=PostManagement.objects.get(id=id)     
    post.visibility.clear()
    post.save()
    for i,j in enumerate(x):       
        post.visibility.add(j)
        post.save()
    serilizer=PosterSerializer(post,many=False)    
    return Response(serilizer.data)