from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import UserProfileItemListView, UserProfileUpdateView, ItemListView, ItemDetailView, UserItemListView

urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('user-items/', UserItemListView.as_view(), name='user-item-list'),
    path('profile/items/', UserProfileItemListView.as_view(), name='user-profile-item-list'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
