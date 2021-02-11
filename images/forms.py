from django import forms
from images.models import Image
from urllib import request
from django.utils.text import slugify
from django.core.files.base import ContentFile

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields =('title', 'url','description')
        widgets = {
            'url':forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The provided URL does not contain the requires image extention.')
        return url

    def save(self, force_insert= False, force_update=False, commit= True):
        image = super().save(commit = False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        #dowload the image from the url
        response = request.urlopen(image_url)
        image.image.save(image_name,
                            ContentFile(response.read()),
                            save = False
        )
        if commit:
            image.save()
        return image