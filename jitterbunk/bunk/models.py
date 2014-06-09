from django.db import models
from django.contrib.auth.models import User


class Bunk(models.Model):
    """ The bunk model. Contains the sender, recipient, and time of bunk."""
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    time = models.DateTimeField('date bunked')


class User(models.Model):
    """ The user model. Contains user and profile photo."""
    user = models.OneToOneField(User)
    # hard coding in user photos right now...
    photo = models.ImageField(upload_to='/img', default=
                              '/static/img/filler_photo.png')
