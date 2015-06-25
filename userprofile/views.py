from django.shortcuts import render

import account.views

from userprofile.forms import Settings, SignupForm
from userprofile.models import UserProfile

"""
class SettingsView(account.views.SettingsView):
  form_class = SettingsForm

  def get_initial(self):
    initial = super(SettingsView, self).get_initial()

    initial["extra_field"] = self.request.user.extra_field

    return initial

  def update_settings(self, form):
    super(SettingsView, self).update_settings(form)

    profile = self.request.user.userprofile
    profile.extra_field = form_cleaned_data['extra_field']
    profile.save()


class SignupView(account.views.SignupView):
  form_class = SignupForm

  def after_signup(self, form):
    profile = self.created_user.userprofile
    profile.extra_field = form_cleaned_data['extra_field']
    profile.save()

    super(SignupView, self).after_signup(form)
"""