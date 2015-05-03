from django.shortcuts import redirect

def homepage(request):
    # if request.user == None:
    #     return redirect('/accounts/login/')
    user = request.user
    if user.is_authenticated():
        try:
            if user.student:
                return redirect('/courses/student/')
        except:
            pass

        try:
            if user.teacher:
                return redirect('/courses/teacher/')
        except:
            pass

        try:
            if user.manager:
                return redirect('/courses/manager/')
        except:
            pass
    else:
        return redirect('/accounts/login/')
