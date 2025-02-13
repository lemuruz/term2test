from django.shortcuts import render

def index(request):
    polls = None
    return render(request,"mypoll/poll_index.html",{'polls' : polls})