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
from  .forms import *
import time



class LoginView(FormView):
	success_url = '/redirecting'
	template_name = "login.html"
	form_class = AuthenticationForm
	redirect_field_name = REDIRECT_FIELD_NAME

	@method_decorator(sensitive_post_parameters('password'))
	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		# Sets a test cookie to make sure the user has cookies enabled
		request.session.set_test_cookie()

		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		auth_login(self.request, form.get_user())

		if self.request.session.test_cookie_worked():
			self.request.session.delete_test_cookie()

		return super(LoginView, self).form_valid(form)

	def get_success_url(self):
		redirect_to = self.success_url
		return redirect_to

class LogoutView(RedirectView):
	url = '/'
	def get(self, request, *args, **kwargs):
		auth_logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)


login = LoginView.as_view()
logout = LogoutView.as_view()


def redirecting(request):
	url = reverse('client_area:dashboard')
	return HttpResponseRedirect(url)


