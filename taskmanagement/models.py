from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Board(BaseModel):
    name = models.CharField(_("Name"), max_length=128)
    
    def __str__(self):
        return self.name
    

class Column(BaseModel):
    name = models.CharField(_("Name"), max_length=32)
    board = models.ForeignKey(
        Board,
        related_name='columns', 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Task(BaseModel):
    title = models.CharField(_('Title'), max_length=128)
    description = models.TextField(_('Description'))
    status = models.ForeignKey(
        Column, 
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_("Status"), 
    )

    def __str__(self):
        return self.title


class Subtask(BaseModel):
    title = models.CharField(_('Title'), max_length=128)
    is_selected = models.BooleanField(_('Is selected'), default=True)
    task = models.ForeignKey(
        Task, 
        related_name='subtasks',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title