from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator,EmptyPage,\
                                PageNotAnInteger
# from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth import logout, login, authenticate
from django.views import View
from django.contrib.auth.models import User, Group

# from django.http import Http404

from .models import Post,Comment,UserProfile
from .forms import EmailPostForm,CommentForm,SearchForm,UserRegisterForm,UserLoginForm


def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    paginator = Paginator(post_list,4)
    page_number = request.GET.get('page',1)
    
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request,'blog/post/list.html',{'posts':posts,'tag':tag})




def post_detail(request,year,month,day,post):

    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                    .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags','-publish')
    paginator = Paginator(similar_posts,2)
    page_number = request.GET.get('page',1)

    try:
        similar_posts = Paginator.page(paginator,page_number)
    except EmptyPage:
        similar_posts = Paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        similar_posts = Paginator.page(1)

    
    
    return render(request,'blog/post/detail.html',
                {'post':post,
                'comments':comments,
                'form':form,
                'similar_posts':similar_posts})



def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read "\
                        f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            
            send_mail(subject, message ,'ahmedshrieframadan@gmail.com',[cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,
                                                'form':form,
                                                'sent':sent})


@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,'blog/post/comment.html',
                {'post':post,
                'form':form,
                'comment':comment})



def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = Post.published.annotate(
                            similarity=TrigramSimilarity('title', query)
                            + TrigramSimilarity('body', query)) \
                            .filter(similarity__gt=0.04).order_by("-similarity")


    return render(request,'blog/post/search.html',
                {'form':form,
                'query':query,
                'results':results})


def home(request):
    numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 100)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/test.html', {'numbers': numbers})


class loginView (View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'blog/users/login.html', {'form': form})

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
                return redirect('blog:profile')
        #     else:
        #         messages.error(
        #             request, 'Invalid username or password.')
        #         return redirect('login')
        # else:
        #     messages.error(
        #         request, "Wrong input data please re enter it.")
        #     return redirect('login')



class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'blog/users/register.html', {'form': form})

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
            # messages.success(
            #     request, "Your are signed up successfully")
            user = authenticate(
                request, username=f"{form['username'].value()}", password=f"{form['password1'].value()}")
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('blog:profile')
        else:
            # messages.error(
            #     request, "Wrong input data please re enter it.")
            # return redirect('register')
            pass


class ProfileView(View):
    def get(self,request):
        user = get_object_or_404(UserProfile,user=request.user)
        return render(request,'blog/users/profile.html',
                    {'user':user})