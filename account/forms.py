from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',  'is_artist', 'is_member')


from django.forms import ModelForm, ValidationError

from .models import Product, Bid, Remark

def valid_bid(amount_, id):
    item = Product.objects.get(pk=id)
    if item.bids.all.count == 0:
        if int(amount_) > item.startBid:
            return True
    if int(amount_) > item.bids.first.amount:
        return True

    return False

class NewProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["title", "desc", "startBid", "img"]
        labels = {
            'title': ('Product Name'),
            'desc': ('Product Description'),
            'startBid': ('Starting Bid ($)'),
            'img': ('Image (URL)'),
            
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        labels = {
            "amount" : ('Enter Bid'),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Remark
        fields = ["message"]
        labels = {
            "message": ('Post Comment: '),
        }
