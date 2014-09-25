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
from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.contrib.localflavor.us.forms import USStateField


class UserInviteForm(forms.Form):
    email = forms.CharField(label='Email', max_length=75, required=True)
    message = forms.CharField(label='Optional message', widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5}), max_length=500, required=False)


class InitiativeForm(forms.Form):
    short_desc = forms.CharField(label='Title', max_length=100)
    long_desc = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={
                'cols': 60,
                'rows': 20}))
    is_public = forms.BooleanField(label='Publish', required=False)


class InvitationForm(forms.Form):
    #email = forms.CharField(max_length=75, widget=widgets.TextInput(attrs={'class': 'required'}))
    email = forms.EmailField(max_length=75)


class SigninForm(forms.Form):
    email = forms.CharField(max_length=75, widget=forms.TextInput(
        attrs={'autocomplete': 'off'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())


class ProfileForm(forms.Form):
    YOUR_STATE_CHOICES = list(STATE_CHOICES)
    YOUR_STATE_CHOICES.insert(0, ('', '---------'))
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=75)
    city = forms.CharField(max_length=50, required=False)
    state = USStateField(widget=forms.Select(
                         choices=YOUR_STATE_CHOICES), required=False)
    #state = forms.CharField(max_length=25, required=False)
    zip = forms.CharField(max_length=10, required=False)


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        max_length=128,
        label='Current Password',
        widget=forms.PasswordInput())
    new_password1 = forms.CharField(max_length=128,
                                    label='New Password',
                                    widget=forms.PasswordInput(),
                                    validators=[MinLengthValidator(6)])
    new_password2 = forms.CharField(
        max_length=128,
        label='Confirm Password',
        widget=forms.PasswordInput())


class ProfileCreateForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=75)
    password1 = forms.CharField(max_length=128,
                                label='Password',
                                widget=forms.PasswordInput(),
                                validators=[MinLengthValidator(6)])
    password2 = forms.CharField(
        max_length=128,
        label='Confirm Password',
        widget=forms.PasswordInput())


class SubjectAddForm(forms.Form):
    short_desc = forms.CharField(label='Subject', max_length=100)
    long_desc = forms.CharField(
        label='Comments',
        widget=forms.Textarea(
            attrs={
                'cols': 60,
                'rows': 20}))


class MessageAddForm(forms.Form):
    comment = forms.CharField(label='Comments', widget=forms.Textarea(
        attrs={'cols': 40, 'rows': 10}))
