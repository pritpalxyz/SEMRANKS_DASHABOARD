# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView ,DetailView, UpdateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.models import PermissionDenied
from django.views.generic.edit import DeleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

from .models import *


class ClientDashboard(TemplateView):
	template_name = 'client_area.html'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(self.__class__, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		projectsAll = projects.objects.filter(client_id=self.request.user)
		all_invoices = 0
		all_reports = []
		for proj in projectsAll:
			query_object = Q(project_id=proj) & Q(invoice_status='pending')
			all_invoices+=int(projectInvoice.objects.filter(query_object).count())

		# allInvoice = projectInvoice.objects.filter()
		context['projectCount'] = projectsAll.count()
		context['pendingInvoice'] = all_invoices
		return context




dashboard = ClientDashboard.as_view()