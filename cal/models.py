# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Entry(models.Model):
    title = models.CharField(max_length=40, verbose_name='Título')
    snippet = models.CharField(max_length=150, blank=True, verbose_name='Dica')
    body = models.TextField(max_length=10000, blank=True, verbose_name='Corpo')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    date = models.DateField(blank=True, verbose_name='Data')
    creator = models.ForeignKey(User, blank=True, null=True,
                                verbose_name='Criado por')
    remind = models.BooleanField(default=False, verbose_name='Lembrete')

    def __unicode__(self):
        if self.title:
            return unicode(self.creator) + u" - " + self.title
        else:
            return unicode(self.creator) + u" - " + self.snippet[:40]

    def short(self):
        if self.snippet:
            return "<i>%s</i> - %s" % (self.title, self.snippet)
        else:
            return self.title
    short.allow_tags = True

    class Meta:
        verbose_name_plural = "entries"

