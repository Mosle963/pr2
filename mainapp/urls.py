from django.urls import path, include
from .views import home, account, post


urlpatterns = [
    path("", home.index, name="index"),
]

urlpatterns += [
    path(
        "account/<int:pk>/update",
        account.AccountUpdateView.as_view(),
        name="account_update",
    ),
    path(
        "account/<int:pk>/details",
        account.account_view,
        name="account_detail",
    ),
    path('toggle-trust-status/<int:user_id>/', account.toggle_trust_status, name='toggle_trust_status'),
    path('autocomplete-users/', account.autocomplete_users, name='autocomplete_users'),
    path('follow/<int:followee_id>', account.follow, name='follow')
]

urlpatterns += [
    path('create-post/', post.create_post, name='create_post'),
    path('edit-post/<int:pk>/', post.PostUpdateView.as_view(), name='post_update'),
    path('delete-post/<int:post_id>/', post.delete_post, name='delete_post'),
    path('update-status/<int:post_id>/', post.update_status, name='update_status'),
    path('refresh-status/<int:post_id>/', post.refresh_status, name='refresh_status'),
]