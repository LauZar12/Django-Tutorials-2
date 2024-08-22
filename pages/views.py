from django.http import HttpResponseRedirect
from django.shortcuts import render # here by default
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

# Create your views here.
class HomePageView(TemplateView):
 template_name = 'pages/home.html'

class AboutPageView(TemplateView):
 template_name='pages/about.html'
 def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Laura Danniela Zárate Guerrero.",
        })
        return context

class ContactPageView(TemplateView):
 template_name='pages/contact.html'
 def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "Contact",
            "mail": "lauralaura@gmail.com",
            "phone": "3333333333",
            "address": "Calle 1 #2-3",
            "author": "Developed by: Laura Danniela Zárate Guerrero.",
        })
        return context

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' # This will allow you to loop through 'products' in your template 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context


class ProductFormView(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0 and price is not None:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductFormView()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductFormView(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

class ProductSuccessView(View):
    template_name = 'products/success.html'
    def get(self, request):
        viewData = {}
        return render(request, self.template_name)


