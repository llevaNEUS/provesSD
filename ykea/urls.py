from django.conf.urls import url
from django.contrib.auth.views import login, logout



from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items/$', views.items, name='items'),
    url(r'^items/(?P<category>.*)/$', views.items, name='items'),
    url(r'^item/$', views.detailed_item, name='details'),
    url(r'^item/(?P<item_number>.*)/$', views.detailed_item, name='details'),
    url(r'^shoppingcart/$', views.shoppingcartview, name='shoppingcart'),
    url(r'^shoppingcart/buy/$', views.buy, name='buy'),
    url(r'^shoppingcart/process/$', views.process, name='process_shoppingcart'),
    url(r'^shoppingcart/done/$', views.done, name='done'),
    url(r'^register/$', views.register, name='register'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),


]
