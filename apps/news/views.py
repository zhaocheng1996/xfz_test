from django.shortcuts import render
from .models import News,NewsCategory,Banner
from django.conf import settings
from .serializers import NewsSerializer,CommentSerizlizer
from utils import restful
from django.http import Http404
from .models import Comment
from .forms import PublicCommentForm
from apps.xfzauth.decorators import xfz_login_required

def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    #按时间倒序排序，越迟发布的越早亮出来
    newses = News.objects.select_related('category','author').all()[0:count]
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners': banners,
    }
    return render(request, 'news/index.html',context=context)

def news_list(request):
    page = int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id', 0))
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        # QuerySet
        # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
        newses = News.objects.select_related('category', 'author').all()[start:end]
    else:
        newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    # page = int(request.GET.get('p', 1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    # category_id = int(request.GET.get('category_id', 0))
    # 0,1
    # 2,3
    # 4,5
    # start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    # end = start + settings.ONE_PAGE_NEWS_COUNT

    # if category_id == 0:
    #     # QuerySet
    #     # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
    #     newses = News.objects.select_related('category', 'author').all()[start:end]
    # # else:
    # #     newses = News.objects.select_related('category', 'author').filter(category__id=category_id)[start:end]
    # # serializer = NewsSerializer(newses, many=True)
    # # data = serializer.data
    # return restful.result(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category','author').prefetch_related('comments__author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html',context=context)
    except News.DoesNotExist:
        raise Http404

#传两个参数，一个是哪条新闻，一个是评论内容
@xfz_login_required
def public_comment(request):
    print('到这里应该没问题')
    form = PublicCommentForm(request.POST)
    print(form,'看看表单有没有返回')
    if form.is_valid():#就在这一步，表单验证不过去
        print('这里的话表单验证完成')
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_errors())



def search(request):
    return render(request,'search/search.html')

