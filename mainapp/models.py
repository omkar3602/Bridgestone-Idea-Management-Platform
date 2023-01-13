from django.db import models
from userauth.models import Account

# # Create your models here.
class BusinessUnit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    idea_champion = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='business_units/', null=True)
    def __str__(self):
        return self.name

class Submission(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    ideator = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Review Pending") # Review Pending, On Hold, Accepted, Rejected
    # attachments = models.ImageField(upload_to ='submission_attachments/')

    def __str__(self):
        return self.name
 
