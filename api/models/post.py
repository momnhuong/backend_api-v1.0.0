from django.db import models
from .account import Account

class Post(models.Model):

  LEVEL_DE = 'Dễ'
  LEVEL_TRUNGBINH = 'Trung Bình'
  LEVEL_KHO = 'Khó'
  LEVELS = (
    ('DE', LEVEL_DE),
    ('TRUNG_BINH', LEVEL_TRUNGBINH),
    ('KHO', LEVEL_KHO)
  )

  CATEGORY_DEFAULT = 'Khai vị'
  CATEGORIES = (
    ('KHAI_VI', 'Khai vị'),
    ('MON_CHINH', 'Món chính'),
    ('TRANG_MIENG', 'Tráng miệng'),
    ('BANH_NGOT', 'Bánh ngọt'),
    ('AN_CHOI', 'Ăn chơi'),
  )

  class Meta:
    db_table = 'post'

  title = models.TextField(blank=True, null=True)
  image = models.TextField(blank=True, null=True)
  workingtime = models.IntegerField(blank=True, null=True)
  material = models.TextField(blank=True, null=True)
  guide = models.TextField(blank=True, null=True)
  category = models.CharField(max_length=50, choices=CATEGORIES,  default=CATEGORY_DEFAULT)
  level = models.CharField(max_length=50, choices=LEVELS,  default=LEVEL_DE)
  user = models.ForeignKey(Account, null=True, related_name='posts', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)