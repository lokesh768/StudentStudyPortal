from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



# View : Home
def home(request):
    return render(request,'dashboard/home.html')

"""

   Views for Notes Section

"""

# View : Notes
@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)

        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        
        messages.success(request, f"Notes Added {request.user.username} Succesfully")
    
    else :
        form = NotesForm()
    
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

# View : Delete-Note
@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

# Class_based_View : Detailed View Of a Note

class NotesDetailView(generic.DetailView):
    model = Notes

"""
   
   Views For Home Work Section

"""
@login_required
def homework(request):

    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False

            # Saving Homeworks 
            homeworks=Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
            )
            homeworks.save()

            messages.success(request,f'Homework Added from {request.user.username}  Successfully!!')
            return redirect("homework")
    else :
        form = HomeworkForm()
    
    homework = Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done = True
    else :
        homework_done =  False
    context = {
        'homeworks':homework,
        'homeworks_done':homework_done,
        'form':form,
    }
    return render(request,'dashboard/homework.html',context)


@login_required
def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect("homework")


@login_required
def delete_homwork(request,pk=None):
    homework =  Homework.objects.get(id=pk)
    homework.delete()
    return redirect("homework")

"""
   
   Views For YouTube Section

"""
@login_required
def youtube(request):

    if request.method=="POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)

        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ""
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)

            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else :
        form = DashboardForm()
    context = {'form':form}
    return render(request,'dashboard/youtube.html',context)

"""
   
   Views For ToDo Section

"""
@login_required
def todo(request):

    if request.method=="POST":
        form = TodoForm(request.POST)

        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished=='on':
                    finished=True
                else :
                    finished=False
            except:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()

            messages.success(request,f'Todos Added from {request.user.username}  Successfully!!')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todos_done=True
    else:
        todos_done=False
    context = {
        'todos':todo,
        'form':form,
        'todos_done':todos_done
    }
    return render(request,'dashboard/todo.html',context)


@login_required
def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)

    if todo.is_finished == True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    
    todo.save()
    return redirect('todo')


@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

"""
   
   Views For Books Section

"""
@login_required
def books(request):

    if request.method=="POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),

            }
            result_list.append(result_dict)

            context = {
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else :
        form = DashboardForm()
    context = {'form':form}
    return render(request,'dashboard/books.html',context)

"""
   
   Views For Books Section

"""


@login_required
def dictionary(request):
    if request.method=="POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][1]['text']
            audio = answer[0]['phonetics'][1]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context={
                'form':form,
                'input':''
            }
        return render(request,'dashboard/dictionary.html',context)
    else :
        form = DashboardForm()
        context = {'form':form}
    return render(request,"dashboard/dictionary.html",context)


@login_required
def wiki(request):

    if request.method == "POST":
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form = DashboardForm()
        context = {'form':form }
    return render(request,'dashboard/wiki.html',context)


@login_required
def conversion(request):

    if request.method=="POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement']=='length':
            measurement_form = ConversionLengthForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                if input and int(input)>=0:
                    if first=='yard' and second=='foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first=='foot' and second=='yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }

        if request.POST['measurement']=='mass':
            measurement_form = ConversionMassForm()
            context = {
                'form':form,
                'm_form':measurement_form,
                'input':True
            }

            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                if input and int(input)>=0:
                    if first=='pound' and second=='kilogram':
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first=='kilogram' and second=='pound':
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }

    else:
        form = ConversionForm()
        context = {
        'form':form,
        'input':False
        }
    return render(request,'dashboard/conversion.html',context)


def register(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Hello {username}, Account Created Succesfully!!')
            return redirect("login")
    else :
        form = UserRegistrationForm()
    context={
       'form':form
    }
    return render(request,'dashboard/register.html',context)



@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)

    homework_done = True if len(homeworks)==0 else False
    todos_done = True if len(todos)==0 else False

    context = {
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }
    return render(request,"dashboard/profile.html",context)

# View : Logout
def logout_page(request):
    logout(request)
    return render(request,'dashboard/logout.html')


