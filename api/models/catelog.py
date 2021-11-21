
from django.db import models
from django.conf import settings


class Catelog(models.Model):

    class Meta:
        db_table = 'catelog'

    name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    on_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    def set_on_active(self, is_bool):
        self.on_active = is_bool
        self.save()
        return
