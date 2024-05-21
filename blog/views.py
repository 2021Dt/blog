from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy,reverse
from django.views.decorators.http import require_http_methods, require_POST,require_GET
from .models import Blog, BlogComment, BlogCategory
from .forms import PubBlogForm,PubCommentForm
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

# Create your views here.

def index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html',context={'blogs':blogs})


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
        return render(request, 'blog_detail.html', context={'blog': blog})
    except Exception as e:
        return render(request, '404.html')


# @login_required(login_url=reverse('dpauth:login'))
# @login_required(login_url=reverse_lazy('dpauth:login'))  # 懒加载
@require_http_methods(['POST', 'GET'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, 'pub_blog.html', context={'categories': categories})
    else:
        form = PubBlogForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category').id
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)

            return JsonResponse({'code': 200, 'msg': '博客发布成功！', 'data': {'blog_id': blog.id}})
        else:
            print(form.errors)
            return JsonResponse({'code': 400, 'msg': '参数错误！请联系作者'})


@require_POST
@login_required()
def pub_comment(request):

    form = PubCommentForm(request.POST)
    if form.is_valid():
        blog_id = request.POST.get('blog_id')
        content = request.POST.get('content')
        BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user)
        # 重定向
        return redirect(reverse_lazy('blog:blog_detail', kwargs={'blog_id': blog_id}))
    # else:
    #     print(form.errors)
    return HttpResponse("Something went wrong", status=400)
#
# @require_POST
# @login_required()
# def pub_comment(request):
#     blog_id = request.POST.get('blog_id')
#     content = request.POST.get('content')
#     BlogComment.objects.create(blog_id=blog_id, content=content, author=request.user)
#     # 重定向
#     return redirect(reverse_lazy('blog:blog_detail', kwargs={'blog_id': blog_id}))

@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    return render(request,'index.html',context={'blogs': blogs})