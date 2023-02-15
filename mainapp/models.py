from django.db import models
from userauth.models import Account

# # Create your models here.
class BusinessUnit(models.Model):
    name = models.CharField(max_length=30, unique=True)
    innovation_champion = models.ForeignKey(Account, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='business_units/', null=True)
    def __str__(self):
        return self.name

class Submission(models.Model):
    title = models.CharField(max_length=50)
    identified_problem = models.CharField(max_length=1000)
    proposed_solution = models.CharField(max_length=1000)
    benefit_of_solution = models.CharField(max_length=1000)
    similar_solutions = models.CharField(max_length=1000, null=True, blank=True)
    
    attachment = models.FileField(upload_to='submission_attachments/', null=True, blank=True)

    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE)
    ideator = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Review Pending") # Review Pending, On Hold, Accepted, Rejected
    remark = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.title
 
