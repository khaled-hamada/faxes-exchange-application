from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import newfaxForm, editfaxForm
from .models import fax, dept,dept_fax, LoggedUserNew,fax_comments
from datetime import datetime,date
from django.db.models import Q
from django.utils import timezone
# Create your views here.

global newfaxf
newfaxf = 0

global redirect_count, return_back,user_in
redirect_count=0
return_back = 0
user_in = 0
#
# global cur_loged_user
# cur_loged_user = None
def home(request):
    ## this function is defined to remove old django 2.2 sessions , which we
    # have used to create the project , because
    #we use django 3.1 in this computer and these makes conflicts



    global redirect_count, return_back
    redirect_count = 0
    return_back = 0

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:

            request.session.set_expiry(0)
            # request.session.set_expiry(1)
            # cur_loged_user = LoggedUser(user)
            #cur_loged_user.connect(login_user)
            LoggedUserNew.login_user(1,request, user)
            failed =0
            login(request, user)
            # result = get_all_logged_in_users(request, user)
            # if result[0] == 1:
            #     return render(request, "faxat/other_user_in.html")
            # for user_l in users:
            #     user_name = user_l.__unicode__()
            #     print("user name is " + str(user_name))
                # if (user_name == 'manager' or user_name == 'vice_manager') :
                #     return render(request, "faxat/denied.html")
            print('username: ' + request.user.username + ' has log in to system at ' + str(datetime.now()))
            #
            # if user.groups.filter(name='فرع التخطيط').exists():
            #     #return redirect('taktet/')
            #     return taktet(request)
            if user.groups.filter(name='المدير').exists():
                return redirect('manager-start-page')
            elif user.groups.all().count() != 0:
                return takt(request)

        else:
            failed =1
            context = {'failed' : failed}
            return render(request, 'faxat/login.html', context = context)
    return render(request, 'faxat/login.html')

@login_required
def logout_view(request):
    global redirect_count,return_back
    return_back = 0

    if request.user != None:
            userna= request.user.username
            LoggedUserNew.logout_user(1,request,request.user)
            #cur_loged_user = LoggedUser.objects.filter(user = request.user).first()
            #cur_loged_user.connect(logout_user)
            logout(request)
            print('username: ' + userna + ' has log out of system at ' + str(datetime.now()))

    return redirect('../')

@login_required
def change_password(request):
    global redirect_count,return_back
    return_back = 0
    success = failed = 0
    if request.method == "POST" :
            cur_user = request.user
            userna=cur_user.username
            LoggedUserNew.logout_user(1,request,request.user)
            #cur_loged_user = LoggedUser.objects.filter(user = request.user).first()
            #cur_loged_user.connect(logout_user)
            old_pass = request.POST['password_old']
            new_pass_1 = request.POST['password_new_1']
            new_pass_2 = request.POST['password_new_2']

            ## check old pass
            if cur_user.check_password(old_pass):
                ## check new pass match
                if new_pass_1 == new_pass_2 :
                    cur_user.set_password(new_pass_1)
                    cur_user.save()
                    logout(request)
                    print('username: ' + userna + ' has log out of system at ' + str(datetime.now()))
                    return redirect('../')
                else :
                    failed = 2
            else:
                failed = 1
    context = {
        'success':success,
        'failed':failed,
    }
    return render(request, "faxat/change_password.html", context = context)



def dalel(request):
    return render(request , 'faxat/dalel.html')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='فرع التخطيط').count() != 0, login_url='/denied/')
def taktet(request):
    return render(request, 'faxat/taktet.html')


############
### new fax wareed to taz.zag
#########
@login_required
@user_passes_test(lambda u: u.groups.filter(name='المتابعة').count() != 0, login_url='/denied/')
def newfax(request):
    global newfaxf
    depts = dept.objects.all()
    next_fax_number = fax.objects.filter(fax_type=0).last().sader + 1
    success = 0
    context ={
        'depts' : depts,
        'next_fax_number':next_fax_number,
        'success':success,
    }
    if request.method == 'POST':
        send_dept = request.POST.getlist('send_depts')
        reply_dept = request.POST.getlist('reply_depts')
        form = newfaxForm(request.POST, request.FILES)
        title = request.POST['title']
        comments = request.POST['comments']
        #print(request.POST)
        if form.is_valid():
            #print(request.POST)
            sader = int(form.cleaned_data.get('sader'))
            sader_edara = form.cleaned_data.get('sader_edara')
            #title = form.cleaned_data.get('title')
            url = form.cleaned_data.get('url')
            #comments = form.cleaned_data.get('comments')
            try:
                replay_to_edara = request.FILES['replay_to_edara']
            except :
                replay_to_edara = None
                
            form=fax( sader = sader,sader_edara = sader_edara,title = title, url = url,
             comments = comments, replay_dept = reply_dept,send_dept=  send_dept, replay_to_edara = replay_to_edara)
            form.save()
            newfaxf = 1
            next_fax_number = fax.objects.filter(fax_type=0).last().sader + 1
            success = 1
            context ={
                'depts' : depts,
                'next_fax_number':next_fax_number,
                'success':success,
            }
            return render(request, 'faxat/newfax.html', context)
    else:
        form = newfaxForm()
    return render(request, 'faxat/newfax.html', context)



