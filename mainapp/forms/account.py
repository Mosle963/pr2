from django import forms
from django.db import transaction
from ..models import Account, CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .home import CustomUserCreationForm
from django.core.exceptions import ValidationError
from datetime import date

 
class AccountBaseForm(forms.ModelForm):
    """
    Base class for other Account From to extend

    fields:
        first_name,
        last_name, 
        date_of_birth, 
        gender,
        city, 
        Bio,
    methods:
        add_helper_layout : define a basic layout for crispy forms
        clean_date_of_birth : make sure age is above 18
        clean_bio : make sure to have some text
    """

    first_name = forms.CharField(
        label="First Name",
        max_length=100,
        help_text="First Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=100,
        help_text="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    date_of_birth = forms.DateField(
        label="Date Of Birth",
        help_text="Date of Birth",
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"type": "date", "class": "form-control"}
        ),
    )
    gender = forms.ChoiceField(
        choices=[("MALE", "MALE"), ("FEMALE", "FEMALE")],
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    city = forms.CharField(
        label="City",
        max_length=50,
        help_text="City",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    bio = forms.CharField(
        label = "Bio",
        max_length=1000,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )

    def clean_date_of_birth(self):
        data = self.cleaned_data["date_of_birth"]
        birthyear = data.year
        today = date.today()
        age = today.year - birthyear
        if (today.month, today.day) < (data.month, data.day):
            age -= 1
        if data > today:
            raise ValidationError("Date of birth cannot be in the future.")
        if age < 16:
            raise ValidationError("You must be at least 16 years old to register.")
        return data

    def clean_bio(self):
        bio = self.cleaned_data['bio'].strip()
        if not bio:
            raise forms.ValidationError("please add some text let people know about you ^_^")
        return bio

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "city",
            "bio"
        )


class AccountSignUpForm(CustomUserCreationForm, AccountBaseForm):
    """
    SignUp a new Account Form_Class

    - extends AccountBaseForm
    - alter fields to add User Fields ( email , password)
    - alter Layout to add User Fields ( email , password)

    methods:
        save:
            - create account object
            - set OneToOne field with the created user
    """

    class Meta(CustomUserCreationForm.Meta, AccountBaseForm.Meta):
        model = CustomUser
        user_fields = CustomUserCreationForm.Meta.fields
        account_fields = AccountBaseForm.Meta.fields
        fields = user_fields + account_fields

    def __init__(self, *args, **kwargs):
        super(AccountSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "User Information",
                "email",
                "password1",
                "password2",
            ),
            Fieldset(
                "Personal Information",
                "first_name",
                "last_name",
                "date_of_birth",
                "gender",
                "city",
                "bio",
            ),
            ButtonHolder(Submit("submit", "Sign Up", css_class="btn-primary")),
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        account = Account.objects.create(
            user=user,
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            date_of_birth=self.cleaned_data["date_of_birth"],
            gender=self.cleaned_data["gender"],
            city=self.cleaned_data["city"],
            bio=self.cleaned_data["bio"],
        )
        account.save()
        return user


class AccountUpdateForm(AccountBaseForm):
    """Update Account User info Form_Class ,extends AccountBaseForm"""

    class Meta(AccountBaseForm.Meta):
        model = Account

    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Personal Information",
                "first_name",
                "last_name",
                "date_of_birth",
                "gender",
                "city",
                "bio",
            ),
            ButtonHolder(Submit("submit", "Save", css_class="btn-primary")),
        )
