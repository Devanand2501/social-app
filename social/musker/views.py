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