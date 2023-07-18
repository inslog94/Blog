from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Tag, Comment
from .forms import PostForm


class Index(View):
    def get(self, req):
        posts = Post.objects.all()
        print(posts)
        context = {
            "posts": posts,
        }
        
        return render(req, "blog/post_list.html", context)
    

class PostDetail(View):
    def get(self, req, pk):
        # post = Post.objects.get(pk=pk)
        # print(post)
        post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=pk)
        print(post)
        
        if post.is_deleted:
            return render(req, "blog/post_deleted.html")
        
        # comments = Comment.objects.select_related('post').filter(post=post)
        comments = post.comment_set.all()
        print('comments', comments)
        
        # tags = Tag.objects.select_related('post').filter(post__pk=pk)
        tags = post.tag_set.all()
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
        context = {
            'form': form
        }
        
        return render(req, "blog/post_form.html", context)
    
    def post(self, req):
        form = PostForm(req.POST)
        print("form 데이터", form)
        if form.is_valid():
            # post = form.save()
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            post = Post(title=title, content=content)
            post.save()
            
            print(title, content)
            # title = form.cleaned_data['title']
            # content = form.cleaned_data['content']
            # print(title, content, form)
            
            return redirect('blog:list')