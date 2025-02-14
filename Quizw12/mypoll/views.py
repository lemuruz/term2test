from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Choice,Poll
def index(request):
    polls = Poll.objects.all()
    return render(request,"mypoll/poll_index.html",{'polls' : polls})

def vote_page(request,poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    return render(request,"mypoll/poll_choose.html",{'poll' : poll,
                                                    'choices' : choices})

def vote(request):
    if request.method == "POST":
        choice_name = request.POST.get("choice")
        choice = get_object_or_404(Choice, name=choice_name)
        choice.vote_count += 1
        choice.save()
        return redirect('mypoll:result', poll_id=choice.poll.id)
    return JsonResponse({"error": "Invalid request"}, status=400)

def result(request,poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    return render(request,"mypoll/poll_result.html",{'poll' : poll,
                                                    'choices' : choices})
