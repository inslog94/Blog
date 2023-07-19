from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    tags = models.ManyToManyField('Tag')
    
    def __str__(self):
        return self.title

    
class Tag(models.Model):
    content = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.content
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content