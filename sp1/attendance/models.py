from django.db import models

# Create your models here.
class Std(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'std'

    def __str__(self):
        return self.name
