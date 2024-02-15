from django.contrib import admin
from masterapp .models import PrinterdataTable,ScannerTable

# Register your models here.
admin.site.register(PrinterdataTable)
admin.site.register(ScannerTable)