from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Product
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseRedirect
import csv, io, os, sys
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
import re




# Create your views here.

@method_decorator(login_required, name='dispatch')
class ProductViewSet(TemplateView):
    """
    Updates and retrieves user accounts
    """
    template_name = "products/product_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductViewSet, self).get_context_data(*args, **kwargs)
        context['products'] = Product.objects.all()
        context['username'] = self.request.user
        return context

@method_decorator(login_required, name='dispatch')
class CSVProductViewSet(APIView):
    """
    Outputs a CSV File of ProductList
    """
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.DictWriter(response, fieldnames=['Name', 'Type', 'Quantity', 'Price', 'Available', 'Stock', 'Total', 'Vendor', 'Created_at'])
        writer.writeheader()
        # use this if username is in url kwargs
        id = self.kwargs.get('id')
        print("id",id)
        if id == None:
            id = self.request.query_params.getlist('id')
        print("id",id)
        if id == None:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(id__in=id)
        for product in products:
            if product.name != "" or product.type != "" or product.quantity != "" or  product.price != "" or product.vendor != "" or product.available != "" or product.total != "" or product.stock != "" or product.created_at != "":
                writer.writerow({'Name': product.name, 'Type': product.type, 'Quantity': product.quantity, 'Price': product.price, 'Available': 1 if product.available == True else 0, 'Stock': product.total, 'Total': product.stock, 'Vendor': product.vendor, 'Created_at': product.created_at})
        return response
    def post(self, request, *args, **kwargs):
        context = {}
        if 'file' in request.FILES:
            csv_file = request.FILES['file']
        else:
            context['error_message'] = "File not selected"
            return render(request,'products/product_list.html',context)
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            context['message'] =  'THIS IS NOT A CSV FILE'
        # dialect = csv.Sniffer().sniff(csv_file.read().decode('UTF-8'), delimiters='\t,')
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        print('context',context)
        print('context',csv_file.name)
        fs = FileSystemStorage()
        csv_file = fs.save(csv_file.name, csv_file)
        # file_name  = str(csv_file)
        # print('fspath',fs.path())
        dir_path = os.path.dirname(os.path.realpath(csv_file))
        print('dir_path',dir_path)
        print('fsuadasrl',csv_file)
        print('fsurl',fs.url(name=csv_file))
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter='\t', quotechar="|"):
            print('re.split(',', column[0])',re.split(',', column[0]))
            if len(column) == 1:
                column = re.split(',', column[0])
            print('column',column)
            if Product.objects.filter(name=column[0],vendor = request.user).count() > 0:
                product = Product.objects.filter(name=column[0],vendor = request.user).first()
            else:
                product = Product()
            product.name = column[0]
            product.type = column[1]
            product.quantity = column[2]
            product.price = column[3]
            product.total = column[6]
            product.stock = column[5]
            product.vendor = request.user
            product.available = True if column[4] == "1" else False
            product.save()
        return HttpResponseRedirect(reverse('products:product_list'))

