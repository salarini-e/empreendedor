from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Curso, Lead

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'parceiro', 'validade', 'user_register', 'data_register')
    search_fields = ('nome', 'parceiro')
    list_filter = ('parceiro', 'validade')
    ordering = ('-data_register',)
    readonly_fields = ('data_register', 'user_register')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user_register = request.user
        super().save_model(request, obj, form, change)

class LeadAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'curso', 'data_register')
    search_fields = ('nome', 'email', 'telefone')
    list_filter = ('curso',)
    ordering = ('-data_register',)
    readonly_fields = ('data_register',)

admin.site.register(Curso, CursoAdmin)
admin.site.register(Lead, LeadAdmin)