############
### new fax sader from taz.zag
#########
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['المتابعة', 'CanSendFax']).count() != 0, login_url='/denied/')
def newfax_sader(request):
    depts = dept.objects.all()
    next_fax_number = fax.objects.filter(fax_type=1).last().sader + 1
    success = 0
    context ={
        'depts' : depts,
        'next_fax_number':next_fax_number,
        'success':success,
    }
    come_from_dept = ""
    for g in  request.user.groups.all():
        come_from_dept += (g.name + " , ")
    if "CanSendFax" in come_from_dept :
        come_from_dept = come_from_dept.replace("CanSendFax", "")
    if request.method == 'POST':
        sader = int(request.POST['sader'])
        sader_edara = request.POST['sader_edara']
        title = request.POST['title']
        url = request.FILES['url']
        comments = request.POST['comments']
        remove = 0
        if 'remove' in request.POST:
            remove = 1
        form=fax(sader = sader,sader_edara = sader_edara, title =title, url = url, comments = comments, date_added = timezone.now(),come_from_dept = come_from_dept,
                        approved = 2, approved_id = User.objects.filter(username='manager').first().first_name, fax_type=1, is_removable = remove)
        form.save()
        ##get all send depts ids from html page
        send_dept = str(request.POST.getlist('send_depts'))
        ## remove single qotation
        sugg_send = send_dept.replace("'",'')
        ## get all depts numric ids
        y=[]
        num=''
        for st in range(len(sugg_send)):
            if sugg_send[st] == '[':
                continue
            elif sugg_send[st] == ',':
                num=int(num)
                y.append(num)
                num=''
            elif sugg_send[st] == ']' and num !='':
                num=int(num)
                y.append(num)
                break
            else:
                num = num + sugg_send[st]
        ## map each fax to it's relevant department
        send=""
        for dep in range(len(y)):
            department = dept.objects.get(id=y[dep])
            send = send + str(department) + ',  '
            dept_fax_add  = dept_fax.objects.create(status= 0, reply_status= 0, dept = department, fax = form, seen=0)
            # if not remove :
            #     dept_fax_add.seen = 1
            dept_fax_add.save()

        if request.user.groups.filter(name = "المتابعة").count() == 0:
            try :
                department = dept.objects.get(name = request.user.groups.first().name)
            except:
                department=""

            if department != "":
                send = send + str(department) + ',  '
                dept_fax_add  = dept_fax.objects.create(status= 0, reply_status= 0, dept = department, fax = form, seen=0)
                # if not remove :
                #     dept_fax_add.seen = 1
                dept_fax_add.save()

        form.send_dept = send
        form.save()
        next_fax_number = fax.objects.filter(fax_type=1).last().sader + 1
        success = 1
        context ={
            'depts' : depts,
            'next_fax_number':next_fax_number,
            'success':success,
        }
        return render(request, 'faxat/new_fax_sader.html',context)
    else:
        form = newfaxForm()
    return render(request, 'faxat/new_fax_sader.html',context)

###############################################################################
#
#\ taktet views
################################################################################

@login_required
@user_passes_test(lambda u: u.groups.all().count() != 0, login_url='/denied/')
def takt(request):
    global redirect_count
    data = []
    s_item=[]
    dep = dept.objects.filter(name = request.user.groups.all().first().name).first()
    #print(dep)
    #dep = dep.first()
    newfax = 0
    unseen_comments_count= 0
    un_notified_comments = 0
    newfax_count = 0
    back_url_f = get_back_url_f(request)

    import datetime as dt
    from django.utils import timezone
    if  request.user.groups.all().first().name == "المتابعة":
        from_date = timezone.now() + dt.timedelta(days = -10)
    else :
        from_date = timezone.now() + dt.timedelta(days = -10)
    to_date = timezone.now()
    x = fax.objects.filter(dept=dep.id,date_aproved__date__gte =from_date ,
            date_aproved__date__lte = to_date ).order_by('-date_aproved')
    #if (len(x)) > 0
    for f in x :
        s_item.append(f)
        rel_fax = dept_fax.objects.filter(dept = dep, fax = f).first()
        status = rel_fax.status
        s_item.append(status)
        s_item.append(rel_fax.reply_status)
        #s_item.append(rel_fax.reply_status)
        #print("dep_name: %s, fax title %s, fax_status %d"%(dep.name, f.title,status))
        #s_item.append(f.id)
        # unseen_comments = len(fax_comments.objects.filter(dept_fax = rel_fax, user_type="manager",seen=0))
        if  request.user.groups.all().first().name == "المتابعة":
            unseen_comments = len(fax_comments.objects.filter(dept_fax__fax = f, user_type__in =['manager','normal_user'], comment_status__in=[1,5,4],seen=0))
            unseen_comments_count += unseen_comments
            # print("unseen_comments_count ---> motab3a: %d"%(unseen_comments_count))
        else :
            unseen_comments = len(fax_comments.objects.filter(dept_fax = rel_fax, user_type__in =['manager','normal_user'], comment_status__in=[2,4],seen=0))
            unseen_comments_count += unseen_comments
        ### get un_notified comments
        if  request.user.groups.all().first().name == "المتابعة":
            m = fax_comments.objects.filter(dept_fax__fax = f, user_type__in =['manager','normal_user'], comment_status__in=[1,5],seen=0 , notified = 0)
            # print("m for motab3a %d" %(len(m)))
        else:
            m = fax_comments.objects.filter(dept_fax = rel_fax, user_type__in =['manager','normal_user'], comment_status__in=[2,4],seen=0 , notified=0)
            # print("m for depts %d" %(len(m)))

        un_notified_comments += len(m)
        m.update(notified =  1)
        s_item.append(unseen_comments)
        data.append(s_item)
        s_item=[]
        if status == 0:
            newfax_count += 1
        ## or status == 1
        if (status == 0  ) and rel_fax.reply_status == 1 and rel_fax.notified == 0:
            newfax += 1
            rel_fax.notified = 1
            rel_fax.save()
        #in case of reply ==0 we can add a seen status
        elif  rel_fax.reply_status == 0 and rel_fax.seen == 0 and redirect_count == 1 and rel_fax.notified == 0:
            rel_fax.notified = 1
            rel_fax.save()
            newfax += 1
            #print("dept name: %s, reply_status: %d, seen: %d, status: %d"%(dep.name, rel_fax.reply_status, rel_fax.seen,status ))
        ### repeatable notification if fax status still 0 or if seen still 0
        if rel_fax.seen == 0 and newfax ==0 :

            min_num = 10
            last_time = rel_fax.last_notified
            last_time_delta = last_time + dt.timedelta(minutes = min_num)
            if timezone.now() > last_time_delta:

                rel_fax.last_notified= timezone.now()
                rel_fax.save()
                newfax +=1

    f_data = sorted(data, key=lambda x:x[3], reverse = True)
    context ={
        'faxes' : f_data,
        'un_notified_fax':newfax,
        'newfax_count':newfax_count,
        'dept_name':dep.name,
        'back_url':back_url_f,
        'un_notified_message':un_notified_comments,
        'new_message_count':unseen_comments_count,

    }
    # print("Count of new faxes :%s"%(dep.name))
    if redirect_count ==0:
        redirect_count = 1
        return redirect("takt-page")
    else:
        return render(request, 'faxat/takt.html',context)



