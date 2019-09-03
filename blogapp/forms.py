from django import forms
from blogapp.models import Post, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control back'}))

    class Meta:
        model = User
        fields = ('username',
                'first_name',
                'last_name',
                'email',
                'password1',
                'password2'
        )
        labels = {
            'first_name':_('First Name'),
            'last_name':_('Last Name')
        }
        help_texts = {
            'username': _('Your Username should be unique.'),
            'password1': _('Password should be minimum of 8 Characters.'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control back'}),
            'first_name': forms.TextInput(attrs={'class':'form-control back name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control back name'}),
        }

    # To remove the help texts.
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['password1','password2']:
            self.fields[fieldname].help_text = None

    # def save(self, commit=True):
    #     """
    #     validate that the supplied email address is unique
    #     """
    #     if User.objects.filter(email__iexact=self.cleaned_data['email']):
    #         raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
    #     return self.cleaned_data['email']

    def save(self,commit=True):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please provide a different email address."))
        else:
            user = super(UserRegisterForm,self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user
 
class PostForm(forms.ModelForm):

     class Meta():
        model  = Post
        fields = ('title','text')
        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass title'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = {'text'}

        widgets = {
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }

class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'form-control back'}))

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control back'}),
            'first_name': forms.TextInput(attrs={'class':'form-control back name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control back name'}),
        }
        help_texts = {
            'username':None,
        }

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('image','description')

        widgets = {
            'description':forms.TextInput(attrs={'class':'form-control back'})
        }
