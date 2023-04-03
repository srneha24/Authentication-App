from django.db import models

from User.models import CustomUser

# Create your models here.


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False, null=False)
    book_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    writer = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'book'
