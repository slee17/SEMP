"""
Original code was written by authors of django-scheduler. The following code was tailored by
Rachel Lee (slee17@cmc.edu) for CMC's Student Employee Management Program.

Original license:
Copyright (c) 2008-2015, Tony Hauber
All rights reserved.
 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:
 
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of the author nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from __future__ import unicode_literals
from six.moves.builtins import str
from six.moves.builtins import object
from six import with_metaclass
from dateutil.rrule import DAILY, MONTHLY, WEEKLY, YEARLY, HOURLY, MINUTELY, SECONDLY

from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from schedule.utils import get_model_bases

freqs = (("YEARLY", _("Yearly")),
         ("MONTHLY", _("Monthly")),
         ("WEEKLY", _("Weekly")),
         ("DAILY", _("Daily")),
         ("HOURLY", _("Hourly")),
         ("MINUTELY", _("Minutely")),
         ("SECONDLY", _("Secondly")))


@python_2_unicode_compatible
class Rule(with_metaclass(ModelBase, *get_model_bases())):
    """
    This defines a rule by which an event will recur.  This is defined by the
    rrule in the dateutil documentation.

    * name - the human friendly name of this kind of recursion.
    * description - a short description describing this type of recursion.
    * frequency - the base recurrence period
    * param - extra params required to define this type of recursion. The params
      should follow this format:

        param = [rruleparam:value;]*
        rruleparam = see list below
        value = int[,int]*

      The options are: (documentation for these can be found at
      http://labix.org/python-dateutil#head-470fa22b2db72000d7abe698a5783a46b0731b57)
        ** count
        ** bysetpos
        ** bymonth
        ** bymonthday
        ** byyearday
        ** byweekno
        ** byweekday
        ** byhour
        ** byminute
        ** bysecond
        ** byeaster
    """
    name = models.CharField(_("name"), max_length=32)
    description = models.TextField(_("description"))
    frequency = models.CharField(_("frequency"), choices=freqs, max_length=10)
    params = models.TextField(_("params"), null=True, blank=True)

    class Meta(object):
        verbose_name = _('rule')
        verbose_name_plural = _('rules')
        app_label = 'schedule'

    def rrule_frequency(self):
        compatibiliy_dict = {
                'DAILY': DAILY,
                'MONTHLY': MONTHLY,
                'WEEKLY': WEEKLY,
                'YEARLY': YEARLY,
                'HOURLY': HOURLY,
                'MINUTELY': MINUTELY,
                'SECONDLY': SECONDLY
                }
        return compatibiliy_dict[self.frequency]

    def get_params(self):
        """
        >>> rule = Rule(params = "count:1;bysecond:1;byminute:1,2,4,5")
        >>> rule.get_params()
        {'count': 1, 'byminute': [1, 2, 4, 5], 'bysecond': 1}
        """
        if self.params is None:
            return {}
        params = self.params.split(';')
        param_dict = []
        for param in params:
            param = param.split(':')
            if len(param) == 2:
                param = (str(param[0]), [int(p) for p in param[1].split(',')])
                if len(param[1]) == 1:
                    param = (param[0], param[1][0])
                param_dict.append(param)
        return dict(param_dict)

    def __str__(self):
        """Human readable string for Rule"""
        return 'Rule %s params %s' % (self.name, self.params)
