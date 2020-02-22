from django.db import models

class OAuth2Token(models.Model):
    name = models.CharField(max_length=40)
    token_type = models.CharField(max_length=40)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expires_at = models.IntegerField()
    user_id = models.CharField(max_length=40)

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
            user_id=self.user_id
        )

class Token(models.Model):
    user_id = models.CharField(max_length=40, primary_key=True)
    access_token = models.CharFiled(masx_length=200)
    expires_at = models.IntegerField()
