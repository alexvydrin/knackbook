from django.forms import ModelForm

from mainapp.models import Article


class NewArticleForm(ModelForm):
    """Форма новой статьи"""

    class Meta:
        model = Article
        fields = ('title', 'content', 'sections', 'tags')

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data=data, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
