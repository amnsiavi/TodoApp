from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from core.models import TodoAppUsers

class TodoAppUsersSerializer(ModelSerializer):
    
    class Meta:
        model = TodoAppUsers
        fields = ['id','username','email','password','bio','DOB','age','is_superuser']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
    
    def update(self,instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance,validated_data)
    
        