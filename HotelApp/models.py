from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
# Create your models here.
class Tablebook(models.Model):
    Date = models.DateTimeField(auto_now=True)
    count = models.IntegerField()
    name = models.CharField(max_length=40)
    num = models.BigIntegerField()
    mail = models.EmailField()
    spl = models.TextField(max_length=300)

@receiver(pre_save,sender = Tablebook)
def customsendmail(sender,instance,**kwargs):
    sub = 'Table Book Ayyipoendhi Bossuu....!'
    msg = '''
            Dear Customer {},Your table booking is confirmed with {} People in the date & Time of {}.From ACN's FOODELICIOU's
    
        They are lot of exclusive offers are running in our 
        restaurant...!
        The main caution and i strongly believe that if 
        once you can visit our hotel you never ever forget 
        the taste of our special desi food items.
        |
        |
        |...Thanks for Booking...!
    '''.format(instance.name,instance.count,instance.Date)
    
    send_mail(subject=sub,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=['{}'.format(instance.mail)])

pre_save.connect(customsendmail,Tablebook)

class ContactTable(models.Model):
    name = models.CharField(max_length=40)
    mail = models.EmailField()
    spl = models.TextField(max_length=300)

@receiver(pre_save,sender = Tablebook)
def customsendmail(sender,instance,**kwargs):
    sub = 'Hey Hi User What Can I Do For You...!'
    msg = '''
            Dear Customer {},Your Thanks for contacting we are From ACN's FOODELICIOU's What can I do for you..>!
    
        They are lot of exclusive offers are running in our 
        restaurant...!
        The main caution and i strongly believe that if 
        once you can visit our hotel you never ever forget 
        the taste of our special desi food items.
        |
        |
        |...Thanks for Contacting Us...!
    '''.format(instance.name)
    
    send_mail(subject=sub,message=msg,from_email=settings.EMAIL_HOST_USER,recipient_list=['{}'.format(instance.mail)])

pre_save.connect(customsendmail,ContactTable)