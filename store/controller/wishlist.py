from django.http import JsonResponse
from django.shortcuts import redirect,render, get_object_or_404
from django.contrib import messages
from store.models import Wishlist,Product,Category
def index(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    context={'wishlist':wishlist}
    return render(request,'store/wishlist.html',context)

def add_to_wishlist(request,product_id):
   if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        wishlist_item = Wishlist(user=request.user, product=product)
        wishlist_item.save()
        return redirect('/')

def remove_to_wishlist(request, product_id):
      if request.method == 'POST':
          if request.user.is_authenticated:
        # Lấy tất cả các mục trong danh sách mong muốn của người dùng cho sản phẩm này
           wishlist_items = Wishlist.objects.filter(user=request.user, product_id=product_id)
        
        # Kiểm tra xem có bất kỳ mục nào trong danh sách không
           if wishlist_items.exists():
            # Nếu có, xóa tất cả chúng
            wishlist_items.delete()
            return JsonResponse({'message': 'All items removed from wishlist'}, status=200)
          else:
            # Nếu không có mục nào, trả về một thông báo lỗi
            return JsonResponse({'error': 'Item not found in wishlist'}, status=404)
      else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)