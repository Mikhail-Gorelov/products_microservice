from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('products/', views.ProductsListView.as_view(), name='hot-products'),
    path('product/<int:pk>/', views.ProductsDetailView.as_view(), name='hot-products-detail'),
    path('category/<int:pk>/', views.CategoriesDetailView.as_view(), name='category-detail'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('product/', views.ProductListView.as_view(), name='product-list'),
    path('product-variant-list/', views.ProductVariantListView.as_view(), name='product-variant-list'),
    path('product/checkout/', views.ProductCheckoutView.as_view(), name='product-checkout'),
    path('secure/', views.SecureView.as_view()),
    path('product-list/', views.ProductsView.as_view(), name='product-list'),
    path('channel-list/', views.ChannelListView.as_view(), name='channel-list'),
    path('product-variant/<int:pk>/', views.ProductsVariantView.as_view(), name='product-variant'),
    path('search-products/', views.SearchProductView.as_view(), name='search-products'),
    path('total-sum/', views.TotalSumView.as_view(), name='total-sum'),
    path('total-weight/', views.TotalWeightView.as_view(), name='total-weight'),
]
