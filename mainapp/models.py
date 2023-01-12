from django.db import models
from userauth.models import Account

# # Create your models here.
class BusinessUnit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    idea_champion = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='business_units/')

    def __str__(self):
        return self.name

class Submission(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    ideator = models.ForeignKey(Account, on_delete=models.CASCADE)
    # attachments = models.ImageField(upload_to ='submission_attachments/')

    def __str__(self):
        return self.name