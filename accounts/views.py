from django.shortcuts import render
from django.views.generic import TemplateView


#Вью для акаунтів

class AccountsView(TemplateView):
    template_name = "accounts/login.html"
