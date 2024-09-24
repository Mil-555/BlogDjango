from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from blog.models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status='published')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')


    return render(request, 'blog/post/list.html',
                  {'posts': posts})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html',
                  {'post': post,})