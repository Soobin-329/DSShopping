from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Category, Maker
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
#from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.
'''
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
'''


class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['name', 'content', 'price', 'material', 'image', 'category', 'maker']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response =  super(ProductCreate, self).form_valid(form)
            return response
        else :
            return redirect('/product/')

class ProductUpdate(LoginRequiredMixin, UpdateView):   # 모델명_form
    model = Product
    fields = ['name', 'content', 'price', 'material', 'image', 'category', 'maker']

    template_name = 'mall/product_update_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdate,self).get_context_data()
        return context

    def form_valid(self, form):
        response = super(ProductUpdate, self).form_valid(form)
        return response


class ProductList(ListView) :
    model = Product
    ordering = '-pk'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count()
        return context


class ProductDetail(DetailView) :
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_product_count'] = Product.objects.filter(category=None).count()
        context['product_lists'] = Product.objects.all()
#        context['comment_form'] = CommentForm
        return context


class ProductSearch(ProductList) :
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        product_list = Product.objects.filter(
            Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : { q }({ self.get_queryset().count() })'

        return context

def category_page(request, slug):
    if slug == 'no_category' :
        category = '미분류'
        product_list = Product.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        product_list = Product.objects.filter(category=category)

    return render(request, 'mall/product_list.html',
                  {
                      'product_list' : product_list,
                      'categories' : Category.objects.all(),
                      'no_category_product_count' : Product.objects.filter(category=None).count(),
                      'category' : category     # 카테고리를 post_list.html로 전달
                  }
            )