@login_required
@user_passes_test( lambda u :u.groups.filter(name='المتابعة').count() != 0 , login_url='/denied/')
def unapproved(request):
    global newfaxf
    #x = reversed(fax.objects.filter(approved=0))
    ## here we use the Q object from django.db.models
    ##
    x = fax.objects.filter( ~Q(approved = 2)).order_by('-date_added') ## get all faxes with approved status != 2  i.e approved =0 or 1
    # x_rev = list((x))
    if len(x) > 0 :
         #print(x)
         newfaxf=1
    else :
        newfaxf = 0
    context ={
        'faxes' : x,
        'newfaxf': newfaxf
    }

    return render(request, 'faxat/unapproved.html',context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='المتابعة').count() != 0 or u.groups.filter(name='المدير').count() != 0 , login_url='/denied/')
def approved(request,fax_type):
    import datetime as dt
    from django.utils import timezone

    from_date = timezone.now() + dt.timedelta(days = -10)
    to_date = timezone.now()

    x = (fax.objects.filter(approved=2, fax_type =fax_type
                            ,date_aproved__date__gte =from_date ,
                            date_aproved__date__lte = to_date)).order_by('-date_aproved')
    backurl = ''
    if request.user.groups.filter(name='المدير').exists():
        backurl = '../manager_start/'
    elif request.user.groups.filter(name='فرع التخطيط').exists():
        backurl = '../taktet'
    result = get_all_unseen_count(x)
    context ={
        'faxes' : result,
        'backurl':backurl,
    }
    return render(request, 'faxat/approved.html',context)


@login_required
def denied(request):
    return render(request, 'faxat/denied.html')



##########################
###get count of all unread messages for each fax for manager only
#######################
def get_all_unseen_count(faxes):
    result = []
    s_item = []
    f_result = []
    unseen_count = 0
    un_notified = 0
    ## for each fax get a list of all reply departs
    for fax in faxes :
        fax_depts =fax.replay_dept
        depts = dept.objects.filter(fax = fax)
        ## for each department in depts
        for dep in depts:
            #if this department is one of the replay departments,then
            if dep.name in fax_depts:
                #get the relevant fax and filter comments table depending
                #on the relevant fax_id
                rel_fax = dept_fax.objects.filter(fax = fax, dept=dep).first()
                unseen_count += len(fax_comments.objects.filter(dept_fax = rel_fax, user_type='normal_user',comment_status__in =[3,1] , seen=0))
                un_not_m = fax_comments.objects.filter(dept_fax = rel_fax, user_type='normal_user', seen=0, notified = 0, comment_status =3)

                un_notified +=  len(un_not_m)
                un_not_m.update(notified = 1)
        s_item.append(fax)
        s_item.append(unseen_count)
        s_item.append(int(fax.fax_type))
        s_item.append(un_notified)
        result.append(s_item)
        unseen_count = 0
        un_notified = 0
        s_item=[]
        f_result = general_sort_on_messgae_count(result)
    return f_result



def general_sort_on_messgae_count(result):
    from operator import itemgetter
    r = sorted(result, key=lambda x:x[1], reverse = True)
    return r



def repeat_notification(approved_phase):
    import datetime as dt
    from django.utils import timezone
    min_num = 10
    un_notified_fax = fax.objects.filter(approved=approved_phase )
    if len(un_notified_fax) > 0:

        if approved_phase == 1 : #manager phase
            ## iterate through all fex until finding one
            for f in un_notified_fax :
                last_time = f.last_notified_m
                last_time_delta = last_time + dt.timedelta(minutes = min_num)
                if timezone.now() > last_time_delta:
                    count =len(un_notified_fax)
                    f.last_notified_m = timezone.now()
                    f.save()
                    return count

        elif approved_phase == 0 : #vice_manager phase
            ## iterate through all fex until finding one
            for f in un_notified_fax :
                last_time = f.last_notified_vm
                last_time_delta = last_time + dt.timedelta(minutes = min_num)
                if timezone.now() > last_time_delta:
                    count =len(un_notified_fax)
                    f.last_notified_vm = timezone.now()
                    f.save()
                    return count

        return 0
###############################################################################
#
#\ manager views
###############################################################################

@login_required
@user_passes_test(lambda u: u.groups.filter(name='المدير').count() != 0, login_url='/denied/')
def manager_start(request):
    # get all unapproved faxes count
    un_approved_count = len( fax.objects.filter(approved=1))
    # un_approved_count_vm = len( fax.objects.filter(approved=1, date_aproved__date__gte =date.today()))
    un_approved_count_vm = len( fax.objects.filter(approved=0))
    ## notify only one time when new fax or message commes
    if request.user.username == 'manager':
        un_notified_fax = fax.objects.filter(approved=1 , notified__in = [1,0])
        ####
        ## if the fax notified first time and do not have been approved yet , then repeat notification

        un_fax_count = len(un_notified_fax)
        un_notified_fax.update(notified = 2)
        if un_fax_count == 0:
            un_fax_count = repeat_notification(1)
    elif  request.user.username == 'vice_manager':
        un_notified_fax = fax.objects.filter(approved=0 ,  notified__in = [2, 0])
        ####

        un_fax_count = len(un_notified_fax)
        un_notified_fax.update(notified = 1)
        if un_fax_count == 0:
            un_fax_count = repeat_notification(0)
    # get all unread messages count for the manager
    result = get_all_unseen_count(fax.objects.filter(approved=2))
    un_seen_count = 0
    un_notified_count = 0
    for item in result :
        un_seen_count += item[1]
        un_notified_count += item[3]
    context = {
        'un_notified_fax':un_fax_count,
        'newfax_count_m':un_approved_count,
        'newfax_count_vm':un_approved_count_vm,
        'un_notified_message':un_notified_count,
        'new_message_count':un_seen_count,
    }
    return render(request, 'faxat/manager_start.html',context = context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='المدير').count() != 0  , login_url='/denied/')
