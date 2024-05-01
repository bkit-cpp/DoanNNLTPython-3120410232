from django.http import JsonResponse
from django.shortcuts import redirect,render
from django.contrib import messages
from .models import Product, Category, Product_Review, Order
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .models import *
# Create your views here.
def home(request):
    categories=Category.objects.filter(status=0)
    categories=Category.objects.all()
    product=Product.objects.filter(status=0)
    product=Product.objects.all()
    labels=[]
    data=[]
    queryset=Order.objects.order_by('-total_price')[:5]
    for item in queryset:
        labels.append(item.fname)
        data.append(item.total_price)
   # orders=Order.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count')
    context={'product':product, 'categories': categories,'labels':labels,'data':data}
    return render(request,"store/index.html",context)

def contact(request):
    return render(request,"store/contact.html")

def shop(request):
    category=Category.objects.filter(status=0)
    category=Category.objects.all()
    product=Product.objects.filter(status=0)
    product=Product.objects.all()
    context={'category':category,'product': product}
    return render(request,"store/shop.html", context)

def shopviews(request, slug):
    if(Category.objects.filter(slug=slug,status=0)):
        products=Product.objects.filter( category__slug=slug)
        category_name=Category.objects.filter(slug=slug).first()
        context={'products':products, 'category_name':category_name}
        return render(request,"store/products/index.html", context)
    else:
        messages.warning(request, "No such category found")
        return redirect('shop')

def productdetails(request, cate_slug, prod_slug):
    if(Category.objects.filter(slug=cate_slug, status=0)):
       if(Product.objects.filter(slug=prod_slug, status=0)):
        products=Product.objects.filter(slug=prod_slug, status=0).first()
        product=Product.objects.all()
     #   review=Product_Review.objects.all()
        review=Product_Review.objects.all()
        print(review)
        category_name=Category.objects.filter(slug=cate_slug).first()
        category=Category.objects.filter(status=0)
        context={'products': products,'product':product,  'category_name':category_name, 'category': category,'reviews':review}
       else:
           messages.error(request,"No such product found")
           return redirect('shop')
    else:
        messages.error(request,"No such product found")
        return redirect('shop')
    return render(request,"store/products/productdetails.html", context)

def Review_rate(request, prod_slug):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        review_text = request.GET.get('review_text')
        review_rating = request.GET.get('review_rating')
        email = request.GET.get('email')
        user = request.user  # Assuming you're using Django's authentication system
        product = Product.objects.get(slug=prod_slug)  # Get product by slug
        # Save the review
        Product_Review.objects.create(
            user=user,
            product=product,
            review_text=review_text,
            review_rating=review_rating,
            email=email
        )
        return redirect('/shop/{{ products.id}}', id=prod_id, prod_slug=prod_slug)
    
def productlistAjax(request):
    products=Product.objects.filter(status=0).values_list('name', flat=True)
    productsList= list(products)
    return JsonResponse(productsList, safe=False)

def searchproduct(request):
    if request.method =='POST':
        searchterm=request.POST.get('searchProducts')
        if searchterm=="":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product=Product.objects.filter(name__contains=searchterm).first()
            if product:
                return redirect('shop/'+product.category.slug+'/'+product.slug)
            else:
                messages.info(request,"No product match your search")
                return redirect(request.META.get('HTTP_REFERER'))
        
    return redirect(request.META.get('HTTP_REFERER'))

