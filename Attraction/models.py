from django.db import models
from Tourist.models import Tourist
from django.core.validators import MinValueValidator, MaxValueValidator
class Attraction(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    star_level = models.IntegerField(verbose_name="星级")
    rating = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="评分")
    description = models.TextField(verbose_name="介绍")
    opening_hours = models.CharField(max_length=100, verbose_name="开放时间")
    popularity = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="热度",
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    comment_count = models.IntegerField(verbose_name="评论数")
    address = models.CharField(max_length=200, verbose_name="地址")
    official_phone = models.CharField(max_length=20, verbose_name="官方电话")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'attraction'
        ordering = ['name']
        verbose_name = '景点'
        verbose_name_plural = '景点'

class Comment(models.Model):
    user = models.ForeignKey(Tourist, on_delete=models.CASCADE, verbose_name="用户")
    attraction = models.ForeignKey(Attraction, related_name='comments', on_delete=models.CASCADE, verbose_name="景点")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    comment_text = models.TextField(verbose_name="评论内容")
    rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name="评分")  # 打分，0.0-5.0
    likes = models.IntegerField(default=0, verbose_name="点赞数")
    optional_image = models.ImageField(upload_to='comments/', blank=True, null=True, verbose_name="可选图片")
    is_featured = models.BooleanField(default=False, verbose_name="是否精华")

    def __str__(self):
        return f'Comment by {self.user.username} on {self.attraction.name}'

    class Meta:
        db_table = 'comment'
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'
        indexes = [
            models.Index(fields=['created_at']),
        ]
