from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from .forms import UserLoginForm , ChangeForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView 
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout , login , authenticate
from django.contrib import messages
from .models import Post, Comment
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
# Create your views here.


class Index(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-publish_date')
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
            user = get_object_or_404(User,username=form.cleaned_data['username'])
            if form.cleaned_data['is_superuser'] == True:
                group = get_object_or_404(Group, name="Admin-Group")
                user.groups.add(group)
                user.save()
            elif form.cleaned_data['is_staff'] == True: 
                group = get_object_or_404(Group,name='Editor-Group')
                user.groups.add(group)
                user.save()
            else:
                group = get_object_or_404(Group,name='User-Group')
                user.groups.add(group)
                user.save()
            messages.success(
                request, "Your are signed up successfully")
            user = authenticate(request, username=f"{form['username'].value()}", password=f"{form['password1'].value()}")
            login(request , user)
            return redirect('profile' ,form['username'].value())
        else:
            messages.error(
                request, "Wrong input data please re enter it.")
            return redirect('register')

class loginView (View) :
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            if (User.objects.all().filter(username=form['username'].value()).exists()) :
                if check_password(form['password'].value() ,User.objects.all().filter(username=form['username'].value())[0].password ) :
                    user = authenticate(request, username=f"{form['username'].value()}", password=f"{form['password'].value()}")
                    login(request , user)
                    return redirect('profile' ,form['username'].value())
                else :
                    messages.error(
                    request, "Wrong password.")
                    return redirect('login')
            else :
                messages.error(
                    request, "Not exist.")
                return redirect('login')
        else:
            messages.error(
                request, "Wrong input data please re enter it.")
            return redirect('login')

class createView (View):
    def get(self, request):
        return render(request, 'blog/create.html')

    def post(self, request):
        user = get_object_or_404(User,id=request.user.id)
        group_user = get_object_or_404(Group,name= "User-Group")

        if not user.groups.filter(name=group_user).exists():
            title = request.POST['title']
            status = request.POST['status']
            content = request.POST['content']
            Post.objects.create(title=title, statue=status,
                                content=content, owner=request.user)
            return redirect('index')
        else:
            return redirect('index')


class DetailPostView(DetailView):

    def get(self, request, pk):

        comments = Comment.objects.all().filter(post_id=pk).order_by('publish_data')
        post = Post.objects.all().filter(id=pk)
        return render(request, 'blog/blog_post.html', {'comments': comments, 'post': post[0]})

    def post(self, request, pk):
        Comment.objects.create(
            post_id=pk, comment_content=request.POST['comment_field'], user_id=request.user.id)
        return redirect('detail_post',pk)
    
def deleteAccount (request , user) :
    if request.method == 'GET' :
        logout(request)
        get_object_or_404(User , username = user).delete() 
        return redirect('index')
    else :
        return HttpResponse('Bad request')

class changePass (PasswordChangeView) :
    def get(self, request):
        form = ChangeForm
        return render(request, 'blog/change password.html', {'form': form})
    def post (self , request) :
        form = ChangeForm(request.POST) 
        if (form.is_valid()) :
            if check_password(form['old_password'].value() , request.user.password) :
                if (form['new_password1'].value() == form['new_password2'].value()):
                    request.user.set_password(form['new_password1'].value())
                    request.user.save()
                    update_session_auth_hash(request , request.user)
                    messages.success(
                        request, "Your password changed")
                    return redirect('profile' , request.user)
                else :
                    messages.error(
                    request, "Wrong input data")
                    return redirect('changepassword')
            else :
                messages.error(
                request, "Wrong input data")
                return redirect('changepassword')
        else :
         messages.error(
                request, "Wrong input data")
        return redirect('changepassword')
class deletePost (View) :
    pass

class editPost (View) :
    pass


class profileView (View) :
    def get (self , request , user) :
        posts = Post.objects.all().filter(owner_id = request.user.id)
        return render(request , 'users/profile.html' , {'user' : request.user , 'posts' : posts })
