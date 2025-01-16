from django import forms

class SubCategorySelectWidget(forms.SelectMultiple):
	"""
	Custom widget to render subcategories in a box-like format.
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.attrs.update({'size': '10', 'style': 'width: 100%;'})

	def render(self, name, value, attrs=None, renderer=None):
		# Render as a single-select list
		if value is None:
			value = []
		final_attrs = self.build_attrs(self.attrs, attrs)
		output = [f'<select name="{name}" {forms.utils.flatatt(final_attrs)} multiple>']
		options = self.render_options(self.choices, value)
		if options:
			output.append(options)
		output.append('</select>')
		return '\n'.join(output) 