from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .forms import SignupForm, LoginForm, EditProfileForm, BlogForm, CreatorForm, CreatorLoginForm, ContactUsForm
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Blog, BlogRead, Creator, Follow, Categories, ContactUs, SimpleUser, BlogLike
from django.db.models import Q,F, Count
from admin_side.models import BlogCountry
from django.http import HttpResponse
from django.views.decorators.http import require_POST

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                print("DEBUG: Authentication failed")  # Debug message
                messages.error(request, 'Invalid credentials')
                return redirect('login')
            
            if user.is_staff or user.is_superuser:
                messages.error(request, 'Admin users cannot login here')
                return redirect('login')

            print(f"DEBUG: User {user.username} authenticated successfully")  # Debug message
            auth_login(request, user)
            return redirect('index')
    
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

  


def edit_profile(request):  
     if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_profile')
     else:
        form = EditProfileForm(instance=request.user)
     return render(request, 'edit_profile.html', {'form': form})

def logout(request):
   request.session.flush()
   return redirect('index')


   
def home_page(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category','')
    blogs = Blog.objects.filter(is_deleted=False).annotate(like_count=Count('likes'))
    categories = Categories.objects.all()

    if query:
        blogs = Blog.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query),
            is_deleted=False
        ).distinct()

    if category_id:
        blogs = blogs.filter(category__id=category_id)
  

    if request.user.is_authenticated:
        liked_blogs = BlogLike.objects.filter(user=request.user).values_list('blog_id',flat=True)
        for blog in blogs:
            blog.is_liked = blog.id in liked_blogs

    else:
        for blog in blogs:
            blog.is_liked = False        


    context = {
        'query': query,
        'blogs': blogs,
        'categories': categories,
        'selected_category': category_id,
    }          

    return render(request, 'index.html',context )
    
    # return redirect('login')


@login_required
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, is_deleted=False)
    related_blogs = Blog.objects.filter(category=blog.category, is_deleted=False).exclude(id=blog.id)[:5]

    if not BlogRead.objects.filter(user=request.user, blog=blog).exists():
        BlogRead.objects.create(user=request.user, blog=blog)
        Blog.objects.filter(id=blog.id).update(views_count=F('views_count') + 1)


    is_liked = BlogLike.objects.filter(blog=blog, user=request.user).exists()
    like_count = BlogLike.objects.filter(blog=blog).count()

    return render(request, "detail.html", {'blog': blog, 'related_blogs': related_blogs,'is_liked': is_liked,'like_count': like_count,})


def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.name = request.user
            blog.save()
            return redirect('index')
        
    else:
        form = BlogForm()
    return render(request,'blog_form.html',{'form':form})    


@require_POST
@login_required
def toggle_like(request, blog_id):
    try:
        blog = get_object_or_404(Blog, pk=blog_id)
        user = request.user

        like, created = BlogLike.objects.get_or_create(blog=blog, user=user)

        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True
        
        return JsonResponse({
            'success': True,
            'is_liked': is_liked,
            'message': 'Like status updated successfully'
        })
    except Exception as e:
        print(f"Error in toggle_like: {str(e)}") 
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)



def content_creator_page(request):
    con = BlogCountry.objects.all()
    return render(request,'content_creator_page.html',{'con':con})
  

def content_creator_form(request):
    if request.method == "POST":
        form = CreatorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks for your submission!')  
            return redirect('creator_login') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CreatorForm()

    return render(request, 'content_creator_form.html', {'form': form}) 





def creator_login(request):
    # Check if already logged in
    # if request.session.get('admin_logged_in', False):
    #     return redirect('')  
    
    if request.method == 'POST':
        form = CreatorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                creator = Creator.objects.get(email=email)
                if check_password(password, creator.password):
                    # Set session variables
                    request.session['admin_logged_in'] = True
                    request.session['creator_id'] = creator.id 
                    request.session['creator_name'] = creator.first_name
                    request.session.set_expiry(3600) 
                    
                    messages.success(request, 'Successfully logged in!')
                    return redirect('index')  
                else:
                    messages.error(request, 'Invalid password')
            except Creator.DoesNotExist:
                messages.error(request, 'Email not found')
        else:
            messages.error(request, 'Please correct the form errors')
    else:
        form = CreatorLoginForm()

    context = {
        'form': form,
        'title': 'Creator Login'
    }
    return render(request, 'creator_login.html', context)

def creator_logout(request):
    request.session.flush()
    messages.success(request, 'Successfully logged out')
    return redirect('creator_login')

@login_required
def creator_profile(request, creator_id):
    creator = get_object_or_404(Creator, id=creator_id)
    blogs = Blog.objects.filter(author=creator, status='approved', is_deleted=False)
    
    # Check if current user is following this creator
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=creator
        ).exists()
    
    context = {
        'creator': creator,
        'blogs': blogs,
        'is_following': is_following,
        'followers_count': creator.followers.count(),
        'blog_count': blogs.count(),
    }
    return render(request, 'creator_profile.html', context)

# follow button 
@login_required
def toggle_follow(request,creator_id):
    if request.method == "POST":
        creator = get_object_or_404(Creator, pk=creator_id)
        user = request.user

        follow_exists = Follow.objects.filter(follower=user, following=creator).exists()

        if follow_exists:
            Follow.objects.filter(follower=user, following=creator).delete()
            is_following = False
            messages.success(request, f"You have unfollowed {creator.first_name}")
        
        else:
            Follow.objects.create(follower=user, following=creator)
            is_following = True
            messages.success(request, f"You are now following {creator.first_name}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'is_following': is_following,
                'followers_count': creator.followers.count()
            })
        return redirect('creator_profile', creator_id=creator.id)
    

def creator_list(request):
    query = request.GET.get('q', '')
    creators = Creator.objects.all().prefetch_related('followers')

    if query:
        creators = Creator.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(country__icontains=query) |
            Q(email__icontains=query),
           
        ).distinct()
        
    
    return render(request,'creator_list.html',{'creators':creators,'query':query})    

@login_required
def about_us(request):
    return render(request,'about_us.html')

@login_required
def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request,'Your problem has been send')
            return redirect('contact_us')
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ContactUsForm()    

    return render(request,'contact_us.html',{'form':form})




@login_required
def contact_us_list(request):
    contact = ContactUs.objects.filter(user=request.user)
    return render(request, 'contact_us_list.html', {'contact': contact})


@login_required
def contact_us_delete(request, contact_id):
    contact = get_object_or_404(ContactUs, pk=contact_id)
    if request.method == "POST":
        contact.delete()
        messages.success(request, 'Contact problem was deleted successfully')
        return redirect('contact_us_list')
    return render(request,'contact_confirm_delete.html',{'contact':contact})


@login_required
def following_list(request):
    following = Follow.objects.filter(follower=request.user).select_related('following')
    return render(request, 'following_list.html',{'following':following})

@login_required
def unfollow_creator(request,creator_id):
    creator = get_object_or_404(Creator, id=creator_id)
    Follow.objects.filter(follower=request.user, following_id=creator_id).delete()
    messages.success(request, f'You unfollow {creator.first_name}{creator.last_name} ')
    return redirect('following_list')


