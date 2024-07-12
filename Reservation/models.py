from django.db import models
from Tourist.models import Tourist
from Rt_Rq.models import Rt_Rq


# 预约
class Reservation(models.Model):
    rv_date = models.DateField()
    tr_id = models.ForeignKey(Tourist, related_name='reservations', on_delete=models.CASCADE)
    rt_rq_id = models.ForeignKey(Rt_Rq, related_name='reservations', on_delete=models.CASCADE)
    status = models.BooleanField()

    def __str__(self):
        return f"Reservation on {self.rv_date} for Tourist {self.tr_id}"

    class Meta:
        db_table = 'reservation'
        verbose_name = "预约"
        verbose_name_plural = "预约"
        ordering = ['rv_date']
