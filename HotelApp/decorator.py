from django.shortcuts import redirect

def checksuperuser(fun):
    def innerfun(request):
        if request.user.is_superuser == True:
            return fun(request)
        else:
            return redirect('bookingurl')
    return innerfun