def manager(request):
    global newfaxf
    #x = reversed(fax.objects.filter(approved=0))
    if request.user.username == 'manager':
        x = fax.objects.filter(approved=1)
    elif request.user.username == 'vice_manager':
        # x = fax.objects.filter(approved=1 , date_aproved__date__gte =date.today())
        x = fax.objects.filter(approved=0 )
    # x_rev = list((x))
    # if len(x) > 0 :
    #      #print(x)
    #      newfaxf=1
    # else :
    #     newfaxf = 0
    context ={
        'faxes' : x,
        # 'newfaxf': newfaxf
    }
    #newfaxf = 0

    return render(request, 'faxat/manager.html',context)

#############################
##
## display all departs with their ids
###############################
@login_required
def depts(request):
    dep = dept.objects.all()
    context ={
        'depts' : dep
    }
    return render(request, 'faxat/depts.html',context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='المدير').count() != 0, login_url='/denied/')
def first_manager_edit(request, fax_id):
    if request.method == 'POST':
        x = fax.objects.get(id=fax_id)
        title = request.POST['title']
        comments = request.POST['comments']
        v_manager_comments = request.POST['v_manager_comments']

        send_dept = request.POST.getlist('send_depts')
        reply_dept = request.POST.getlist('reply_depts')

        x.title = title
        x.comments = comments
        x.v_manager_comments = v_manager_comments
        x.replay_dept = reply_dept
        x.send_dept = send_dept
        x.approved = 1
        x.approved_id = request.user.first_name
        x.date_aproved = datetime.now()
        x.save()
        return redirect('/manager/')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='المدير').count() != 0, login_url='/denied/')
def edit(request, fax_id):

    x = fax.objects.get(id=fax_id)
    sugg_send = x.send_dept
    sugg_reply = x.replay_dept
    sugg_send = sugg_send.replace("'",'')
    sugg_reply = sugg_reply.replace("'",'')
    y=[]
    num=''
    for st in range(len(sugg_send)):
        if sugg_send[st] == '[':
            continue
        elif sugg_send[st] == ',':
            num=int(num)
            y.append(num)
            num=''
        elif sugg_send[st] == ']' and num !='':
            num=int(num)
            y.append(num)
            break
        else:
            num = num + sugg_send[st]
    sugg_send = y
    z=[]
    num=''
    for st in range(len(sugg_reply)):
        if sugg_reply[st] == '[':
            continue
        elif sugg_reply[st] == ',':
            num=int(num)
            z.append(num)
            num=''
        elif sugg_reply[st] == ']':
            if num != '':
                num=int(num)
                z.append(num)
                break
        else:
            num = num + sugg_reply[st]
    sugg_reply = z
    #print(sugg_reply)
    #print(sugg_send)
    depts = dept.objects.all()
    context ={
        'faxes' : x ,
        'depts' : depts,
        'sugg_send' : sugg_send,
        'sugg_reply' : sugg_reply,
    }
    if request.method == 'POST':
        ## fax must go to both manager and vice_manager before approving it
        ## if mnager want vice manager to add his comments to the fax before redirecting it to all departments
        if "redirect_to_m" in request.POST:
            #print("before redirecting to vice_manager")
            return first_manager_edit(request, fax_id)
            #print("after redirecting to vice_manager")
        reply=''
        send=''
        title = request.POST['title']
        comments = request.POST['comments']
        manager_comments = ""
        if "manager_comments" in request.POST:
            manager_comments = request.POST['manager_comments']
            x.manager_comments = manager_comments
        elif 'v_manager_comments' in request.POST:
            v_manager_comments = request.POST['v_manager_comments']
            x.v_manager_comments = v_manager_comments
        send_dept = request.POST.getlist('send_depts')
        reply_dept = request.POST.getlist('reply_depts')

        x.title = title
        x.comments = comments

        #test print
        x.save()
        for dep in range(len(send_dept)):
            department = dept.objects.get(id=send_dept[dep])
            #print("send to " + str(department))
            send = send + str(department) + ',  '
            #only reply dept. have this option
            #department.fax.add(x)
            if send_dept[dep] not in reply_dept:
                dept_fax_add  = dept_fax.objects.create(status= 0, reply_status= 0, dept = department, fax = x, seen=0)
                dept_fax_add.save()
        for dep in range(len(reply_dept)):
            department = dept.objects.get(id=reply_dept[dep])
            #print("reply from " + str(department))
            reply = reply + str(department) + ',  '
            #create a throug model with the status
            dept_fax_add  = dept_fax.objects.create(status= 0, reply_status= 1, dept = department, fax = x, seen=0)

        # print("send to " + str(send))
        # print("reply from " + str(reply))
        # print(reply.split(',  '))
        # print(send.split(',  '))
        x.replay_dept = reply
        x.send_dept = send
        x.approved = 2
        #if the fax is not already approved by the manager
        #if x.approved_id == ' ' :
        x.approved_id = request.user.first_name
        x.date_aproved = datetime.now()
        x.save()
        return redirect('/manager/')
    return render(request, 'faxat/edit.html',context)






