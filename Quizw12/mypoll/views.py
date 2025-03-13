from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Choice,Poll
def index(request):
    polls = Poll.objects.filter(private = False)

    classify = pollclassify(polls)

    return render(request,"mypoll/poll_index.html",{'pageHead' : "All Polls",
                                                    'normalPoll' : classify[0],
                                                    'warmPoll' : classify[1],
                                                    'hotPoll' : classify[2]})

def privatePoll(request):
    polls = Poll.objects.filter(private = True)

    classify = pollclassify(polls)

    return render(request,"mypoll/poll_index.html",{'pageHead' : "Private Polls",
                                                    'normalPoll' : classify[0],
                                                    'warmPoll' : classify[1],
                                                    'hotPoll' : classify[2]})

def pollclassify(polls):
    warmPoll = []
    hotPoll = []
    normalPoll = []
    for poll in polls:
        choices = Choice.objects.filter(poll=poll)
        sumOfVote = []
        for choice in choices:
            sumOfVote.append(int(choice.vote_count))
        if sum(sumOfVote) >= 50:
            hotPoll.append(poll)
        elif sum(sumOfVote) >= 10:
            warmPoll.append(poll)
        else:
            normalPoll.append(poll)
        
    return [normalPoll,warmPoll,hotPoll,]

def vote_page(request,poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    return render(request,"mypoll/poll_choose.html",{'poll' : poll,
                                                    'choices' : choices,
                                                    'poll_id' : poll_id})

def vote(request):
    if request.method == "POST":
        choice_name = request.POST.get("choice")
        poll_id = request.POST.get("poll_id")
        choice = get_object_or_404(Choice, name=choice_name,poll = get_object_or_404(Poll, id=poll_id))
        choice.vote_count += 1
        choice.save()
        return redirect('mypoll:result', poll_id=choice.poll.id)
    return JsonResponse({"error": "Invalid request"}, status=400)

def result(request,poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = Choice.objects.filter(poll=poll)
    

    return render(request,"mypoll/poll_result.html",{'poll' : poll,
                                                'choices' : choices})

