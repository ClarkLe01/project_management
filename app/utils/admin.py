from django.contrib import admin
from .models import Currency, ProgrammingLanguage


class CurrenciesAdmin(admin.ModelAdmin):
    list_display = ['code', 'value']
    search_fields = ('code',)


# Register your models here.
admin.site.register(Currency, CurrenciesAdmin)
admin.site.register(ProgrammingLanguage)
