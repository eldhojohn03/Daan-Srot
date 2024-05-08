from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name=None
    last_name=None
    usertype=models.CharField(max_length=15,null=True)

class Donor(CustomUser):
    name=models.CharField(max_length=30,null=True)
    address=models.TextField(null=True)
    phone=models.CharField(max_length=10,null=True,unique=True)
    donortype=models.CharField(max_length=20,null=True)

class Organization(CustomUser):
    org_name=models.CharField(max_length=40,null=True)
    registration_no=models.IntegerField()
    city=models.CharField(max_length=20,null=True)
    state=models.CharField(max_length=20,null=True)
    phone=models.CharField(max_length=10,null=True,unique=True)
    org_address=models.TextField(null=True)
    unique_id=models.CharField(max_length=20,null=True)
    org_type=models.CharField(max_length=20,null=True)
    name_treasurer=models.CharField(max_length=40,null=True)
    name_secretary=models.CharField(max_length=40,null=True)
    name_chairman=models.CharField(max_length=40,null=True)
    acc_holder_name=models.CharField(max_length=40,null=True)
    acc_number=models.CharField(max_length=20,null=True)
    ifsc=models.CharField(max_length=30,null=True)
    upi_id=models.CharField(max_length=30,null=True)
    approved=models.BooleanField(default=False,null=True)
    disapproved=models.BooleanField(default=False,null=True)
    verifiername=models.CharField(max_length=30,null=True)

class Admin(CustomUser):
    name=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=10,null=True,unique=True)

# class OrganizationFiles(models.Model):
#     username=models.CharField(max_length=20)
#     reg_certificate = models.FileField(upload_to='pdf_files')
#     pancard=models.FileField(upload_to='pdf_files')
#     secretary_aadhar=models.FileField(upload_to='pdf_files')
#     treasurer_aadhar=models.FileField(upload_to='pdf_files')
#     chairman_aadhar=models.FileField(upload_to='pdf_files')
#     qrcode=models.FileField(upload_to='pdf_files')

class Transaction(models.Model):
    transaction_id=models.CharField(max_length=40,null=True)
    donor_username=models.EmailField(null=True)
    org_username=models.EmailField(null=True)
    amount=models.FloatField(null=True)
    advertise=models.BooleanField(default=False,null=True)
    approvefromorg=models.BooleanField(default=False,null=True)

class Needs(models.Model):
    org_username=models.EmailField(null=True)
    clothes=models.BooleanField(default=False,null=True)
    educational=models.BooleanField(default=False,null=True)
    food=models.BooleanField(default=False,null=True)
    medicine=models.BooleanField(default=False,null=True)
    description=models.TextField(null=True)
