from django.urls import path
from . import views,views_node

urlpatterns = [
    path('', views.hello),
    path('bidder/<int:id>',views_node.home),
    path('auctioneer',views.home),
    path('bidder/bid',views_node.get_amount),
    path('bidder/<int:id>/withdraw',views_node.withdraw),
    path('auctioneer/result',views.end),
]