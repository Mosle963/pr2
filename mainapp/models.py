from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from datetime import date
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime
from relative_datetime import DateTimeUtils        

class CustomUser(AbstractUser):
    """
    extend AbstractUser and do configurations

    - Create a new class called User that subclasses AbstractUser
    - Removed the username field
    - Made the email field required and unique
    - Set email as the unique identifier for the User model
    - Specified that all objects for the class come from the CustomUserManager
    - added flags to show the user type (employee/company)

    """
    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email_address", unique=True)
    is_trusted = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Account(models.Model):
    """
    Account model handle users' account

    Has the following attributes:
        user : OneToOneField with User instance , primary key
        first_name,
        last_name, 
        date_of_birth, 
        gender,
        city, 
        Bio,

    methods:
        __str__ : return firs_tname + last_name to represent inctanse
        get_age : calculate the employee age based on date_of_birth
        get_absolute_url : return url link to employee detail page
        get_fields : return fields we want to show in employee detail page
    """

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField("First Name", max_length=100)
    last_name = models.CharField("Last Name", max_length=100)
    date_of_birth = models.DateField("Date Of Birth",)
    gender = models.CharField("Gender", max_length=8, choices=[("MALE", "MALE"), ("FEMALE", "FEMALE")])
    city = models.CharField("City", max_length=50)
    bio = models.TextField("Bio", max_length=1000)
    last_api_call = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """String for representing the Account object (in Admin site etc.)."""
        return self.first_name + " " + self.last_name

    def get_age(self):
        """function return user age based on thier birthday"""
        today = date.today()
        birthyear = self.date_of_birth.year
        age = today.year - birthyear
        # Account for birthdays not yet passed in the current year
        my_birth_month = self.date_of_birth.month
        my_birth_day = self.date_of_birth.day
        if (today.month, today.day) < (my_birth_month, my_birth_day):
            age -= 1
        return str(age)

    def get_absolute_url(self):
        """Return url to page shows user details"""
        return reverse("account_detail", kwargs={"pk": self.pk})

    def get_fields(self):
        """return info to be showed in user details page"""
        fields = []
        for field in self._meta.fields:
            if field.verbose_name not in [
                "user",
                "Date Of Birth",
                "last api call"
            ]:
                val = field.value_from_object(self)
                info = (field.verbose_name, val)
                fields.append(info)
            if field.verbose_name in ["Date Of Birth"]:
                info = ("Age", self.get_age())
                fields.append(info)
        return fields

from enum import Enum

class Status(Enum):
    P = "Processing.."
    V = "Verified"
    DP = "Disproven"
    DF = "Definitely False"
    PF = "Probably False"
    NS = "Not Sure"
    PT = "Probably True"
    DT = "Definitely True"

class Post(models.Model):
    post_id = models.BigAutoField("Post id",primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="account")
    post_text = models.TextField("Post Text", max_length=5000)
    true_prob = models.FloatField("Prop",default = -1)
    status = models.CharField(
        max_length=50,
        choices=[(status.name, status.value) for status in Status],
        default=Status.P.value
    )
    checker = models.ForeignKey(Account,null=True, blank=True,on_delete=models.SET_NULL,related_name="checker")
    created_at = models.DateTimeField("Created at", auto_now_add = True)
    updated_at = models.DateTimeField("Updated at", auto_now = True)
    
    class Meta:
        verbose_name = "Post"
        ordering = ["-post_id"]

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of Post."""
        return reverse("post_detail", kwargs={"pk": self.post_id})

    def __str__(self):
        """String for representing the Post object (in Admin site etc.)."""
        return f"Post (id : {self.post_id}) by " + self.account.__str__()

    def get_fields(self):
        """return fields (name,value) we want to show in Post detail page"""
        fields = [
            ("Post Text",post_text.value_from_object(self))
        ]
        return fields

    def approve(self,checker_id):
        user = get_object_or_404(CustomUser, id=checker_id)
        self.checker = user.account
        self.status = Status.V.value
        self.save()

    def disapprove(self,checker_id):
        user = get_object_or_404(CustomUser, id=checker_id)
        self.checker = user.account
        self.status = Status.DP.value
        self.save()

    def reset(self):
        self.checker = None
        self.save()
        self.set_status()
    
    def set_status(self):
        P = self.true_prob
        P = P * 100
        P = int(P)
        
        if 0 <= P <= 20:
            self.status = Status.DF.value
        elif 21 <= P <= 40:
            self.status = Status.PF.value
        elif 41 <= P <= 60:
            self.status = Status.NS.value
        elif 61 <= P <= 80:
            self.status = Status.PT.value
        elif 81 <= P <= 100:
            self.status = Status.DT.value
        else:
            self.status = Status.P.value
        
        self.save()
    
    def get_relative_time(self):
        now = datetime.now()
        past_date = self.created_at
        relative_time = DateTimeUtils.relative_datetime(past_date)[0]
        ago = " ago" 
        if relative_time == "just now":
            ago =""
        return relative_time+ago

class Following(models.Model):
    follower = models.ForeignKey(Account, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(Account, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followee')