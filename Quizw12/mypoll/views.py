from django.shortcuts import render

def index(request):
    return render(request,"mypoll/poll_index.html")