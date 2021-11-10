from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .models import *
from .utils import *



class SouvenirHome(DataMixin, ListView):
    model = Souvenir
    template_name = "souvenir/index.html"
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Souvenir.objects.filter(availability=True).select_related('cat')



# def index(request):
#     context = {
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0
#     }
#     return render(request, "souvenir/index.html", context=context)


class About(DataMixin, ListView):
    model = Souvenir
    template_name = 'souvenir/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='About')
        return dict(list(context.items()) + list(c_def.items()))

# def about(request):
#     return render(request, 'souvenir/about.html', {'menu': menu, 'title': 'About site'})


class AddGoods(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddGoodsForm
    template_name = 'souvenir/addgoods.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))


# def add_goods(request):
#     if request.method == 'POST':
#         form = AddGoodsForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddGoodsForm()
#     return render(request, 'souvenir/addgoods.html', {'form': form, 'menu': menu, 'title': 'Add goods'})

class FeedbackFormView(DataMixin, FormView):
    form_class = FeedbackForm
    template_name = 'souvenir/feedback.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='братная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# @login_required
# def feedback(request):
#     return HttpResponse("Обратная связь")


class ShowGoods(DataMixin, DetailView):
    model = Souvenir
    template_name = "souvenir/goods.html"
    slug_url_kwarg = 'goods_slug'
    context_object_name = 'goods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['goods'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_goods(request, goods_slug):
#     goods = get_object_or_404(Souvenir, slug=goods_slug)
#
#     context = {
#         'goods': goods,
#         'menu': menu,
#         'title': goods.title,
#         'cat_selected': goods.cat_id
#     }
#     return render(request, "souvenir/goods.html", context=context)


class SouvenirsCategory(DataMixin, ListView):
    template_name = "souvenir/index.html"
    context_object_name = 'posts'

    def get_queryset(self):
        return Souvenir.objects.filter(cat__slug=self.kwargs['cat_slug'], availability=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_slug):
#
#     context = {
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_slug
#     }
#     return render(request, "souvenir/index.html", context=context)


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'souvenir/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'souvenir/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
