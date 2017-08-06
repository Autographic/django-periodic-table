# Django Periodic Table
# An implementation of the periodictable module for Django.
# Copyright (C) 2017 Murray Pearson, murray@autographic.ca
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

import periodictable as pt


LARGEST_ATOMIC_NUMBER = 118 # as of 2017, anyhow... ;-)

# Element categorization codes
METAL =         0
NONMETAL =      1
METALLOID =     2
HALOGEN =       3
NOBLE_GAS =     4
ALKALI_METAL =  5
ALKALI_EARTH =  6
LANTHANIDE =    7
ACTINIDE =      8

# Categorizing elements by atomic number
NONMETALS =     1,2,6,7,8,10,15,16,18,34,36,54,86,118
METALLOIDS =    5,14,32,33,51,52,84
HALOGENS =      9,17,35,53,85,117
NOBLE_GASES =   2,10,18,36,54,86,118
ALKALI_METALS = 3,11,19,37,55,87
ALKALI_EARTHS = 4,12,20,38,56,88
LANTHANIDES =   tuple ( range ( 57, 72 ) )
ACTINIDES =     tuple ( range ( 89, 104 ) )

# Group labels by column number (there is no zeroth column, of course)
PERIODIC_TABLE_GROUPS = ( None,'1A','2A','3B','4B','5B','6B','7B',
    '8B','8B','8B','1B','2B','3A','4A','5A','6A','7A','8A' )


class PeriodicTableManager(models.Manager):
    "Generic periodic table search methods."
    
    @property
    def normal_elements( self ):
        "Exclude deuterium and tritium: atomic numbers aren't repeated in sets."
        return super(PeriodicTableManager, self
            ).get_queryset().filter(pk__lt=1000 )
    
    @property
    def nonmetals( self ):
        """Returns a QuerySet containing the nonmetals."""
        return self._Q_query_filter ( NONMETALS )
    
    @property
    def metalloids( self ):
        """Returns a QuerySet containing the metalloids."""
        return self._Q_query_filter ( METALLOIDS )
    
    @property
    def halogens( self ):
        """Returns a QuerySet containing the halogens."""
        return self._Q_query_filter ( HALOGENS )
    
    @property
    def alkali_metals( self ):
        """Returns a QuerySet containing the alkali metals."""
        return self._Q_query_filter ( ALKALI_METALS )
    
    @property
    def alkali_earths( self ):
        """Returns a QuerySet containing the alkali earths."""
        return self._Q_query_filter ( ALKALI_EARTHS )
    
    @property
    def noble_gases( self ):
        """Returns a QuerySet containing the noble gases."""
        return self._Q_query_filter ( NOBLE_GASES )
    
    @property
    def metals( self ):
        """Returns a QuerySet containing the metals."""
        # Exclude these categories from the generalized metals category.
        other_elements = list( NONMETALS ) + list( METALLOIDS ) + \
            list( HALOGENS ) + list( NOBLE_GASES )
        return self._Q_query_exclude ( other_elements )
    
    @property
    def lanthanides( self ):
        """Returns a QuerySet containing the lanthanides."""
        return self._range_query_filter ( 57, 71 )
    
    @property
    def actinides( self ):
        """Returns a QuerySet containing the actinides."""
        return self._range_query_filter ( 89, 103 )
    
    def group_name( self, group ):
        """Returns a QuerySet with the elements in a given group name."""
        try: # if given a group number, change it to the group name
            group_name = PERIODIC_TABLE_GROUPS[int(group)]
        except ValueError: group_name = group
        group_name = group_name.upper() # case insensitive search
        if group_name == '8B': # This consists of multiple groups
            return self._Q_query_filter ( (8,9,10), 'group' )
        return self.get_queryset().filter ( 
            group = PERIODIC_TABLE_GROUPS.index(group_name) )
    
    
    # Utility functions
    def _build_Q_query ( self, element_numbers, criterion='atomic_number' ):
        "Build a query to select non-contiguous ranges of elements."
        Q_template = 'Q(%s="%%d")' % criterion
        return eval (
            '|'.join([ Q_template % n for n in element_numbers ] ))
    
    def _Q_query_filter ( self, element_numbers, criterion='atomic_number' ):
        "Build a query to select non-contiguous ranges of elements."
        return self.get_queryset().filter (
            self._build_Q_query( element_numbers, criterion ))
        #return super(PeriodicTableManager, self).get_queryset().filter (
        #    self._build_Q_query( element_numbers, criterion ))
    
    def _Q_query_exclude ( self, element_numbers, criterion='atomic_number' ):
        "Build a query to select non-contiguous ranges of elements."
        return self.get_queryset().exclude (
            self._build_Q_query( element_numbers, criterion ))
        #return super(PeriodicTableManager, self).get_queryset().exclude (
        #    self._build_Q_query( element_numbers, criterion ))
    
    def _range_query_filter ( self, low, high ):
        "Build a query to select contiguous ranges of elements."
        return self.get_queryset().filter ( 
            atomic_number__gte=low).filter ( atomic_number__lte=high )
        #return super(PeriodicTableManager, self).get_queryset().filter ( 
        #    atomic_number__gte=low).filter ( atomic_number__lte=high )


