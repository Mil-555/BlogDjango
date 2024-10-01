from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import comment
from django.views.generic import ListView

from blog.forms import CommentForm
from blog.models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',{'posts': posts, 'page': page})

def post_detail(request, year, month, day, slug):

    new_comment = None

    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    comment_form = CommentForm()

    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comment_form': comment_form,
                   'comments':comments,
                   'new_comment': new_comment})

class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 3