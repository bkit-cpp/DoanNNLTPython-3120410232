import random
from django.http import JsonResponse
from django.shortcuts import redirect,render
from django.contrib import messages
from store.models import Product, Cart,Order,OrderItems
def index(request):
  cart_items = request.session.get('cart', [])
  products = []
  total_price = 0
    
  for item in cart_items:
        product = Product.objects.filter(id=item['product_id']).first()
        if product:
            subtotal = product.selling_price * item['product_qty']
            total_price += subtotal
            products.append({
                'product': product, 
                "id":item['product_id'],
                'name':item['product_name'],
                'quantity': item['product_qty'], 
                'subtotal': subtotal,
                'total_price': total_price  # Thêm giá trị tổng giá của giỏ hàng
            })
#   raw_carts = request.session.get('cart', [])
#   for item in raw_carts:
#       if item.product
  
  context = {'cart': products, 'total_price': total_price}
  return render(request, "store/checkoutpage.html", context)



#  if request.method == "POST":
#         if request.user.is_authenticated:
#             # Lấy thông tin giỏ hàng từ session
#             cart_items = request.session.get('cart', [])
#             for item in cart_items:
#                 prod_id = item['product_id']
#                 prod_qty = item['product_qty']
#                 product_check = Product.objects.filter(id=prod_id).first()
#                 if product_check:
#                     exist_cart_item = Cart.objects.filter(user=request.user, product_id=prod_id, product_qty=prod_qty).first()
#                     if exist_cart_item:
#                         new_qty = exist_cart_item.product_qty + prod_qty
#                         if product_check.quantity >= new_qty:
#                             exist_cart_item.product_qty = new_qty
#                             exist_cart_item.save()
#                         else:
#                             return JsonResponse({'status': "Updated Failed"})
#                     else:
#                         if product_check.quantity >= prod_qty:
#                             Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
#                         else:
#                             return JsonResponse({'status': "Only " + str(product_check.quantity) + " quantity available"})
#                 else:
#                     return JsonResponse({'status': "No such product found"})
#             # Xóa giỏ hàng từ session sau khi đã checkout xuống cơ sở dữ liệu
#             del request.session['cart']
#             return JsonResponse({'status': "Checkout successfully"})
#         else:
#             return JsonResponse({'status': "Login to continue"})
#     return redirect("/")


def placeorder(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Lấy thông tin từ form
            fname = request.POST.get('fname')
            flname = request.POST.get('flname')
            fcompany = request.POST.get('fcompany')
            faddress = request.POST.get('faddress')
            fTownCity = request.POST.get('fTownCity')
            fCountry = request.POST.get('fCountry')
            fPostcodeZip = request.POST.get('fPostcodeZip')
            fMobile = request.POST.get('fMobile')
            Email_filed = request.POST.get('Email_filed')
            order_note = request.POST.get('orderNote')
            payment_mode = request.POST.get('payment_mode')
            
            # Lấy thông tin giỏ hàng từ session
            cart_items = request.session.get('cart', [])
            order_total = 0  # Tổng giá trị của đơn hàng
            order_items = []  # Danh sách các OrderItems
            
            for item in cart_items:
                prod_id = item['product_id']
                prod_qty = item['product_qty']
                product_check = Product.objects.filter(id=prod_id).first()
                
                if product_check:
                    if product_check.quantity >= prod_qty:
                        order_total += product_check.selling_price * prod_qty
                        order_items.append({
                            'product': product_check,
                            'quantity': prod_qty,
                            'price': product_check.selling_price
                        })
                    else:
                        return JsonResponse({'status': "Only " + str(product_check.quantity) + " quantity available"})
                else:
                    return JsonResponse({'status': "No such product found"})
            
            # Tạo một đối tượng Order mới
            new_order = Order.objects.create(
                user=request.user,
                fname=fname,
                flname=flname,
                fcompany=fcompany,
                faddress=faddress,
                fTownCity=fTownCity,
                fCountry=fCountry,
                fPostcodeZip=fPostcodeZip,
                fMobile=fMobile,
                Email_filed=Email_filed,
                order_note=order_note,
                total_price=order_total,
                payment_mode=payment_mode
            )
            
            # Tạo các đối tượng OrderItems cho đơn hàng
            for item in order_items:
                OrderItems.objects.create(
                    order=new_order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                )
                
            # Xóa giỏ hàng từ session sau khi đã checkout xuống cơ sở dữ liệu
            del request.session['cart']
            messages.success(request,"Checkout Successfully")
        else:
            messages.error(request,"Login to Continue")
    return redirect("/")