###############################################################################
#
#\ view fax status for each department
################################################################################
@login_required
@user_passes_test(lambda u: u.groups.all().count() != 0, login_url='/denied/')
def viewfax(request, fax_id):
    global return_back
    #this  is not complete it must be a function returns that back url for the return button
    backurl = get_back_url(request)
    url='/view/'
    x = fax.objects.get(id=fax_id)
    context ={
            'faxes' : x,
            'backurl' : backurl
        }
    dep_name = request.user.groups.all()[0].name
    if dep_name in x.replay_dept or dep_name in x.send_dept  :
        depts = x.dept_set.filter(name = dep_name)
        #print(depts)
        dep = depts.first()
        rel_fax = dept_fax.objects.filter(fax = x.id , dept=dep.id)
        #print(rel_fax.values(''))
        rel_fax = rel_fax.first()

        if rel_fax.status == 0:
            status = 'تم وصول الفاكس'
        elif rel_fax.status == 1:
            status = 'جاري العمل عليه'
        elif rel_fax.status ==2:
            status = 'تم الانتهاء منه'
        elif rel_fax.status == 3:
            status = 'تم الانتهاء منه و العرض على السيد مدير المنطقة'
        if return_back == 1:
                #print('here from search function')
                return_back = 0
                backurl = '../../search'
        comments = fax_comments.objects.filter(dept_fax = rel_fax)

        ## update fax with user who have seen it and the time it has been seen at
        if rel_fax.seen == 0:
            rel_fax.seen_by = request.user.first_name
            rel_fax.last_notified = timezone.now()
            rel_fax.save()
        #in case of reply ==0 we can add a seen status
        # if rel_fax.reply_status == 0 and rel_fax.seen == 0 :
        if  rel_fax.seen == 0 and  rel_fax.reply_status == 0 :
            rel_fax.status=2
            rel_fax.seen = 1
            rel_fax.save()
        elif rel_fax.seen ==0 and  rel_fax.reply_status == 1:
            rel_fax.seen = 1
            rel_fax.status=1
            rel_fax.save()

        ## update unseen manager or vice_manager comments from seen=0 to seen = 1
        mark_as_read(request,rel_fax,['manager', 'normal_user'] , [2,4])
        context ={
            'faxes' : x,
            'status' : status,
            'comments':comments,
            'backurl' : backurl,
            'reply_status':rel_fax.reply_status,
            'dept_fax':rel_fax,
        }
        if request.method == 'POST':
            #get current department only
            #dep = x.dept_set.filter(name = dep_name).first()
            #print(dep)
            #get relevant fax instance from the many to many relation ship
            #rel_fax = dep.fax.filter(id = x.id).first()
            #print(rel_fax)
            status = request.POST['status']
            if rel_fax.seen == 1 and int(status) >= rel_fax.status:
                rel_fax.status = int(status)

            ### check if user write a comment or attach any files
            ## status = 1  from all users to motab3a
            #add_new_comment(request,rel_fax,'normal_user',1 )
            rel_fax.save()
            url=url + str(fax_id)
            return redirect(url)
    else:
        return redirect('/denied/')
    return render(request, 'faxat/viewfax.html',context)



def mark_as_read(request, rel_fax, user_type , comment_status):
    f = fax.objects.get(dept_fax = rel_fax)
    unseen_comments = fax_comments.objects.filter(dept_fax = rel_fax, user_type__in=user_type ,comment_status__in=comment_status, seen = 0)
    # print(unseen_comments)
    for comment in unseen_comments:
        # print("see commants as manager or motab3a 2")
        comment.seen = 1
        comment.seen_by = request.user.first_name
        comment.save()


### case 1 and 2 from depts to motab3a and vice versa
def add_new_comment(request,rel_fax, user_type ,status):
        # rel_fax = dept_fax.objects.get(id=rel_fax.id)
        comment = ""
        document=None
        has_comment = 0
        if 'dept_comment' in request.POST:
            #print('i have a comment from manager')
            comment =request.POST['dept_comment']
            # print('i have a comment from manager: %s'%(str(comment)))
            has_comment = 1
        if 'dept_document' in request.FILES:
            #print('i have a document from manager')
            has_comment = 1
            document =request.FILES['dept_document']

        if has_comment:
            has_comment = 0
            if document :
                # print('i have a document from manager')
                new_comment = fax_comments.objects.create(seen =0, dep_comment = comment, dep_document = document,writer= request.user.first_name, dept_fax = rel_fax, date = datetime.now(), user_type = user_type ,comment_status = status )
            elif comment !="":
                # print('i have a comment from manager')
                new_comment = fax_comments.objects.create(seen =0, dep_comment = comment, dep_document = document,writer= request.user.first_name, dept_fax = rel_fax, date = datetime.now(), user_type = user_type , comment_status = status)





def add_manager_comment(request, rel_fax):
    rel_fax = dept_fax.objects.get(id = rel_fax )
    if request.method == 'POST':
        try:
            id = int(request.POST['rel_fax'])
        except:
            id  = rel_fax


        if request.user.groups.filter(name = "المتابعة").count() !=  0:
            # print("تخطيط")
            ## case 1  from motab3a to all depts
            if rel_fax.dept.name == "المتابعة":
                ## from motab3a to manager   status = 3
                add_new_comment(request,rel_fax, 'normal_user' , 3)
            else :
                ## from motab3a to all depts   status = 2
                add_new_comment(request,rel_fax, 'normal_user' , 2)
        else :
            ### case = 4 from manager to all
            if rel_fax.dept.name == "المتابعة":
                add_new_comment(request,rel_fax, 'manager', 5)
            else:
                add_new_comment(request,rel_fax, 'manager', 4)

        return redirect('viewfaxt-page',rel_fax.fax.id)


    comments = fax_comments.objects.filter(dept_fax = rel_fax)
    ## update un seen user comments to be seen by manager or vice manager
    ## i have 2 case in this function manager and motab3a
    ## case 1 motab3a only see manager to motab3a and depts to motab3a
    # mark_as_read(request,rel_fax,['manager', 'normal_user'] , [2,4])
    if request.user.groups.first().name == "المتابعة":
        # print("see commants as  motab3a 2")
        mark_as_read(request,rel_fax, ['normal_user','manager'] , [1,5])
    else:
        # print("see commants as manager ")
        ## case 2 manager  only see  motab3a reply
        mark_as_read(request,rel_fax ,['normal_user'] ,[3])
    context ={
        'rel_fax_id' : rel_fax,
        # 'status' : status,
        'comments':comments,
        # 'backurl' : backurl,
        # 'reply_status':rel_fax.reply_status
    }

    return render(request, 'faxat/add_manager_comment.html',context)



