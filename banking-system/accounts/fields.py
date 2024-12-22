# # core/fields.py

# from django import forms
# import random

# class CaptchaField(forms.CharField):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.widget.attrs.update({'class': 'shadow appearance-none border border-gray-500 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
    
#     def clean(self, value):
#         super().clean(value)
#         try:
#             # Generate random 6-digit number
#             random_number = ''.join(random.choices('0123456789', k=6))
#             if value and value == random_number:
#                 return value
#             else:
#                 raise forms.ValidationError("Incorrect captcha. Please try again.")
#         except ValueError:
#             raise forms.ValidationError("Invalid captcha format.")
