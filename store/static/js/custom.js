$(document).ready(function(){
  $('.btn-plus').click(function(e){
    e.preventDefault();
    var row = $(this).closest('.product_data'); // Lấy hàng chứa nút đã nhấn
    var inc_value = row.find('.qty-input').val(); // Lấy giá trị số lượng từ ô nhập liệu tương ứng
    var value = parseInt(inc_value, 10); // Chuyển đổi giá trị thành số nguyên
    value = isNaN(value) ? 0 : value; // Kiểm tra nếu giá trị là NaN, gán giá trị mặc định là 0
    if (value < 10){
        value++; // Tăng giá trị lên 1
        row.find('.qty-input').val(value); // Cập nhật giá trị số lượng trong ô nhập liệu
    }
  });

  $('.btn-minus').click(function(e){
    e.preventDefault();
    var row = $(this).closest('.product_data'); // Lấy hàng chứa nút đã nhấn
    var dec_value = row.find('.qty-input').val(); // Lấy giá trị số lượng từ ô nhập liệu tương ứng
    var value = parseInt(dec_value, 10); // Chuyển đổi giá trị thành số nguyên
    value = isNaN(value) ? 0 : value; // Kiểm tra nếu giá trị là NaN, gán giá trị mặc định là 0
    if (value > 1){
        value--; // Giảm giá trị đi 1
        row.find('.qty-input').val(value); // Cậ
    }
});

$('.addtoCartBtn').click(function(e){
    e.preventDefault();
    var product_id=$(this).closest('.product_data').find('.prod_id').val();
    var product_qty=$(this).closest('.product_data').find('.qty-input').val();
    var product_name=$(this).closest('.product_data').find('.prod_name').val();
    var token=$('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
      method:"POST",
      url:"/add-to-cart",
      data:{
        'product_id':product_id,
        'product_qty':product_qty,
        'product_name':product_name,
        csrfmiddlewaretoken:token
      },
  
      success:function(response){
    
         console.log(product_id)
         console.log(product_qty)
         alertify.success(response.status)
      }
    });
});

 $('.delete-cart-item').click(function(e){
   e.preventDefault();
   //var product_id=$(this).closest('.product_data').find('.prod_id').val();
// var product_qty=$(this).closest('.product_data').find('.prod-qty').val();
var product_id=$(this).attr('data-item') ;
var product_name=$(this).closest('.product_data').find('.prod-name').data('product-name');
   var token=$('input[name=csrfmiddlewaretoken]').val();
   $.ajax({
     type:"POST",
     url:"/delete-cart-item",
     data:{
      'product_id':product_id,
      'product_name':product_name,
      csrfmiddlewaretoken:token
     },
     success:function(response){
      console.log(product_name)
      alertify.success(response.status)
      $('.cartdata').load(location.href+".cartdata");
      
     }
   });
 });


 $('.changeQuantity').click(function(e){
  e.preventDefault();
  var product_id=$(this).attr('data-item');
  var product_qty=$(this).closest('tr').find('.qty-input').val();
  var product_name=$(this).closest('.product_data').find('.prod-name').data('product-name');
  var token=$('input[name=csrfmiddlewaretoken]').val();
  $.ajax({
    method:"POST",
    url:"/update-cart",
    data:{
      'product_id':product_id,
      'product_qty':product_qty,
      'product_name':product_name,
      csrfmiddlewaretoken:token
    },


    success:function(response){
       console.log(response)
       console.log(product_id)
       console.log(product_qty)
       console.log(product_name)
       alertify.success(response.status)
       $('.cartdata').load(location.href+".cartdata");
    }
  });
});


  // Xử lý sự kiện khi nhấn nút "Checkout"
  $('#checkout-btn').click(function(e){
      e.preventDefault();
      var confirmation = confirm("Are you sure you want to proceed to checkout?");
      if (confirmation) {
          // Gửi yêu cầu đến view checkout bằng Ajax
          $.ajax({
              type: "POST",
              url: "/checkout",
              data: {
                  csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
              },
              success: function(response) {
                alertify.success(response.status)
                  // Sau khi checkout thành công, chuyển hướng người dùng đến trang khác hoặc làm gì đó khác tùy theo yêu cầu
                  $('.cartdata').load(location.href+".cartdata"); // Ví dụ: chuyển hướng đến trang "checkout/success" nếu checkout thành công
              }
          });
      }
  });


 
});