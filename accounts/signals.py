from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from .models import UserProfile,User


@receiver(post_save,sender=User)
def post_save_create_profile_reciver(sender,instance,created,**kwrgs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('user profile is created')
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
        except:
            profile=UserProfile.objects.get(user=instance)
            print('profile is not exist,but i created on')
    print("user updated")

@receiver(pre_save,sender=User)
def pre_save_profile_reciver(sender,instance,**kwargs):
    print(instance.username,"this user is being saved")