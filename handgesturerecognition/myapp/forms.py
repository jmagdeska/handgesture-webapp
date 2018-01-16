# -*- coding: utf-8 -*-

from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Одберете слика:'
    )

# class ImageUploadForm(forms.Form):
#     """Image upload form."""
#     image = forms.ImageField(
#     	label='Select an image')