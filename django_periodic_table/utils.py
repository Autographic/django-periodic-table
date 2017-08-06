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

from .models import Element


def assign_group_numbers():
    "Set the group numbers for the entire table."
    qs = Element.objects
    def sg(symbol, group):
        e = qs.get(symbol=symbol)
        e.group = group
        e.save()
    def sl(symbols,group):
        for s in symbols: sg(s,group)
    
    sg('H',1)
    qs.alkali_metals.update( group=1 )
    qs.alkali_earths.update( group=2 )
    sl(['Sc','Y'], 3 )
    qs.lanthanides.update( group=3 )
    qs.actinides.update( group=3 )
    sl(['Ti','Zr','Hf','Rf'], 4 )
    sl(['V','Nb','Ta','Db'], 5 )
    sl(['Cr','Mo','W','Sg'], 6 )
    sl(['Mn','Tc','Re','Bh'], 7 )
    sl(['Fe','Ru','Os','Hs'], 8 )
    sl(['Co','Rh','Ir','Mt'], 9 )
    sl(['Ni','Pd','Pt','Ds'], 10 )
    sl(['Cu','Ag','Au','Rg'], 11 )
    sl(['Zn','Cd','Hg','Cn'], 12 )
    sl(['B','Al','Ga','In','Tl','Nh'], 13 )
    sl(['C','Si','Ge','Sn','Pb','Fl'], 14 )
    sl(['N','P','As','Sb','Bi','Mc'], 15 )
    sl(['O','S','Se','Te','Po','Lv'], 16 )
    qs.halogens.update( group=17 )
    qs.noble_gases.update( group=18 )

