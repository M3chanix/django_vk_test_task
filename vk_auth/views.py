from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests


def index(request):
    return render(request, 'vk_auth/button.html')

def get_vk_data(request):
    return redirect("https://oauth.vk.com/authorize?client_id=7329149&display=page&redirect_uri=https://18.184.167.95/vk_auth/get_user_info/&scope=friends&response_type=code&v=5.103")

def get_vk_code(request):
    code = request.GET["code"]
    access_token_data = {"cleint_id":"7329149", "client_secret":"j7cilOYg0kv0sMvG1rsZ",
                         "redirect_uri":"https://18.184.167.95/vk_auth/get_user_info/", "code":code}
    access_token_response = requests.get("https://oauth.vk.com/access_token", data=get_data)
    access_token = access_token_response.json["access_token"]
    user_info_data = {"user_id":access_token_response.json["user_id"]}
    user_info_response = requests.get("https://api.vk.com/method/users.get", data=user_info_data)
    user_friends_data = {"user_id":access_token_response.json["user_id"],
                         "order":"random", "count":"5", "fields":"first_name, last_name"}
    user_friends_response = requests.get("https://api.vk.com/method/friends.get", data=user_friends_data)

    context = {'user':user, 'friend_list':friend_list}
    return render(request, 'vk_auth/user_info.html', context)
