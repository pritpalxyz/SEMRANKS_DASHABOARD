# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.conf import settings
import random, os,string, uuid
from datetime import timedelta
from datetime import  datetime

def get_a_to_z_upload_path(sub_folder, filename):
    ext = filename.split(".").pop()
    folder = random.choice(string.ascii_lowercase)
    name = '%s_%s' % (folder, uuid.uuid4().hex)
    folder_path = os.path.join(settings.MEDIA_SUB_FOLDER_NAME, sub_folder, folder)
    folder_root = os.path.join(settings.MEDIA_ROOT, folder_path)
    if not os.path.exists(folder_root):
        os.makedirs(folder_root)
    return os.path.join(folder_path, '%s.%s' % (name, ext))

def get_project_document(instance,filename):
    return get_a_to_z_upload_path('document_secure_project',filename)


class subscription_plans(models.Model):
    ACTIVE_STATUS = (
        ('active','active'),
        ('hidden','hidden'),
    )
    plan_name = models.CharField(max_length=1000,default='')
    monthly_price = models.CharField(max_length=1000,default='')
    setup_fee = models.CharField(max_length=1000,default='')
    view_stat = models.CharField(max_length=1000,choices=ACTIVE_STATUS)
    plan_description = models.TextField(default='')
    date_time = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.plan_name + " | " + self.monthly_price


class taxSlab(models.Model):
    tax_name = models.CharField(max_length=1000,default='')
    tax_percent = models.CharField(max_length=100,default='5')

    def __str__(self):
        return self.tax_name + " | " + self.tax_percent


class serviceItem(models.Model):
    service_name = models.CharField(max_length=1000,default='')
    serivce_description = models.CharField(max_length=1000,default='')
    service_price = models.CharField(max_length=1000,default='')

    def __str__(self):
        return self.service_name + " | " + self.service_price


class projectReportType(models.Model):
    report_type = models.CharField(max_length=1000,default='')

    def __str__(self):
        return  self.report_type


class addons(models.Model):
    ACTIVE_STATUS = (
        ('active', 'active'),
        ('hidden', 'hidden'),
    )
    addon_name = models.CharField(max_length=1000, default='')
    monthly_price = models.CharField(max_length=1000, default='')
    view_stat = models.CharField(max_length=1000, choices=ACTIVE_STATUS)
    addon_description = models.TextField(default='')
    date_time = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.addon_name + " | " + self.monthly_price


# WHOLE PROJECT DETAILS
class projects(models.Model):
    STATUS = (
        ('Deactivated','Deactivated'),
        ('Activated','Activated'),
        ('Halted','Halted'),
        ('Completed','Completed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.ForeignKey(User)
    project_name = models.CharField(max_length=1000,default='')
    website_url = models.CharField(max_length=1000,default='')
    project_description = models.TextField(default='')
    project_status = models.CharField(max_length=1000,default='Deactivated',choices=STATUS)

    # PLAN DETAILS
    subscription_plans_name = models.CharField(max_length=1000,default='')
    subscription_plans_monthly_price = models.CharField(max_length=1000,default='')
    subscription_plans_setup_fee = models.CharField(max_length=1000,default='')
    subscription_plans_description = models.CharField(max_length=1000,default='')
    subscription_plans_id = models.CharField(max_length=1000,default='')#ID FROM PARENT MODEL ONLY INTERNAL USE
    date_time = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.client_id.username + " | " + self.project_name + " | " + self.website_url


# ADDONS ALONG WITH CURRENT PROJECT
class project_addons(models.Model):
    STATUS = (
        ('Deactivated', 'Deactivated'),
        ('Activated', 'Activated'),
    )
    project_id = models.ForeignKey(projects)
    addons_id = models.ForeignKey(addons)
    addon_status = models.CharField(max_length=1000,default='Deactivated',choices=STATUS)
    date_time = models.DateTimeField(null=True, auto_now_add=True)


# SOME Project Files before start project
class projectFiles(models.Model):
    SHOW_STAT = (
        ('show','show'),
        ('hide','hide'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(projects)
    uploaded_by = models.ForeignKey(User)
    file_title = models.CharField(max_length=1000,default='')
    document_file = models.FileField(upload_to=get_project_document)
    view_stat = models.CharField(max_length=500,choices=SHOW_STAT,default='show')
    date_time = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.file_title


# WEEKLY MONTHLY PROJECTS REPORT
class projectReports(models.Model):
    SHOW_STAT = (
        ('waiting','waiting'),
        ('approved','approved'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(projects)
    file_extension = models.CharField(max_length=1000, default='')
    uploaded_by = models.ForeignKey(User)
    report_type = models.ForeignKey(projectReportType)
    file_title = models.CharField(max_length=1000, default='')
    document_file = models.FileField(upload_to=get_project_document)
    view_stat = models.CharField(max_length=500, choices=SHOW_STAT, default='waiting')
    date_time = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.project_id.project_name + " | " + self.uploaded_by.username + " | " + self.file_title


# COMMUNICATION WITH CLIENT ABOUT PROJECT
class projectPosts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(projects)
    posted_by =  models.ForeignKey(User)
    comment = models.TextField(default='')
    date_time = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return self.project_id.project_name + " | " + self.comment



def increment_invoice_number():
    last_invoice = projectInvoice.objects.all().order_by('invoice_number').last()
    if not last_invoice:
        return 'SEM101'
    invoice_no = last_invoice.invoice_number
    invoice_int = int(invoice_no.split('SEM')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'SEM' + str(new_invoice_int)
    return new_invoice_no

# PROJECT MANUAL INVOICE CREATIONS
class projectInvoice(models.Model):



    INVOICE_STATUS = (
        ('generating','generating'),
        ('pending','pending'),
        ('paid','paid'),
        ('failed','failed'),
    )
    INVOICE_TYPE = (
        ('online','online'),
        ('cash','cash'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=500, default=increment_invoice_number, null=True, blank=True)
    project_id = models.ForeignKey(projects)
    created_date = models.DateField(null=True, auto_now_add=True)
    due_date = models.DateTimeField(datetime.today() + timedelta(days=4))
    taxable = models.ForeignKey(taxSlab)
    notes = models.TextField(default='')
    invoice_total_cost = models.CharField(max_length=1000,default='0')
    invoice_status = models.CharField(max_length=1000,choices=INVOICE_STATUS,default='generating')
    invoice_type = models.CharField(max_length=1000, choices=INVOICE_TYPE,default='online')

    def __str__(self):
        return self.invoice_number


# ITEMS FOR INVOICE
class invoiceItems(models.Model):
    invoice_id = models.ForeignKey(projectInvoice)
    item_type = models.TextField(default='')
    item_name = models.TextField(default='')
    item_description = models.TextField(default='')
    item_quantity = models.CharField(max_length=100,default='')
    item_cost = models.CharField(max_length=1000,default='')
    item_total_cost = models.CharField(max_length=1000,default='')

    def __str__(self):
        return self.item_type + " | " + self.item_name + " | " + self.item_total_cost