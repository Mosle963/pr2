from django import forms
from ..models import Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,HTML


class PostBaseForm(forms.ModelForm):
    """
    Base class for other Post From to extend

    fields:
        post_text
    """
    post_text = forms.CharField(
        label="",
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10})    
        )
    
    class Meta:
        fields = ('post_text',)

    def add_helper_layout(self):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '',
                'post_text',
            ),
            ButtonHolder(
    Submit('submit', 'Save', css_class='btn-primary btn-lg'),
    HTML('<a class="btn btn-secondary btn-lg" href="{% url \'index\' %}">Cancel</a>')
)

        )


class PostCreateForm(PostBaseForm):
    """Create Post Form_Class, extends PostBaseForm"""
    class Meta(PostBaseForm.Meta):
        model = Post

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        self.add_helper_layout()


class PostUpdateForm(PostBaseForm):
    """Update Post Form_Class, extends PostBaseForm"""

    class Meta(PostBaseForm.Meta):
        model = Post

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        self.add_helper_layout()
