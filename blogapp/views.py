from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.urls import reverse

from blogapp.models import Post, Comment
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.decorators import login_required
from blogapp.forms import PostForm, CommentForm, UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib import messages



# DetailView and DeleteView are quite similar as CreateView and UpdateView are.

class AboutView(TemplateView):
    template_name = 'blogapp/about.html'

class PostListView(ListView):
    model = Post

    # template_name = 'blogapp/xyz.html' ==> own template name
    # can set our own template name like app/name.html instead of using the generic template name
    # like <app>/<model>_<viewtype>.html <=> 'blogapp/post_list.html' ==> generic template name

    # it loops over the name objectlist which consists of all the posts we want that variable to be called as 'posts'
    # like context_object_name = 'posts'  <=> 'post_list' in post_list.html

    # context_object_name = 'posts'


    # we can do this for listing according to order

    ordering = ['-published_date']

    # or can do this

    # def get_queryset(self):
    #     return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blogapp/userpost_list.html'
    paginate_by = 3

    def get_queryset(self,*args,**kwargs):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-published_date')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User,username=self.kwargs.get('username'))
        return context

class PostDetailView(DetailView):
    model = Post


# IMPORTANT
# Create view by default look for the template name blogapp/post_form.html
# We can't decorate classes in python using decorators.
# So to need that only logged in user can create a Post we need mixin known as LoginRequiredMixin
# always put this mixin in far-left in the class.

class CreatePostView(LoginRequiredMixin, CreateView):

    form_class = PostForm
    model = Post

    # method to save the author of the post as current user.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):

    form_class = PostForm
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


# By default DeleteView looks for <app>/<model>_confirm_delete.html
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    # success_url is for delete view after succesfully deleting the view.
    success_url = reverse_lazy('blogapp:post_draft_list')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class DraftListView(LoginRequiredMixin,ListView):
    redirect_field_name = 'blogapp/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


def registrationofuser(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()

    return render(request,'blogapp/register.html',{'form':form})


@login_required
def profile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('blogapp:profile')
        else:
            print(u_form.errors,p_form.errors)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request,'blogapp/profile.html',context)

###############################################
###############################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blogapp:post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        # form.instance.author = request.user # you can do this to auto save the author of comment
        # or can do something like
        # comment.author = request.user in form.is_valid() method.

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blogapp:post_detail',pk=post.pk)

    else:
        form = CommentForm()
    return render(request,'blogapp/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blogapp:post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('blogapp:post_detail',pk=comment.post.pk)

############################################################################################################################
# View to check out another user's profile. But then I merged it with the userpost_list to see user's post as well.       ##
#                                                                                                                         ##
# @login_required                                                                                                         ##
# def userprofile(request,username):                                                                                      ##
#     user = get_object_or_404(User,username=username) # username = username is correct not username = 'username'         ##
#     return render(request,'blogapp/userprofile.html',{'user':user})                                                     ##
                                                                                                                          ##
############################################################################################################################
