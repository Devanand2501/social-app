from django.shortcuts import render,redirect
from .models import Profile
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'index.html',{})


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

        if request.method == "POST":
            current_profile_user = request.user.profile
            
            action = request.POST.get('follow')
            print("hello")

            if action == "unfollow":
                current_profile_user.follows.remove(my_profile)
            elif action == "follow":
                current_profile_user.follows.add(my_profile)
            current_profile_user.save()
        return render(request,'profile.html',{ "my_profile" : my_profile })
    else:
        messages.error(request,("Erro: You are not loged in"))
        return redirect('home')