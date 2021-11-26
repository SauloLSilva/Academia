from django.contrib import admin
from .models import Planos
# Register your models here.

@admin.register(Planos)
class Planos(admin.ModelAdmin):
    list_display = ('nome_plano','quantidade_aulas', 'valor')