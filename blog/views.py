from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from .forms import UserRegisterForm
from .forms import UserLoginForm, ChangeForm, EditUserProfileForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .models import Post, Comment
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.views import generic
from django.urls import reverse_lazy
# Create your views here.


class Index(ListView):
    model = Post
    queryset = Post.objects.filter(statue= Post.Status.PUBLISHED).order_by('-publish_date')
    template_name = 'blog/index.html'
    paginate_by = 3


class ViewDraftPosts(ListView):
    model = Post
    queryset = Post.objects.filter(statue= Post.Status.DRAFT).order_by('-publish_date')
    template_name = 'blog/index.html'
    paginate_by = 3


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = get_object_or_404(
                User, username=form.cleaned_data['username'])
            user.first_name = form['first'].value()
            user.last_name = form['last'].value()
            if form.cleaned_data['is_superuser'] == True:
                group = get_object_or_404(Group, name="Admin-Group")
                user.groups.add(group)
                user.is_staff = True
                user.save()
            elif form.cleaned_data['is_staff'] == True:
                group = get_object_or_404(Group, name='Editor-Group')
                user.groups.add(group)
                user.save()
            else:
                group = get_object_or_404(Group, name='User-Group')
                user.groups.add(group)
                user.save()
            messages.success(
                request, "Your are signed up successfully")
            user = authenticate(
                request, username=f"{form['username'].value()}", password=f"{form['password1'].value()}")
            login(request, user)
            return redirect('profile', form['username'].value())
        else:
            messages.error(
                request, "Wrong input data please re enter it.")
            return redirect('register')


class loginView (View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        print(request.user)
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username = f"{form.cleaned_data['username']}"
            password = f"{form.cleaned_data['password']}"
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                return redirect('profile', form['username'].value())
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
        return render(request, 'blog/create.html')

    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        group_user = get_object_or_404(Group, name="User-Group")

        if not user.groups.filter(name=group_user).exists():
            title = request.POST['title']
            status = request.POST['status']
            content = request.POST['content']
            category = request.POST['categories']
            Post.objects.create(title=title, statue=status,categories=category,
                                content=content, owner=request.user)
            return redirect('index')
        else:
            return redirect('index')


class DetailPostView(DetailView):

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        comments = Comment.objects.filter(post=post).order_by('-publish_data')
        return render(request, 'blog/blog_post.html', {'comments': comments, 'post': post})

    def post(self, request, pk):
        Comment.objects.create(
            post_id=pk, comment_content=request.POST['comment_field'], user_id=request.user.id)
        return redirect('detail_post', pk)


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
        posts = Post.objects.filter(owner_id=request.user.id)
        return render(request, 'users/profile.html', {'user': request.user, 'posts': posts})


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


class deletePost (View):
    pass


class editPost (View):
    pass


class like (View):
    def get(self, request):
        return redirect(request.META.get('HTTP_REFERER'))


def admin(request):
    return redirect('/admin/auth/user')
