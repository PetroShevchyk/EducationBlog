from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
import uuid

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, **extra_fields)
    
    def create_superuser(self, name=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    certificate = models.ImageField(upload_to='certificates', blank=True, null=True)
    friends = models.ManyToManyField('self')
    friends_count = models.IntegerField(default=0)
    info = models.TextField(blank=True, null=True)

    posts_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_certificate(self):
        if self.certificate:
            return 'http://127.0.0.1:8000' + self.certificate.url
        else:
            return ''

    def get_avatar(self):
        if self.avatar:
            return 'http://127.0.0.1:8000' + self.avatar.url
        else:
            return 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMwAAADACAMAAAB/Pny7AAAAYFBMVEX///9UWV1QVVnY2dpjZ2tCSU2nqao/RUpNUldKT1RGTFH6+vr29vbm5+c8Q0iIi43e3+Bvc3Y0O0F8f4Lt7u5bX2PLzM2WmZvExsePkpS5u7yvsbLQ0tJ1eHwsNDueoKLQ22e3AAAF50lEQVR4nO2d7ZKjKhBAAxJF/MTvqInv/5arSeXm7kxmBrWxe7Y4P/bHbm0Vp4C2xaZzOjkcDkrEVe6Nzczo5VWMPZodJM0wtVmphahrIXSZtdPQJNij2kDU+NlVcKVCKfkdKUOluLhmfhNhj24VeasFDyVnn+Ay5EK3OfYIjRmv85jfiLyEOLs22KM0oquDb0T+EwrqDnukPxF5ojBQuesUwiO9eZLsZqhy17lldGNb1Z+VucqCOvcV9qjfk19MNsuHyQkuFANb1OlwrcpCqDtyOycearnFhTFZD8TSnHhiG11mGz6Rsoku4ert8oLLC6WVlq2MYh9RGbbBizLY58JYUGI7PJmKvS6MFRO2xYN+97wsBD22x8LId+z9F5yP2CZzOqY3x+S/kRo9UYtbIJfZpsV+3PQMZJEtcIa8bXKoRbYgNWrSGflnOBfGzj5mJuDBRLInnHt4LnELOjHz1CDGAA/kcfl/ArSpiaAnZpkarF2T7MyV36Gwnpw++Cqb15mPJAMbyh5wjuPiAWT+nylwQsDe18v3IL10pjZcGEsxXDxbMhjrzLeyyuZ1hhHPtIVYtsA1gowll9nmeJfEnszxSUBnT+b4T2qDPZnhcJnWnkx7uExpT+b4o1pbkRklNjsZJ+NknMy/IVMCHjL/jTz+OXOxNzOXw2V8ezLHv539U1mzZ0/m+EOA2J4MwpcAYesMQBzvcpo2VWT9TIhR3jDaOjdDqQewctTMWIHhcrpayQHkFUWmsbLOUqTqbTufNHBcTq2Nz4DHH808SCxMTYH1TTOG/9ykMrRCgBH+0zle0VkFPTUqQ6ymb4DzM455qwa4eAazdGZmFJD1ZgK5TNMHzJ1DrOqMJ3EJFgNUiV2jefKgXtK4QKyce9LDuDDsctMHE8hCU0Tq5zOAUq2Ayj2NGOKWBvrmf5LstQlK9NL5F0m5660zpeSy3DbdYZNSu3tatZtt0pbexdNh2x06Hh5fkGFAsyXplILoXfoqYyvTzpBhvo39QK/DFbMjQ00ihfmKxNfKUEcq7ROLYp/wfB0Y6MhA+wSy5J+I8kGnP+SeKtVDTukK8NdEydiq4stIHaaqbZLfoXInrpoLu6XqgxBX6S28NL+wNVBU9a0obkWRpkGQpkVxu4m2r37RlHwm8Zqu77vGox66HA6Hw+Fw7CWaiReqJPc8bxznP/Kkuv/V8m/Y4zMimkef5GPvt9lVyHTJzBaWzGzhVqRSXLPW75s8md3ISi0dM5uhLcW5KIKzetve8J45y1Cdg7Q4i7IdGoLdNau86adMnNOz+q6z4UcrNf8HkU3zNFE51ojybrhcWaC2npupgF0vQ4f/5hmNs0gdmB5ifIVUQT0LjagtNKZy6f25T+Q5Q0u30HJCOuSofF0z8x1iJsRq7R+/f/KSSzv9ACQvD52eqKtTa/ca5h2U1oc1Pax6ZtrFdCu8YIc02Ez62rbKQ6fubZ+AVJ1xb9n9OqKzOTtxk5mcI0Mhg6yxluvkU22pocFXhPVkp7FW1GvYp4oJXOreQmCLs+09TPcgGXwNal4fPy0PuKyBl1p/VAx7q1OAfi3MLN3IMKWAKxOyUIy9FrAqwQSucnGPDUg+QMIFyIaIC4hNRcVlsdmZqkX4e/+FyvYlAxdCLrPNrivcvaXri1tJdzw9kxv26D9y2x4EbJxY7GN7/8MMJU3+HrkxsWngWjHDwdmmysHKzg3ZvcjrlqeNvZ5f+9jSMSynOTHL1Kx/VxssXfffz/raYbITs2VqYH6GwQ5rf9whKcmusnmdrXwZgL/oC8m6S8ORjb7ScASrWu5XkL9dAI/Uax6c8G3lYVnVpJ5yLFsIVhxARxnhWLYQrniBjmuiedkTXpufCcbIp7E/U5jL2OkrD8mKHvV22uNAsqLVDvVgtio9G0gnMwtn89cA2N/7scHZvKmDkzkUJ0MVJ0MVJ0MVJ0MVJ0MVJ0MVJ0MVJ0MVJ0MVJ0MVJ0MVJ0MVJ0OVNTIpJ05qLjMwQRxm/kkj8cjjGj85sPgDeLCCjGW01/UAAAAASUVORK5CYII='


class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(User, related_name='received_friendshiprequests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_friendshiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)