def add_dept_comment(request, rel_fax):
    rel_fax = dept_fax.objects.get(id = rel_fax )

    # return redirect('viewfax-page',rel_fax.id)
    ## update unseen manager or vice_manager comments from seen=0 to seen = 1
    mark_as_read(request,rel_fax,['manager', 'normal_user'] , [2,4])

    if request.method == 'POST':
        add_new_comment(request,rel_fax,'normal_user',1 )


    comments = fax_comments.objects.filter(dept_fax = rel_fax)
    context ={
        'rel_fax' : rel_fax.fax.id,
        # 'status' : status,
        'comments':comments,
        # 'backurl' : backurl,
        # 'reply_status':rel_fax.reply_status
    }

    return render(request, 'faxat/add_dept_comment.html',context)


@login_required
@user_passes_test(lambda u:  u.groups.filter(name='المدير').count() != 0  or  u.groups.filter(name='المتابعة').count() != 0, login_url='/denied/')
def close_commeting(request,rel_fax ):
    rel_fax = dept_fax.objects.get(id = rel_fax )
    rel_fax.reply_status = 0
    rel_fax.save()
    ## remove dept name from the fax
    fax = rel_fax.fax
    reply_dept = fax.replay_dept
    if rel_fax.dept.name in reply_dept:
        reply_dept = reply_dept.replace( rel_fax.dept.name, "")
        fax.replay_dept = reply_dept
        fax.save()

    return redirect('viewfaxt-page',rel_fax.fax.id)


@login_required
@user_passes_test(lambda u:  u.groups.filter(name='المدير').count() != 0  or  u.groups.filter(name='المتابعة').count() != 0, login_url='/denied/')
def allow_commeting(request,rel_fax ):
    rel_fax = dept_fax.objects.get(id = rel_fax )
    rel_fax.reply_status = 1
    rel_fax.save()
    rel_fax.save()
    ## add dept name to the fax
    fax = rel_fax.fax
    reply_dept = fax.replay_dept
    if rel_fax.dept.name not in reply_dept:
        reply_dept = reply_dept + str(", " + rel_fax.dept.name)
        fax.replay_dept = reply_dept
        fax.save()

    return redirect('viewfaxt-page',rel_fax.fax.id)

###############################################################################
#
#\view all  approved fax status for taktet department  only
################################################################################
from django.urls import resolve
@login_required
@user_passes_test(lambda u:  u.groups.filter(name='المدير').count() != 0  or  u.groups.filter(name='المتابعة').count() != 0, login_url='/denied/')
def viewfaxt(request, fax_id):

    global return_back
    status=''
    x = fax.objects.get(id=fax_id)
    depts_all = dept.objects.filter(fax = x)
    m_dept = dept.objects.get(name = "المتابعة" )
    depts = [m_dept] + [d for d in depts_all.exclude(id = m_dept.id) ]

    ### get relevant fax of motab3a first and if not seen see it
    rel_fax = dept_fax.objects.filter(dept = m_dept , fax = x ).first()
    if rel_fax !=None and request.user.groups.filter(name='المتابعة').count() != 0:
        #in case of reply ==0 we can add a seen status
        # if rel_fax.reply_status == 0 and rel_fax.seen == 0 :
        if  rel_fax.seen == 0 and  rel_fax.reply_status == 0 :
            rel_fax.status=2
            rel_fax.seen = 1
            rel_fax.seen_by = request.user.first_name
            rel_fax.last_notified = timezone.now()
            rel_fax.save()
        elif rel_fax.seen ==0 and  rel_fax.reply_status == 1:
            rel_fax.seen = 1
            rel_fax.status=1
            rel_fax.seen_by = request.user.first_name
            rel_fax.last_notified = timezone.now()
            rel_fax.save()



    replay_depts = x.replay_dept
    send_dept = x.send_dept
    dep_status =[]
    s_dep=[]
    for dep in depts :
        if  dep.name in replay_depts or dep.name in send_dept :
        #print(dep)

            ## for html page view faxt
            ## this is dep.0
            s_dep.append(dep.name)
            #print(dep.fax.filter(id = x.id).first().status )
            dep_fax  = dept_fax.objects.filter(fax = x.id , dept=dep.id).first()

            st = dep_fax.status
            if st == 0:
                status = 'تم وصول الفاكس'
            elif st == 1:
                status = 'جاري العمل عليه'
            elif st ==2:
                status = 'تم الانتهاء منه'
            elif st == 3:
                status = 'تم الانتهاء منه و العرض على السيد مدير المنطقة'

            ## this is dep.1
            s_dep.append(status)
            ## this is dep.2
            s_dep.append(dep_fax.seen)

            #dep_fax related comments
            comments = fax_comments.objects.filter(dept_fax = dep_fax)
            ## this is dep.3
            s_dep.append(comments)
            ## this is dep.4
            s_dep.append(dep_fax.id)
            ## this is dep.5
            unseen_messages = len(fax_comments.objects.filter(dept_fax = dep_fax, user_type='normal_user', seen=0))
            #print(comments.exclude(writer__icontains='عميد' , seen = 0))
            s_dep.append(unseen_messages)

            ## this is dep.6 which means if the department has rights to reply or not
            s_dep.append(dep_fax.reply_status)
            s_dep.append(dep_fax.seen_by) ## dep.7
            s_dep.append(dep_fax.last_notified) ##dep.8


            # s_dep.append(x.url)
            # print("fax id %d" %dep_fax.id)
            # if(dep_fax.dep_document):
                # print("fax image %s" %(str(dep_fax.dep_document.url)))
                # print("fax image %s" %(str(dep_fax.dep_comment)))

            dep_status.append(s_dep)

            s_dep=[]
    current_ulr = str((request.META['HTTP_REFERER']))
    # print("current_ulr %s"%(current_ulr))
    # print("return_back value %d"%(return_back))
    no_ret=0
    if  'report_page' in current_ulr:
        no_ret=1
    context ={
        'faxes' : x,
        'fax_type':x.fax_type,
        'status' : status,
        'depts':dep_status,
        'return_back':return_back,
        'document':x.url,
        'no_ret':no_ret,
    }


    if return_back == 1:
            #print("here in viewfaxt from search page !")
            return_back = 0
    return render(request, 'faxat/viewfaxt.html',context)