class Element(models.Model):
    atomic_number = models.PositiveSmallIntegerField ( 
        validators = [
            MaxValueValidator ( LARGEST_ATOMIC_NUMBER,
                _(u'The largest atomic number is %d.' % ( 
                    LARGEST_ATOMIC_NUMBER
                )),
            ),
        ], 
    )
    
    symbol = models.CharField ( _("chemical symbol"),
        max_length=3, # support IUPAC temporary element symbols too
    )
    
    group = models.PositiveSmallIntegerField (
        default=0, # yes, the default is an invalid value!
        validators = [
            MinValueValidator ( 1,
                _(u'The smallest atomic group number is 1.'),
            ),
            MaxValueValidator ( 18,
                _(u'The largest atomic group number is 18.'),
            ),
        ], 
    )
    
    
    CATEGORY_LABELS = {
        METAL:          _(u'metal'),
        NONMETAL:       _(u'nonmetal'),
        METALLOID:      _(u'metalloid'),
        ALKALI_METAL:   _(u'alkali metal'),
        ALKALI_EARTH:   _(u'alkali earth'),
        HALOGEN:        _(u'halogen'),
        NOBLE_GAS:      _(u'noble gas'),
        LANTHANIDE:     _(u'lanthanide'),
        ACTINIDE:       _(u'actinide'),
    }

    CSS_CLASSES = {
        METAL:          'dpt_met',
        NONMETAL:       'dpt_nmet',
        METALLOID:      'dpt_moid',
        ALKALI_METAL:   'dpt_amet',
        ALKALI_EARTH:   'dpt_aear',
        HALOGEN:        'dpt_hal',
        NOBLE_GAS:      'dpt_nob',
        LANTHANIDE:     'dpt_lan',
        ACTINIDE:       'dpt_act',
    }
    
    @property
    def atomic_mass(self):
        "The element's mass in amu."
        return self._ptentry.mass
    
    @property
    def density(self):
        "Element's density in kg m^-3."
        return self._ptentry.density
    
    @property
    def name(self):
        "The element's name in English."
        return self._ptentry.name
    
    @property
    def ions(self):
        "A list of ions for this element."
        return self._ptentry.ions
    
    @property
    def isotopes(self):
        "A list of isotopes for this element."
        return self._ptentry.isotopes
    
    @property
    def metallicity( self, labels=None ):
        "Metal, nonmetal or metalloid categorization."
        n = self.atomic_number
        if labels is None: labels = self.CATEGORY_LABELS
        if n in NONMETALS:      return labels [ NONMETAL ]
        elif n in METALLOIDS:   return labels [ METALLOID ]
        return labels [ METAL ]
    
    @property
    def metallicity_css( self ):
        "Metal, nonmetal or metalloid categorization by CSS classes."
        return self.metallicity ( labels = self.CSS_CLASSES )
    
    @property
    def category( self, labels=None ):
        "Any special groups (noble gases, actinides, etc.)."
        n = self.atomic_number
        if labels is None: labels = self.CATEGORY_LABELS
        if n in HALOGENS:       return labels [ HALOGEN ]
        if n in NOBLE_GASES:    return labels [ NOBLE_GAS ]
        if n in ALKALI_METALS:  return labels [ ALKALI_METAL ]
        if n in ALKALI_EARTHS:  return labels [ ALKALI_EARTH ]
        if n in LANTHANIDES:    return labels [ LANTHANIDE ]
        if n in ACTINIDES:      return labels [ ACTINIDE ]
    
    @property
    def category_css( self, labels=None ):
        "Any special groups (noble gases, actinides, etc.) as CSS classes."
        return self.category ( labels = self.CSS_CLASSES )
    
    @property
    def period(self):
        "The row of the periodic table on which this element resides."
        n = self.atomic_number
        line = 0
        for ng in NOBLE_GASES:
            line += 1
            if n > ng: continue
            return line
    
    @property
    def group_name(self):
        "The group name of the element, e.g., 8B for iron."
        return PERIODIC_TABLE_GROUPS[ self.group ]
    
    @property
    def group_members(self):
        "All the members of this element's group."
        return self.__class__.objects.group_name( self.group )
    
    @property
    def html_class(self):
        "String of HTML classes, for meaningful rendering."
        met = self.metallicity
        cat = METAL
    
    objects = PeriodicTableManager()
    
    def __str__(self):
        return u"%s(%s)" % (self.name, self.symbol)
    
    @property
    def _ptentry(self):
        # Is this unnecessary optimization?
        try: return self._cached_pt_entry
        except AttributeError:
            self._cached_pt_entry = pt.__getattribute__(self.symbol)
            return self._cached_pt_entry

