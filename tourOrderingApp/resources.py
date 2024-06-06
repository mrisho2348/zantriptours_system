from import_export import resources
from tourOrderingApp.models import  Country,  Transportation

class CountryResource(resources.ModelResource):
    class Meta:
        model = Country

class TransportationResource(resources.ModelResource):
    class Meta:
        model = Transportation
        


        
