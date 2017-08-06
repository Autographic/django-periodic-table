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

from django.test import TestCase

from .models import Element, NONMETALS, METALLOIDS, METAL, NONMETAL, METALLOID


class PeriodicTableTestCase(TestCase):
    fixtures = [ 'initial_data' ]
    
    def setUp(self):
        self.silver = Element.objects.get ( symbol='Ag' ) # Arbitrary choice
        self.oganesson = Element.objects.get ( atomic_number=118 )
        self.hydrogens = Element.objects.filter ( atomic_number=1 )
        self.hydrogen = Element.objects.normal_elements.filter ( atomic_number=1 )
    
    def test_find_elements(self):
        """Locate the correct elements in the table."""
        self.assertEqual ( self.silver.atomic_number, 47 )
        self.assertEqual ( self.oganesson.atomic_mass, 294 )
        self.assertEqual ( len( self.hydrogens ), 3 ) # Including D and T
        self.assertEqual ( len( self.hydrogen  ), 1 ) # Hydrogen only
    
    def test_atomic_properties(self):
        e = self.silver
        self.assertEqual ( e.atomic_number, 47 )
        self.assertEqual ( e.symbol, 'Ag' )
        self.assertEqual ( e.atomic_mass, 107.8682 )
        self.assertEqual ( e.density, 10.5 )
        self.assertEqual ( e.name, 'silver' )
        self.assertEqual ( e.ions, (-2, -1, 1, 2, 3, 4) )
        # Wow, silver has a lot of isotopes... from 94 to 127.
        self.assertEqual ( e.isotopes, list(range( 94, 128 )) )
        self.assertEqual ( e.metallicity, METAL )
        self.assertEqual ( e.period, 5 )
        self.assertEqual ( self.oganesson.metallicity, NONMETAL )
        self.assertEqual ( self.oganesson.period, 7 )
    
    def test_selectors ( self ):
        self.assertEqual ( Element.objects.metals.count(), 91 )
        self.assertEqual ( Element.objects.nonmetals.count(), 16 )
        self.assertEqual ( Element.objects.metalloids.count(), 7 )
        
        self.assertEqual ( Element.objects.noble_gases.count(), 7 )
        self.assertEqual ( Element.objects.halogens.count(), 6 )
        self.assertEqual ( Element.objects.alkali_metals.count(), 6 )
        self.assertEqual ( Element.objects.alkali_earths.count(), 6 )
        self.assertEqual ( Element.objects.actinides.count(), 15 )
        self.assertEqual ( Element.objects.lanthanides.count(), 15 )

