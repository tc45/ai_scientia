from django import forms
from .constants import ICON_CHOICES

class IconSelectWidget(forms.Select):
    template_name = 'learning/widgets/icon_select.html'
    
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['class'] = 'icon-select form-control'
        self.choices = ICON_CHOICES

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-icon'] = value
        return option

    @property
    def media(self):
        return forms.Media(
            css={
                'all': (
                    'admin/css/vendor/select2/select2.min.css',
                    'admin/css/autocomplete.css',
                    'css/icon-select.css',
                )
            },
            js=(
                'admin/js/vendor/jquery/jquery.min.js',
                'admin/js/vendor/select2/select2.full.min.js',
                'js/icon-select.js',
            )
        ) 