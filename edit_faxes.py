#configure setting for import files
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faxes.settings')
import django
django.setup()
from faxat import models


faxes = models.fax.objects.all()
print(len(faxes))
for fax in faxes:

    fax.approved = 2
    fax.save()



for fax in faxes:
    print(fax.approved)
