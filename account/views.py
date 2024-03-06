from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'auctions/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_member:
                login(request, user)
                return redirect('index')
            elif user is not None and user.is_artist:
                login(request, user)
                return redirect('index')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'auctions/login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'admin.html')


def customer(request):
    return render(request,'customer.html')


def employee(request):
    return render(request,'employee.html')

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Product, User, Bid

from .forms import BidForm, CommentForm, NewProductForm



def index(request):
    return render(request, "auctions/index.html", {
        "products" : Product.objects.filter(status=False),
        "bids" : Bid.objects.all()
    })




def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def create(request):
    if request.method == "POST":
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewProductForm()
        return render(request, "auctions/create.html", {"form": form})

def auctions(request, id):
    item = Product.objects.get(pk=id)
    bidform = BidForm
    commentform = CommentForm
    return render(request, "auctions/auctions.html", {"product": item, "bidform": bidform, "commentform": commentform})

def end_auction(request, id):
    if request.method == "POST":
        product = Product.objects.get(pk=id)
        product.status = True
        product.save()
        return HttpResponseRedirect(reverse("auction", args=[id]))

def watch_auction(request, id):
    if request.method == "POST":
        if "add" in request.POST:
            product = Product.objects.get(pk=id)
            product.watchers.add(request.user)
            product.save()
        else:
            product = Product.objects.get(pk=id)
            product.watchers.remove(request.user)
            product.save()
        
    return HttpResponseRedirect(reverse("auction", args=[id]))

def add_comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = Product.objects.get(pk=id)
            comment.save()
        return HttpResponseRedirect(reverse("auction", args=[id]))

def add_bid(request, id):
    
    def bid_valid(amount_):
        item = Product.objects.get(pk=id)
        bids = Bid.objects.filter(product=item)
        for bid in bids:
            if bid.amount > amount_:
                return False
        if item.startBid > amount_:
            return False

        return True
    
    if request.method == "POST":
        form = BidForm(request.POST, request.FILES)
        bid = form.save(commit=False)
        if bid_valid(bid.amount):
            bid.user = request.user
            bid.product = Product.objects.get(pk=id)
            bid.save()
        else:
            message = "Bid should must be greater than above price."
            return render(request, "auctions/auctions.html", {"product": Product.objects.get(pk=id), "bidform": BidForm, "commentform": CommentForm, "message": message})

        return HttpResponseRedirect(reverse("auction", args=[id]))

def watchlist(request):
    
    products = Product.objects.filter(watchers = request.user)
    
    return render(request, "auctions/watchlist.html", {
        "products" : products,
        "bids" : Bid.objects.all()
    })

