from django.shortcuts import render
import random
from django.db.models import Max
from .forms import ChangeForm
from .forms import AddForm
from .models import *
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.core.mail import send_mail
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from decimal import Decimal


#token check page
def newaccount(request):
	if request.method == "POST":
		form = request.POST
		temp = form.get('token')
		counter = 0
		token = Token.objects.filter(token = temp)
		for a in token:
			counter = counter + 1
		if counter == 1:
			token = Token.objects.get(token = temp)
			context = {
				'Token':token
			}
			return render(request,'registration.html',context)
		else:
			return render(request,'wrongtoken.html')
	else:
		return render(request,'token.html')

def instructor_reg_sup(request,iid):
	form = request.POST
	instructor = InstructorInfo()
	instructor.instructorID = iid
	instructor.first_name = form.get('FirstName')
	instructor.last_name = form.get('LastName')
	fullname = instructor.first_name + ' ' + instructor.last_name
	instructor.intro = form.get('self_intro')
	instructor.save()
	instructor = Instructor.objects.get(instructorID = iid)
	instructor.name = fullname
	instructor.save()
	return render(request,'regsucc.html')

#role: 1 for learner 2 for ins 3 for admin
#django sign_up
class SignUp(generic.CreateView):
	form_class = UserCreationForm
	def get_success_url(self,*args):
		return reverse('registrate', kwargs={'username': self.object.username,'token':self.kwargs['token']})
	template_name = 'signup.html'

def newaccount_sup(request,username,token):
		id = token
		token = Token.objects.get(token = id)
		if token.role == 1:
			staff = Staff.objects.get(staffID = token.staffID)
			if Progress.objects.all().count()!=0:
				learner = Progress.objects.all().order_by('learnerID').last()
				lid = learner.learnerID + 1
			else:
				lid = 1
			temp = UserLogin()
			temp.username = username
			temp.role = 1
			temp.userID = lid
			temp.save()
			temp = Progress()
			temp.learnerID = lid
			temp.takecourse = 0
			temp.progress = 0
			temp.learnerName = staff.first_name
			temp.save()
			temp = Learner()
			temp.email = staff.email
			temp.first_name = staff.first_name
			temp.last_name = staff.last_name
			temp.learnerID = lid
			temp.save()
			token.delete()
			return render(request,'regsucc.html')
		else:
			if Instructor.objects.all().count()!=0:
				instructor = Instructor.objects.all().order_by('instructorID').last()
				iid = instructor.instructorID + 1
			else:
				iid = 1
			temp = UserLogin()
			temp.username = username
			temp.role = 2
			temp.userID = iid
			temp.save()
			temp = Instructor()
			temp.instructorID = iid
			temp.name = username
			temp.create_course = 0
			temp.save()
			token.delete()
			context = {
				'iid':iid
			}
			return render(request,'Instructor_reg_sup.html',context)

def learner_signup(request):
	if(request.method == "POST"):
		form = request.POST
		staff = Staff.objects.filter(staffID = form.get('staffID'))
		counter = 0
		for a in staff:
			counter = counter + 1
		if counter == 1:
			staff = Staff.objects.get(staffID = form.get('staffID'))
			address = staff.email
			temp = ''
			for x in range(6):
				temp = temp + str(random.randint(1,9))
			while Token.objects.filter(token = temp).exists():
				temp = ''
				for x in range(6):
					temp = temp + str(random.randint(1,9))
			token = Token()
			token.token = temp
			token.role = 1
			token.staffID = staff.staffID
			token.save()
			msg = 'You have just applied for ICE learner account. Your token is: '
			msg = msg + temp
			msg = msg + '\n' + 'Please go to this link to complete the registration:\n'
			msg = msg + '127.0.0.1:8000/newaccount \n'
			send_mail(
			'ICE learner registration',
			msg,
			'ICE@gmail.com',
			[address],
			fail_silently=False,
			)
			return render(request,'appsucc.html')
		else:
			return render(request,'appfail.html')
	else:
		return render(request,'learner_apply.html')

