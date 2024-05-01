from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.http import HttpResponse
from django.contrib import messages
from store.form   import CustomerUserForm
def register(request):
    form=CustomerUserForm()
    if request.method=='POST':
       form=CustomerUserForm(request.POST)
       if(form.is_valid):
           form.save()
           messages.success(request,"Register Successful")
           return redirect("/login")
    context={'form':form}
    return render(request,"store/auth/register.html", context)


def loginpage(request):
   if request.user.is_authenticated:
       messages.warning(request,"You are already logged in")
       return redirect("/")
   else:
       if request.method=='POST':
          username=request.POST.get('username')
          pwd=request.POST.get('password')
          user=authenticate(request, username=username, password=pwd)
          if user is not None:
              login(request,user)
              messages.success(request,"Login is Successfully")
              return redirect("/")
          else:
            messages.error(request,"Invalid UserName or Password")
            return("/login")
       return render(request,"store/auth/login.html")
   
def logoutpage(request):
    if request.user.is_authenticated:
       logout(request)
       messages.success(request,"Logged out Successfully")
    return redirect("/")

