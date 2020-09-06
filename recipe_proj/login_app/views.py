# from django.shortcuts import render, redirect, HttpResponse
# from login_app.models import User
# from django.contrib import messages
# import bcrypt

# # Create your views here.
# def login(request):
#     if request.method == 'POST':
#         print("reached login method")
#         this_user = User.objects.filter(username=request.POST['username'])
#         if this_user:
#             logged_user = this_user[0]
#             if bcrypt.checkpw(request.POST['password'].encode('utf8'), logged_user.password.encode('utf8')):
#                 print('successful login')
#                 request.session['userid'] = logged_user.id
#                 request.session['username'] = logged_user.username
#         return redirect('/')
#     return render(request,"login.html")

# def register(request):
#     if request.method == "POST":
#         errors = User.objects.validate(request.POST)
#         if len(errors) > 0:
#             for value in errors.values():
#                 messages.error(request, value)
#             return redirect('')
#         pw = request.POST['password']  # helper variable to keep things readable
#         pw_hash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt()).decode()
#         this_user = User.objects.create(first_name=request.POST['first_name'],
#                                         last_name=request.POST['last_name'],
#                                         email=request.POST['email'],                    
#                                         password=pw_hash)
#         request.session['userid']=this_user.id
#         return redirect('../')
#     return render(request,"registration.html")

