from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create Tweet model
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="tweets")
    body = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self) -> str:
        return (
            f"{self.user}"
            f"({self.created_at:%Y-%M-%D %H:%M})"
            f"{self.body}..."
        )


# Create profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )
    profile_image = models.ImageField(null=True,blank=True,upload_to='images/')
    date_modified = models.DateTimeField(User, auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return self.user.username


# Create profile when new user created
# @receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        user_profile = Profile(user=instance)
        user_profile.save()
        # To follow yourself
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)
