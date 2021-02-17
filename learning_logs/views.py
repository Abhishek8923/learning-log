from django.shortcuts import render,redirect,get_object_or_404
from .forms import TopicForm,EntryForm
from .models import Topic,Entry
from django.contrib.auth.decorators import login_required 
from django.http import Http404
# Create your views here.

def check_topic_owner(topic,request):
    if topic.owner != request.user:
        raise Http404

def index(request):
    """the homepage for learning_log"""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """to display all the topics"""
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics':topics}
    return render(request,'learning_logs/topics.html',context)    

@login_required
def topic(request,topic_id):
    topic=get_object_or_404(Topic,id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)    

@login_required
def new_topic(request):
    """to add new topic"""
    if request.method != 'POST':
        # if no data submitted create a blank form
        form=TopicForm()
    else:
        #POST data submitted process data
        form=TopicForm(data=request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    #display a blank or invalid form
    context={'form':form}
    return render(request,'learning_logs/new_topic.html',context)            

@login_required        
def new_entry(request,topic_id):
    """add a new entry for a particular topic"""
    topic=Topic.objects.get(id=topic_id)
    check_topic_owner(topic,request)    

    if request.method != 'POST':
        #create a blank form
        form=EntryForm()
    else:
        #submitting a form
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)  

    #for blank or invalid form
    context={'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)          

@login_required
def edit_entry(request,entry_id):
    """edit exesting entry"""
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    #if topic.owner != request.user:
        #raise Http404
    check_topic_owner(topic,request)    

    if request.method != 'POST':
        form=EntryForm(instance=entry)
    else:
        #post data submitted
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    #for new or invalid form
    context={'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)