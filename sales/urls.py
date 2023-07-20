from django.urls import path
from . import views

urlpatterns = [
    path('sales_report',views.sales_report, name='sales_report'),
    path('sales_report_by_product\<int:id>',views.sales_report_by_product, name='sales_report_by_product'),
    path('generate_excel',views.generate_excel, name='generate_excel'),
    
]