#learner homepage
def redirect(request):
	name = request.user.username
	user = UserLogin.objects.get(username = name)
	if user.role == 1:
		return learner(request, user.userID)
	elif user.role == 2:
		return instructorHome(request,user.userID)
	else:
		return administrator(request)

def sendmail(request):
	form = request.POST
	address = form.get('email')
	temp = ''
	for x in range(6):
		temp = temp + str(random.randint(1,9))
	while Token.objects.filter(token = temp).exists():
		temp = ''
		for x in range(6):
			temp = temp + str(random.randint(1,9))
	token = Token()
	token.token = temp
	token.role = 2
	token.staffID = 0
	token.save()
	msg = 'You are invited to join the ICE as instructor. Your token is: '
	msg = msg + temp
	msg = msg + '\n' + 'Please go to this link to complete the registration:\n'
	msg = msg + '127.0.0.1:8000/newaccount \n'
	send_mail(
	'ICE instructor invitation',
	msg,
	'ICE@gmail.com',
	[address],
	fail_silently=False,
	)
	return administrator(request)

def administrator(request):
	return render(request,'admin.html')

def loggedout(request):
	return render(request,'loggedout.html')

@login_required
def learner(request, id):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	id = int(id)
	if temp.role == 1 and temp.userID == id:
		learner = Progress.objects.filter(learnerID = id)
		courses = []
		passed = []
		for a in learner:
			temp = Temp()
			name = a.learnerName
			if a.takecourse != 0:
				temp.pass_date = a.pass_date
				course = Course.objects.filter(courseID = a.takecourse)
				for c in course:
					temp.courseID = c.courseID
					temp.title = c.title
					temp.progress = a.progress
				if a.progress < 100:
					courses.append(temp)
				else:
					passed.append(temp)
		context = {
			'lid': id,
			'name': name,
			'courses': courses,
			'passed':passed
		}

		return render(request, 'learner.html', context)
	else:
		return render(request, 'badlogin.html')

@login_required
def course(request,p,cid,lid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	lid = int(lid)
	if temp.role == 1 and temp.userID == lid:
		learner = Progress.objects.get(takecourse = cid, learnerID = lid)
		course = Course.objects.filter(courseID = cid)
		avamodules = []
		unavamodules = []
		check = 0
		if p == 0:
			check = 1
		i = 0
		n = 0
		p = int(p)
		learner.progress = p
		learner.save()
		for a in course:
			mod = ModuleT()
			title = a.title
			if a.contains_modules != 0:
				n = n + 1
				mod.counter = n
				if i <= p:
					allmod = Module.objects.filter(moduleID = a.contains_modules)
					for b in allmod:
						mod.modID = b.moduleID
						mod.title =  b.moduleTitle
					avamodules.append(mod)
					i = i + 1
				else:
					allmod = Module.objects.filter(moduleID = a.contains_modules)
					for b in allmod:
						mod.modID = b.moduleID
						mod.title =  b.moduleTitle
					unavamodules.append(mod)
					i = i + 1
		if p == n:
			learner.progress = 100
			learner.pass_date = datetime.datetime.now()
			learner.save()
			learnername = learner.learnerName
			learner = Learner.objects.get(learnerID = lid)
			address = learner.email
			msg = 'You have completed the course '
			msg = msg + title
			msg = msg + '\n' + 'CECU units have been awarded accordingly.\n'
			msg = msg + 'Congratulations!\n'
			send_mail(
			'ICE course complete',
			msg,
			'ICE@gmail.com',
			[address],
			fail_silently=False,
			)
		context = {
			'title': title,
			'avamodules': avamodules,
			'unavamodules':unavamodules,
			'counter': n,
			'cid':cid,
			'p':p,
			'lid':lid,
			'check':check
		}

		return render(request, 'course.html', context)
	else:
		return render(request,'badlogin.html')

@login_required
def module(request, lid,mid,cid,p,counter):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	lid = int(lid)
	if temp.role == 1 and temp.userID == lid:
		module = Module.objects.filter(moduleID = mid)
		components = []
		quizAvail = 0
		if int(p) < int(counter):
			quizAvail = 1
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
			'lid':lid,
			'check':quizAvail
		}

		return render(request, 'module.html', context)
	else:
		return render(request,'badlogin.html')

