from django.shortcuts import render
from django.db.models import Max
from .forms import ChangeForm
from .forms import AddForm
from .models import *

# Create your views here.
def learner(request, id):

	learner = Learner.objects.filter(learnerID = id)
	courses = []
	for a in learner:
		temp = Temp()
		name = a.learnerName
		course = Course.objects.filter(courseID = a.takecourse)
		for c in course:
			temp.courseID = c.courseID
			temp.title = c.title
			temp.progress = a.progress
		courses.append(temp)
	context = {
		'lid': id,
		'name': name,
		'courses': courses
	}
	
	return render(request, 'learner.html', context)
	
def instructor(request):
	
	return render(request, 'instructor.html')
	
def course(request,p,cid,lid):
	learner = Learner.objects.get(takecourse = cid, learnerID = lid)
	course = Course.objects.filter(courseID = cid)
	avamodules = []
	unavamodules = []
	i = 0
	n = 0
	p = int(p)
	learner.progress = p
	learner.save()
	for a in course:
		mod = ModuleT()
		if i <= p:
			title = a.title
			mod.modID = a.contains_modules
			mod.counter =  i+1
			i = i+1
			avamodules.append(mod)
		else:
			mod.modID = a.contains_modules
			mod.counter =  i+1
			i = i+1
			unavamodules.append(mod)
	
	context = {
		'title': title,
		'avamodules': avamodules,
		'unavamodules':unavamodules,
		'counter': n,
		'cid':cid,
		'p':p,
		'lid':lid
	}
	
	return render(request, 'course.html', context)
	
def module(request, lid,mid,cid,p):
	
	module = Module.objects.filter(moduleID = mid)
	components = []
	for a in module:
		title = a.moduleTitle
		quiz = a.containsQuiz
		component = Component.objects.filter(compID = a.containsComp)
		for c in component:
			components.append(c)
	
	context = {
		'components':components,
		'quiz':quiz,
		'title': title,
		'p':p,
		'cid': cid,
		'lid':lid
	}
	
	return render(request, 'module.html', context)
	
def quiz(request, lid,qid, cid, p):

	quiz = Quiz.objects.filter(quizID = qid)
	questions = []
	for a in quiz:
		question = Question.objects.get(questionID = a.questionID)
		questions.append(question)
	
	i = int(p)
	i = i+1
	p = str(i)
	context = {
		'questions':questions,
		'cid':cid,
		'p':p,
		'lid':lid
	}
	
	return render(request, 'quiz.html', context)
	
def instructor(request, iid, cid):
		
	course = Course.objects.filter(courseID = cid)
	modules = []
	i = 0
	for a in course:
		mod = ModuleT()
		title = a.title
		mod.modID = a.contains_modules
		mod.counter =  i+1
		i = i+1
		modules.append(mod)
		
	
	context = {
		'title': title,
		'modules': modules,
		'cid':cid,
		'iid':iid
	}
	
	return render(request, 'courseIns.html', context)	
	
def createModule(request,iid,cid):
	mid = Module.objects.all().latest('moduleID')
	course = Course.objects.filter(courseID = cid)
	newmid = mid.moduleID + 1
	for c in course:
		title = c.title
		created_by = c.created_by
	newcourse = Course.objects.create(courseID = cid, title = title, created_by = created_by, contains_modules = newmid)
	mod = Module.objects.create(moduleID = newmid,moduleTitle = 'Unnamed',containsComp = 0, containsQuiz = 0)
	
	return instructor(request, iid, cid)
	
def moduleIns(request, mid):
	
	module = Module.objects.filter(moduleID = mid)
	components = []
	form1 = ChangeForm()
	form2 = AddForm()
	for a in module:
		title = a.moduleTitle
		quiz = a.containsQuiz
		component = Component.objects.filter(compID = a.containsComp)
		for c in component:
			components.append(c)
	
	context = {
		'components':components,
		'quiz':quiz,
		'title': title,
		'mid':mid,
		'form1':form1,
		'form2':form2
	}
	
	return render(request, 'moduleIns.html', context)
	
def changeModName(request,mid):
	form = ChangeForm(request.POST)
	if form.is_valid():
		module = Module.objects.filter(moduleID = mid)
		title = form.cleaned_data['MN']
		for m in module:
			m.moduleTitle = title
			m.save()
	
	return moduleIns(request, mid)
	
def addComp(request,mid):
	form = AddForm(request.POST)
	if form.is_valid():
		newmod = Module()
		module = Module.objects.filter(moduleID = mid)
		for m in module:
			newmod.moduleID = m.moduleID
			newmod.moduleTitle = m.moduleTitle
			newmod.containsQuiz = m.containsQuiz
		newmod.containsComp = form.cleaned_data['MN']
		newmod.save()
	
	return moduleIns(request, mid)
		
def addQuiz(request,mid):
	form = AddForm(request.POST)
	if form.is_valid():
		quiz = form.cleaned_data['MN']
		module = Module.objects.filter(moduleID = mid)
		for m in module:
			m.containsQuiz = quiz
			m.save()
	
	return moduleIns(request, mid)
		
	
		
		
		
		
		