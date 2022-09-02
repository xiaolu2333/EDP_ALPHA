from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserProfile(AbstractUser):
    ROLE = [
        ('SAD', '系统管理员'),
        ('SCA', '安全保密管理员'),
        ('SAU', '安全审计员'),
        ('OGU', '普通用户'),
    ]
    STATUS = [
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
    ]

    role = models.CharField(max_length=128, choices=ROLE, blank=False)
    status = models.CharField(max_length=128, choices=STATUS, blank=False)

    class Meta:
        verbose_name_plural = verbose_name = '用户基本信息'

    def __str__(self):
        return self.username
