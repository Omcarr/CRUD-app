from django.http  import HttpResponse
from django.shortcuts import redirect


def unauth_user(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
          return view_func(request,*args,**kwargs)
    return wrapper

#decorater takes in a fucntion as a paramter, does what in the wrapper of decorater and then executes the function was decorated using it
#here we want to check is user is authenticated, if they are then simply execute the function which demanded them to be an auth user
#otherwise redirect them to page they can access without being authenticated

def allowed_user(allowed_roles=[]):
    def decorater(view_func):
        def wrapper(request,*args,**kwargs):
                group = None
                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name

                if group in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You are not authorized to view this page')
        return wrapper
    return decorater