from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from TodoApp.models import TodoListModel
from TodoApp.api.serializer import TodoAppSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_todo_list(request):
    
    try:
        if request.user:
            instance = TodoListModel.objects.filter(user=request.user)
            serializer = TodoAppSerializer(instance,many=True)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_todo_list(request):
    
    try:
        if request.user:
            if len(request.data) == 0:
                return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
            serializer = TodoAppSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({'msg':'Todo List Created'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_Put_Patch(request,pk):
    
    try:
        if request.method == 'DELETE':
            if request.user:
                instance = TodoListModel.objects.filter(user=request.user, pk=pk)
                instance.delete()
                return Response({'msg':'deleteion sucessfult'},status=status.HTTP_200_OK)
        elif request.method == 'GET':
            if request.user:
                instance = TodoListModel.objects.filter(user=request.user,pk=pk)
                serilaizer = TodoAppSerializer(instance)
                return Response({'data':serilaizer.data},status=status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            if request.user:
                if len(request.data) == 0:
                    return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
                
                instance = TodoListModel.objects.filter(user=request.user, pk=pk)
                serializer = TodoAppSerializer(instance,data=request.data)
                if serializer.is_valid():
                    return Response({'msg':'Todo List Updated','user':serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'PATCH':
            if request.user:
                if len(request.data) == 0:
                    return Response({'errors':'Recieved Empty Object'},status=status.HTTP_400_BAD_REQUEST)
                instance = TodoListModel.objects.filter(user=request.user, pk=pk)
                serilaizer = TodoAppSerializer(instance,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'Updated Sucessfully','user':serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'errors':serilaizer.errors,'user':serializer.data},status=status.HTTP_400_BAD_REQUEST)        
    except ValidationError as ve:
        return Response({'errors':ve.detail},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'errors':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    