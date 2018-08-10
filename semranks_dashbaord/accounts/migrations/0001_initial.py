# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-10 07:18
from __future__ import unicode_literals

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='account_credentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=1000)),
                ('password', models.CharField(default='', max_length=1000)),
                ('account_for', models.CharField(default='others', max_length=1000)),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='client_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_website', models.CharField(default='', max_length=1000)),
                ('contact_email', models.CharField(default='', max_length=1000)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('billing_address', models.CharField(default='', max_length=1000)),
                ('contact_number', models.CharField(default='', max_length=1000)),
                ('billing_contact_number', models.CharField(default='', max_length=1000)),
                ('skype_account', models.CharField(default='', max_length=1000)),
                ('setup_fee', models.CharField(choices=[('pending', 'pending'), ('free', 'free'), ('paid', 'paid')], default='pending', max_length=1000)),
                ('about_client', models.TextField(default='')),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='employee_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_type', models.CharField(choices=[('remote', 'remote'), ('inoffice', 'inoffice')], max_length=1000)),
                ('semrank_email', models.CharField(default='', max_length=1000)),
                ('contact_email', models.CharField(default='', max_length=1000)),
                ('address', models.CharField(default='', max_length=1000)),
                ('contact_number', models.CharField(default='', max_length=1000)),
                ('alternate_contact_number', models.CharField(default='', max_length=1000)),
                ('skype_account', models.CharField(default='', max_length=1000)),
                ('description', models.TextField(default='')),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='user_documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=1000)),
                ('document', models.FileField(upload_to=accounts.models.get_user_document)),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('client', 'client'), ('employee', 'employee')], max_length=1000)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
