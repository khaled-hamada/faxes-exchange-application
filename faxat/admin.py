from django.contrib import admin
from faxat.models import fax, dept,dept_fax, LoggedUserNew,fax_comments

# Register your models here.

admin.site.register(fax)
admin.site.register(dept_fax)
admin.site.register(dept)
admin.site.register(fax_comments)
admin.site.register(LoggedUserNew)
