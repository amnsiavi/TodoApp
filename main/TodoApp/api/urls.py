from django.urls import path

from TodoApp.api.views import (get_todo_list, create_todo_list, delete_Put_Patch)


urlpatterns = [
    
    path('list/',get_todo_list,name='get_todo_list'),
    
    path('create/', create_todo_list, name='create_todo_list'),
    
    path('<int:pk>/',delete_Put_Patch, name='delete_Put_Patch'),
    
    
    
]
