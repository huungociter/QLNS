from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Person

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='khách hàng')
        instance.groups.add(group)

        newid = len(Person.objects.filter(id__contains='kh'))+1
        if int(newid) <= 9:
            newid = '0'+ str(newid)

        Person.objects.create(
            id='kh_0' + newid,
            ho_ten= instance.username,
            email= instance.email,
            user=instance
        )

post_save.connect(customer_profile, sender=User)