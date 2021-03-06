from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.utils.timezone import make_naive
from django.views.generic import View, TemplateView

from webapp.models import Article
from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT


class IndexView(View):
    def get(self, request):
        is_admin = request.GET.get('is_admin', None)
        data = Article.objects.all()
        return render(request, 'index.html', context={
            'articles': data
        })


class ArticleView(TemplateView):
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)

        context['article'] = article
        return context


class ArticleCreateView(View):
    def get(self, request):
        return render(request, 'article_create.html', context={
            'form': ArticleForm()
        })

    def post(self, request):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                description=form.cleaned_data['description'],
                maxdescription=form.cleaned_data['maxdescription'],
                status=form.cleaned_data['status'],
                type=form.changed_data['type'],
                publish_at=form.cleaned_data['publish_at']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article_create.html', context={
                'form': form
            })

class ArticleUpdateView(TemplateView):
    template_name = 'article_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(initial={
            'description': article.description,
            'maxdescription': article.maxdescription,
            'status': article.status,
            'type': article.type,
            'publish_at': make_naive(article.publish_at).strftime(BROWSER_DATETIME_FORMAT)
        })
        context['article'] = article
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.description = form.cleaned_data['description']
            article.maxdescription = form.cleaned_data['maxdescription']
            article.status = form.cleaned_data['status']
            article.type = form.cleaned_data['type']
            article.publish_at = form.cleaned_data['publish_at']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return self.render_to_response({
                'article': article,
                'form': form
            })


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'article_delete.html', context={'article':article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
