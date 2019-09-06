from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from .views import EndView, BookView, CancelView, CostView, AvailableView

urlpatterns = [
    url('available/', AvailableView.as_view(), name='login'),
    url('book/', BookView.as_view(), name='book'),
    url('cancel/', CancelView.as_view(), name='cancel'),
    url('cost/', CostView.as_view(), name='cost'),
    url('end/', EndView.as_view(), name='end'),

]
