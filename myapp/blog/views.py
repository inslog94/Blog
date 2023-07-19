from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Tag, Comment
from .forms import PostForm, TagForm


class Index(View):
    def get(self, req):
        posts = Post.objects.all()
        tags = Tag.objects.all()
        print(posts)
        context = {
            "posts": posts,
            "tags": tags,
        }
        
        return render(req, "blog/post_list.html", context)
    

class PostDetail(View):
    def get(self, req, pk):
        # post = Post.objects.get(pk=pk)
        # print(post)
        post = Post.objects.prefetch_related('comment_set').get(pk=pk)
        print(post)
        
        if post.is_deleted:
            return render(req, "blog/post_deleted.html")
        
        # comments = Comment.objects.select_related('post').filter(post=post)
        comments = post.comment_set.all()
        print('comments', comments)
        
        # tags = Tag.objects.select_related('post').filter(post__pk=pk)
        tags = post.tags.all()
        print("tags", tags)
        context = {
            "post": post,
            "comments": comments,
            "tags": tags
        }
        
        return render(req, "blog/post_detail.html", context)
    
    
class Search(View):
    def get(self, req):
        query = req.GET.get('name')
        print(query)
        posts = Post.objects.filter(title__contains=query)
        print(posts)
        context = {
            "query": query,
            "posts": posts
        }
        
        return render(req, 'blog/post_search.html', context)
    

class TagSearch(View):
    def get(self, req):
        query = req.GET.get('name')
        print(query)
        tag = Tag.objects.get(content=query)
        posts = tag.post_set.all()
        print(posts)
        context = {
            "query": query,
            "posts": posts
        }
        
        return render(req, 'blog/post_search.html', context)

    
class PostDelete(View):
    def post(self, req, pk):
        post = Post.objects.get(pk=pk)
        print("delete", post)
        post.is_deleted = True
        post.save()
        
        return redirect('blog:list')
    
    
class PostWrite(View):
    def get(self, req):
        form = PostForm()
        tagForm = TagForm()
        context = {
            'form': form,
            'tagForm': tagForm
        }
        
        return render(req, "blog/post_form.html", context)
    
    def post(self, req):
        post_form_data = {
            "title": req.POST.get("title"),
            "content": req.POST.get("content"),
        }
        
        form = PostForm(data=post_form_data)
        
        tag_form_data = {
            "content": req.POST.get("tags")
        }
        tag_form = TagForm(data=tag_form_data)

        if form.is_valid() and tag_form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            post = Post(title=title, content=content)
            post.save()
            
            form_content = tag_form.cleaned_data['content'].split(",")
            tags = []
            if tag_form:
                print(form_content)
                for i in form_content:
                    tag, created = Tag.objects.get_or_create(content=i)
                    tags.append(tag)
                post.tags.set(tags)
        
            return redirect('blog:list')


class PostUpdate(View):
    def get(self, req, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(initial={'title': post.title, 'content': post.content})
        context = {
            'content': post.content,
            'form': form,
            'post': post,
        }
        
        return render(req, 'blog/post_edit.html', context)
    
    def post(self, req, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(req.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.save()
            
            return redirect('blog:detail', pk=pk)