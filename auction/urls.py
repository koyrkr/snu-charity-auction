from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # 회원가입/로그인/인증
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('join/', views.join_view),
    path('join-admin/', views.join_admin_view),
    path('join-done/', views.join_done_view),
    path('join-admin-done/', views.join_admin_done_view),
    path('exit/', views.exit_view),
    path('mypage/', login_required(views.mypage_view)),
    path('user-update/', views.user_update),
    path('auction/', login_required(views.auction_view)),
    path('auction/apply/<int:auction_id>', login_required(views.auction_apply_view)),
    path('auction-history/', login_required(views.auction_history_view)),
    path('auction/create/', login_required(views.create_auction_view)),
    path('auction/modify/<int:auction_id>/', login_required(views.modify_auction_view)),
    path('auction/detail/<int:auction_id>/', login_required(views.auction_detail_view)),
    path('auction/detail/<int:auction_id>/delete/', login_required(views.delete_auction)),
    path('user-list/', views.user_list_view),
    path('user-list/<int:user_id>/delete/', views.delete_user),
    path('user-list/<int:user_id>/take_auth/', views.take_authority),
    path('user-list/<int:user_id>/give_auth/', views.give_authority),

    path('admin/auction/', login_required(views.auction_admin_view)),
    path('admin/auction/update-state/<int:auction_id>/<state>', login_required(views.update_auction_state)),

    path('api/join/', views.join),
    path('api/join-admin/', views.join_admin),
    path('api/auction/create/', views.create_auction),
    path('api/auction/modify/', views.modify_auction),
]

