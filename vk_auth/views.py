from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import requests
import authlib.integrations.django_client as authl

oauth = authl.OAuth()

oauth.register(
    name='vk',
    client_id='7329149',
    client_secret='qX4MZgUvCmE8GcXZgRTT',
    access_token_url='https://oauth.vk.com/access_token',
    access_token_params=None,
    authorize_url='https://oauth.vk.com/authorize',
    authorize_params=None,
    api_base_url='https://api.vk.com/method/',
    client_kwargs={'v':'5.103'},
)


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
            token = OAuth2Token.find(name='github', user_id=request.session["user_id"])
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
            #print("redirecting")
            #return redirect("https://oauth.vk.com/authorize?client_id=7329149&display=page&redirect_uri=http://84.201.133.154/auth/get_user_info/&scope=friends&response_type=code&v=5.103")
    else:
        return HttpResponse("Please enable cookies and try again")

def login(request):
        vk = oauth.create_client('vk')
        redirect_uri = 'http://84.201.133.154/auth/authorize/'
        return vk.authorize_redirect(request, redirect_uri, client_id='7329149')
        #return redirect('https://oauth.vk.com/authorize?client_id=7329149&redirect_uri=http://84.201.133.154/auth/authorize/')

def authorize(request):
        vk = oauth.create_client('vk')
        redirect_uri = 'http://84.201.133.154/auth/get_user_info/'
        token = oauth.vk.authorize_access_token(request)
        request.session['user_id'] = token.to_token()['user_id'] 
        #записать токен(если он сам не записывается в базу) и вернуть пользователя для сохранения в куки
        # перейти к пооучению и отрисовке данных из вк
        return redirect('get_vk_data')

def get_vk_data(request):
        token = OAuth2Token.find(name='vk', user_id=request.session['user_id'])
        user_info_data = {'user_id':request.session['user_id']}
        user_info_resp = oauth.vk.post('users.get', token=token.to_token(), data=user_info_data)
        friends_info_data = {'user_id':request.session['user_id'], 'count':'5', 'fields':'first_name, last_name'}
        friends_info_resp = oauth.vk.post('friends.get', token=token.to_token(), data=friends_info_data)
        context = {'user':user_info_resp.json()[0], 'friend_list':friends_info_resp.json()['response']['items']}
        return render(request, 'vk_auth/user_info.html', context)


