import threading
import requests
from django.utils.timezone import now
from .models import Post, CustomUser
import time
import random


def check_true_prob(post_id, user_id):

    post = Post.objects.get(pk=post_id)
    user = CustomUser.objects.get(pk=user_id)
    account = user.account

    if account.last_api_call:
        time_since_last_call = now() - account.last_api_call
        if time_since_last_call.total_seconds() < 60:
            variance = random.randint(10, 30)
            time.sleep(variance)

    response = requests.post('https://svuites23pr601.pythonanywhere.com/api/predict/',
        json={'text': post.post_text})
    print("response",response)
    account.last_api_call = now()
    account.save(update_fields=['last_api_call'])
    if response.status_code == 200:
        data = response.json()
        post.true_prob = data['true_prob']
        post.save(update_fields=['true_prob'])
        post.set_status()
    elif response.status_code == 400:
        start_thread(post_id,user_id)


def start_thread(post_id, user_id):
    threading.Thread(target=check_true_prob, args=(post_id, user_id)).start()