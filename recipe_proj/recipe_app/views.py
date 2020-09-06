from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from recipe_app.models import *
import bcrypt,random

def register(request):
    if request.method == "POST":
        errors = User.objects.validate(request.POST)
        if len(errors) > 0:
            for value in errors.values():
                messages.error(request, value)
            return redirect('')
        pw = request.POST['password']  # helper variable to keep things readable
        pw_hash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt()).decode()
        this_user = User.objects.create(first_name=request.POST['first_name'],
                                        last_name=request.POST['last_name'],
                                        username=request.POST['username'],
                                        email=request.POST['email'],                    
                                        password=pw_hash)
        request.session['userid']=this_user.id
        return redirect('/')
    return render(request,"registration.html")


def login(request):
    if request.method == 'POST':
        print("reached login method via POST")
        this_user = User.objects.filter(username=request.POST['username'])
        if this_user:
            logged_user = this_user[0]
            if bcrypt.checkpw(request.POST['password'].encode('utf8'), logged_user.password.encode('utf8')):
                print('successful login')
                request.session['userid'] = logged_user.id
                request.session['username'] = logged_user.username
        return redirect('/')
    print("reached login via GET")
    return render(request,"login.html")


def index(request):
    if 'userid' in request.session:
        recipe_ids=Recipe.objects.all().values_list('id', flat=True)
        this_id=random.choice(recipe_ids)
        context={
            "recipe":Recipe.objects.get(id=this_id),
        }
        return render(request, "index.html",context)
        # return render(request,"index.html")
    else:
        return redirect('./login')


def all_recipes(request):
    context={
        "recipes":Recipe.objects.all(),
    }
    return render(request,"all_recipes.html",context)


def detail(request,id):
    # return HttpResponse(f"placholder for recipe #{id} detail.html")
    context={
        "recipe":Recipe.objects.get(id=id),
    }
    return render(request,"detail.html",context)


def logout(request):
    request.session.flush()
    return redirect('/')


def create(request):
    if request.method=="POST":
        creator=User.objects.get(id=request.session['userid'])
        title=request.POST['title']
        this_recipe=Recipe(title=title,creator=creator)
        this_recipe.save()
        # process ingredient list
        ingredient_list=request.POST.getlist('ingredients[]')
        for x in ingredient_list:      
            this_ingredient=Ingredient(content=x,recipe=this_recipe)
            this_ingredient.save()
        print("saved ingredients")
        # process step list
        step_list=request.POST.getlist('steps[]')
        for x in step_list:      
            this_step=Step(content=x,recipe=this_recipe)
            this_step.save()
        print("saved steps, processed recipe submission")
        return redirect('/')
    return render(request,"create.html")


def review(request,id):
    if request.method=="POST":
        recipe=Recipe.objects.get(id=id)
        content=request.POST['content']
        poster=User.objects.get(id=request.session['userid'])
        this_review=Review(content=content,poster=poster,recipe=recipe)
        this_review.save()
        print("saved a review!")
        return redirect('/')

    context={
        "recipe":Recipe.objects.get(id=id)
    }
    return render(request,"review.html",context)
    

def edit_account(request,id):
    if request.method == "POST":
        this_user=User.objects.get(id=id)
        first_name= request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        this_user.first_name=first_name
        this_user.save()
        return redirect('/')
    #else if GET, render the form to user
    context={
        "user":User.objects.get(id=id)
    }
    return render(request,"myaccount.html",context)

def edit_recipe(request,id):
    