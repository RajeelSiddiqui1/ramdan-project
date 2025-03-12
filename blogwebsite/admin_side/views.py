# admin_side/views.py
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import LoginForm, StaffForm, StaffEditForm,CategoryForm,BlogForm,BlogStatusForm,BlogCountryForm
from .models import Admin, Staff, BlogCountry
from user.models import Categories,Blog,SimpleUser, Creator

def dashboard(request):
    # Redirect to admin_login if neither admin nor staff is logged in
    if not (request.session.get('admin_logged_in', False) ):
        return redirect('admin_side:admin_login')
    context = {
        'title': 'Dashboard',
        'admin_name': request.session.get('admin_name', ''),
        'admin_email': request.session.get('admin_email', ''),
    }
    return render(request, 'dashboard.html',context)

def admin_login(request):
   
    if request.session.get('admin_logged_in', False):
        return redirect('admin_side:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                admin = Admin.objects.get(email=email)
                if check_password(password, admin.password):
                    request.session['admin_logged_in'] = True
                    request.session['admin_name'] = admin.name
                    return redirect('admin_side:dashboard')
                messages.error(request, 'Invalid credentials')
            except Admin.DoesNotExist:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'admin_login.html', {'form': form})

def admin_logout(request):
    request.session.flush()
    return redirect('admin_side:admin_login')

def staff_login(request):
    # If staff is already logged in, go to dashboard
    if request.session.get('staff_logged_in', False):
        return redirect('admin_side:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                staff = Staff.objects.get(email=email)
                if check_password(password, staff.password):
                    request.session['staff_logged_in'] = True
                    request.session['staff_id'] = staff.id
                    return redirect('admin_side:dashboard')
                messages.error(request, 'Invalid credentials')
            except Staff.DoesNotExist:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'staff_login.html', {'form': form})

def staff_list(request):
    if not (request.session.get('admin_logged_in', False)):
        return redirect('admin_side:admin_login')
    
    staff = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff': staff})

