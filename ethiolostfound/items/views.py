from rest_framework import generics, permissions, filters, response, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Item, CustomUser
from django_filters.rest_framework import DjangoFilterBackend, FilterSet,CharFilter
from .serializers import ItemSerializer, UserSerializer



class ItemFilter(FilterSet):
    search = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['search', 'item_type', 'location']
class ItemListView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by('-date_posted')
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['item_type', 'location']
    ordering_fields = ['date_posted', 'title']
    ordering = ['-date_posted']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise ValueError("User must be authenticated to create an item.")

class UserItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user).order_by('-date_posted')

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        if item.user != request.user:
            return response.Response({'detail': 'Not permitted to edit this item.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        if item.user != request.user:
            return response.Response({'detail': 'Not permitted to delete this item.'}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)

class UserProfileItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user).order_by('-date_posted')

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

