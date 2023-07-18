from django.shortcuts import render
from django.views import View
from .models import Post, Tag, Comment


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