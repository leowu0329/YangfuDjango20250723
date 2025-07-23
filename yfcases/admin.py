from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

class YfcaseAdmin(ImportExportModelAdmin):
  list_display = [field.name for field in Yfcase._meta.fields]

class CityAdmin(ImportExportModelAdmin):
  list_display = [field.name for field in City._meta.fields]

class TownshipAdmin(ImportExportModelAdmin):
  list_display = [field.name for field in Township._meta.fields]

class LandAdmin(ImportExportModelAdmin):
  list_display = [field.name for field in Land._meta.fields]

class BuildAdmin(ImportExportModelAdmin):
  list_display = [field.name for field in Build._meta.fields]

class FinalDecisionAdmin(ImportExportModelAdmin):
  list_display = [field.name for field in FinalDecision._meta.fields]

class SurveyAdmin(ImportExportModelAdmin):
  list_display = [field.name for field in Survey._meta.fields]

admin.site.register(Yfcase,YfcaseAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Township,TownshipAdmin)
admin.site.register(Land,LandAdmin)
admin.site.register(Build,BuildAdmin)
admin.site.register(FinalDecision,FinalDecisionAdmin)
admin.site.register(Survey,SurveyAdmin)
