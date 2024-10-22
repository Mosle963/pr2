from django.shortcuts import get_object_or_404, redirect, reverse,render
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from ..models import CustomUser, Account,Post,Status
from ..forms.account import AccountSignUpForm, AccountUpdateForm
from django.db.models import Q



def profile_view(request, pk):
    account = Account.objects.get(user_id=pk)
    nav = request.GET.get('nav', 'posts')
    
    if nav == 'verified':
        post_list = Post.objects.filter(checker=account, status=Status.V.value)
    elif nav == 'disproven':
        post_list = Post.objects.filter(checker=account, status=Status.DP.value)
    else:
        post_list = Post.objects.filter(account=account)
    
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
        'account': account,
        'page_obj': page_obj,
    }
    return render(request, 'mainapp/account/account_details.html', context)


class AccountSignUpView(UserPassesTestMixin, CreateView):
    """
    View to handle sign-up

    - redirect to home page after logging in
    - deny permission for already authenticated users and redirect them to home
    """

    model = CustomUser
    form_class = AccountSignUpForm 
    template_name = 'registration/account_signup_form.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')


class AccountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View to update Account information

    - redirect with Get[changed] set to 1 after sucessfully updateing
    - deny permission for any one but account owner
    """

    model = Account
    form_class = AccountUpdateForm
    template_name = 'mainapp/account/account_update.html'

    def get_success_url(self):
        return reverse(
        'account_detail',
        kwargs={
            'pk': self.object.user.id 
        }
    )
       
    def test_func(self):
        return self.get_object().user.id == self.request.user.id




@user_passes_test(lambda u: u.is_staff)
def toggle_trust_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_trusted = not user.is_trusted
    user.save()
    return redirect('account_detail', pk=user_id) 


def autocomplete_users(request):
    if 'query' in request.GET:
        query = request.GET.get('query', '')
        accounts = Account.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(user__email__icontains=query)
        )[:10]
        results = [{'username': f"{account.first_name} {account.last_name}", 'profile_url': account.get_absolute_url()} for account in accounts]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)
