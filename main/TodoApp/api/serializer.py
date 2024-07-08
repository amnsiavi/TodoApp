from rest_framework.serializers import ModelSerializer
from TodoApp.models import TodoListModel


class TodoAppSerializer(ModelSerializer):
    
    class Meta:
        model = TodoListModel
        fields = fields = ['id','title','description','tasks','completed']