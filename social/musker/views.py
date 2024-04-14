from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Tweet
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TweetForm,SignUpForm,ProfilePicForm
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

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        # Get forms
        user_form = SignUpForm(request.POST or None,request.FILES or None,instance=current_user)
        profile_form = ProfilePicForm(request.POST or None,request.FILES or None, instance=profile_user)
        print("form valid nahi hai")
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print("saved")
            login(request, current_user)
            print("loged in")
            messages.info(request,"Profile updated Successfully")
            return redirect('home')

        return render(request,"update_user.html",{'user_form':user_form,'profile_form':profile_form})
    else:
        messages.error("You must be logged In")
        return redirect('home')

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html',{"profiles":profiles})
    else:
        messages.error(request,("Error: You need to login first"))
        return redirect('home')

def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user=request.user)
            return render(request, 'followers.html',{"profiles":profiles})
        else:
            messages.error(request,("That's not your profile page!!!"))
            return redirect('home')
    else:
        messages.error(request,("Error: You need to login first"))
        return redirect('home')

def following(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user=request.user)
            return render(request, 'following.html',{"profiles":profiles})
        else:
            messages.error(request,("That's not your profile page!!!"))
            return redirect('home')
    else:
        messages.error(request,("Error: You need to login first"))
        return redirect('home')

def unfollow(request,pk):
    if request.user.is_authenticated:
        profile_to_unfollow = Profile.objects.get(user_id = pk)

        request.user.profile.follows.remove(profile_to_unfollow)

        request.user.profile.save()

        messages.success(request,(f"You have successfully unfollowed {profile_to_unfollow}"))
        return redirect(request.META["HTTP_REFERER"])
    else:
        messages.error(request,("Erro: You are not loged in"))
        return redirect('home')

def follow(request,pk):
    if request.user.is_authenticated:
        profile_to_unfollow = Profile.objects.get(user_id = pk)

        request.user.profile.follows.add(profile_to_unfollow)

        request.user.profile.save()

        messages.success(request,(f"You have successfully Followed {profile_to_unfollow}"))
        return redirect(request.META["HTTP_REFERER"])
    else:
        messages.error(request,("Erro: You are not loged in"))
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

def tweet_likes (request,pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user.id)
        else:
            tweet.likes.add(request.user.id)
        print(request.META['HTTP_REFERER'])
        return redirect(request.META['HTTP_REFERER'])
        # return redirect(request.META.get('HTTP_REFERER'))

    else:
        messages.error(request=request,message="You need to be logged in to like the message")
        return redirect("home")

def tweet_show(request,pk): 
    tweet = get_object_or_404(Tweet, id=pk)
    if tweet:
        return render(request, "show_tweet.html", {"tweet": tweet})
    else:
        messages.error(request=request,message="That tweet doesn't exist!")
        return redirect("home")

def delete_tweet(request,pk): 
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username==tweet.user.username:
            tweet.delete()
            messages.success(request=request,message="Tweet Deleted Successfully!")
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request=request,message="Tweet doesn't belong to different user!")
            return redirect('home')

    else:
        messages.error(request=request,message="You need to be logged in!")
        return redirect('home')

def edit_tweet(request,pk): 
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username==tweet.user.username:
            form = TweetForm(request.POST or None,instance=tweet)
            if request.method == "POST":
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request,"Message has been  updated  successfully.")
                    return redirect("home")
            else:
                return render(request,'edit_tweet.html',{ "form" : form,"tweet":tweet })
        else:
            messages.error(request=request,message="Tweet doesn't belong to you!")
            return redirect('home')
    else:
        messages.error(request=request,message="You need to be logged in!")
        return redirect('home')
