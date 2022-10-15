from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from user_side.models import Account,PostManagement
from rest_framework  import status
from  user_side.serializer import AccountSerializer,PosterSerializerWithUser
from rest_framework import viewsets
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
    serializer_class=PosterSerializerWithUser
    
 
    
#visibility changing of post  
@api_view(['PATCH'])    
@permission_classes([IsAdminUser])
def visibility_change(request,id): 
    data=request.data       
    x=list(data['select'])     
    x=(map(int,x))    
    post=PostManagement.objects.get(id=id)     
    post.visibility.clear()
    post.save()
    for i,j in enumerate(x):       
        post.visibility.add(j)
        post.save()
    serilizer=PosterSerializerWithUser(post,many=False)    
    return Response(serilizer.data)