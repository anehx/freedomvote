from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput
from easy_thumbnails.files import get_thumbnailer
from django.templatetags.static import static

class ImagePreviewFileInput(ClearableFileInput):

    def render(self, name, value, attrs=None,):

        substitutions = {
            'clear_checkbox_label': self.clear_checkbox_label,
            'initial' : '<img class="img-responsive img-thumbnail" src="%s">' % (
                get_thumbnailer(value)['medium'].url if value and hasattr(value, 'url') else static('images/placeholder.svg')
            )
        }
        template = '%(initial)s%(input)s'

        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if not self.is_required:
            template = '%(initial)s%(clear_template)s%(input)s'
            checkbox_name = self.clear_checkbox_name(name)
            checkbox_id = self.clear_checkbox_id(checkbox_name)
            substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
            substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
            substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
            substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)