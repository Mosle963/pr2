from django.urls import path, include
from .views import home, account, post


urlpatterns = [
    path("", home.index, name="index"),
]

urlpatterns += [
    path(
        "account/<int:pk>/update/<int:changed>",
        account.AccountUpdateView.as_view(),
        name="account_update",
    ),
    path(
        "account/<int:pk>/details",
        account.profile_view,
        name="account_detail",
    ),
]

urlpatterns += [
    path('update-status/<int:post_id>/', post.update_status, name='update_status'),
    path('delete-post/<int:post_id>/', post.delete_post, name='delete_post'),
    path('edit-post/<int:pk>/<int:changed>', post.PostUpdateView.as_view(), name='post_update'),
    path('create-post/', post.create_post, name='create_post')
    

]


'''
urlpatterns += [
    path(
        "post/create",
        post.PostCreateView.as_view(),
        name="post_create",
    ),
    path(
        "post/<int:pk>/update/<int:changed>",
        post.PostUpdateView.as_view(),
        name="post_update",
    ),
    path(
        "post/<int:pk>/details",
        post.PostDetailView.as_view(),
        name="post_detail",
    ),
    path("post/list", post.PostListView.as_view(), name="post_list"),
    path(
        "post/list/mine",
        post.Post_Account_ListView.as_view(),
        name="post_account_list",
    ),
    path(
        "post/<int:pk>/delete",
        post.PostDeleteView.as_view(),
        name="post_delete",
    ),
]
'''