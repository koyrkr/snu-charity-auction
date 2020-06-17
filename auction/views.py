from datetime import datetime

from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import dateformat, timezone

from auction.models import Auction, User, AuctionHistory


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/auction')
    else:
        return render(request, 'index.html')


def join_view(request):
    return render(request, 'join.html')


def join_admin_view(request):
    return render(request, 'join-admin.html')


def join(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password1']
    user = User(username=username, email=email, password=make_password(password))
    user.save()
    return HttpResponseRedirect('/join-done')


def join_admin(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password1']
    user = User(username=username, email=email, password=make_password(password), is_admin=True)
    user.save()
    return HttpResponseRedirect('/join-admin-done')


def join_done_view(request):
    return render(request, 'join-done.html')


def join_admin_done_view(request):
    return render(request, 'join-admin-done.html')


def exit_view(request):
    user = request.user
    user.deleted_datetime = datetime.now()
    user.save()
    request.session.clear()
    return render(request, 'exit.html')


def auction_view(request):
    auctions = Auction.objects.all()
    for auction in auctions:
        if timezone.now() >= auction.start_datetime and auction.state == '준비':
            auction.state = '진행중'
            auction.save()
        if timezone.now() >= auction.end_datetime and auction.state == '진행중':
            auction.state = '완료'
            auction.save()

    auction_type = request.GET.get('auction_type')
    end_date = request.GET.get('end_date')
    price = request.GET.get('price')
    keyword = request.GET.get('keyword')

    if auction_type is not None and auction_type != '1':
        auctions = auctions.filter(type=int(auction_type))
    if end_date is not None:
        gte_date = timezone.now() - timezone.timedelta(days=365)
        lt_date = timezone.now() + timezone.timedelta(days=365)
        if end_date == '2':
            lt_date = timezone.now() + timezone.timedelta(days=3)
        if end_date == '3':
            gte_date = timezone.now() + timezone.timedelta(days=3)
            lt_date = timezone.now() + timezone.timedelta(days=5)
        if end_date == '4':
            gte_date = timezone.now() + timezone.timedelta(days=5)
            lt_date = timezone.now() + timezone.timedelta(days=7)
        if end_date == '5':
            gte_date = timezone.now() + timezone.timedelta(days=7)
        auctions = auctions.filter(end_datetime__gte=gte_date, end_datetime__lt=lt_date)
    if price is not None:
        gte_price = 0
        lt_price = 10000000
        if price == '2':
            lt_price = 20000
        if price == '3':
            gte_price = 20000
            lt_price = 40000
        if price == '4':
            gte_price = 40000
            lt_price = 6000
        if price == '5':
            gte_price = 60000
        auctions = auctions.filter(winning_bid__gte=gte_price, winning_bid__lt=lt_price)
    if keyword is not None:
        auctions = auctions.filter(name__contains=keyword)

    context = {'auctions': auctions}
    return render(request, 'auction.html', context=context)


def auction_apply_view(request, auction_id):
    user = request.user
    bid = int(request.POST['bid'])
    auction = Auction.objects.get(id=auction_id)
    min_bid = auction.winning_bid + 1000
    if not bid >= min_bid:
        message = '입찰가가 가능한 최소 입찰가보다 작습니다.'
    elif bid % 1000 != 0:
        message = '입찰은 1,000원 단위로 가능합니다.'
    else:
        AuctionHistory.objects.filter(auction_id=auction_id).update(is_valid=False)
        auction_history = AuctionHistory(auction_id=auction_id, user_id=user.id, bid=bid, is_valid=True)
        auction_history.save()
        auction.winning_bid = bid
        auction.winning_user_id = user.id
        auction.participants_count = auction.participants_count + 1
        auction.updated_datetime = timezone.now()
        auction.save()
        message = '입찰되었습니다.'

    context = {'message': message, 'auction_id': auction_id}
    return render(request, 'auction-apply.html', context=context)


def auction_history_view(request):
    user = request.user
    auction_history = AuctionHistory.objects.filter(user_id=user.id)
    context = {'auction_history': auction_history}
    return render(request, 'auction-history.html', context=context)


def create_auction_view(request):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')

    return render(request, 'create-auction.html')


def mypage_view(request):
    context = {'user': request.user}
    return render(request, 'mypage.html', context=context)


def user_update(request):
    username = request.POST['username']
    password = request.POST['password1']
    user = request.user
    user.username = username
    user.set_password(password)
    user.save()
    auth.login(request, user)
    return HttpResponseRedirect('/')


def create_auction(request):
    admin_id = request.user.id
    name = request.POST['name']
    contents = request.POST['contents']
    start_datetime = request.POST['start-datetime']
    end_datetime = request.POST['end-datetime']
    min_bid = request.POST['min-bid']
    max_bid = request.POST['max-bid']

    file = request.FILES['image1']
    print(file)

    auction = Auction(
        admin_id=admin_id,
        name=name,
        contents=contents,
        image1 = file,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        min_bid=min_bid,
        max_bid=max_bid,
    )
    auction.save()

    return HttpResponseRedirect('/')


def modify_auction_view(request, auction_id):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')

    auction = Auction.objects.get(id=auction_id)
    formatted_start_datetime = dateformat.format(auction.start_datetime, 'Y-m-d H:i:s')
    formatted_end_datetime = dateformat.format(auction.end_datetime, 'Y-m-d H:i:s')
    context = {'auction': auction, 'formatted_start_datetime': formatted_start_datetime,
               'formatted_end_datetime': formatted_end_datetime}
    return render(request, 'modify-auction.html', context=context)


def modify_auction(request):
    auction_id = request.POST['auction-id']
    name = request.POST['name']
    contents = request.POST['contents']
    start_datetime = request.POST['start-datetime']
    end_datetime = request.POST['end-datetime']
    min_bid = request.POST['min-bid']
    max_bid = request.POST['max-bid']

    auction = Auction.objects.get(id=auction_id)
    auction.name = name
    auction.contents = contents
    auction.start_datetime = start_datetime
    auction.end_datetime = end_datetime
    auction.min_bid = min_bid
    auction.max_bid = max_bid
    auction.save()

    return HttpResponseRedirect(f'/auction/detail/{auction_id}')


def delete_auction(request, auction_id):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')
        
    auction = Auction.objects.get(id=auction_id)
    auction.deleted_datetime = datetime.now()
    auction.save()
    return HttpResponseRedirect('/')


def auction_detail_view(request, auction_id):
    auction = Auction.objects.get(id=auction_id)
    if timezone.now() >= auction.start_datetime and auction.state == '준비':
        auction.state = '진행중'
        auction.save()
    if timezone.now() >= auction.end_datetime and auction.state == '진행중':
        auction.state = '완료'
        auction.save()
    auction_history = AuctionHistory.objects.filter(auction_id=auction_id).order_by('created_datetime').reverse()
    min_bid = auction.min_bid
    if auction_history:
        min_bid = auction.winning_bid + 1000
    print(auction.image1)
    context = {'auction': auction, 'auction_history': auction_history, 'min_bid': min_bid}
    return render(request, 'auction-detail.html', context)


def user_list_view(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'user-list.html', context=context)


def delete_user(request, user_id):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')
    
    if request.user.id == user_id:
        return render(request, 'no-authorization.html')
        
    user = User.objects.get(id=user_id)
    user.deleted_datetime = datetime.now()
    user.save()
    return HttpResponseRedirect(f'/user-list')


def take_authority(request, user_id):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')
    
    if request.user.id == user_id:
        return render(request, 'no-authorization.html')
        
    user = User.objects.get(id=user_id)
    user.has_permit = False
    user.save()
    return HttpResponseRedirect(f'/user-list')


def give_authority(request, user_id):
    if not request.user.is_admin:
        return render(request, 'no-authorization.html')
    
    if request.user.id == user_id:
        return render(request, 'no-authorization.html')
        
    user = User.objects.get(id=user_id)
    user.has_permit = True
    user.save()
    return HttpResponseRedirect(f'/user-list')


def auction_admin_view(request):
    auctions = Auction.objects.all()
    context = {'auctions': auctions}
    return render(request, 'auction-admin.html', context)


def update_auction_state(request, auction_id, state):
    auction = Auction.objects.get(id=auction_id)
    if state == 3:
        auction.state = '완료'
    elif state == 4:
        auction.state = '낙찰'
    elif state == 5:
        auction.state = '취소'
    auction.save()
    return HttpResponseRedirect('/admin/auction/')
