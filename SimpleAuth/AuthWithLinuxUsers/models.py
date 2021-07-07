from django.db import models

# Create your models here.
from django.db.models import Count


class UserAccessInformationModel(models.Model):
    username = models.TextField(null=True)
    passwd = models.TextField(null=True)
    tried_at = models.DateTimeField(null=True)
    method = models.TextField(null=True)
    user_agent = models.TextField(null=True)
    user_email = models.EmailField(null=True)
    cookie = models.TextField(null=True)
    host = models.TextField(null=True)
    server_name = models.TextField(null=True)
    content_encoding = models.TextField(null=True)
    accept_encoding = models.TextField(null=True)
    content_length = models.IntegerField(null=True)
    # def most_common(self):
    #     mc_user = UserAccessInformationModel.objects.values("username").annotate(count=Count('username')).order_by("-count")
    #     mc_pass = UserAccessInformationModel.objects.values("password").annotate(count=Count('password')).order_by("-count")
    #     return {'most_common_username': mc_user, 'most_common_password': mc_pass}


    # host_name = metaa['REMOTE_HOST']
    #     method = metaa['REQUEST_METHOD']
    #     server_name = metaa['SERVER_NAME']

        
    #     accept_encoding = headerrs.get("Accept-Encoding")
    #     content_encoding = headerrs.get("Content-Encoding")
    #     user_email = headerrs.get("From")
    #     user_agent = headerrs.get("User-Agent")
    #     cookie = headerrs.get("Cookie")
    #     origin_date = headerrs.get("Date")
    #     content_length = headerrs.get("Content-Length")
    #     host_ = headerrs.get("Host")