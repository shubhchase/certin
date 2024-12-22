# core/forms.py

from django import forms
from .models import BlogPost, Comment, ServiceRequest
from .models import ContactMessage
from accounts.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comment',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }    

##end        

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BlogPostForm(forms.ModelForm):
    # image = forms.FileField(required=False)  # Allow any file type
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'author']   


class StarUserForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False),
        label="Select User",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount to Add",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("The amount must be a positive number.")
        return amount


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['name', 'email', 'service_type', 'purpose', 'company_address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),  
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        