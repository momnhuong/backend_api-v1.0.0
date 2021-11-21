from django.db import models


class Role(models.Model):
    class Meta:
        db_table = 'role'
    name = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.name
