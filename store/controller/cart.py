from django.http import JsonResponse
from django.shortcuts import redirect,render
from django.contrib import messages
from store.models import Product, Cart
# def checkout(request):
#      if request.method=="POST":
#       if request.user.is_authenticated:
#          prod_id=int(request.POST.get('product_id'))
#          product_check=Product.objects.filter(id=prod_id).first()
#          if(product_check):
#            # if(Cart.objects.filter(user=request.user.id, product_id=prod_id)):
#             prod_qty=int(request.POST.get('product_qty'))
#             exist_cart_item=Cart.objects.filter(user=request.user, product_id=prod_id, product_qty=prod_qty)
#             if exist_cart_item:
#                new_qty=exist_cart_item.product_qty+prod_qty
#                if product_check.quantity>=new_qty:
#                    exist_cart_item.product_qty=new_qty
#                    exist_cart_item.save()
#                    return JsonResponse({'status':"Updated cart Successfully"})
#                else:
#                     return JsonResponse({'status':"Updated Failed"})
#             else:
#                 if product_check.quantity>=prod_qty:
#                     Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
#                     return JsonResponse({'status':"Product added successfully"})
#                 else:
#                     return JsonResponse({'status':"Only"+ str(product_check.quantity)+"quantity available"})
#          else:
#              return JsonResponse({'status':"No such product found"}) 
#       else:
#           return JsonResponse({'status':"Login to continue"})
    
#      return redirect("/")

def addtocart(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.filter(id=prod_id).first()
            
            if product_check:
                prod_qty = int(request.POST.get('product_qty'))
                prod_name=product_check.name
                cart_item = {'product_id': prod_id, 'product_qty': prod_qty, 'product_name':prod_name}
                
                # Lấy danh sách sản phẩm đã thêm vào giỏ hàng từ session
                cart = request.session.get('cart', [])
                
                # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng chưa
                found = False
                for item in cart:
                    if item['product_id'] == prod_id:
                        found = True
                        item['product_qty'] += prod_qty
                        if product_check.quantity < item['product_qty']:
                            return JsonResponse({'status': "Only" + str(product_check.quantity) + " quantity available"})
                        break
                
                # Nếu sản phẩm chưa tồn tại trong giỏ hàng, thêm mới vào
                if not found:
                    if product_check.quantity >= prod_qty:
                        cart.append(cart_item)
                    else:
                        return JsonResponse({'status': "Only" + str(product_check.quantity) + " quantity available"})
                
                # Lưu giỏ hàng vào session
                request.session['cart'] = cart
                return JsonResponse({'status': "Product added successfully"})
                
            else:
                return JsonResponse({'status': "No such product found"}) 
        else:
            return JsonResponse({'status': "Login to continue"})
    
    return redirect("/")

def viewcart(request):
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
    
    context = {'cart': products, 'total_price': total_price}
    return render(request, "store/cart.html", context)

def deletecartitem(request):
 
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')  
            if prod_id is not None and prod_id != '':
                try:
                    # Lấy danh sách sản phẩm đã thêm vào giỏ hàng từ session
                    cart = request.session.get('cart', [])

                    # Tìm kiếm sản phẩm cần xóa trong giỏ hàng dựa trên product_id
                    for item in cart:
                        if item['product_id'] == int(prod_id):
                            # Xóa sản phẩm khỏi giỏ hàng
                            cart.remove(item)
                            # Cập nhật giỏ hàng trong session
                            request.session['cart'] = cart
                            return JsonResponse({'status': "Product removed successfully"})
                    
                    # Nếu không tìm thấy sản phẩm trong giỏ hàng
                    return JsonResponse({'status': "Product not found in the cart"})
                    
                except ValueError:
                    return JsonResponse({'status': "Invalid product ID"})
            else:
                return JsonResponse({'status': "Invalid product ID"})
        else:
            return JsonResponse({'status': "Login to continue"})

    return JsonResponse({'status': "Invalid request"})

def updatecart(request):
   if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            new_qty = request.POST.get('product_qty')

            if prod_id is not None and new_qty is not None:
                try:
                    prod_id = int(prod_id)
                    new_qty = int(new_qty)

                    cart = request.session.get('cart', [])
                    found = False
                    for item in cart:
                        if item['product_id'] == prod_id:
                            found = True
                            product_check = Product.objects.filter(id=prod_id).first()
                            if product_check:
                                if new_qty <= product_check.quantity:
                                    item['product_qty'] = new_qty
                                    request.session['cart'] = cart
                                    return JsonResponse({'status': "Cart updated successfully"})
                                else:
                                    return JsonResponse({'status': "Only " + str(product_check.quantity) + " quantity available"})
                            else:
                                return JsonResponse({'status': "No such product found"})
                    
                    if not found:
                        return JsonResponse({'status': "Product not found in the cart"})
                except ValueError:
                    return JsonResponse({'status': "Invalid product ID or quantity"})
            else:
                return JsonResponse({'status': "Invalid product ID or quantity"})
        else:
            return JsonResponse({'status': "Login to continue"})
   else:
        return JsonResponse({'status': "Invalid request"})
    
    

def checkout(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # Lấy thông tin giỏ hàng từ session
            cart_items = request.session.get('cart', [])
            for item in cart_items:
                prod_id = item['product_id']
                prod_qty = item['product_qty']
                product_check = Product.objects.filter(id=prod_id).first()
                if product_check:
                    exist_cart_item = Cart.objects.filter(user=request.user, product_id=prod_id, product_qty=prod_qty).first()
                    if exist_cart_item:
                        new_qty = exist_cart_item.product_qty + prod_qty
                        if product_check.quantity >= new_qty:
                            exist_cart_item.product_qty = new_qty
                            exist_cart_item.save()
                        else:
                            return JsonResponse({'status': "Updated Failed"})
                    else:
                        if product_check.quantity >= prod_qty:
                            Cart.objects.create(user=request.user, product_id=prod_id, product_qty=prod_qty)
                        else:
                            return JsonResponse({'status': "Only " + str(product_check.quantity) + " quantity available"})
                else:
                    return JsonResponse({'status': "No such product found"})
            # Xóa giỏ hàng từ session sau khi đã checkout xuống cơ sở dữ liệu
            del request.session['cart']
            return JsonResponse({'status': "Checkout successfully"})
        else:
            return JsonResponse({'status': "Login to continue"})
    return redirect("/")

    
    