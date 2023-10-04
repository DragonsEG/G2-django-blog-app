from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import *
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.generic import DetailView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views import generic
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Create your views here.


class Index(View):
    def get(self, request):
        post = Post.objects.none()
        is_category_selected = 0
        categoriesToCheck = categories.objects.all()
        for category in categoriesToCheck:
            if (category.checked):
                is_category_selected = 1
                post |= Post.objects.all().filter(categories=category)

        if (is_category_selected == 0):
            post = Post.objects.all().filter(
                statue=Post.Status.PUBLISHED).order_by('-publish_date')

        post = post.order_by('-publish_date')
        paginate = Paginator(post, 3)
        page_num = request.GET.get('page')
        page = paginate.get_page(page_num)
        return render(request, 'blog/index.html', {'page': page, 'categories': categoriesToCheck})

    def post(self, request):
        categoriesToCheck = categories.objects.all()
        for category in categoriesToCheck:
            if (request.POST.get(category.name)):
                category.checked = True
                category.save()
            else:
                category.checked = False
                category.save()

        return redirect('index')


class RegisterView(View):
    def get(self, request):
        form = None
        if (request.GET.get('status') == 'company'):
            form = CompanyRegistration()
        else:
            form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form, 'status': request.GET.get('status')})

    def post(self, request):
        filterData = request.POST.copy()
        is_company = filterData['data'] == 'company'
        del filterData['data']
        if (is_company):
            form = CompanyRegistration(filterData)
        else:
            form = UserRegisterForm(filterData)
        if form.is_valid():
            if (is_company):
                company.objects.create(
                    name=form['username'].value(), mail=form['email'].value())
                form.save()
                user = authenticate(
                    request, username=f"{form['username'].value()}", password=f"{form['password1'].value()}")
                login(request, user)
                group = get_object_or_404(Group, name='Company')
                user.groups.add(group)
                user.save()
            else:
                form.save()
                user = get_object_or_404(
                    User, username=form.cleaned_data['username'])
                user.first_name = form['first'].value()
                user.last_name = form['last'].value()
                group = ""
                if form.cleaned_data['is_superuser'] == True:
                    group = get_object_or_404(Group, name="Admin-Group")
                    user.is_staff = True
                else:
                    group = get_object_or_404(Group, name='User-Group')

                user.groups.add(group)
                user.save()
                user = authenticate(
                    request, username=f"{form['username'].value()}", password=f"{form['password1'].value()}")
                login(request, user)
            messages.success(
                request, "Your are signed up successfully")
            return redirect('profile', user=user.username)
        else:
            messages.error(
                request, "Wrong input data please re enter it.")
            return JsonResponse({"message": "wrong"})


class loginView (View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = f"{form.cleaned_data['username']}"
            password = f"{form.cleaned_data['password']}"
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile', user=user.username)
            else:
                messages.error(
                    request, 'Invalid username or password.')
                return redirect('login')
        else:
            messages.error(
                request, "Wrong input data please re enter it.")
            return redirect('login')


class createView (View):
    def get(self, request):
        category = categories.objects.all()
        return render(request, 'blog/create.html', {'categories': category})

    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        group_user = get_object_or_404(Group, name="User-Group")
        if not user.groups.filter(name=group_user).exists():
            title = request.POST['title']
            status = request.POST['status']
            content = request.POST['content']
            category = get_object_or_404(
                categories, name=request.POST['categories'])
            post = Post()
            post.title = title
            post.statue = status
            post.content = content
            post.owner = request.user
            post.save()
            post.categories.add(category)
            post.save()
            return redirect('index')
        else:
            return redirect('index')


class DetailPostView(DetailView):

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comments = Comment.objects.filter(post=post).order_by('-publish_data')
        return render(request, 'blog/blog_post.html', {'comments': comments, 'post': post, 'id': pk})

    def post(self, request, pk):
        # this is wrong we have to make if only when it comes from comment button because we are going to to add like button
        if (request.POST.get('want') == 'comment'):
            Comment.objects.create(
                post_id=pk, comment_content=request.POST.get('data'), user_id=request.user.id)
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'fail'})


def deleteAccount(request, user):
    if request.method == 'GET':
        logout(request)
        get_object_or_404(User, username=user).delete()
        return redirect('index')
    else:
        return HttpResponse('Bad request')


class changePass (PasswordChangeView):
    def get(self, request):
        form = ChangeForm
        return render(request, 'blog/change password.html', {'form': form})

    def post(self, request):
        form = ChangeForm(request.POST)
        if (form.is_valid()):
            if check_password(form['old_password'].value(), request.user.password) and (form['new_password1'].value() == form['new_password2'].value()):

                request.user.set_password(form['new_password1'].value())
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(
                    request, "Your password changed")
                return redirect('profile', request.user)
            else:
                messages.error(
                    request, "Wrong input data")
                return redirect('changepassword')
        else:
            messages.error(
                request, "Wrong input data")
        return redirect('changepassword')


class profileView (View):
    def get(self, request, user):
        # Retrieve all posts by the user
        currentUser = get_object_or_404(User, username=user)
        if (currentUser.id != request.user.id):
            if (request.GET.get('status') == 'draft'):
                return HttpResponseForbidden()
        posts = Post.objects.filter(
            owner=currentUser.id).order_by('-publish_date')

        # Check if 'status' parameter is passed in the request
        status_param = request.GET.get('status', None)

        # Initialize current_state with a default value of "published"
        # Default to "published" if no status parameter is provided
        current_state = "published"

        if status_param == 'draft':
            posts = posts.filter(statue=Post.Status.DRAFT)
            current_state = "draft"
        else:
            posts = posts.filter(statue=Post.Status.PUBLISHED)
            current_state = "published"

        return render(request, 'users/profile.html', {'currentUser': currentUser, 'posts': posts, 'current_state': current_state})


class PostEditView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk, owner=request.user)
        return render(request, 'blog/edit_post.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk, owner=request.user)
        title = request.POST['title']
        status = request.POST['status']
        content = request.POST['content']
        category = request.POST['categories']
        post.title = title
        post.statue = status
        post.categories = category
        post.content = content
        post.save()
        return redirect('index')


class PostDeleteView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk, owner=request.user)
        return render(request, 'blog/delete_post.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk, owner=request.user)
        post.delete()
        return redirect('index')


class EditUserProfileView(generic.UpdateView):
    form_class = EditUserProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user


def admin(request):
    return redirect('/admin/auth/user')


class like (View):
    def get(self, request):
        return redirect(request.META.get('HTTP_REFERER'))


def acceptWriter(request, user):
    pass


def rejectWriter(request, user):
    pass


def editComment():
    pass


def deleteComment():
    pass


def addCategory(request):
    if request.method == 'POST':
        categories.objects.create(name=request.POST.get('category'))
        return JsonResponse({'message': 'success'})
    else:
        return HttpResponseForbidden()
