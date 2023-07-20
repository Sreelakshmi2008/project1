from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from order.models import *
from django.db.models import Sum
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup
from django.template.loader import get_template
from django.template import RequestContext
import io
# Create your views here.




# sales report page
def sales_report(request):
    # sales_data = Order.objects.filter(status='Delivered').values('created_at', 'order_number').annotate(
    #     quantity_sold=Sum('orderitem__quantity'),
    #     total_sales=Sum('orderitem__quantity' * 'orderitem__unit_price')
    # )
    products = Product.objects.all()
    context = {
         'products': products,
    }
    return render(request, 'admin_templates\sales_report.html', context)



# sales report of each product page
def sales_report_by_product(request,id):
    product = Product.objects.get(pk=id)
    orders = OrderItem.objects.filter(product=product)
    s = product.productvariant.all()
    total_stock = 0
    for s in s:
      total_stock += s.pdt_stock
      
    delivered_orders = []
    delivered_quantity = 0
    for order in orders:
        if order.order.status == 'Delivered':
           delivered_orders.append(order)
           delivered_quantity += order.quantity
    
    number_delivered_orders = len(delivered_orders)

    
    context = {
        'product':product,
        'orders':orders,
         'delivered_quantity':delivered_quantity,
        'number_delivered_orders':number_delivered_orders,
        'total_stock':total_stock
    }
    

    return render(request, 'admin_templates\sales_report_by_product.html',context)



# converting into excel
def generate_excel(request):
    # Get the HTML table data
    html_content = request.GET['html_content']

    # Create an Excel workbook
    wb = Workbook()
    ws = wb.active

    # Write the HTML table data to the Excel workbook
    for row in html_content.split('\n'):
        row_data = row.split(',')
        ws.append(row_data)

    # Save the Excel workbook
    output = io.BytesIO()
    wb.save(output)

    # Create the response object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="table.xlsx"'

    # Write the Excel workbook data to the response object
    response.write(output.getvalue())

    return response