from django.contrib.auth.models import AbstractUser


# ----------------------------------------------------------------
# user model
class User(AbstractUser):
    """
    Model representing user
    """
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
