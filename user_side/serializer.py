from rest_framework import serializers
from .models import Account,PostManagement

# user details serializer
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        exclude = ['password','is_staff','is_superuser','last_login','date_joined']
       
# user details serializer
class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostManagement
        fields='__all__'
   
    
# user details serializer
class PosterSerializerWithUser(serializers.ModelSerializer):
    user=AccountSerializer(many=False)
    class Meta:
        model=PostManagement
        fields='__all__'
    