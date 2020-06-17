from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    """Custom user model with email auth and admin support"""

    # whether or not they are admin from this site
    # Not to be confused with `is_staff`, which indicates login capability of
    # the django-admin interface. Not sure we should remove one.
    is_admin = models.BooleanField(default=False)
    has_permit = models.BooleanField(default=True)
    deleted_datetime = models.DateTimeField(null=True)

    # email must be unique & non-null when used as a username
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    # email must not exist in required fields when used as username
    REQUIRED_FIELDS = ['username']


def image_path1(instance, filename):
    return f'static/images/{instance.name}/1.jpg'


def image_path2(instance, filename):
    return f'static/images/{instance.name}/2.jpg'


def image_path3(instance, filename):
    return f'static/images/{instance.name}/3.jpg'


class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='admin_auction_set')
    name = models.CharField(max_length=255, null=False, blank=False)
    type = models.IntegerField(default=2, null=False)
    contents = models.TextField(null=False, blank=True)
    image1 = ProcessedImageField(
        upload_to=image_path1,
        processors=[ResizeToFill(800, 800)],
        format='JPEG',
        options={'quality': 90},
        null=True
    )
    image2 = ProcessedImageField(
        upload_to=image_path2,
        processors=[ResizeToFill(800, 800)],
        format='JPEG',
        options={'quality': 90},
        null=True
    )
    image3 = ProcessedImageField(
        upload_to=image_path3,
        processors=[ResizeToFill(800, 800)],
        format='JPEG',
        options={'quality': 90},
        null=True
    )
    state = models.CharField(max_length=20, null=False, blank=False)  # 준비, 진행중, 완료, 낙찰, 취소
    start_datetime = models.DateTimeField(null=False, blank=False)
    end_datetime = models.DateTimeField(null=False, blank=False)
    min_bid = models.IntegerField(null=False)
    max_bid = models.IntegerField(null=False)
    participants_count = models.IntegerField(default=0, null=False)
    winning_bid = models.IntegerField(default=0, null=False)  # now_bid랑 동일한 역할로 이거 쓸게요. 경매 진행중일 때는 현재 입찰가, 경매 끝나고 나서는 낙찰가로 사용.
    winning_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='won_auction_set', null=True)
    created_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)
    updated_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)
    deleted_datetime = models.DateTimeField(null=True)


class AuctionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bid = models.IntegerField(null=False)
    is_valid = models.BooleanField(null=False)
    created_datetime = models.DateTimeField(default=datetime.now, null=False, blank=False)
