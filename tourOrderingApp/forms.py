from django import forms
from django.core.validators import FileExtensionValidator
from tourOrderingApp.models import About, ContactRequest, Feedback, Hotel
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ImportCountryForm(forms.Form):
    country_records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportTourCategoryForm(forms.Form):
    records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
class ImportTransportationForm(forms.Form):
    records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
    
class ImportActivityForm(forms.Form):
    records_file = forms.FileField(
        label='Choose an Excel file',
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])],
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )
    

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'cont_in', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'cont_in', 'placeholder': 'Your Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'cont_in', 'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'textarea2', 'placeholder': 'Message', 'style': 'color:#676767;'}),
        }
        
class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['content']     
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message', 'required': True}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/png, image/jpeg, image/jpg', 'required': True}),  # Add image field widget with required attribute
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            file_type = image.content_type.split('/')[1]
            if file_type not in ['png', 'jpeg', 'jpg']:
                raise ValidationError(_('File type is not supported. Please upload a PNG, JPEG, or JPG file.'), code='invalid')
        return image