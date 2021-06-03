from django.db import models
from datetime import datetime

# Create your models here.
from django.utils.timezone import now
#import datetime
class fax(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key = True)
    sader = models.IntegerField(default=0)
    sader_edara = models.IntegerField(default=0)
    title = models. TextField()

    url = models.FileField(upload_to='faxat_data/faxes/%Y/%m/%d')
    replay_to_edara = models.FileField(upload_to='faxat_data/replay_to_edara/%Y/%m/%d', null=True, blank = True)

    comments = models. TextField(default=' ')
    ## 0 wared tag.zag ,  1. sader from tag.zag

    replay_dept = models.TextField(default=' ')
    send_dept = models.TextField(default=' ')
    come_from_dept = models.TextField(default=' ')

    manager_comments = models.TextField(default=' ')
    v_manager_comments = models.TextField(default=' ')
    #date_added = models.DateTimeField(default = datetime.now , null =True, blank = True , editable = False)
    date_added = models.DateTimeField(default = now , null =True, blank = True , editable = False)
    approved = models.IntegerField(default=0)
    approved_id = models.TextField(default=' ')
    #date_aproved = models.DateTimeField(default =  datetime.now, null =True , blank = True,   editable = False)
    date_aproved = models.DateTimeField(default = now, null =True , blank = True,   editable = False)
    fax_type = models.IntegerField(default=0)
    notified = models.IntegerField(default=0)
    is_removable = models.IntegerField(default=0)
    last_notified_m = models.DateTimeField(default =now)
    last_notified_vm = models.DateTimeField(default = now)

    def __str__(self):
        return self.title + "    " + str(self.sader)

class dept(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=30)
    fax = models.ManyToManyField(fax, through ='dept_fax',  blank=True)
    def __str__(self):
        return self.name



class dept_fax(models.Model):
    objects = models.Manager()
    status = models.IntegerField(default=0)
    reply_status = models.IntegerField(default=0)
    #in case of send only faxes no reply need
    seen = models.IntegerField(default = 0)
    dept = models.ForeignKey(dept, on_delete = models.CASCADE, null = True)
    fax = models.ForeignKey(fax, on_delete = models.CASCADE, null = True)
    notified = models.IntegerField(default=0)
    last_notified = models.DateTimeField(default = now)
    seen_by = models.CharField(max_length = 264 , default="")


    def __str__(self):
        return self.dept.name +  "  --  fax title :-> " + self.fax.title



class fax_comments(models.Model):

    # to count number of unseen comments and display them to user
    seen = models.IntegerField(default = 0)
    dep_comment = models.TextField(default="")
    dep_document = models.FileField(upload_to='faxat_data/comments/%Y/%m/%d', null=True)
    writer = models.CharField(max_length=264 , null = True)
    user_type = models.CharField(max_length=264, null=True)
    dept_fax = models.ForeignKey(dept_fax, on_delete = models.CASCADE)
    date = models.DateTimeField()
    notified = models.IntegerField(default=0)
    last_notified = models.DateTimeField(default = now)
    ## message_status
    ## s = 1    from dept to motab3a
    ##s = 2    from motab3a to dept
    ## s = 3   from motab3a to manager
    ## s = 4  from manager to all other depts except motab3a
    ## s = 5  from manager to motab3a
    comment_status = models.IntegerField(default = 10)
    seen_by = models.CharField(max_length = 264 , default="")
    def __str__(self):
        return self.writer

from django.contrib.auth.models import User
class LoggedUserNew(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user.username

    def login_user(sender, request, user, **kwargs):
        #print("current user count : %d" %(LoggedUserNew.objects.filter(user= user).count()))
        if(LoggedUserNew.objects.filter(user= user).count() == 0):
                print("register new user: "+str(user))
                LoggedUserNew(user=user).save()


    def logout_user(sender, request, user, **kwargs):
        try:
            #print("log_out  user (1): "+str(user))
            u = LoggedUserNew.objects.filter(user=user).first()
            if u != None :
                u.delete()
        except LoggedUserNew.DoesNotExist:
            #print("log_out  user (2): "+str(user))
            pass
