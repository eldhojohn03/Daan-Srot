from django.contrib import admin
from .models import *
admin.site.register(CustomUser)
admin.site.register(Donor)
admin.site.register(Organization)
#admin.site.register(OrganizationFiles)
admin.site.register(Transaction)
admin.site.register(Needs)