################################
##
##  get back ulr for each logged in user , used for return back button on the page of view the fax data
##############################
def get_back_url_f(request):
    backurl=''
    if request.user.groups.filter(name='فرع التخطيط').exists():
        backurl = '../taktet'
    # elif request.user.groups.all().count() != 0 :
    #     #print("nozom here")
    #     backurl = '../../takt'
    return backurl



################################
##
##  get back ulr for each logged in user , used for return back button on the page of view the fax data
##############################
def get_back_url(request):
    backurl=''
    if request.user.groups.all().count() != 0 :
         #print("nozom here")
         backurl = '../../takt'
    return backurl




##############################
#
#
###################################

@login_required
def search(request):
    global return_back

    if request.method == 'POST':
        return_back = 1
        ############ step 1 get html input search data
        sader= 0 if request.POST['sader']=='' else  request.POST['sader']
        sader_edara= 0 if request.POST['sader_edara']=='' else  request.POST['sader_edara']
        title = request.POST['title']
        date_f= 0 if request.POST['date']=='' else  request.POST['date']
        approved_by = request.POST['approved_by']
        from_date = 0 if request.POST['from_date']=='' else  request.POST['from_date']
        to_date = 0 if request.POST['to_date']=='' else  request.POST['to_date']
        dept_name = "" if request.POST['dept_name']=='' else  request.POST['dept_name']
        not_seen = 0  if request.POST['not_seen']=='' else int(request.POST['not_seen'])
        all_faxes = "" if request.POST['all_faxes']=='' else (request.POST['all_faxes'])
        ## step 2 : get all relevant faxes denpend on html input
        if date_f !=0:
            faxes = fax.objects.filter(date_added__date =date_f )
        elif sader !=0 :
            faxes = fax.objects.filter(sader = sader )
        elif sader_edara != 0:
            faxes = fax.objects.filter(sader_edara = sader_edara )
        elif title !='':
            faxes = fax.objects.filter(title__contains = title )
        elif approved_by !='':
            #print("approved_by" + approved_by)
            faxes = fax.objects.filter(approved_id__contains = approved_by )
        elif dept_name !='':
            #print("approved_by" + approved_by)
            faxes = fax.objects.filter(dept__name__contains = dept_name )
        elif from_date !=0 and to_date != 0:
            faxes = fax.objects.filter(date_added__date__gte =from_date , date_added__date__lte = to_date  )
        elif not_seen != 0:
            faxes = fax.objects.filter(dept_fax__seen = 0  ).distinct()
        elif not_seen != 0:
            faxes = fax.objects.filter(dept_fax__seen = 0  ).distinct()
        elif all_faxes != "":
            faxes = fax.objects.all()

        ###################################################
        else:
            faxes = None
        ######################################################

        data = []
        s_item=[]
        ## step 3 : get dep faxes only from all faxes depending on current user dept id
        dep = ""
        back_url_f = get_back_url_f(request)


        if faxes != None:
        #########################################################################################################################
            if request.user.groups.filter(name='المدير').count() != 0 or  request.user.groups.filter(name='المتابعة').count() != 0:
                # dep = ""
                if   request.user.groups.filter(name='المتابعة').count() != 0 :
                    dep = dept.objects.filter(name = request.user.groups.all().first().name).first()
                x = faxes.order_by('-date_aproved')
            else :
                dep = dept.objects.filter(name = request.user.groups.all().first().name).first()
                x = faxes.filter(dept=dep.id).order_by('-date_aproved')
        # back_url_f = get_back_url_f(request)
        ## step 4 : for each fax in the faxes get revelvant fax status from the trough model
            if request.user.groups.filter(name='المدير').count() == 0 and  request.user.groups.filter(name='المتابعة').count() == 0 :
                for f in x :
                    rel_fax = dept_fax.objects.filter(dept = dep, fax = f).first()
                    if rel_fax.seen == 0 and not_seen !=0:
                        s_item.append(f)
                        status = rel_fax.status
                        s_item.append(status)
                        s_item.append(rel_fax.reply_status)
                        data.append(s_item)
                        s_item=[]
                    elif not_seen ==0 :
                        s_item.append(f)
                        status = rel_fax.status
                        s_item.append(status)
                        s_item.append(rel_fax.reply_status)
                        data.append(s_item)
                        s_item=[]

            else :
                for f in x :
                    s_item.append(f)
                    data.append(s_item)
                    s_item=[]
        ##################################################################################################

        ## step 5 : construct the context dict for all needed data in the html page
        #print("name used in html page %s" %(str(request.user.username)))
        context ={
            'faxes' : data,
            'dept_name':dep.name if dep !="" else "",
            'back_url':back_url_f,
            'name': request.user.groups.all().first().name,

        }
        return render(request, 'faxat/search.html',context=context)

    else:
        return render(request, 'faxat/search.html')



@login_required
@user_passes_test(lambda u: u.groups.filter(name='المتابعة').count() != 0  , login_url='/denied/')
def delete_fax(request, fax_id):
    approved_status = 0
    delete_fax = fax.objects.get(id = fax_id)
    approved_status = delete_fax.approved
    ## 1- here stands for fax sader , user can delete only fax sader
    delete_fax.delete()

    if approved_status == 0:
        ## not approved yet
        return redirect('unapproved-page')
    else :
        ## approved from sader
        return redirect('approved-page', 1)



@login_required
@user_passes_test(lambda u: u.groups.filter(name='المتابعة').count() != 0  , login_url='/denied/')
def forward_fax_to_manager(request, fax_id):

    forward_fax = fax.objects.get(id = fax_id)
    forward_fax.approved = 1
    forward_fax.save()

    return redirect('unapproved-page')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='المتابعة').count() != 0  , login_url='/denied/')
