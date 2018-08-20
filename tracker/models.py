from django.conf import settings as django_settings


from django.template.defaultfilters import date
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.urls import reverse

# Create your models here.


# #  
# Rule
# #

from dateutil.rrule import (
    YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY,
    MO, TU, WE, TH, FR, SA, SU
)

freqs = (("YEARLY", _("Yearly")),
         ("MONTHLY", _("Monthly")),
         ("WEEKLY", _("Weekly")),
         ("DAILY", _("Daily")),
         ("HOURLY", _("Hourly")),
         ("MINUTELY", _("Minutely")),
         ("SECONDLY", _("Secondly")))

class Rule(models.Model):
    '''
    Defines a rule by which an event recur
    '''
    name = models.CharField(_("name"), max_length=32)
    description = models.TextField|(_("description"))
    frequency = models.CharField(_("frequency"), choices=freqs, max_length=10)
    params = models.TextField(_("params"), blank=True)

    _week_days = {'MO': MO,
                  'TU': TU,
                  'WE': WE,
                  'TH': TH,
                  'FR': FR,
                  'SA': SA,
                  'SU': SU}

    class Meta:
        verbose_name = _("rule")
        verbose_name_plural = _("rules")
    
    def rrule_frequency(self):
        compatibility_dict = {
            'YEARLY': YEARLY,
            'MONTHLY': MONTHLY,
            'WEEKLY': WEEKLY,
            'DAILY': DAILY,
            'HOURLY': HOURLY,
            'MINUTELY': MINUTELY,
            'SECONDLY': SECONDLY
        }
        return compatibility_dict[self.frequency]
    
    def __str__(self):
        """Human readable string for Rule"""
        return 'Rule %s params %s' % (self.name, self.params)




















# #  
# Event
# #


class Event(models.Model):
    '''
    Meta information about event
    '''
    start = models.DateTimeField(_("start"), db_index=True)
    end = models.DateTimeField(_("end"), db_index=True, help_text=_("The end time must be later than the start time."))
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creator = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("creator"),
        related_name='creator'
    )
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)

    color_event = models.CharField(_("Color event"), blank=True, max_length=10)
    # objects = EventManager()

    class Meta(object):
        verbose_name = _("event")
        verbose_name_plural = _("events")
        index_together = (
            ('start', 'end'),
        )
    
    def __str__(self):
        return ugettext('%(title)s: %(start)s - %(end)s') % {
            'title': self.title,
            'start': date(self.start, django_settings.DATE_FORMAT),
            'end': date(self.end, django_settings.DATE_FORMAT),
        }

    @property
    def seconds(self):
        return (self.end - self.start).total_seconds()

    @property
    def minutes(self):
        return float(self.seconds) / 60

    @property
    def hours(self):
        return float(self.seconds) / 3600
    
    def get_absolute_url(self):
        return reverse('event', args=[self.id])