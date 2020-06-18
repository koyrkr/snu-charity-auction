from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from auction.models import Auction, User


class AuctionTestCase(TestCase):
    def setUp(self):
        User.objects.create(is_admin=1, username='test', password='test', email='test@test.kr')
        User.objects.create(is_admin=0, username='test2', password='test', email='test2@test.kr')
        Auction.objects.create(
            admin_id=1,
            name='아디다스 슈퍼스타',
            type=2,
            contents='-',
            state='준비',
            start_datetime=timezone.now(),
            end_datetime=timezone.now()+timedelta(days=3),
            min_bid=1000,
            max_bid=1000000,
            created_datetime=timezone.now(),
            updated_datetime=timezone.now()
        )

    def test_index(self):
        response = self.client.get('/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_auction_without_auth(self):
        response = self.client.get('/auction/')
        self.assertEqual(response.status_code, 302)  # expected redirect

    def test_auction(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/auction/')
        self.assertEqual(response.status_code, 200)

    def test_auction_detail(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/auction/detail/1/')
        self.assertEqual(response.status_code, 200)

    def test_apply_auction(self):
        user = User.objects.get(id=2)
        self.client.force_login(user)
        params = {'bid': 1000}
        response = self.client.post('/auction/apply/1/', params)
        self.assertEqual(response.status_code, 200)
        auction = Auction.objects.get(id=1)
        self.assertEqual(auction.winning_bid, 1000)
        self.assertEqual(auction.winning_user_id, 2)

    def test_get_auction_history(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/auction-history/')
        self.assertEqual(response.status_code, 200)

    def test_modify_auction(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/auction/modify/1/')
        self.assertEqual(response.status_code, 200)

    def test_delete_auction(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/auction/delete/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_user_list(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/user-list/')
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/user-list/2/delete/')
        self.assertEqual(response.status_code, 302)

    def test_take_auth_user(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/user-list/2/take_auth/')
        self.assertEqual(response.status_code, 302)

    def test_give_auth_user(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get('/user-list/2/give_auth/')
        self.assertEqual(response.status_code, 302)
