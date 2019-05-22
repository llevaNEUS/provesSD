# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    CATEGORIES = (
        ("beds", "Beds & mattressess"),
        ("furn", "Furniture, wardrobes & shelves"),
        ("sofa", "Sofas & armchairs"),
        ("table", "Tables & chairs"),
        ("texti", "Textiles"),
        ("deco", "Decoration & mirrors"),
        ("light", "Lighting"),
        ("cook", "Cookware"),
        ("tablw", "Tableware"),
        ("taps", "Taps & sinks"),
        ("org", "Organisers & storage accesories"),
        ("toys", "Toys"),
        ("leis", "Leisure"),
        ("safe", "safety"),
        ("diy", "Do-it-yourself"),
        ("floor", "Flooring"),
        ("plant", "Plants & gardering"),
        ("food", "Food & beverages")
    )
    item_number = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_new = models.BooleanField()
    size = models.CharField(max_length=40)
    instructions = models.FileField(upload_to="instructions")
    featured_photo = models.ImageField(upload_to="photos")
    category = models.CharField(max_length=5, choices=CATEGORIES)

    def __str__(self):
        return (
                   '[**NEW**]' if self.is_new else '') + "[" + self.category + "] [" + self.item_number + "] " + self.name + " - " + self.description + " (" + self.size + ") : " + str(
            self.price) + " €"


class User_account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.DecimalField(max_digits=12, decimal_places=2)

class Shoppingcart(models.Model):
    id_sc = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Item, through='Itemquantity')
    user = models.ForeignKey(User_account, on_delete=models.CASCADE)

class Itemquantity(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shoppingcart = models.ForeignKey(Shoppingcart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Bill(models.Model):
    id_sc = models.AutoField(primary_key=True)
    user = models.ForeignKey(User_account, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    items = models.ManyToManyField(Item, through='Line_Bill')

class Line_Bill(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)


