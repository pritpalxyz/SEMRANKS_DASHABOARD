# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.conf import settings
import random, os,string, uuid

def get_a_to_z_upload_path(sub_folder, filename):
	ext = filename.split(".").pop()
	folder = random.choice(string.ascii_lowercase)
	name = '%s_%s' % (folder, uuid.uuid4().hex)
	folder_path = os.path.join(settings.MEDIA_SUB_FOLDER_NAME, sub_folder, folder)
	folder_root = os.path.join(settings.MEDIA_ROOT, folder_path)
	if not os.path.exists(folder_root):
		os.makedirs(folder_root)
	return os.path.join(folder_path, '%s.%s' % (name, ext))



def get_user_document(instance,filename):
	return get_a_to_z_upload_path('document_secure',filename)


class userRoles(models.Model):
	USER_TYPE = (
		('client','client'),
		('employee','employee')
	)
	user_id = models.ForeignKey(User)
	user_type = models.CharField(max_length=1000,choices=USER_TYPE)


	def __str__(self):
		return self.user_id.username + " | " + self.user_type


# ALL EMPLOYEE INFORMATION
class employee_info(models.Model):
	EMP_TYPE = (
		('remote','remote'),
		('inoffice','inoffice')
	)
	user_id = models.ForeignKey(User)
	employee_type = models.CharField(max_length=1000, choices=EMP_TYPE)
	semrank_email = models.CharField(max_length=1000,default='')
	contact_email = models.CharField(max_length=1000,default='')
	address = models.CharField(max_length=1000,default='')
	contact_number = models.CharField(max_length=1000,default='')
	alternate_contact_number = models.CharField(max_length=1000,default='')
	skype_account = models.CharField(max_length=1000,default='')
	description = models.TextField(default='')
	date_time = models.DateTimeField(null=True, auto_now_add=True)


	def __str__(self):
		return self.user_id.username


# ALL CLIENT INFORMATION
class client_info(models.Model):
	SETUP_FEE_TYPE = (
		('pending','pending'),
		('free','free'),
		('paid','paid'),
	)
	user_id = models.ForeignKey(User)
	client_website =  models.CharField(max_length=1000,default='')
	contact_email = models.CharField(max_length=1000, default='')
	country = CountryField()
	billing_address = models.CharField(max_length=1000, default='')
	contact_number = models.CharField(max_length=1000, default='')
	billing_contact_number = models.CharField(max_length=1000, default='')
	skype_account = models.CharField(max_length=1000, default='')
	setup_fee = models.CharField(max_length=1000, default='pending',choices=SETUP_FEE_TYPE)
	about_client  = models.TextField(default='')
	date_time = models.DateTimeField(null=True, auto_now_add=True)


	def __str__(self):
		return self.user_id.username


# ANY CLIENT OR EMPLOYEE DOCUMENTS NEED TO UPLOAD ( ALL FORMAT ALLOWED )
class user_documents(models.Model):
	user_id = models.ForeignKey(User)
	document_name = models.CharField(max_length=1000)
	document = models.FileField(upload_to=get_user_document)
	date_time = models.DateTimeField(null=True, auto_now_add=True)

	def __str__(self):
		return self.user_id.username


class account_credentials(models.Model):
	added_by =  models.ForeignKey(User)
	username = models.CharField(max_length=1000, default='')
	password = models.CharField(max_length=1000, default='')
	account_for = models.CharField(max_length=1000, default='others')
	date_time = models.DateTimeField(null=True, auto_now_add=True)

	def __str__(self):
		return self.added_by.username

