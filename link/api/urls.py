from rest_framework import routers
from link.api.views import CreateDataSet, DeleteDataSet
from link.api.views import DeleteRecord, AddRecord
from django.urls import path, include

app_name='linkapp'
router = routers.SimpleRouter()

urlpatterns = [
        path('create-data-set',     CreateDataSet.as_view(), name='create-set'),
        path('delete-data-set',     DeleteDataSet.as_view(), name='delete-set'),
        path('add-record',          AddRecord.as_view(), name='add-record'),
        path('delete-record',       DeleteRecord.as_view(), name='delete-record'),
]
urlpatterns += router.urls
