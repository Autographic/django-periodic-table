from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Element


class IndexView(TemplateView):
    template_name = "django_periodic_table/periodic_table_index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        lan = context['lanthanides'] = Element.objects.lanthanides.all()
        act = context['actinides'] = Element.objects.actinides.all()
        mtd = {}
        for e in Element.objects.normal_elements.all():
            if e in lan or e in act: continue
            g, p = e.group, e.period
            try: mtd[p]
            except KeyError: mtd[p] = {}
            mtd[p][g] = e
        periods = list(mtd.keys())
        periods.sort()
        main_table = []
        for period in periods:
            pl = []
            for group in [i+1 for i in range(18)]:
                try:
                    pl.append(mtd[period][group])
                except: pl.append(None)
            main_table.append(pl)
        context['main_table'] = main_table
        return context
