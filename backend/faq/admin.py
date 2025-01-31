# backend/faq/admin.py
from django.contrib import admin
from .models import FAQ
from ckeditor.widgets import CKEditorWidget
from django import forms

class FAQAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorWidget())
    answer_hi = forms.CharField(widget=CKEditorWidget(), required=False)
    answer_bn = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = FAQ
        fields = '__all__'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm
    list_display = ('question', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')