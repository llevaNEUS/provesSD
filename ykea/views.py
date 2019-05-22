from django.shortcuts import render
from .models import Item, Shoppingcart, Itemquantity, User_account
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import ItemSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated

def index(request):
    context = {
        'categories': [i[0] for i in Item.CATEGORIES]
    }
    return render(request, 'ykea/index.html', context)


def items(request, category=""):
    items_by_category = Item.objects.filter(category=category)
    context = {
        'items': items_by_category,
        'category': category,
    }
    return render(request, 'ykea/items.html', context)


def detailed_item(request, item_number=""):
    try:
        item = Item.objects.get(item_number=item_number)
    except Item.DoesNotExist:
        item = ""
    context = {
        'item': item
    }
    return render(request, 'ykea/item_detail.html', context)

@login_required
def shoppingcartview(request):
    if not "shoppingcart" in request.session:
        shoppingcart = Shoppingcart()
        shoppingcart.user = User_account.objects.get(user=request.user)
        shoppingcart.save()
        request.session["shoppingcart"] = shoppingcart.id_sc
    else:
        shoppingcart = Shoppingcart.objects.get(id_sc=request.session["shoppingcart"])
    for key in request.POST:
        if key.startswith("checkbox"):
            item = Item.objects.get(item_number=request.POST[key])
            try:
                Itemquantity.objects.get(item=item, shoppingcart=shoppingcart)
            except Itemquantity.DoesNotExist:
                item_quantity = Itemquantity(item=item, shoppingcart=shoppingcart, quantity=1)
                item_quantity.save()

    return HttpResponseRedirect(reverse('buy'))


@login_required
def buy(request):
    shoppingcart = Shoppingcart.objects.get(id_sc=request.session["shoppingcart"])
    context = {
        'money' : shoppingcart.user.money,
        'shoppingcart': shoppingcart
    }
    return render(request, 'ykea/shoppingcart.html', context)

@login_required
def process(request):
    if request.POST:
        print(request.POST)
        if 'delete' in request.POST:
            return delete(request)
        elif 'buy' in request.POST:
            return process_done(request)

@login_required
def process_done(request):
    shoppingcart = Shoppingcart.objects.get(id_sc=request.session["shoppingcart"])
    total = 0
    for key in request.POST:
        if key.startswith("q"):
            item = Item.objects.get(item_number=key[1:])
            iq = Itemquantity.objects.get(item=item, shoppingcart=shoppingcart)
            iq.quantity = request.POST[key]
            iq.save()
    return HttpResponseRedirect(reverse('done'))

@login_required
def done(request):
    id_sc = request.session.pop("shoppingcart")
    shoppingcart = Shoppingcart.objects.get(id_sc=id_sc)
    total = 0
    for item in shoppingcart.items.all():
        iq = Itemquantity.objects.get(item=item, shoppingcart=shoppingcart)
        total = total + (float(iq.quantity) * float(item.price))

    context = {
        'shoppingcart': shoppingcart,
        'total': total}
    return render(request, 'ykea/done.html', context)

@login_required
def delete(request):
    shoppingcart = Shoppingcart.objects.get(id_sc=request.session["shoppingcart"])

    for key in request.POST:
        if key.startswith("checkbox"):
            item = Item.objects.get(item_number=request.POST[key])
            itq = Itemquantity.objects.get(item=item, shoppingcart=shoppingcart)
            itq.delete()

    return HttpResponseRedirect(reverse('shoppingcart'))


def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedin/")
    else:
        # Show an error page
        return HttpResponseRedirect("/account/invalid/")


def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/account/loggedout/")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user_account = User_account()
            user_account.user = new_user
            user_account.money = 100
            user_account.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })



class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Items to be viewed or edited.
    """
    queryset = Item.objects.all().order_by('item_number')
    serializer_class = ItemSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'destroy' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        
        return [permission() for permission in permission_classes]

    #permission_class = [IsAdminUser,]
    #http_method_names = ['get', 'post', 'head']



