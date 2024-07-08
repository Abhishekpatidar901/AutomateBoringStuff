# pdfapp/forms.py
from django import forms

class PDFUploadForm(forms.Form):
    pdf = forms.FileField(label='Upload your PDF', required=True)
    question = forms.CharField(label='Ask a question about your PDF:', required=False)