from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from .models import Account,PostManagement
from rest_framework  import status
from .serializer import AccountSerializer,PosterSerializer
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import  TokenObtainPairView
from rest_framework.decorators import permission_classes


# admin register   view

@api_view(['POST'])
def user_register(request):
    try:
        data=request.data
        name=data['name']     
        email=data['email']
        password=data['password']
        confirm_password=data['confirm_password']

        # validatations for blank
        if email=='' or name=='' or name ==''  or password=='' or confirm_password=='':
            message={'error':' fill the blanks'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        # validation for password matching
        elif password!=confirm_password:
            message={'error':'password missmatch'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        # for password length check
        elif len(password)<6:
            message={'error':'password contain min 6 charector'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
        
        # checking the email is already exist or not
        elif Account.objects.filter(email=email).exists():
            message={'error':'This email is already exist'}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
            
        # creating a object of Account model for signup 
        user=Account.objects.create(
            name=name,         
            email=email,
            password=make_password(password),
                             
        )
        serializere=AccountSerializer(user,many=False)
        return Response(serializere.data)
    except:
        message={'error':'there is a error occure'}
        return Response(message,status=status.HTTP_400_BAD_REQUEST)
    
    

# customizing and adding data to jwt token
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)     
        serializer=AccountSerializer(self.user).data
        for k ,v in serializer.items():
            data[k]=v
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)    
        token['admin'] = user.is_admin 
        return token
    
# for simple jwt customization
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    
    
# for editing user details
class update_user(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Account.objects.filter(is_admin=False)
    serializer_class=AccountSerializer
    
# creation of poster 
class poster(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=PostManagement.objects.all()
    serializer_class=PosterSerializer
    
# for user posts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def self_post(request):
    user=request.user
    poster=PostManagement.objects.filter(user=user)
    serializer=PosterSerializer(poster,many=True)
    return Response(serializer.data)
    
# for user posts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def others_post(request):
    user=request.user
    poster=PostManagement.objects.filter(visibility=user)
    serializer=PosterSerializer(poster,many=True)
    return Response(serializer.data)
    
    
@api_view(['PATCH'])    
def change(request,id): 
    data=request.data 
    print(data)
    x=data['select']     
    x=list(map(int,x))    
    post=PostManagement.objects.get(id=id)   
    print(post.visibility.values)
    print(post.visibility,'dddddd')
    post.visibility.clear()
    post.save()
    for i,j in enumerate(x):       
        post.visibility.add(j)
        post.save()
    serilizer=PosterSerializer(post,many=False)    
    return Response(serilizer.data)