def loadComp(request):
	lid = request.GET.get('lid', 0)
	mid = request.GET.get('mid', 0)
	cid = request.GET.get('cid', 0)
	p = request.GET.get('p', 0)
	counter = request.GET.get('counter', 0)

	module = Module.objects.filter(moduleID = mid)
	components = []
	quizAvail = 0
	if p < counter:
		quizAvail = 1
	for a in module:
		title = a.moduleTitle
		quiz = a.containsQuiz
		component = Component.objects.filter(compID = a.containsComp)
		for c in component:
			components.append(c)
	componentarray = []
	for i in components:
			componentarray.append(i.content)
	result = {
	 "title": title,
	 "quiz": quiz,
	 "component": componentarray
	}

	return JsonResponse(result)

def viewlist(request,lid):
	list = []
	CCECU = 0
	temp = Progress.objects.filter(learnerID = lid).order_by('pass_date')
	for a in temp:
		if str(a.pass_date) != "2000-01-01":
			course = History()
			dummy = Course.objects.filter(courseID = a.takecourse).first()
			course.title = dummy.title
			course.date = a.pass_date
			course.CECU = dummy.CECU
			course.CCECU = CCECU + course.CECU
			list.append(course)
			CCECU = course.CCECU

	context = {
		'list':list,
		'lid':lid
	}

	return render(request,'history.html',context)

@login_required
def courseModule(request,p,cid,lid,mid,counter):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	lid = int(lid)
	if temp.role == 1 and temp.userID == lid:
		learner = Progress.objects.get(takecourse = cid, learnerID = lid)
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
			title = a.title
			n = n + 1
			mod.counter = n
			if a.contains_modules != 0:
				if i <= p:
					allmod = Module.objects.filter(moduleID = a.contains_modules)
					for b in allmod:
						mod.modID = b.moduleID
						mod.title =  b.moduleTitle
					avamodules.append(mod)
					i = i + 1
				else:
					allmod = Module.objects.filter(moduleID = a.contains_modules)
					for b in allmod:
						mod.modID = b.moduleID
						mod.title =  b.moduleTitle
					unavamodules.append(mod)
					i = i + 1

		module = Module.objects.filter(moduleID = mid)
		components = []
		quizAvail = 0
		p = str(p)
		if p < counter:
			quizAvail = 1
		for a in module:
			title = a.moduleTitle
			quiz = a.containsQuiz
			component = Component.objects.filter(compID = a.containsComp)
			for c in component:
				components.append(c)

		context = {
			'title': title,
			'avamodules': avamodules,
			'unavamodules':unavamodules,
			'counter': n,
			'cid':cid,
			'p':p,
			'lid':lid,
			'components':components,
			'quiz':quiz,
			'check':quizAvail,
		}

		return render(request, 'coursemod.html', context)
	else:
		return render(request,'badlogin.html')

@login_required
def quiz(request, lid,qid, cid, p):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	lid = int(lid)
	if temp.role == 1 and temp.userID == lid:
		info = Quiz.objects.filter(quizID = qid).first()
		total = info.numOfQuestion
		draw = info.draw
		get = []
		exist = 0
		while draw > 0:
			exist = 0
			q = random.randint(1,total)
			for a in get:
				if a == q:
					exist = 1
			if exist == 0:
				get.append(q)
				draw = draw - 1
		quiz = Quiz.objects.filter(quizID = qid)
		questions = []
		counter = 0
		for a in quiz:
			counter = counter + 1
			for b in get:
				if b == counter:
					question = Question.objects.get(questionID = a.questionID)
					questions.append(question)

		context = {
			'questions':questions,
			'cid':cid,
			'p':p,
			'lid':lid,
			'qid':qid
		}

		return render(request, 'quiz.html', context)
	else:
		return render(request,'badlogin.html')

