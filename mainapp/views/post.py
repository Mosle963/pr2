from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    ListView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Post,Account
from ..forms.post import PostUpdateForm, PostCreateForm
import json
from ..tasks import start_thread
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post.objects.create(account=request.user.account, post_text=content)
            start_thread(post.post_id, request.user.id)
            return JsonResponse({'success': True, 'post_id': post.post_id})
        return JsonResponse({'success': False, 'error': 'seems like you forgot to add your news..'})
    return JsonResponse({'success': False, 'error': 'UnknownError, please try again in a few moments'})

def update_status(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        new_status = data.get('new_status')
        checker_id = data.get('checker_id')
        post = get_object_or_404(Post, post_id=post_id)

        if new_status == 'approve':
            post.approve(checker_id)
        elif new_status == 'disapprove':
            post.disapprove(checker_id)
        else:
            post.reset()

        # Fetch updated checker and status info
        checker_url = post.checker.get_absolute_url() if post.checker else ''
        checker_name = str(post.checker) if post.checker else ''
        new_status = post.status
        return JsonResponse({
            'success': True,
            'new_status': new_status,
            'checker_url': checker_url,
            'checker_name': checker_name
        })

    return JsonResponse({'success': False})

def delete_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, post_id=post_id)
        post.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update Post information

    - redirect with Get[changed] set to 1 after sucessfully updateing
    - deny permission for any one but Post owner
    """

    model = Post
    form_class = PostUpdateForm
    template_name = "mainapp/post/post_update.html"

    def get_success_url(self):
        return reverse(
            "post_update", kwargs={"pk": self.object.post_id, "changed": 1}
        )

    def test_func(self):
        return self.get_object().account.user.id == self.request.user.id

    def form_valid(self, form):
        response = super().form_valid(form)
        start_thread(self.object.post_id, self.request.user.id)
        return response


