from django import forms
from django.utils.safestring import mark_safe
from .constants import ICON_CHOICES

class IconSelectWidget(forms.Select):
    template_name = 'learning/widgets/icon_select.html'
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs.update({
            'class': 'icon-select form-control',
            'data-placeholder': 'Select an icon'
        })
        self.choices = ICON_CHOICES

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-icon'] = value
            # Ensure label is clean text
            option['label'] = label.split('>')[-1].strip()
        return option

    def optgroups(self, name, value, attrs=None):
        groups = super().optgroups(name, value, attrs)
        for group in groups:
            for option in group[1]:
                if option['value']:
                    option['label'] = option['label'].split('>')[-1].strip()
        return groups

    # def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
    #     option = super().create_option(name, value, label, selected, index, subindex, attrs)
    #     if value:
    #         option['attrs']['data-icon'] = value
    #     return option

    # @property
    # def media(self):
    #     return forms.Media(
    #         css={
    #             'all': (
    #                 'admin/css/vendor/select2/select2.min.css',
    #                 'admin/css/autocomplete.css',
    #                 'css/icon-select.css',
    #             )
    #         },
    #         js=(
    #             'admin/js/vendor/jquery/jquery.min.js',
    #             'admin/js/vendor/select2/select2.full.min.js',
    #             'js/icon-select.js',
    #         )
    #     ) 