from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, Http404

from blogapp.token import activation_token
from .models import author, category, article, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CreateForm, CreateRegisterUserForm, CreateAuthorForm, CreateCommentForm, CreateCategoryForm
from django.contrib import messages
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail


class index(View):
    def get(self, request):
        post = article.objects.all()
        search = request.GET.get('search')
        if search:
            post = post.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)

            )
        paginator = Paginator(post, 8)
        page = request.GET.get('page')
        total_article = paginator.get_page(page)

        context = {
            'post': total_article
        }
        return render(request, 'templates/index.html', context)


class getauthor(View):
    def get(self, request, name):
        post_author = get_object_or_404(User, username=name)
        auth = get_object_or_404(author, name=post_author.id)
        post = article.objects.filter(article_author=auth.id)
        context = {
            'auth': auth,
            'post': post,
        }
        return render(request, 'templates/profile.html', context)


class getsingle(View):
    def get(self, request, id):
        post = get_object_or_404(article, pk=id)
        first = article.objects.first()
        last = article.objects.last()
        get_comment = Comment.objects.filter(post=id)
        related = article.objects.filter(category=post.category).exclude(id=id)[:4]
        form = CreateCommentForm()

        context = {
            'post': post,
            'first': first,
            'last': last,
            'related': related,
            'form': form,
            'comment': get_comment
        }
        return render(request, 'templates/single.html', context)

    def post(self, request, id):
        post = get_object_or_404(article, pk=id)
        form = CreateCommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = post
            instance.save()
            return redirect('single_post', id=id)


class getTopic(View):
    def get(self, request, name):
        cat = get_object_or_404(category, name=name)
        post = article.objects.filter(category=cat.id)
        return render(request, 'templates/category.html', {'post': post, 'cat': cat})


class getLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'templates/login.html')

    def post(self, request):
        user = request.POST.get('username')
        password = request.POST.get('password')
        auth = authenticate(request, username=user, password=password)
        if auth is not None:
            login(request, auth)
            messages.success(request, 'Congrats! Loing Successfully!')
            return redirect('index')

        else:
            messages.add_message(request, messages.ERROR, 'Wrong username or password! please try again.')
            return redirect('login')


class getLogout(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have logged out successfully.')
        return redirect('index')


def getCreate(request):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        form = CreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'A new article is published successfully!')
            return redirect('index')
        return render(request, 'templates/create.html', {'form': form})
    else:
        return redirect('login')


def getUpdate(request, pid):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(article, id=pid)
        form = CreateForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.article_author = u
            instance.save()
            messages.success(request, 'Article is updted successfully!')
            return redirect('profile')
        return render(request, 'templates/update.html', {'form': form})
    else:
        return redirect('login')


def getDelete(request, pid):
    if request.user.is_authenticated:
        post = get_object_or_404(article, id=pid)
        post.delete()
        messages.error(request, 'Article is deleted successfully!')
        return redirect('profile')
    else:
        return redirect('login')


def getProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
            post = article.objects.filter(article_author=authorUser.id)
            return render(request, 'templates/logged_in_profile.html', {'post': post, 'user': authorUser})
        else:
            form = CreateAuthorForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.name = user
                instance.save()
                return redirect('profile')
            return render(request, 'templates/create_author.html', {'form': form})

    else:
        return redirect('login')


def getRegister(request):
    form = CreateRegisterUserForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()
        site = get_current_site(request)
        mail_subject = "Confirmation message for blog"
        message = render_to_string('templates/confirm_email.html', {
            'user': instance,
            'domain': site.domain,
            'uid': instance.id,
            'token': activation_token.make_token(instance)
        })
        to_email = form.cleaned_data.get('email')
        to_list = [to_email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, to_list, fail_silently=False)
        return HttpResponse('<h1>Thanks for your registration. A confirmation link was sent to your email.<h1>')
    return render(request, 'templates/register.html', {'form': form})


def topics(request):
    topics = category.objects.all()
    return render(request, 'templates/topics.html', {'topics': topics})


def newTopic(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            form = CreateCategoryForm(request.POST or None)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'New topic added successfully!')
                return redirect('topics')
            return render(request, 'templates/new_topic.html', {'form': form})
        else:
            raise Http404('You are not authorized to access this page!')
    else:
        redirect('login')

def activate(request):
    return render_to_string()