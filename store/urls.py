from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('designs/', views.design_collection, name='design_collection'),
    path('designs/<int:design_id>/', views.collections_by_design, name='collections_by_design'),
    path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),
    path('collections/<int:collection_id>/add_review/', views.add_review, name='add_review'),
    path('order-success/', views.order_success, name='order_success'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
