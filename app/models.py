from django.db import models
import uuid

# Create your models here.

class DancingDate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sname = models.CharField(max_length=50,null=False)
    ddate = models.DateField(null=False)
    ntime = models.IntegerField(null=False)
    scontact = models.CharField(max_length=50,null=False)

    def __str__(self) -> str:
        return self.sname
    
