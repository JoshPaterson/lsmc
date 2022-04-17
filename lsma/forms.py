from django import forms

class ImageRadioSelect(forms.RadioSelect):
    ...


class PageChoiceForm(forms.Form):
    page_number = forms.IntegerField(widget=ImageRadioSelect())

    def __init__(self, *args, **kwargs):
        pages = kwargs.pop('pages', None)
        super(PageChoiceForm, self).__init__(*args, **kwargs)
        if pages:
            self.fields['page_number'].widget.choices = [(page.number, page.number) for page in pages]