from django import forms
from .models import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Text"}
            )
        }

    def clean_text(self):
        text = self.cleaned_data.get("text")
        if len(text.strip()) < 1:
            raise ValidationError("Text must be at least 1 character long.")
        return text


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Text",
                    "id": "edited-text",
                }
            )
        }

    def clean_text(self):
        text = self.cleaned_data.get("text")
        if len(text.strip()) < 1:
            raise ValidationError("Text must be at least 1 character long.")
        return text


class FollowForm(forms.Form):
    pass


class LikeUnlikeForm(forms.Form):
    pass
