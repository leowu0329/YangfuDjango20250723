from import_export import resources
from .models import *
from users.models import *

class YfcaseResource(resources.ModelResource):
  class Meta:
    model=Yfcase

class CityResource(resources.ModelResource):
  class Meta:
    model=City

class TownshipResource(resources.ModelResource):
  class Meta:
    model=Township