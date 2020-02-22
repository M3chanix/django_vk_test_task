from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import requests


def index(request):
    return render(request, 'vk_auth/button.html')

def get_vk_data(request):
    print(request.user)
    print("redirecting")
    return redirect("https://oauth.vk.com/authorize?client_id=7329149&display=page&redirect_uri=http://84.201.133.154/auth/get_user_info/&scope=friends&response_type=code&v=5.103")

def get_vk_code(request):
    code = request.GET["code"]
    print("code:", code)
    access_token_data = {"client_id":"7329149", "client_secret":"qX4MZgUvCmE8GcXZgRTT",
            "redirect_uri":"http://84.201.133.154/auth/get_user_info/", "code":code}
    access_token_response = requests.post("https://oauth.vk.com/access_token", data=access_token_data) 
    print("access token response:", access_token_response)
    access_token_json = access_token_response.json()
    access_token = access_token_json["access_token"]
    print("access_token:", access_token)
    user_info_data = {"user_id":access_token_json["user_id"], "access_token":access_token, "v":"5.103"}

    user_info_response = requests.post("https://api.vk.com/method/users.get", data=user_info_data)

    user_friends_data = {"user_id":access_token_json["user_id"],
            "order":"random", "count":"5", "fields":"first_name, last_name", "access_token":access_token, "v":"5.103"}
    user_friends_response = requests.post("https://api.vk.com/method/friends.get", data=user_friends_data)

    context = {'user':user_info_response.json()["response"][0], 'friend_list':user_friends_response.json()["response"]["items"]}
    return render(request, 'vk_auth/user_info.html', context)

