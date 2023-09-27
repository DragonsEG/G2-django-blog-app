from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Post, Comment
from django.contrib.auth.models import User,Group
from django.shortcuts import get_object_or_404
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
            return redirect('index')
        else:
            messages.error(
                request, "Wrong input data please re enter it.")
            return redirect('register')


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
            print(title, status, content)
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
