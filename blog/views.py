from django.shortcuts import render,get_object_or_404,redirect
from django.utils.text import slugify

from .models import Post,Comment


def post_list(request):
    posts = Post.objects.all().filter(status=Post.Status.PUBLISHED).order_by('-publish')
    count = posts.count()
    zipped = zip(range(1, count + 1), posts)
    return render(request,'blog/post/list.html',{'zipped':zipped})


def post_detail(request,id):

    post = get_object_or_404(Post,id=id)
    comment_field = request.GET.get('comment_field',None)
    if comment_field != None and comment_field != ""  :
        get_comment = request.GET['comment_field'] 
        if get_comment is not None:
            comments = Comment.objects.create(post=post,body=get_comment)

    comments = post.comments.all().order_by('-created')
    return render(request,'blog/post/detail.html',{'post':post,'comments':comments})


def post_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        slug = slugify(title)
        body = request.POST['body']
        status = request.POST['status']
        print(status)
        Post.objects.create(title=title,body=body,slug=slug,status=status,author=request.user)
        return redirect('blog:post_list')
    
    return render(request,'blog/post/create.html')


def post_draft(request):
    drafted_posts = Post.objects.filter(status=Post.Status.DRAFT).order_by('-publish')

    
    state = request.GET.get('publish')

    if state != None:
        user_id = request.GET.get('user_id')
        post = get_object_or_404(Post,id=user_id)
        post.status = Post.Status.PUBLISHED
        post.save()

    return render(request,'blog/post/draft.html',{'draft_posts':drafted_posts})