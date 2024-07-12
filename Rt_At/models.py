from django.db import models
from Route.models import Route
from Attraction.models import Attraction


# 线路-景点对应表
class Rt_At(models.Model):
    rt_id = models.ForeignKey(Route, related_name='route_attractions', on_delete=models.CASCADE)
    at_id = models.ForeignKey(Attraction, related_name='attraction_routes', on_delete=models.CASCADE)

    class Meta:
        db_table = 'rt_at'
        verbose_name = '线路-景点对应表'
        verbose_name_plural = '线路-景点对应表'
