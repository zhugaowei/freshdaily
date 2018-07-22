from django.shortcuts import redirect,HttpResponse
from django.http import HttpResponseRedirect

def login(func):
    def login_fun(request,*args,**kwargs):
        print(3)
        if request.session.has_key('user_id'):
            print(1)
            return func(request,*args,**kwargs)

        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url',request.get_full_path())
            print(2)
            return red
    return login_fun