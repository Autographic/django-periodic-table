from django.utils.translation import ugettext_lazy as _


LARGEST_ATOMIC_NUMBER = 118 # as of 2017, anyhow... ;-)

# Element categorization codes
METAL =             0
NONMETAL =          1
METALLOID =         2
HALOGEN =           3
NOBLE_GAS =         4
ALKALI_METAL =      5
ALKALI_EARTH =      6
LANTHANIDE =        7
ACTINIDE =          8
TRANSITION_METAL =  9
BASIC_METAL =       10
SOLID =             11
LIQUID =            12
GAS =               13


##### Categorizing elements by atomic number #####

# Metallicity
NONMETALS =         1,2,6,7,8,9,10,15,16,17,18,34,35,36,53,54,85,86,118
METALLOIDS =        5,14,32,33,51,52,84
METALS =            tuple ( [ i for i in range(1, LARGEST_ATOMIC_NUMBER+1)
    if i not in METALLOIDS and i not in NONMETALS ])

# Phase at standard temperature and pressure
STP_LIQUIDS =       35,80
STP_GASES =         1,2,7,8,9,10,17,18,36,54,86,118
STP_SOLIDS =        tuple ( [ i for i in range(1, LARGEST_ATOMIC_NUMBER)
    if i not in STP_LIQUIDS and i not in STP_GASES ])

# Element types
HALOGENS =          9,17,35,53,85,117
NOBLE_GASES =       2,10,18,36,54,86,118
ALKALI_METALS =     3,11,19,37,55,87
ALKALI_EARTHS =     4,12,20,38,56,88
LANTHANIDES =       tuple ( range ( 57, 72 ) )
ACTINIDES =         tuple ( range ( 89, 104 ) )
TRANSITION_METALS = tuple (
    list ( range ( 21,31 ) ) + list ( range ( 39,49 ) ) + 
    list ( range ( 72,81 ) ) + list ( range ( 104,113 ) )
    )
BASIC_METALS =      13,31,49,50,81,82,83,113,114,115,116


# Group labels by column number (there is no zeroth column, of course)
PERIODIC_TABLE_GROUPS = ( None,'1A','2A','3B','4B','5B','6B','7B',
    '8B','8B','8B','1B','2B','3A','4A','5A','6A','7A','8A' )


CATEGORY_LABELS = {
    METAL:          _(u'metal'),
    NONMETAL:       _(u'nonmetal'),
    METALLOID:      _(u'metalloid'),
    SOLID:          _(u'solid [STP]'),
    LIQUID:         _(u'liquid [STP]'),
    GAS:            _(u'gas [STP]'),
    ALKALI_METAL:   _(u'alkali metal'),
    ALKALI_EARTH:   _(u'alkali earth'),
    HALOGEN:        _(u'halogen'),
    NOBLE_GAS:      _(u'noble gas'),
    LANTHANIDE:     _(u'lanthanide'),
    ACTINIDE:       _(u'actinide'),
    TRANSITION_METAL: _(u'transition metal'),
    BASIC_METAL:    _(u'basic metal'),
}

CSS_CLASSES = {
    METAL:          'dpt_met',
    NONMETAL:       'dpt_nmet',
    METALLOID:      'dpt_moid',
    SOLID:          'dpt_solid',
    LIQUID:         'dpt_liquid',
    GAS:            'dpt_gas',
    ALKALI_METAL:   'dpt_amet',
    ALKALI_EARTH:   'dpt_aear',
    HALOGEN:        'dpt_hal',
    NOBLE_GAS:      'dpt_nob',
    LANTHANIDE:     'dpt_lan',
    ACTINIDE:       'dpt_act',
    TRANSITION_METAL: 'dpt_tmet',
    BASIC_METAL:    'dpt_bmet',
}