def staff_create(request):
    # Only admins can create staff, so check admin_logged_in only
    if not request.session.get('admin_logged_in', False):
        return redirect('admin_side:admin_login')
    
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member created successfully')
            return redirect('admin_side:staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form})

def staff_edit(request, staff_id):
    if not request.session.get('admin_logged_in', False):
        return redirect('admin_side:admin_login')
    
    staff = get_object_or_404(Staff, pk=staff_id)
    
    if request.method == "POST":
        form = StaffEditForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member updated successfully')
            return redirect('admin_side:staff_list')
    else:
        form = StaffEditForm(instance=staff)
    
    context = {
        'form': form,
        'title': 'Edit Staff',
        'admin_name': request.session.get('admin_name', ''),
        'admin_email': request.session.get('admin_email', ''),
        'staff': staff  # Add staff object to access current image
    }
    return render(request, 'staff_form.html', context)

def staff_delete (request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    if request.method == "POST":
        staff.delete()
        messages.success(request, 'Staff member deleted successfully')
        return redirect('admin_side:staff_list')
    return render(request,'staff_confirm_delete.html',{'staff':staff})


def category_list(request):
    cat = Categories.objects.all()
    return render(request,'category_list.html',{'cat':cat})


def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            if Categories.objects.filter(name=category_name).exists():
                messages.warning(request, 'Category already exists')
                return redirect('admin_side:category_form')
            
            form.save()
            messages.success(request,'Category Created Successfully')
            return redirect('admin_side:category_list')
        else:
            messages.warning(request,'Category was not Created ')
            return redirect('admin_side:category_form')

    else:  
        form = CategoryForm()

    return render(request,'category_form.html',{'form':form}) 


def category_edit(request, cat_id):
    check = get_object_or_404(Categories, pk=cat_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=check)
        if form.is_valid():
            form.save()
            messages.success(request,'Category Edit Successfully')
            return redirect('admin_side:category_list')
        else:
            messages.warning(request,'Something went Wrong!!!')   
            return redirect('admin_side:category_form') 
    else:
        form = CategoryForm(instance=check)

    return render(request,'category_form.html',{'form':form})    


def category_delete(request, cat_id):
    cat = get_object_or_404(Categories, pk=cat_id)
    if request.method == "POST":
        cat.delete()
        messages.success(request, 'Category deleted successfully')
        return redirect('admin_side:category_list') 
    
    return render(request,'category_confirm_delete.html',{'cat':cat})
    


def blog_list(request):
    blogs = Blog.objects.filter(status='approved', is_deleted=False)
    return render(request, 'blog_list.html', {'blogs': blogs})


def admin_blog_published(request):
    blogs = Blog.objects.filter(is_deleted=False)
    status_form = BlogStatusForm()
    
    if request.method == "POST":
        status_form = BlogStatusForm(request.POST)
        if status_form.is_valid():
            action = status_form.cleaned_data['action']
            blog_id = request.POST.get('blog_id')
            if not blog_id:
                messages.error(request, 'No blog selected')
                return redirect('admin_side:admin_blog_published')
            blog = get_object_or_404(Blog, pk=blog_id)  # Consider adding author/Admin filter if needed
            if action == 'delete':
                blog.is_deleted = True
                blog.save()
                messages.success(request, 'Blog has been deleted')
            else:
                blog.status = action
                blog.save()
                messages.success(request, f'Blog status updated to {action}')
            return redirect('admin_side:admin_blog_published')
    
    return render(request, 'admin_blog_published.html', {
        'blogs': blogs,
        'status_form': status_form,
    })
            

def blog_detail(request,blog_id):
    blog = get_object_or_404(Blog,pk=blog_id)
    return render(request,'blog_detail.html',{'blog':blog})            

def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            messages.success(request, 'Blog has been created successfully')
            return redirect('admin_side:blog_list')
    else:
        form = BlogForm()
    return render(request, 'admin_blog_form.html', {'form': form})

def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id) 
        
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid(): 
            blog = form.save(commit=False) 
            blog.save()
            messages.success(request, 'Blog has been updated successfully')
            return redirect('admin_side:blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'admin_blog_form.html', {'form': form})


def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        blog.delete()
        messages.success(request, 'Blog has been deleted successfully')
        return redirect('admin_side:blog_list')
    return render(request, 'blog_confirm_delete.html', {'blog': blog})


def user_list(request):
    users = SimpleUser.objects.all()
    return render(request,'user_list.html',{'users':users})


def country_list(request):
    con = BlogCountry.objects.all()
    return render(request,'country_list.html',{'con':con})


def country_list(request):
    con = BlogCountry.objects.all()
    return render(request, 'country_list.html', {'con': con})


def country_create(request):
    if request.method == "POST":
        form = BlogCountryForm(request.POST, request.FILES)
        if form.is_valid():
            con = form.save(commit=False)
            con.save()
            messages.success(request, 'Country has been uploaded successfully')
            return redirect('admin_side:country_list')
    else:
        form = BlogCountryForm()  # ✅ Fixed form

    return render(request, 'country_form.html', {'form': form})


def country_edit(request, con_id):
    con = get_object_or_404(BlogCountry, pk=con_id)  # ✅ Fixed model reference

    if request.method == "POST":
        form = BlogCountryForm(request.POST, request.FILES, instance=con)
        if form.is_valid():
            con = form.save(commit=False)
            con.save()
            messages.success(request, 'Country has been updated successfully')
            return redirect('admin_side:country_list')
    else:
        form = BlogCountryForm(instance=con)  # ✅ Fixed form

    return render(request, 'country_form.html', {'form': form})


def country_delete(request, con_id):
    con = get_object_or_404(BlogCountry, pk=con_id)  # ✅ Fixed model reference
    if request.method == "POST":
        con.delete()
        messages.success(request, 'Country has been deleted successfully')
        return redirect('admin_side:country_list')  # ✅ Fixed redirect

    return render(request, 'country_confirm_delete.html', {'blog': con})


def creator_list(request):
    cat = Creator.objects.all()
    return render(request,'creator_list.html',{'cat':cat})