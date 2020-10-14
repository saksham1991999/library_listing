from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from . import models


class LibraryForm(forms.ModelForm):
    class Meta:
        model = models.library
        exclude = ['owner', 'verified','visible','views','location']
        # labels = {
        #     'type': _('Select Type'),
        #     'property_name': _('Property Name'),
        #     'city': _('City'),
        #     'bedrooms': _('No of Bedrooms'),
        #     'bathrooms': _('No of Bathrooms'),
        #     'rooms': _('No of Rooms'),
        #     'construction_status': _('Construction Status (Optional)'),
        #     'available_from': _('Available from Date (YYYY-MM-DD) (Optional)'),
        #     'price_sq': _('Price per sq m (Optional)'),
        #     'total_price': _('Total Price'),
        #     'additional_features': _('Additional Features'),
        #     'image': _('Main Image'),
        #     'label': _('Label (Optional)'),
        #     'features': _('Features (Multi-Select)'),
        # }
        widgets = {
            'opening_time': forms.TimeInput(),
            'closing_time': forms.TimeInput(),
            'ammenities': forms.SelectMultiple(attrs={'style':'height:auto;'}),
            'payment_methods': forms.SelectMultiple(attrs={'style':'height:auto;'}),
            'mobile_no': forms.TextInput(attrs={'pattern':'[0-9]{10}'}),
            'pincode': forms.TextInput(attrs={'pattern': '[0-9]{6}'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name']
        # labels =
        # widgets =

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = models.enquiry
        fields = ['name', 'email', 'contact_no', 'preferred_joining_date', 'preferred_time_slot', 'remarks']

class RatingsForm(forms.ModelForm):
    class Meta:
        model = models.library_ratings
        fields = ['rating', 'comment']

class BugReportForm(forms.ModelForm):
    class Meta:
        model = models.bug_report
        fields = '__all__'
        # labels =
        widgets = {
            'contact_no': forms.TextInput(attrs={'pattern':'[0-9]{10}'})

        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = models.testimonial
        fields = '__all__'
        # labels =
        # widgets =

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = models.newsletter
        fields = '__all__'

class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = '__all__'

class ImagesForm(forms.ModelForm):
    class Meta:
        model = models.library_images
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'multiple': True})
        }
