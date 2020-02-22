from django.apps import AppConfig
from authlib.django.client import OAuth


class VkAuthConfig(AppConfig):
    name = 'vk_auth'

    def ready(self):
        oauth = OAuth()

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
