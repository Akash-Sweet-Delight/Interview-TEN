from django.urls import path
from .views import BookItemView, CancelBookingView, UploadCSVFileView, MemberListview, InventoeyListView


urlpatterns = [
    path('upload/<str:file_type>/', UploadCSVFileView.as_view(), name='upload_csv'),
    path('book/', BookItemView.as_view(), name='book'),
    path('cancel/', CancelBookingView.as_view(), name='cancel'),
    path('members/', MemberListview.as_view(), name='members_list'),
    path('inventory/', InventoeyListView.as_view(), name='inventory_list')
]
