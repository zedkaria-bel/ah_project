from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, escales, ESCALES
from .CONST import poste, dpt
from django.db.models.fields import BLANK_CHOICE_DASH


cmps = ()
i=1
# cmps = (
#     (1, ''),
# )
for escale in escales.iterator():
    cmps = (*cmps, (escale.full_name, escale.full_name))
    i+=1


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Nom', required = True,
    widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    last_name = forms.CharField(max_length=30, label='Prénom', required = True,
    widget=forms.TextInput(attrs={'placeholder': 'Prénom'}))
    poste = forms.ChoiceField(choices = poste, required = True)
    escale = forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(cmps), required=False)
    dpt = forms.ChoiceField(choices = dpt, required = False)

    def signup(self, request, user):
        # print('"' + self.cleaned_data['escale'] + '"')
        # print(self.cleaned_data['dpt'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # pylint: disable=E1101
        profile = Profile.objects.get(user_id = user.id)
        profile.poste = dict(poste).get(int(self.cleaned_data['poste']))
        if self.cleaned_data['escale'] != '':
            profile.escale = ESCALES.objects.get(full_name=self.cleaned_data['escale'])
            profile.dpt = None
        else:
            profile.dpt = dict(dpt).get(int(self.cleaned_data['dpt']))
            profile.escale = None
        profile.save()
        user.save()
