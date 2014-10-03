# -*- coding: utf-8 -*-
import time
import calendar
from datetime import date, datetime, timedelta

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory
from cal.models import Entry
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from cal.forms import EntryForm


mnames = u"Janeiro Fevereiro Março Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro"
mnames = mnames.split()


def _show_users(request):
    """Return show_users setting; if it does not exist, initialize it."""
    s = request.session
    if not "show_users" in s:
        s["show_users"] = True
    return s["show_users"]


def reminders(request):
    """Return the list of reminders for today and tomorrow."""
    year, month, day = time.localtime()[:3]
    reminders = Entry.objects.filter(date__year=year, date__month=month,
                                     date__day=day, creator=request.user,
                                     remind=True)
    tomorrow = datetime.now() + timedelta(days=1)
    year, month, day = tomorrow.timetuple()[:3]
    return list(reminders) + list(Entry.objects.filter(date__year=year,
                                  date__month=month,
                                  date__day=day, creator=request.user,
                                  remind=True))


@login_required
def main(request, year=None):
    """Main listing, years and months; three years per page."""
    # prev / next years
    if year:
        year = int(year)
    else:
        year = time.localtime()[0]

    nowy, nowm = time.localtime()[:2]
    lst = []

    for y in [year, year+1, year+2]:
        mlst = []
        for n, month in enumerate(mnames):
            entry = current = False
            entries = Entry.objects.filter(date__year=y, date__month=n+1)
            if not _show_users(request):
                entries = entries.filter(creator=request.user)

            if entries:
                entry = True
            if y == nowy and n+1 == nowm:
                current = True
            mlst.append(dict(n=n+1, name=month, entry=entry, current=current))
        lst.append((y, mlst))

    return render_to_response("cal/main.html",
                              dict(years=lst, user=request.user, year=year,
                                   reminders=reminders(request)))


@login_required
def month(request, year=datetime.now().year,
          month=datetime.now().month, change=None):
    """Listing of days in `month`."""
    year, month = int(year), int(month)

    # apply next / previous change
    if change in ("next", "prev"):
        now, mdelta = date(year, month, 15), timedelta(days=31)
        if change == "next":
            mod = mdelta
        elif change == "prev":
            mod = -mdelta

        year, month = (now+mod).timetuple()[:2]

    # init variables
    cal = calendar.Calendar()
    month_days = cal.itermonthdays(year, month)
    nyear, nmonth, nday = time.localtime()[:3]
    lst = [[]]
    week = 0

    for day in month_days:
        entries = current = False
        if day:
            entries = Entry.objects.filter(date__year=year,
                                           date__month=month, date__day=day)
            if not _show_users(request):
                entries = entries.filter(creator=request.user)
            if day == nday and year == nyear and month == nmonth:
                current = True

        lst[week].append((day, entries, current))
        if len(lst[week]) == 7:
            lst.append([])
            week += 1

    return render_to_response("cal/month.html",
                              dict(year=year, month=month, user=request.user,
                                   month_days=lst, mname=mnames[month-1],
                                   reminders=reminders(request)))


class EntryCreate(CreateView):
    form_class = EntryForm
    template_name = 'cal/day2.html'

    def get_context_data(self, **kwargs):
        context = super(EntryCreate, self).get_context_data(**kwargs)
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)

        context['year'] = year
        context['month'] = month
        context['day'] = day
        context['qst'] = Entry.objects.filter(date__year=year,
                                              date__month=month,
                                              date__day=day,
                                              creator=self.request.user)
        return context

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.creator = self.request.user
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        self.instance.date = date(int(year), int(month), int(day))
        return super(EntryCreate, self).form_valid(form)

    def get_success_url(self):
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        return reverse_lazy('entry-create', args=(year, month, day))


class EntryUpdateView(UpdateView):
    form_class = EntryForm
    template_name = 'cal/update.html'
    model = Entry

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView, self).get_context_data(**kwargs)
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)

        context['year'] = year
        context['month'] = month
        context['day'] = day

        context['qst'] = Entry.objects.filter(date__year=year,
                                              date__month=month,
                                              date__day=day,
                                              creator=self.request.user)
        return context

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.creator = self.request.user
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        self.instance.date = date(int(year), int(month), int(day))
        return super(EntryUpdateView, self).form_valid(form)

    def get_success_url(self):
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        return reverse_lazy('entry-create', args=(year, month, day))


class EntryDeleteView(DeleteView):
    model = Entry
    success_url = reverse_lazy('entry-create')

    def get_context_data(self, **kwargs):
        context = super(EntryDeleteView, self).get_context_data(**kwargs)
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        context['year'] = year
        context['month'] = month
        context['day'] = day

        return context

    def get_success_url(self):
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        return reverse_lazy('entry-create', args=(year, month, day))


class EntryDetailView(DetailView):
    template_name = 'cal/detail.html'
    model = Entry

    def get_context_data(self, **kwargs):
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        context['year'] = year
        context['month'] = month
        context['day'] = day

        return context

    def get_success_url(self):
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        return reverse_lazy('entry-create', args=(year, month, day))


def add_csrf(request, **kwargs):
    """Add CSRF and user to dictionary."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d

entry_create = EntryCreate.as_view()
entry_update = EntryUpdateView.as_view()
entry_delete = EntryDeleteView.as_view()
entry_detail = EntryDetailView.as_view()
