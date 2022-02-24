from django import forms
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from .models import product
class productform(forms.ModelForm):
    class Meta:
        model= product
        fields=['name','cat','description','price','availableproduct']
