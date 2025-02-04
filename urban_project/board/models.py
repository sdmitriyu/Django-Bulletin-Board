from django.db import models
from django.contrib.auth.models import User

class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True, default='default.jpg')

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return f"{self.title} - Likes: {self.like_set.count()}, Dislikes: {self.dislike_set.count()}"

class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like by {self.user} on {self.advertisement}'


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='dislikes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Dislike by {self.user} on {self.advertisement}'





