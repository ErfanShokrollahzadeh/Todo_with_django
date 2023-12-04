from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name='todos')

    def __str__(self):
        return f'{self.title} / Is done: {self.is_done}'

    class Meta:
        db_table= 'todos'
