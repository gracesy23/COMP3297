from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course, Module, Question, Quiz, Component
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
#from .forms import AddForm
from django.views import generic

class CourseView(generic.ListView):
    template_name = 'course/course.html'

    def get_queryset(self):
        return Course.objects.all()


class DetailView(generic.DetailView):
    model = Course
    template_name = 'course/detail.html'


class ModuleView(generic.DetailView):
    model = Module
    template_name = 'course/module.html'


"""def ModuleViewDef(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    return render (request, 'course/module.html', {'module': module })"""



class CourseCreate(CreateView):
    model = Course
    fields = ['name', 'instructor', 'email', 'type', 'description']

class ModuleCreate(CreateView):
    model = Module
    fields = ['name', 'course']

def AddCom(request, pk):

    com_id = request.POST.get('component_id')
    component = Component.objects.get(id=com_id)
    component.module_id=pk
    component.is_select=True
    component.save()
    context = {
        'component' : component,
        'module' : module,
    }
    return render(request, "course/try.html", context)

def addQuiz(request, pk):

    q_id = request.POST.get('quiz_id')
    quiz = Quiz.objects.get(id=q_id)
    quiz.module_id=pk
    quiz.is_select=True
    quiz.save()
    module = Module.objects.get(id=pk)
    module.have_quiz=True
    module.save()
    context = {
        'quiz' : quiz,
    }
    return render(request, "course/try.html", context)

"""class ComponentFormView(View):
    form_class = ComponentForm
    template_name = 'course/component_form.html/'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            component = form.save(commit=False)
            component.save()"""


"""from django.shortcuts import render, get_object_or_404
from .models import Course, Module


def index(request):
    all_courses=Course.objects.all()
    return render(request, 'course/course.html', {'all_courses': all_courses})

def detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render (request, 'course/detail.html', {'course': course})


def empty(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    try:
        selected_module = course.module_set.get(pk=request.POST['module'])
    except (KeyError, Module.DoesNotExist):
        return render (request, 'course/detail.html', {
            'course': course,
            'error_message': "You did not select a valid module",
        })
    else:
        selected_module.is_empty=True
        selected_module.save()
        return render (request, 'course/detail.html', {'course': course})"""
