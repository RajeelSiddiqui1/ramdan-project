from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from user.models import Creator, Blog, BlogRead, Follow
from user.forms import COUNTRIES
from django.contrib.auth.hashers import check_password
from .forms import CreatorLoginForm, BlogForm, StoryForm, CreatorForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Story


def dashboard(request):
    creator_id = request.session.get('creator_id')
    if not request.session.get('creator_logged_in') or not creator_id:
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')

    creator = get_object_or_404(Creator, id=creator_id)

    blogs = Blog.objects.filter(author=creator, status='approved', is_deleted=False)

   
    context = {
        'creator': creator,
        'blogs': blogs,
        'title': 'Creator Dashboard',
        'creator_name': request.session.get('creator_name', 'Creator'),
        'creator_id': creator_id,  
    }
    return render(request, 'creator_dashboard.html', context)


def creator_login(request):
    if request.session.get('creator_logged_in') and request.session.get('creator_id'):
        messages.info(request, 'You are already logged in!')
        return redirect('creator_dashboard:dashboard')
    
    if request.method == 'POST':
        form = CreatorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            creator = Creator.objects.get(email=email)
            if check_password(password, creator.password):
                request.session['creator_logged_in'] = True
                request.session['creator_id'] = creator.id
                request.session['creator_name'] = creator.first_name
                request.session.set_expiry(3600)
                messages.success(request, 'Successfully logged in!')
                return redirect('creator_dashboard:dashboard')
            else:
                messages.error(request, 'Invalid password')
        else:
            messages.error(request, 'Please correct the form errors')
    else:
        form = CreatorLoginForm()
    context = {
        'form': form,
        'title': 'Creator Login'
    }
    return render(request, 'creator_login.html', context)


def creator_profile_edit(request, creator_id):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    try:
        creator = Creator.objects.get(id=request.session.get('creator_id'))
    except Creator.DoesNotExist:
        messages.error(request, 'Creator not found.')
        return redirect('creator_dashboard:creator_login')

    # Ensure user can only edit their own profile
    if str(creator.id) != str(creator_id):
        messages.error(request, 'You can only edit your own profile.')
        return redirect('creator_dashboard:dashboard')

    if request.method == "POST":
        form = CreatorForm(request.POST, request.FILES, instance=creator)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been updated successfully')
            return redirect('creator_dashboard:dashboard')
    else:
        form = CreatorForm(instance=creator)
    
    return render(request, 'edit_creator_profile.html', {'form': form})
         


def creator_logout(request):
    if 'creator_logged_in' in request.session:
        del request.session['creator_logged_in']
    if 'creator_id' in request.session:
        del request.session['creator_id']
    if 'creator_name' in request.session:
        del request.session['creator_name']
    messages.success(request, 'Successfully logged out')
    return redirect('creator_dashboard:creator_login')

def follower_list(request):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect(reverse_lazy('creator_dashboard:creator_login'))
    
    creator = get_object_or_404(Creator, id=request.session.get('creator_id'))
    followers = Follow.objects.filter(following=creator).select_related('follower')
    
    context = {'creator': creator, 'followers': followers}
    return render(request, 'follower_list.html', context)


def creator_blog_list(request):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    blogs = Blog.objects.filter(author=creator, status='approved', is_deleted=False)
    context = {
        'creator':creator,
        'blogs': blogs,
        'creator_name': request.session.get('creator_name', 'Creator'),
    }
    return render(request, 'creator_blog_list.html', context)


def creator_blog_detail(request, blog_id):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog_detail2.html', {'blog': blog,'creator':creator})


def creator_blog_create(request):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = creator
            blog.save()
            messages.success(request, 'Blog has been created successfully please wait for admin response')
            return redirect('creator_dashboard:blog_list2')
    else:
        form = BlogForm()
    return render(request, 'creator_blog_form2.html', {'form': form,'creator':creator})

def creator_blog_edit(request, blog_id):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = creator
            blog.status = 'pending'
            blog.save()
            messages.success(request, 'Blog has been updated successfully please wait for admin response')
            return redirect('creator_dashboard:blog_list2')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'creator_blog_form2.html', {'form': form,'creator':creator})

def creator_blog_delete(request, blog_id):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        blog.delete()
        messages.success(request, 'Blog has been deleted successfully')
        return redirect('creator_dashboard:blog_list2')
    return render(request, 'blog_confirm_delete2.html', {'blog': blog,'creator':creator})


def blog_views_check(request,blog_id):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    blog = get_object_or_404(Blog, pk=blog_id)
    views = BlogRead.objects.filter(blog=blog).order_by('-timestamp')
    return render(request, 'blog_views.html', {
        'creator':creator,
        'blog': blog,
        'views': views,
        'views_count': views.count()
    })


def creator_story_list(request):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    story = Story.objects.all()
    context = {
        'creator':creator,
        'story': story,
        'creator_name': request.session.get('creator_name', 'Creator'),
    }
    return render(request, 'stories.html', context)


def create_story(request):
    if not request.session.get('creator_logged_in') or not request.session.get('creator_id'):
        messages.warning(request, 'Your session has expired. Please login again.')
        return redirect('creator_dashboard:creator_login')
    
    creator = Creator.objects.get(id=request.session.get('creator_id'))
    if request.method == "POST":
        form = StoryForm(request.POST,request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.creator = creator
            story.save()
            messages.success(request, 'Blog has been created successfully')
            return redirect('creator_dashboard:stories')
        
        else:
             messages.success(request, 'Blog not created successfully')
             return redirect('creator_dashboard:stories')
    
    else:
        form = StoryForm()
    
    return render(request,'story_create.html',{'form':form})
