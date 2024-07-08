from django.urls import path


from core.api.views import (get_users,register,get_user, delete_update_user)




urlpatterns=[
    #User List 
    path('user/list',get_users,name='get_users'),
    path('user/register',register,name='register'),
    
    # Single Users
    path('user/<int:pk>',get_user,name='get_user'),
    
    # DELETE, PUT, PATCH
    path('user/mod/<int:pk>',delete_update_user,name='delete_update_user')
]