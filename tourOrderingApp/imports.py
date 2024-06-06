# views.py
from decimal import Decimal, InvalidOperation
import logging
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse

from tourOrderingApp.forms import ImportCountryForm,  ImportTransportationForm
from tourOrderingApp.models import Country, Transportation
from tourOrderingApp.resources import CountryResource, TransportationResource

logger = logging.getLogger(__name__)


def import_country_records(request):
    if request.method == 'POST':
        form = ImportCountryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = CountryResource()
                new_records = request.FILES['country_records_file']

                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly
                
                for data in imported_data:
                    try:
                        country_record = Country.objects.create(
                            name=data[0],                                        
                                              
                        )
                    except IntegrityError:
                        messages.warning(request, f'Duplicate entry found for {data[0]}. Skipping this record.')
                        continue

                return redirect('manage_country') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportCountryForm()

    return render(request, 'admin_template/import_country.html', {'form': form})



def import_transportation_record(request):
    if request.method == 'POST':
        form = ImportTransportationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resource = TransportationResource()
                new_records = request.FILES['records_file']

                # Use tablib to load the imported data
                dataset = resource.export()
                imported_data = dataset.load(new_records.read(), format='xlsx')  # Assuming you are using xlsx, adjust accordingly
                
                for data in imported_data:
                    try:
                        transportation_record = Transportation.objects.create(
                            name=data[0],                                        
                            capacity=data[1],                                        
                            type=data[2],                                        
                            availability=data[3],                                        
                            image=data[4],                                        
                                              
                        )
                    except IntegrityError:
                        messages.warning(request, f'Duplicate entry found for {data[0]}. Skipping this record.')
                        continue

                return redirect('transportation_list') 
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    else:
        form = ImportTransportationForm()

    return render(request, 'admin_template/import_transportation_record.html', {'form': form})

