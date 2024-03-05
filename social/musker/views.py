from django.shortcuts import render,redirect
from .models import Profile,Tweet
from django.contrib import messages
from .forms import TweetForm,SignUpForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request,"Message has been sent successfully")
                return redirect("home")

        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request,'index.html',{"tweets":tweets,"form":form})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request,'index.html',{"tweets":tweets})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successfully logged in")
            return redirect("home")
        else:
            messages.error(request,"Failed to log in")
            return redirect("login")

    else:
        return render(request,'login.html',{})

def user_logout(request):
    logout(request)
    messages.success(request,"You have successfully logged out")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"WELCOME!!!")
            return redirect('home')
    return render(request,'register.html',{'form':form})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html',{"profiles":profiles})
    else:
        messages.error(request,("Error: You need to login first"))
        return redirect('home')

def profile(request,pk):
    if request.user.is_authenticated:
        my_profile = Profile.objects.get(user_id = pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            current_profile_user = request.user.profile
            
            action = request.POST.get('follow')
            print("hello")

            if action == "unfollow":
                current_profile_user.follows.remove(my_profile)
            elif action == "follow":
                current_profile_user.follows.add(my_profile)
            current_profile_user.save()
        return render(request,'profile.html',{ "my_profile" : my_profile,"tweets":tweets })
    else:
        messages.error(request,("Erro: You are not loged in"))
        return redirect('home')