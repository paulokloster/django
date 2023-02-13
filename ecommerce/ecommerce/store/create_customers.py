from django.contrib.auth.models import User
from store.models import Customer

for user in User.objects.all():
    if not Customer.objects.filter(user=user).exists():
        Customer.objects.create(
            user=user, name=user.username, email=user.email)
