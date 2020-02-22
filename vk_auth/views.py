from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import requests
from vk_auth.models import Token


def index(request):
    #set test cookies
    request.session.set_test_cookie()
    return render(request, 'vk_auth/button.html')

def check_auth(request):
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        #check user_id from cookies
        if "user_id" in request.session:
            #получить токен из базы по имени и пользователю
            token = Token.objects.get(user_id=request.session["user_id"])
            if token is not None:
                #перейти к получению и отрисовке данных из vk
                return redirect('get_vk_data')
            else:
                #перейти к авторизации и получению токена
                return redirect('login')
                #передать присвоенный user_id в cookie
        else:
            #перейти к авторизации и получению токена
            return redirect('login')
            #передать присвоенный user_id в cookie
    else:
        return HttpResponse("Please enable cookies and try again")


def login(request):
        redirect_uri = 'http://84.201.133.154/auth/authorize/'
        client_id = '7329149'
        #return redirect('https://oauth.vk.com/authorize', 
        #        data={'client_id':client_id, 'redirect_uri':redirect_uri})
        return redirect('https://oauth.vk.com/authorize?client_id=7329149&display=page&redirect_uri=http://84.201.133.154/auth/authorize/&scope=friends&response_type=code&v=5.103')


def authorize(request):
        code = request.GET['code']
        redirect_uri = 'http://84.201.133.154/auth/authorize/'
        client_id = '7329149'
        client_secret = 'qX4MZgUvCmE8GcXZgRTT'
        response = requests.post('https://oauth.vk.com/access_token', data={'code':code, 'redirect_uri':redirect_uri, 
                                                                        'client_id':client_id, 'client_secret':client_secret})
        response = response.json()
        token = Token(user_id=response['user_id'], access_token=response['access_token'], expires_in=response['expires_in'])
        token.save()
        request.session['user_id'] = response['user_id']
        #записать токен(если он сам не записывается в базу) и вернуть пользователя для сохранения в куки
        # перейти к пооучению и отрисовке данных из вк
        return redirect('get_vk_data')

def get_vk_data(request):
        user_id = request.session['user_id']
        access_token = Token.objects.get(user_id=user_id).access_token
        user_info_data = {'user_id':user_id, 'access_token':access_token, 'v':'5.103'}
        user_info_resp = requests.post('https://api.vk.com/method/users.get', data=user_info_data)
        friends_info_data = {'user_id':user_id, 'count':'5', 'fields':'first_name, last_name', 'v':'5.103', 'access_token':access_token}
        friends_info_resp = requests.post('https://api.vk.com/method/friends.get', data=friends_info_data)
        context = {'user':user_info_resp.json()['response'][0], 
                'friend_list':friends_info_resp.json()['response']['items']}
        return render(request, 'vk_auth/user_info.html', context)


