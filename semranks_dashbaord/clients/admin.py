# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(subscription_plans)
admin.site.register(taxSlab)
admin.site.register(serviceItem)
admin.site.register(projectReportType)
admin.site.register(addons)
admin.site.register(projects)
admin.site.register(project_addons)
admin.site.register(projectFiles)
admin.site.register(projectReports)
admin.site.register(projectPosts)
admin.site.register(projectInvoice)
admin.site.register(invoiceItems)
