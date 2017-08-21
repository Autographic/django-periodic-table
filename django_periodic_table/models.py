from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

import periodictable as pt
from .settings import *


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
        # Simplified approach: just construct the list of metals above.
        return self._Q_query_filter ( METALS )
        
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
    
    @property
    def transition_metals( self ):
        """Returns a QuerySet containing the trnaition metals."""
        return self._Q_query_filter ( TRANSITION_METALS )
    
    @property
    def basic_metals( self ):
        """Returns a QuerySet containing the basic metals."""
        return self._Q_query_filter ( BASIC_METALS )
    
    def group_by_name( self, group ):
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
    
    def _Q_query_exclude ( self, element_numbers, criterion='atomic_number' ):
        "Build a query to select non-contiguous ranges of elements."
        return self.get_queryset().exclude (
            self._build_Q_query( element_numbers, criterion ))
    
    def _range_query_filter ( self, low, high ):
        "Build a query to select contiguous ranges of elements."
        return self.get_queryset().filter ( 
            atomic_number__gte=low).filter ( atomic_number__lte=high )


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
    
    ptvideo = models.CharField ( _("PeriodicVideos entry on YouTube"),
        help_text="YouTube video code for this element's entry by Periodicvideos."
        max_length=11,
        default="",
    )
    
    # Respecification of CSS classes is easy through subclassing
    CSS_CLASSES = CSS_CLASSES
    
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
    
    def phase_at_stp( self, labels=CATEGORY_LABELS ):
        "Solid, liquid or gas at standard temperature and pressure."
        n = self.atomic_number
        if n in STP_LIQUIDS:    return labels [ LIQUID ]
        elif n in STP_GASES:    return labels [ GAS ]
        # TODO: add label for unknown properties
        return labels [ SOLID ]
    
    def phase_at_stp_css( self ):
        "CSS classes for STP matter phase."
        return self.phase_at_stp ( labels = self.CSS_CLASSES )
    
    def metallicity( self, labels=CATEGORY_LABELS ):
        "Metal, nonmetal or metalloid categorization."
        n = self.atomic_number
        if n in NONMETALS:      return labels [ NONMETAL ]
        elif n in METALLOIDS:   return labels [ METALLOID ]
        return labels [ METAL ]
    
    def metallicity_css( self ):
        "Metal, nonmetal or metalloid categorization by CSS classes."
        return self.metallicity ( labels = self.CSS_CLASSES )
    
    def category( self, labels=CATEGORY_LABELS ):
        "Any special groups (noble gases, actinides, etc.)."
        n = self.atomic_number
        if n in HALOGENS:           return labels [ HALOGEN ]
        if n in NOBLE_GASES:        return labels [ NOBLE_GAS ]
        if n in ALKALI_METALS:      return labels [ ALKALI_METAL ]
        if n in ALKALI_EARTHS:      return labels [ ALKALI_EARTH ]
        if n in LANTHANIDES:        return labels [ LANTHANIDE ]
        if n in ACTINIDES:          return labels [ ACTINIDE ]
        if n in TRANSITION_METALS:  return labels [ TRANSITION_METAL ]
        if n in BASIC_METALS:       return labels [ BASIC_METAL ]
        return ''
    
    def category_css( self ):
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
        # Anticipating elements after oganesson...
        return line + 1
    
    @property
    def group_name(self):
        "The group name of the element, e.g., 8B for iron."
        return PERIODIC_TABLE_GROUPS[ self.group ]
    
    @property
    def group_members(self):
        "All the members of this element's group."
        return self.__class__.objects.group_name( self.group )
    
    @property
    def css_class(self):
        "String of HTML classes, for meaningful presentation."
        values = [
            self.metallicity_css(),
            self.category_css(),
            self.phase_at_stp_css(),
        ]
        return ' '.join([ i for i in values if len(i) ])
    
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
