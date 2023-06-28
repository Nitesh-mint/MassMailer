from django import forms


class UploadJson(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={ #attrs in for the css class
        'class': 'form-control',
    }))
