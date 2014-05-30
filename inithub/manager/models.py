'''
Copyright 2012-2014 Rich Termondt

This file is part of Inithub-web.

Inithub-web is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Inithub-web is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Inithub-web.  If not, see <http://www.gnu.org/licenses/>.

@author: rtermondt
'''
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import uuid
# need to calulate success somehow?? This is the secret sauce

# if a company has at least x contributors, and x % of those contributors
# deem company success

# TODO: need to hookup and test UserProfile


def make_uuid():
    return str(uuid.uuid4())


class Profile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=25)
    country = models.CharField(max_length=10)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # start release 0.2
    is_disabled = models.BooleanField(default=False)
    confirm_key = models.CharField(max_length=36, unique=True, editable=False)
    is_confirmed = models.BooleanField(default=False)
    # end release 0.2


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Profile_Rating(models.Model):
    profile = models.ForeignKey(Profile)
    profile_reviewer = models.ForeignKey(Profile, related_name='reviewer')
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comments = models.TextField()
    is_removed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Interest(models.Model):
    short_desc = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Interests(models.Model):
    profile = models.ForeignKey(Profile)
    interest = models.ForeignKey(Interest)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Service(models.Model):
    short_desc = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Services(models.Model):
    profile = models.ForeignKey(Profile)
    service = models.ForeignKey(Service)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Initiative(models.Model):
    profile = models.ForeignKey(
        Profile, editable=False)  # this is the initiator
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    uuid = models.CharField(max_length=36, unique=True,
                            default=make_uuid, editable=False)
    publish_date = models.DateTimeField(null=True, blank=True, default=None)


class Initiative_Service(models.Model):
    initiative = models.ForeignKey(Initiative)
    service = models.ForeignKey(Service)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Initiative_Service_Offer(models.Model):
    profile = models.ForeignKey(Profile)
    initiative = models.ForeignKey(Initiative)
    service = models.ForeignKey(Service)
    is_accepted = models.BooleanField(default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Initiative_Rating(models.Model):
    initiative = models.ForeignKey(Initiative)
    profile = models.ForeignKey(Profile)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comments = models.TextField()
    is_removed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Initiative_Service_Profile(models.Model):
    initiative_service = models.ForeignKey(Initiative_Service)
    profile = models.ForeignKey(Profile)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Milestone(models.Model):
    short_desc = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Milestones(models.Model):
    initiative = models.ForeignKey(Initiative)
    milestone = models.ForeignKey(Milestone)
    target_date = models.DateField(null=True)
    complete_date = models.DateField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


class Promotion(models.Model):
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField()
    code = models.CharField(max_length=10)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Invitation(models.Model):
    email = models.CharField(max_length=75, unique=True)
    signup_key = models.CharField(max_length=100)
    promotion = models.ForeignKey(Promotion)
    profile = models.ForeignKey(Profile, null=True, blank=True, default=None)
    approved_date = models.DateTimeField(null=True, blank=True, default=None)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Subject(models.Model):
    profile = models.ForeignKey(Profile)
    initiative = models.ForeignKey(Initiative)
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField()
    is_public = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Message(models.Model):
    profile = models.ForeignKey(Profile)
    subject = models.ForeignKey(Subject)
    comment = models.TextField()
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Message_History(models.Model):
    message = models.ForeignKey(Message)
    profile = models.ForeignKey(Profile)
    is_read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


# start release 0.2
class Subscription(models.Model):
    short_desc = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Subscription_Profile(models.Model):
    subscription = models.ForeignKey(Subscription)
    profile = models.ForeignKey(Profile)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Subscription_Message(models.Model):
    subscription = models.ForeignKey(Subscription)
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField()
    is_html = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Subscription_Message_Profile(models.Model):
    subscription_message = models.ForeignKey(Subscription_Message)
    profile = models.ForeignKey(Profile)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
# end release 0.2


# start release 0.15
class Profile_Invite(models.Model):
    profile = models.ForeignKey(Profile)
    invitation = models.ForeignKey(Invitation)
    message = models.TextField()


class Payment_Receipt(models.Model):
    processor = models.CharField(max_length=50)
    ref_id = models.CharField(max_length=50)
    short_desc = models.CharField(max_length=50)
    table_desc = models.CharField(max_length=50)
    table_key = models.IntegerField()
    profile = models.ForeignKey(Profile)
    amount = models.IntegerField()
    is_subscription = models.BooleanField(default=False)
    currency_code = models.CharField(max_length=5)
    transaction_date = models.DateTimeField(auto_now_add=True)
# end release 0.15

'''
class Item(models.Model):
    uuid = models.CharField(max_length=36, unique=True, editable=False)
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField()
    'table_desc = models.CharField(max_length=100)
    'table_key = models.CharField(max_length=36, unique=True, editable=False)
    amount = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Attribute(models.Model):
    short_desc = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Item_Attribute(models.Model):
    item = models.ForeignKey(Item)
    attribute = models.ForeignKey(Attribute)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Discount(models.Model):
    code = models.CharField(max_length=10)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Item_Discount(models.Model):
    item = models.ForeignKey(Item)
    discount = models.ForeignKey(Discount)
    amount = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class Receipt(models.Model):
    item = models.ForeignKey(Item, null=True, blank=True, default=None)
    profile = models.ForeignKey(Profile)
    discount = models.ForeignKey(Discount, blank=True, null=True)
    amount = models.IntegerField()
    currency_code = models.CharField(max_length=5)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
'''
