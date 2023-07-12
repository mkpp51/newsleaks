from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from NewsPortal import settings
from .filters import PostFilter
from .forms import PostForm
from .models import Post, Author, Category


@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'protected_page.html'


@login_required
def add_subscriber(request, category: str):
    Category.objects.get(cat_name=category).subscribers.add(request.user)
    user = request.user

    send_mail(
        subject='''NEWSPORTAL. You've successfully subscribed!''',
        message=f'Hello, {user.username}!\nThank you for subscribing to publications in the category: {category}.',
        from_email=None,
        recipient_list=[f'{user.email}', ],
    )

    return redirect('/news_portal/categories/')


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


def category(request, category: int):
    category = get_object_or_404(Category, cat_name=category)
    return render(request, 'category.html', {'category': category})


class PostList(ListView):
    model = Post
    template_name = 'news_portal.html'
    context_object_name = 'news_portal'
    ordering = '-post_pub_date'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     post = form.save(commit=False)
    #     post.post_type = 'NS'
        # post = self.object
        # post_url = f'http://127.0.0.1:8000/{post.get_absolute_url()}'
        # categories = post.post_cat.all()
        # subscribers_emails = []
        # category_name = []
        # for category in categories:
        #     category_name.append(category.cat_name)
        #     subscribers = category.subscribers.all()
        #     subscribers_emails = [user.email for user in subscribers]
        #
        # send_mail(
        #     subject=f'NEWSPORTAL. New publication!',
        #     message=f'There is new publication in your favorite {category_name} category:\n'
        #             f'{post.post_text[:50]}...'
        #             f'Follow the link:\n{post_url}',
        #     from_email=settings.SERVER_EMAIL,
        #     recipient_list=subscribers_emails
        # )

        # return response


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     post = form.save(commit=False)
    #     post.post_type = 'AR'
        # post = self.object
        # post_url = f'http://127.0.0.1:8000/{post.get_absolute_url()}'
        # categories = post.post_cat.all()
        # subscribers_emails = []
        # category_name = []
        # for category in categories:
        #     category_name.append(category.cat_name)
        #     subscribers = category.subscribers.all()
        #     subscribers_emails = [user.email for user in subscribers]
        #
        # send_mail(
        #     subject=f'NEWSPORTAL. New publication!',
        #     message=f'There is new publication in your favorite {category_name} category:\n'
        #             f'{post.post_text[:50]}...'
        #             f'Follow the link:\n{post_url}',
        #     from_email=settings.SERVER_EMAIL,
        #     recipient_list=subscribers_emails
        # )

        # return response


class ProtectedNewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NS'
        return super().form_valid(form)


class ProtectedArticlesEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = '/news_portal/'


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = '/news_portal/'


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-post_pub_date')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['form'] = PostForm()
        return context
