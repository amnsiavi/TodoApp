from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password


from core.models import TodoAppUsers
from core.api.serializer import TodoAppUsersSerializer
from core.permissions import AdminUser, RegularUser


@api_view(['GET'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_users(request):
    
    try:
        instance = TodoAppUsers.objects.all()
        serializer = TodoAppUsersSerializer(instance,many=True)
        return Response({
            'data':serializer.data
        },status=status.HTTP_200_OK)
    except ValidationError as ve:
        return Response({
            'errors':ve.detail
        },status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'errors':str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AdminUser|RegularUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_user(request,pk):
    
    try:
        instance = TodoAppUsers.objects.get(pk=pk)
        serializer = TodoAppUsersSerializer(instance)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
@api_view(['POST'])
def register(request):
    
    try:
        if len(request.data) == 0:
            return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
        if 'username' not in request.data:
            raise ValueError('Username is required')
        if 'email' not in request.data:
            raise ValueError('Email is reqiured')
        if 'password' not in request.data:
            raise ValueError('Password is Required')
        
        seriliazer = TodoAppUsersSerializer(data=request.data)
        if seriliazer.is_valid():
            seriliazer.save()
            return Response({'User Registeration Sucessful'},status=status.HTTP_201_CREATED)
        else:
            return Response({'errors':seriliazer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        
    except ValidationError as ve:
        return Response({
            'errors':ve.detail
        },status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'errors':str(e)
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
@api_view(['DELETE','PUT','PATCH'])
@permission_classes([AdminUser,IsAuthenticated])
@authentication_classes([JWTAuthentication])      
def delete_update_user(request,pk):
    
    try:
        
        if request.method == 'DELETE':
            instance = TodoAppUsers.objects.get(pk=pk)
            instance.delete()
            return Response({
                'msg':"User Deleted Sucessfully"
            },status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            if request.user:
                if len(request.data) == 0:
                    return Response({'errors':'Recieved Empty Object'})
                instance = TodoAppUsers.objects.get(pk=pk)
                serializer = TodoAppUsersSerializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'User Updated Sucessfully'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            if request.user:
                if len(request.data) == 0:
                    return Response({'errors':'Recieved Empty Object'})
                instance = TodoAppUsers.objects.get(pk=pk)
                serializer = TodoAppUsersSerializer(instance,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'User  Updated Sucessfully'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            
    
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)