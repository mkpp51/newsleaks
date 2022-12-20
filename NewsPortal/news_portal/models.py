from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_r = self.post_set.all().aggregate(postRating=Sum('post_rating'))
        p_rat = 0
        p_rat += post_r.get('postRating')

        com_r = self.auth_user.comment_set.all().aggregate(commentRating=Sum('com_rating'))
        c_rat = 0
        c_rat += com_r.get('commentRating')

        self.auth_rating = p_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return self.auth_user.username


class Category(models.Model):
    cat_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.cat_name}'


news = 'NS'
article = 'AR'
POST_TYPE = [
    (news, 'Новость'),
    (article, 'Статья')

]


class Post(models.Model):
    post_type = models.CharField(max_length=2, choices=POST_TYPE, default=article)
    post_pub_date = models.DateTimeField(auto_now_add=True)
    post_header = models.CharField(max_length=255, null=False)
    post_text = models.TextField(null=False)
    post_rating = models.SmallIntegerField(default=0)

    post_auth = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_cat = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def post_preview(self):
        return f'{self.post_text[:125]}...'

    def __str__(self):
        return f'{self.post_header}: {self.post_text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    com_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    read_user = models.ForeignKey(User, on_delete=models.CASCADE)
    com_text = models.CharField(max_length=255, null=False)
    com_pub_date = models.DateTimeField(auto_now_add=True)
    com_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.com_rating += 1
        self.save()

    def dislike(self):
        self.com_rating -= 1
        self.save()
