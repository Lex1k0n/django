from django.db import models


class Mail(models.Model):

    email = models.EmailField(max_length=60)

    def __str__(self):
        return self.email


class Blueprint(models.Model):

    name = models.CharField(max_length=30)
    text = models.TextField(max_length=1500)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, txt):
        new_bp = cls(name=name, text=txt)
        return new_bp
