from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from Tourist.models import Tourist

class Attraction(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    star_level = models.IntegerField(verbose_name="星级")
    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="评分", default=0)
    description = models.TextField(verbose_name="介绍")
    opening_hours = models.CharField(max_length=100, verbose_name="开放时间")
    popularity = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="热度",
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    address = models.CharField(max_length=200, verbose_name="地址")
    official_phone = models.CharField(max_length=100, verbose_name="官方电话")
    search_count = models.IntegerField(default=0, verbose_name="搜索次数")  # 新增搜索次数字段

    def __str__(self):
        return self.name

    def update_popularity(self):
        # 热度算法：考虑搜索次数、评分和评论数
        if self.search_count + self.comment_count == 0:
            self.popularity = 0
        else:
            self.popularity = min(
                10,
                (self.search_count + (self.rating * self.comment_count)) / 10
            )
        self.save()

    def update_rating(self):
        comments = self.comments.all()
        total_rating = sum(comment.rating for comment in comments)
        self.rating = total_rating / comments.count() if comments.count() > 0 else 0
        self.save()

    def update_comment_count(self):
        self.comment_count = self.comments.count()
        self.save()

    class Meta:
        db_table = 'attraction'
        ordering = ['name']
        verbose_name = '景点'
        verbose_name_plural = '景点'

class AttractionImage(models.Model):
    attraction = models.ForeignKey(Attraction, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='attraction_images/', verbose_name="景点图片")

    def __str__(self):
        return f"Image for {self.attraction.name}"

class Comment(models.Model):
    user = models.ForeignKey(Tourist, on_delete=models.CASCADE, verbose_name="用户")
    attraction = models.ForeignKey(Attraction, related_name='comments', on_delete=models.CASCADE, verbose_name="景点")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    comment_text = models.TextField(verbose_name="评论内容")
    rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="评分")  # 打分，0.0-5.0
    likes = models.IntegerField(default=0, verbose_name="点赞数")
    is_featured = models.BooleanField(default=False, verbose_name="是否精华")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.attraction.update_rating()
        self.attraction.update_comment_count()
        self.user.points += 10  # 每次评论增加10积分  vip
        self.user.update_user_type()  # 更新用户类型
        self.user.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.attraction.update_rating()
        self.attraction.update_comment_count()
        self.user.update_user_type()  # 更新用户类型
        self.user.save()

    def __str__(self):
        return f'Comment by {self.user.user.username} on {self.attraction.name}'

    class Meta:
        db_table = 'comment'
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'
        indexes = [
            models.Index(fields=['created_at']),
        ]

class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comment_images/', verbose_name="评论图片")

    def __str__(self):
        return f"Image for comment by {self.comment.user.user.username}"
