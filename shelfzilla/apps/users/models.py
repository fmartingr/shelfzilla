from hashlib import md5
from django.contrib.auth.models import User as UserModel


class User(UserModel):
    @property
    def avatar(self):
        avatar = '{}{}?s=300'.format(
            'http://www.gravatar.com/avatar/',
            md5(self.email.lower()).hexdigest()
        )
        return avatar

    class Meta:
        proxy = True
