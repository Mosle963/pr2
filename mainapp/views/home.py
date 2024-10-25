from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import UserPassesTestMixin
from ..models import Post,Status,Account
from ..forms.home import CustomLoginForm
from ..forms.post import PostCreateForm
from django.template.loader import render_to_string
from django.http import JsonResponse

class SignUpView(UserPassesTestMixin, TemplateView):
    template_name = 'registration/signup.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')


class LoginView(UserPassesTestMixin, LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')



def index(request):
    nav = request.GET.get('nav', 'posts')
    
    if nav == 'verified':
        post_list = Post.objects.filter(status=Status.V.value)
    elif nav == 'disproven':
        post_list = Post.objects.filter(status=Status.DP.value)
    elif nav == 'following':
        current_user_account = Account.objects.get(user=request.user)
        query = """
            SELECT p.*
            FROM mainapp_post p
            JOIN mainapp_following f ON p.account_id = f.followee_id
            WHERE f.follower_id = %s
        """
        post_list = Post.objects.raw(query, [current_user_account.user_id])
    else:
        post_list = Post.objects.all()
    
    paginator = Paginator(post_list, 10)  # Show 10 posts per page
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    if int(page_number) > paginator.num_pages or int(page_number) < 1:
        page_obj.object_list = []
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {'page_obj': page_obj}
        html_content = render_to_string('mainapp/post/_posts_section.html', context, request=request)
        return JsonResponse({
            'content': html_content,
        })
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mainapp/index.html', context)

def info_view(request):
    return render(request, 'mainapp/info.html')


def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