@login_required
def instructor(request, iid, cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		course = Course.objects.filter(courseID = cid)
		modules = []
		i = 0
		for a in course:
			title = a.title
			if a.contains_modules != 0:
				i = i+1
				mod = ModuleT()
				mod.modID = a.contains_modules
				module = Module.objects.filter(moduleID = a.contains_modules)
				for b in module:
					mod.title =  b.moduleTitle
				mod.place = i
				modules.append(mod)
		empty = 1
		if i > 1:
			empty = 0

		context = {
			'title': title,
			'modules': modules,
			'cid':cid,
			'iid':iid,
			'empty': empty
		}

		return render(request, 'courseIns.html', context)
	else:
		return render(request,'badlogin.html')

@login_required
def createModule(request,iid,cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		if Module.objects.all().count()!=0:
			mid = Module.objects.all().latest('moduleID')
			newmid = mid.moduleID + 1
		else:
			newmid = 1
		course = Course.objects.filter(courseID = cid)
		for c in course:
			title = c.title
			created_by = c.created_by
		newcourse = Course.objects.create(courseID = cid, title = title, created_by = created_by, contains_modules = newmid)
		mod = Module.objects.create(moduleID = newmid,moduleTitle = 'Unnamed',containsComp = 0, containsQuiz = 0)

		return instructor(request, iid, cid)
	else:
		return render(request,'badlogin.html')

@login_required
def change_mod_order(request,iid,cid):
	form = request.POST
	origin = int(form.get('origin'))
	destination = int(form.get('destination'))
	i = 0
	if origin == destination or origin == destination+1:
		return instructor(request,iid,cid)
	elif origin < destination:
		courses = Course.objects.filter(courseID = cid)
		for a in courses:
			if a.contains_modules != 0:
				i = i + 1
				if i == origin:
					temp = a.contains_modules
				if i > origin:
					dummy.contains_modules = a.contains_modules
					dummy.save()
				if i == destination:
					a.contains_modules = temp
					a.save()
					break
				dummy = a
		return instructor(request,iid,cid)
	else:
		temp = 0
		alpha = 0
		courses = Course.objects.filter(courseID = cid)
		for a in courses:
			if a.contains_modules != 0:
				i = i + 1
				if i == destination + 1:
					alpha = a.contains_modules
					dummy = a
				if i > destination + 1 and i != origin:
					alpha = a.contains_modules
					a.contains_modules = temp
					a.save()
				if i == origin:
					dummy.contains_modules = a.contains_modules
					dummy.save()
					a.contains_modules = temp
					a.save()
					break
				temp = alpha
		return instructor(request,iid,cid)

def change_comp_order(request, mid,iid,cid):
	form = request.POST
	origin = int(form.get('origin'))
	destination = int(form.get('destination'))
	i = 0
	if origin == destination or origin == destination+1:
		return moduleIns(request, mid,iid,cid)
	elif origin < destination:
		modules = Module.objects.filter(moduleID = mid)
		for a in modules:
			if a.containsComp != 0:
				i = i + 1
				if i == origin:
					temp = a.containsComp
				if i > origin:
					dummy.containsComp = a.containsComp
					dummy.save()
				if i == destination:
					a.containsComp = temp
					a.save()
					break
				dummy = a
		return moduleIns(request, mid,iid,cid)
	else:
		temp = 0
		alpha = 0
		modules = Module.objects.filter(moduleID = mid)
		for a in modules:
			if a.containsComp != 0:
				i = i + 1
				if i == destination + 1:
					alpha = a.containsComp
					dummy = a
				if i > destination + 1 and i != origin:
					alpha = a.containsComp
					a.containsComp = temp
					a.save()
				if i == origin:
					dummy.containsComp = a.containsComp
					dummy.save()
					a.containsComp = temp
					a.save()
					break
				temp = alpha
		return moduleIns(request, mid,iid,cid)

@login_required
def moduleIns(request, mid,iid,cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		module = Module.objects.filter(moduleID = mid)
		components = []
		choice = []
		temp = []
		form1 = ChangeForm()
		form2 = AddForm()
		i = 0
		for a in module:
			title = a.moduleTitle
			quiz = a.containsQuiz
			if a.containsComp != 0:
				i = i + 1
				component = Component.objects.get(compID = a.containsComp)
				temp = ComponentT()
				temp.title = component.title
				temp.compID = component.compID
				temp.content = component.content
				temp.componentType = component.componentType
				temp.used = component.used
				temp.place = i
				components.append(temp)
		allComp = Component.objects.filter(courseID = cid)
		for a in allComp:
			if a.used == 0:
				choice.append(a)

		#add a quiz part
		allQuiz = Quiz.objects.filter(courseID = cid)
		temp = QuizT(quizID = 0,numOfQuestion = 0)
		counter = 0
		quizlist = []
		for a in allQuiz:
			if a.title != temp.quizID and temp.quizID != 0:
				quizlist.append(temp)
				temp = QuizT()
				temp.quizID = a.title
			elif a.quizID != temp.quizID:
				temp.title = a.title
				temp.quizID = a.title
			temp.numOfQuestion = temp.numOfQuestion + 1
		quizlist.append(temp)
		empty = 1
		if i > 1:
			empty = 0

		context = {
			'components':components,
			'quiz':quiz,
			'title':title,
			'mid':mid,
			'form1':form1,
			'form2':form2,
			'iid':iid,
			'cid':cid,
			'choice':choice,
			'quizlist':quizlist,
			'empty':empty
		}

		return render(request, 'moduleIns.html', context)
	else:
		return render(request,'badlogin.html')

@login_required
def changeModName(request,mid,iid,cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		form = ChangeForm(request.POST)
		if form.is_valid():
			module = Module.objects.filter(moduleID = mid)
			title = form.cleaned_data['name']
			for m in module:
				m.moduleTitle = title
				m.save()

		return moduleIns(request, mid,iid,cid)
	else:
		return render(request,'badlogin.html')

@login_required
def addComp(request,mid,iid,cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		form = request.POST

		newmod = Module()
		module = Module.objects.filter(moduleID = mid)
		for m in module:
			newmod.moduleID = m.moduleID
			newmod.moduleTitle = m.moduleTitle
			newmod.containsQuiz = m.containsQuiz
		temp = form.get('compID')
		newmod.containsComp = temp
		newmod.save()
		comp = Component.objects.get(compID = temp)
		comp.used = 1
		comp.save()

		return moduleIns(request, mid,iid,cid)
	else:
		return render(request,'badlogin.html')

@login_required
def addQuiz(request,mid,iid,cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		form = request.POST
		quiz = form.get('quizID')
		module = Module.objects.filter(moduleID = mid)
		for m in module:
			m.containsQuiz = quiz
			m.save()

		return moduleIns(request, mid,iid,cid)
	else:
		return render(request,'badlogin.html')

@login_required
def quizCheck(request,qid,p,lid,cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	lid = int(lid)
	if temp.role == 1 and temp.userID == lid:
		quiz = Quiz.objects.filter(quizID = qid)
		form = request.POST
		total = 0
		correct = 0
		passed = 0
		standard = 0
		for a in quiz:
			standard = a.standard
			total = a.draw
			question = Question.objects.get(questionID = a.questionID)
			ans = "ansTo"
			ans = ans + str(question.questionID)
			if form.get(ans) != '':
				if question.answer == form.get(ans):
					correct = correct + 1
		result = correct/total
		result = round(result,2)
		result = result * 100
		if result >= standard:
			passed = 1
			p = int(p)
			p = p + 1
			learner = Progress.objects.get(takecourse = cid, learnerID = lid)
			learner.progress = p
			learner.save()
		
		context = {
			'passed':passed,
			'result':result,
			'lid':lid,
			'cid':cid,
			'p':p
		}

		return render(request,'quizSubmit.html',context)
	else:
		return render(request,'badlogin.html')

@login_required
def instructorHome(request, iid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		instructor = Instructor.objects.filter(instructorID = iid)
		courses = []
		for a in instructor:
			name = a.name
			if a.create_course != 0:
				temp = Temp()
				course = Course.objects.filter(courseID = a.create_course).first()
				temp.courseID = course.courseID
				temp.title = course.title
				temp.category = course.category
				temp.description = course.description
				temp.progress = course.created_by
				courses.append(temp)
		context = {
			'iid': iid,
			'name': name,
			'courses': courses
		}

		return render(request, 'instructorHomepage.html', context)
	else:
		return render(request,'badlogin.html')

@login_required
def create_new_course(request,iid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	iid = int(iid)
	if temp.role == 2 and temp.userID == iid:
		if(request.method == "POST"):
			form = request.POST
			if form.get('course_title') == '':
				return instructorHome(request,iid)
			else:
				course = Course()
				if Course.objects.all().count()!=0:
					cid = Course.objects.all().latest('courseID')
					cid = cid.courseID + 1
				else:
					cid = 1
				course.courseID = cid
				course.created_by = iid
				course.title = form.get('course_title')
				course.description = form.get('course_description')
				course.category = form.get('cateID')
				course.CECU = form.get('CECU')
				course.contains_modules = 0
				course.save()
				instructor = Instructor()
				temp = Instructor.objects.filter(instructorID = iid).first()
				instructor.name = temp.name
				instructor.instructorID = iid
				instructor.create_course = cid
				instructor.save()
				return instructorHome(request,iid)
		else:
			cate_list = Category.objects.all()
			cate = []
			for a in cate_list:
				cate.append(a)
			context = {
				'iid':iid,
				'cate':cate
			}
			return render(request, 'new_course.html',context)
	else:
		return render(request,'badlogin.html')

@login_required
def view_all_courses(request,lid,cate,alert):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	lid = int(lid)
	if temp.role == 1 and temp.userID == lid:
		learner = Progress.objects.filter(learnerID = lid)
		enrolled_courses = []
		for a in learner:
			enrolled_courses.append(a.takecourse)

		courses = []

		if cate == '0':
			course = Course.objects.all().order_by('courseID')
			cid = 0
			for c in course:
				if c.courseID != cid:
					cid = c.courseID
					temp = CourseT()
					temp.courseID = cid
					temp.title = c.title
					temp.description = c.description
					temp.enroll = 1
					temp.CECU = c.CECU
					for a in enrolled_courses:
						if cid == a:
							temp.enroll = 0
					instructor = Instructor.objects.get(create_course = cid)
					temp.taught_by = instructor.name
					instructor = InstructorInfo.objects.get(instructorID = instructor.instructorID)
					temp.autobio = instructor.intro
					courses.append(temp)
		else:
			course = Course.objects.all().filter(category = cate).order_by('courseID')
			cid = 0
			for c in course:
				if c.courseID != cid:
					cid = c.courseID
					temp = CourseT()
					temp.courseID = cid
					temp.title = c.title
					temp.description = c.description
					temp.enroll = 1
					temp.CECU = c.CECU
					for a in enrolled_courses:
						if cid == a:
							temp.enroll = 0
					instructor = Instructor.objects.get(create_course = cid)
					temp.taught_by = instructor.name
					courses.append(temp)
		cate_list = Category.objects.all()
		cate = []
		for a in cate_list:
			cate.append(a)
		context = {
			'courses':courses,
			'lid':lid,
			'alert':alert,
			'cate':cate
		}

		return render(request, 'view_all_courses.html',context)
	else:
		return render(request,'badlogin.html')

@login_required
def enroll(request,lid,cid):
	name = request.user.username
	temp = UserLogin.objects.get(username = name)
	lid = int(lid)
	if temp.role == 1 and temp.userID == lid:
		learner = Progress.objects.filter(learnerID = lid).first()
		new_learner = Progress()
		new_learner.learnerID = lid
		new_learner.learnerName = learner.learnerName
		new_learner.takecourse = cid
		new_learner.progress = 0
		new_learner.save()

		return view_all_courses(request,lid,'0',1)
	else:
		return render(request,'badlogin.html')
