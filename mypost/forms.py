from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(
        label = "Contenu du post",
        widget=forms.Textarea(
            attrs={'required': True,
                 'cols': 30, 'rows': 10,
                 'class': 'form-control'}
        )
    )

    title = forms.CharField(
        label = "Titre",
        widget = forms.TextInput(
            attrs = {
                'required': True,
                'cols': 30, 'row':2,
                'class':'form-control',
            }
        )
    )

    overwiew = forms.CharField(
        label = "Bref appercu du post",
        widget = forms.TextInput(
            attrs = {
                'required': True,
                'cols': 30, 'row':20,
                'class':'form-control',
            }
        )
    )

    key_words = forms.CharField(
        label = "Mots clés...  Facultatif",
        required=False,
        widget = forms.TextInput(
            attrs = {
                'cols': 30, 'row':2,
                'class':'form-control',
            }
        )
    )



    class Meta:
        model = Post
        fields = ('title','overwiew','key_words', 'content', 'post_image','previous_post', 'next_post' )


class CommentForm(forms.ModelForm):
    email = forms.EmailField(
                    required = False,
                    widget = forms.TextInput(
                        attrs = {
                            'class': 'form-control',
                            'placeholder':"Your E-mail... not required!"
                        }
                    )
    )

    comment_body = forms.CharField(
                    widget = forms.Textarea(
                        attrs = {
                            'class': 'form-control',
                            'rows':"10", 'cols':"50",
                        }
                    )
    )
    class Meta:
        model =  Comment
        fields = ('comment_body',)
