from django.db import models
from core.models import TodoAppUsers


# Create your models here.
class TodoListModel(models.Model):
    
    def intiate_dic():
        return {}
    
    title = models.CharField(max_length=50)
    description = models.TextField()
    tasks = models.JSONField(default=intiate_dic)
    completed = models.BooleanField(default=False)
    
    user = models.ForeignKey(TodoAppUsers,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

