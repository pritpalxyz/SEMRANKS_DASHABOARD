# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


admin.site.register(client_info)
admin.site.register(userRoles)
admin.site.register(employee_info)
admin.site.register(user_documents)
admin.site.register(account_credentials)
