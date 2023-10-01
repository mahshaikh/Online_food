from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User,UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from .utils import detectUser


def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are all ready logged in')
        return redirect('dashboard')
    elif request.method == 'POST':
        print(request.POST)
        form=UserForm(request.POST)
        if form.is_valid():
            #create the user using the form
            #password=form.cleaned_data['password']
            #user=form.save(commit=False)
            #user.set_password(password)
            #user.role=User.CUSTOMER
            #user.save()

            # create the user using another method create_user
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']

            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=user.CUSTOMER
            user.save()
            messages.success(request,'your account register successfully')
            return redirect('registerUser')
        else:
            print("User is invalid")
            print("form.errors")


    else:
        form=UserForm()
    context={
           'form':form,
    }
    return render(request,'accounts/registerUser.html',context)

def registervendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are all ready logged in')
        return redirect('my_Account')
    elif request.method == 'POST':
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)

        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,'your account has been registered successfully plz wait for the approval')
            return redirect('registerVendor')
        else:
            print("invaild")
            print(form.errors)


    else:
        form=UserForm()
        v_form=VendorForm()
    context={
        'form':form,
        'v_form':v_form,
    }
    return render(request,'accounts/registerVendor.html',context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'you are all ready logged in')
        return redirect('my_Account')

    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
       
        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are now logged in')
            return redirect('my_Account')

        else:
            messages.error(request,"invaild login user")
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"you are logout")
    return redirect('login')

@login_required(login_url='login')
def my_Account(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')