def backward_fax_to_vice_manager(request, fax_id):

    backward_fax = fax.objects.get(id = fax_id)
    backward_fax.approved = 0
    backward_fax.save()

    return redirect('unapproved-page')

from . import models
# from models import dept,fax,dept_fax,fax_comments
@login_required
@user_passes_test(lambda u: u.groups.filter(name='فرع التخطيط').count() != 0 or u.groups.filter(name='المدير').count() != 0  or u.groups.filter(name='المتابعة').count() != 0, login_url='/denied/')
def report_page(request):

    search_date = date.today()
    from_date = to_date =  date.today()
    if request.method == "POST":
        if "from_date" in request.POST:
            from_date = request.POST['from_date']
        if "to_date" in request.POST:
            to_date = request.POST['to_date']

    depts = models.dept.objects.all()
    data = []
    s_item=[]

    for dept in depts:
        ## all faxes arrived to this part today
        dept_fax = models.fax.objects.filter(dept=dept.id, date_aproved__date__gte = from_date ,  date_aproved__date__lte = to_date)
        if len(dept_fax) !=0 : ## has any faex arrived today
            arrived_fax = 0
            seen_fax = 0
            unseen_fax = 0
            messages_m = 0
            messages_d= 0
            sader = []
            sader_n =[]
            arrived_fax = len(dept_fax)
            s_item.append(dept.name)  ## s.0 dept name
            s_item.append(arrived_fax)## s.1 arrived count
            for fax in dept_fax :
                rel_fax = models.dept_fax.objects.filter(dept = dept, fax = fax).first()
                if rel_fax.seen ==0:
                    sader = []
                    unseen_fax += 1
                    sader.append(fax.id)
                    sader.append(fax.sader)
                    sader_n.append(sader)
                if rel_fax.reply_status ==1 :
                    messages_m +=len(models.fax_comments.objects.filter(dept_fax = rel_fax, user_type=['manager','normal_user'], comment_status__in=[4,5,2] ,seen=0))
                    messages_d +=len(models.fax_comments.objects.filter(dept_fax = rel_fax, user_type='normal_user',comment_status__in=[1,3] , seen=0))


            s_item.append(arrived_fax - unseen_fax) ## s.2  seen count
            s_item.append(unseen_fax) ## s.3  unseen count
            s_item.append(sader_n) ## s.4  fax_id s.4.0 and sader numbers s.4.1
            s_item.append(messages_m) ## s.5 sader messages
            s_item.append(messages_d) ## s.6  wareed messages
            percentage = round(((arrived_fax - unseen_fax) / arrived_fax)*100)
            s_item.append(percentage) ## s.7  percentage
            # s_item.append(sader_n) ## s.8

            data.append(s_item)
            # print("s_item %s"%(str(s_item)))
            s_item = []


    data = sorted(data, key=lambda x:x[7])
    context={'data':data,'from_date':get_arabic_date(from_date), 'to_date':get_arabic_date(to_date)}
    return  render(request,'faxat/report_page.html', context = context)










def get_arabic_num(number):
    arabicNumbers = {
                        0:'۰',
                        1:'١'
                        ,2: '٢'
                        ,3: '٣'
                        ,4: '٤'
                        , 5:'٥'
                        , 6:'٦'
                        , 7:'٧'
                        , 8:'٨'
                        , 9:'٩'


                    }
    return arabicNumbers.get(number)

def get_arabic_date(search_date):
    str_date = str(search_date)
    output =""
    for num in str_date:
        if num !='-':
            output += str(get_arabic_num(int(num)))
        else:
            output +=' / '
    output = output.split('/')
    result=""
    for part in range(len(output)-1,-1,-1):
        result +=output[part]+' / '
    result = result.rstrip(' / ')
    return result
##############################
#get a list of all current users logged in
#
###########################
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import datetime


def clean_sessions():
    Session.objects.all().delete()

def get_all_logged_in_users(request, cur_user):
    logged_out  =None
    status  = 0
    # global user_in
    # print("gloabal user_in %d" %(user_in))
    # # Query all non-expired sessions
    # # use timezone.now() instead of datetime.now() in latest versions of Django
    # sessions = Session.objects.filter(expire_date__gte=datetime.now())
    # uid_list = []
    #
    # # Build a list of user ids from that query
    # for session in sessions:
    #     data = session.get_decoded()
    #     uid_list.append(data.get('_auth_user_id', None))
    #     # session.set_expiry(0)
    # # Query all logged in users based on id list
    # # users = User.objects.filter(id__in=uid_list)
    users =LoggedUserNew.objects.filter(user__groups__name = 'المدير')
    # print("current  logged in management  accounts are %d" %(len(users)))
    if (users.count() > 1):
        for user in users :
            if user.user.username != cur_user.username :
                status = 1
                logged_out = user
                remove_all_sessions(user.user,request)
                #log_out_manage(request)
                # logout(request)

                #break


    # for user in users:
    #     user_name = user.__unicode__()
    #     print("user name is " + str(user_name))
    #     if (user_name == 'manager' or user_name == 'vice_manager') :
    #         #user_in == 0
            #print("here")
            #return redirect("faxat/denied.html")
            #logout_view(request)
        # elif (user_name == 'manager' or user_name == 'vice_manager') and user_in == 0:
        #     user_in == 1


    #return User.objects.filter(id__in=uid_list)
    #return render(request, "faxat/denied.html")
    return [status , logged_out , cur_user]

def log_out_manage(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, "faxat/other_user_in.html")


def remove_all_sessions(user,request):
        #request.user = user
        #LoggedUserNew.logout_user(1,request,user)
        LoggedUserNew.logout_user(1,request,user)
        user_sessions = []
        all_sessions  = Session.objects.filter(expire_date__gte=timezone.now())
        for session in Session.objects.all():

            if str(user.pk) == session.get_decoded().get('_auth_user_id'):
                user_sessions.append(session.pk)
        return Session.objects.filter(pk__in=user_sessions).delete()
