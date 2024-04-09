import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class OrderFilter(django_filters.FilterSet):
    #custom additions get separtae lables to be displayed on search(filter) line
    start_date = DateFilter(field_name="date_created", lookup_expr='gte',label='Start Date')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte',label='End Date')
    class Meta:
        model= Order
        
       
        fields= '__all__'
        exclude=['customer','date_created']
        
     