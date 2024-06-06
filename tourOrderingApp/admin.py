from datetime import timezone
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from tourist_system import settings
from .models import CustomUser, AdminHOD, Country,  Transportation
from django.utils.html import format_html
# Register your models here.


