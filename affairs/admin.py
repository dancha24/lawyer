from django.contrib import admin
from django.db.models import QuerySet
from django.forms import BaseInlineFormSet
from .models import Affairs, ExtraAffairs, ExtraPerfomer
from .forms import AffairsForm


class ExtraPerfomerInlineFormSet(BaseInlineFormSet):

    def get_queryset(self,):
        global qs1488
        qs443 = super(ExtraPerfomerInlineFormSet, self).get_queryset()
        qs = qs443.query.where.children[0]
        sq = list(qs443)
        sqq = len(sq)
        if 0 == sqq:
            return qs443.none()
        qs1 = qs.rhs
        courses = Affairs.objects.get(id=qs1).performer.all()
        len1 = len(courses)
        if 0 == len1:
            return qs443.none()
        i = 0
        list1 = list()
        while i < len1:
            course = courses.values('id')
            a = list(course)
            b = a[i]
            c = b['id']
            list1.append(c)
            i += 1
        qs = ExtraPerfomer.objects.filter(performer_id__in=list1, affairs_id=qs1)
        return qs


class ExtraPerfomerInline(admin.TabularInline):
    model = ExtraPerfomer
    extra = 0
    formset = ExtraPerfomerInlineFormSet
    show_change_link = True
    readonly_fields = ('performer',)
    fields = ('performer', 'sum', 'payment',)

    # def get_queryset(self, request):
    #      qs = ExtraPerfomer.objects.all()
    #      a = request.resolver_match.kwargs
    #      b = a.items()
    #      y = list(b)
    #      u = list(y[0])
    #      i = u[1]
    #      courses = Affairs.objects.get(id=i).performer.all()
    #      da = courses[0]
    #      da1 = courses.count()
    #      dar = da1 - 1
    #      i1 = 0
    #      i2 = 0
    #      result = []
    #      qs4433 = super(ExtraPerfomerInlineFormSet, self).get_queryset()
    #      while i1 <= dar:
    #          da2 = courses[i1]
    #          da3 = da2.id
    #          qy3 = qs4433.filter(pk=da3)
    #          while i1 == i2:
    #              result.append((qy3, i1))
    #              i2 += 1
    #          i1 = i1 + 1
    #          qy3 = result
    #          qy33 = qy3[0]
    #          qy333 = qy33[0]
    #      result1 = tuple(result)
    #
    #      dad = da.id
    #
    #      m2 = ExtraPerfomer.objects.get(id=dad)  # он просто у меня есть
    #      m1 = Affairs.objects.get(id=i)
    #
    #      # x2 = m2.objects.filter(performer=m1.id)
    #
    #      # x = ExtraPerfomer.objects.values_list('id')
    #
    #      ccc = Affairs.objects.values_list('id', flat=True).last()
    #      course = super(ExtraPerfomerInlineFormSet, self).get_queryset()
    #      qs33 = ExtraPerfomer.objects.get(id=dad)
    #      courv = Affairs.objects.get(id=i).performer.all()
    #      qs11 = Affairs.objects.filter(pk__in=i).order_by('-id')
    #
    #      queryset = super(ExtraPerfomerInlineFormSet, self).get_queryset()
    #      ids = queryset.order_by('-id').values('pk')
    #      qs448 = ExtraPerfomer.objects.filter(pk=dad)
    #
    #      test1 = courv.values_list('id')
    #      test = ExtraPerfomer.objects.values().order_by('id')
    #
    #      for qs333 in queryset:
    #          qs333 = ExtraPerfomer.objects.filter(pk=dad)
    #
    #      qs443 = super(ExtraPerfomerInlineFormSet, self).get_queryset()
    #      qy = qs443.filter(pk=dad)
    #      return qy


@admin.register(Affairs)
class UserAccessAdmin(admin.ModelAdmin):
    change_list_template = 'admin/affairs_list.html'
    change_form_template = 'admin/affairs_view.html'
    add_form = AffairsForm
    form = AffairsForm
    list_display = ('name', 'customers', 'jobcategories')
    list_filter = ('deal_status', 'prise_status', 'customers', 'performer', 'jobcategories')
    list_editable = ['customers']
    search_fields = ['name']
    autocomplete_fields = ['customers', 'performer', 'jobcategories']
    ordering = ('date_in',)
    date_hierarchy = 'date_in'
    inlines = [ExtraPerfomerInline]

    # def changelist_view(self, request, extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['all_sum_all_performers'] = Performers.all_sum_all_performers()
    #     extra_context['all_sum_already_all_performers'] = Performers.all_sum_already_all_performers()
    #     extra_context['all_debt_all_performers'] = Performers.all_debt_all_performers()
    #     # extra_context['deals_in_no_prise_count'] = Affairs.deals_in_no_prise_count()
    #     # extra_context['deals_in_no_prise_sum'] = Affairs.deals_in_no_prise_sum()
    #     return super().changelist_view(request, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['deals_in_count'] = Affairs.deals_in_count()
        extra_context['deals_in_prise_sum'] = Affairs.deals_in_prise_sum()
        extra_context['deals_in_no_prise_count'] = Affairs.deals_in_no_prise_count()
        extra_context['deals_in_no_prise_sum'] = Affairs.deals_in_no_prise_sum()
        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None, ):
        extra_context = extra_context or {}
        extra_context['osm_data'] = Affairs.objects.get(pk=object_id)
        return super(UserAccessAdmin, self).change_view(request, object_id,
                                                        form_url, extra_context=extra_context)


@admin.register(ExtraAffairs)
class ExtraAffairsAdmin(admin.ModelAdmin):
    list_display = ('name', 'affairs', 'sum', 'comment', 'file')

