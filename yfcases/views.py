# encoding: utf-8
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.core.paginator import Paginator 
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xhtml2pdf.default import DEFAULT_FONT
from django_pdfkit import PDFView
from users.models import *
from .models import *
from .forms import *
from .resources import *
from django.db import transaction


def export_yfcase(reauest):
  yfcase_resource = YfcaseResource()
  yfcase = yfcase_resource.export()
  response = HttpResponse(yfcase.xlsx,content_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="member.xlsx"'
  return response



# @method_decorator(login_required,name='dispatch')   
# class YfcaseListView(ListView):
#   model=Yfcase
#   template_name="home.html"


# 所有(在途+結案)
@login_required
def yfcase_list_all_include_close(request):
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  queryset_list = Yfcase.objects.all()
  query = request.GET.get('q')
  if query:
    queryset_list = queryset_list.filter(
      Q(yfcaseCaseNumber__icontains=query)|
      Q(yfcaseCityWithTownship__icontains=query)|
      Q(yfcaseStreet__icontains=query)|
      Q(yfcaseNumber__icontains=query)|
      Q(finaldecisions__finalDecision__icontains=query)|
      Q(finaldecisions__regionalHead__icontains=query)|
      Q(user__userFullName__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10) 

  page = request.GET.get('page')
  queryset = paginator.get_page(page)

  context={
    "object_list" : queryset,
    "title": "List",
    }
  return render(request, "home.html", context)

# 所有(在途)
@login_required
def yfcase_list_all(request):
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  queryset_list = Yfcase.objects.all().filter(yfcaseCaseStatus="在途")
  query = request.GET.get('q')
  if query:
    queryset_list = queryset_list.filter(
      Q(yfcaseCaseNumber__icontains=query)|
      Q(yfcaseCityWithTownship__icontains=query)|
      Q(yfcaseStreet__icontains=query)|
      Q(yfcaseNumber__icontains=query)|
      Q(finaldecisions__finalDecision__icontains=query)|
      Q(finaldecisions__regionalHead__icontains=query)|
      Q(user__userFullName__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10) 

  page = request.GET.get('page')
  queryset = paginator.get_page(page)

  context={
    "object_list" : queryset,
    "title": "List",
    }
  return render(request, "home.html", context)
  
# 個人(List)
@login_required
def yfcase_list(request):
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  # 登入者姓名
  request_userid=request.user.id
  queryset_list = Yfcase.objects.filter(user_id=request_userid).filter(yfcaseCaseStatus="在途")
  query = request.GET.get('q')
  if query:
    queryset_list = queryset_list.filter(
      Q(yfcaseCaseNumber__icontains=query)|
      Q(yfcaseCityWithTownship__icontains=query)|
      Q(yfcaseStreet__icontains=query)|
      Q(yfcaseNumber__icontains=query)|
      Q(finaldecisions__finalDecision__icontains=query)|
      Q(finaldecisions__regionalHead__icontains=query)|
      Q(user__userFullName__icontains=query)
    ).distinct()
  paginator = Paginator(queryset_list, 10) 

  page = request.GET.get('page')
  queryset = paginator.get_page(page)

  context={
    "object_list" : queryset,
    "title": "List"
    }
  return render(request, "home.html", context)


@method_decorator(login_required,name='dispatch')
class YfcaseDetailView(DetailView):
  model=Yfcase
  form_class = YfcaseForm
  template_name="yfcase/yfcase_detail.html"
  success_url = reverse_lazy('yfcase:yfcase_detail')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['title'] = '建立項目'
    return context

class YfcaseCreateView(CreateView):
  model=Yfcase
  form_class = YfcaseForm
  template_name="yfcase/yfcase_create.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(YfcaseCreateView,self).get_context_data(**kwargs)
    context["author_id"]=self.request.user.id
    context['value'] = '建立'
    context['title'] = '新增基本資料'
    return context

class YfcaseUpdateView(UpdateView):
  model=Yfcase
  form_class = YfcaseForm
  template_name='yfcase/yfcase_update.html'
    
  def get_success_url(self, **kwargs):
    return reverse_lazy("yfcase:yfcase_detail", args=(self.object.id,))

  def form_valid(self, form):
    if form.cleaned_data['yfcaseCaseNumber'] is None:
        form.add_error('yfcaseCaseNumber', 'Incident with this email already exist')
        return self.form_invalid(form)
    return super(YfcaseUpdateView, self).form_valid(form)
    
  def get_context_data(self, **kwargs):
    context = super(YfcaseUpdateView,self).get_context_data(**kwargs)

    pk = Yfcase.objects.get(pk=self.kwargs.get('pk')).lands.all

    context["author_id"]=self.request.user.id
    context['value'] = '更新'
    context['title'] = '更新基本資料'
    context.update({
        'yland': pk,
    })
    return context

class YfcaseDeleteView(DeleteView):
  model=Yfcase
  template_name="yfcase/yfcase_delete.html"
  success_url=reverse_lazy('yfcase:home')

# ==========================  Land  =========================
def land_create(request,yfcase_id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = LandForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增地號",
  }
  return render(request, "land/land_form.html",context)

def land_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(Land,id=id)
  form=LandForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "更新地號",
  }
  return render(request, "land/land_form.html",context)

def land_delete(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(Land, id=id)
  if request.method == "POST":
    instance.delete()
    # messages.success(request, 'Data Deleted.')
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context = {
    "instance": instance,
    "instance_yfcase": instance_yfcase,
    "title": "刪除建號"
  }
  return render(request, "land/land_delete.html", context)

# ==========================  Build  =========================
def build_create(request,yfcase_id=None):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = BuildForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增建號",
  }
  return render(request, "build/build_form.html",context)

def build_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(Build,id=id)
  form=BuildForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "更新建號",
  }
  return render(request, "build/build_form.html",context)

def build_delete(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(Build, id=id)
  if request.method == "POST":
    instance.delete()
    # messages.success(request, 'Data Deleted.')
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context = {
    "instance": instance,
    "instance_yfcase": instance_yfcase,
    "title": "刪除建號"
  }
  return render(request, "build/build_delete.html", context)

# ==========================  Auction  =========================
def auction_create(request,yfcase_id=None):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = AuctionForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增拍賣資訊",
  }
  return render(request, "auction/auction_form.html",context)

def auction_update(request,yfcase_id=None,id=id):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(Auction,id=id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = AuctionForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "instance" : instance,
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "更新拍賣資訊",
  }
  return render(request, "auction/auction_form.html",context)

# ==========================  Survey  =========================
def survey_create(request,yfcase_id=None):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = SurveyForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增拍賣資訊",
  }
  return render(request, "survey/survey_form.html",context)

def survey_update(request,yfcase_id=None,id=id):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(Survey,id=id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = SurveyForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "instance" : instance,
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "更新拍賣資訊",
  }
  return render(request, "survey/survey_form.html",context)
  
# ==========================  ObjectBuild  =========================
def objectbuild_create(request,yfcase_id=None):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = ObjectBuildForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增參考物件",
  }
  return render(request, "objectbuild/objectbuild_form.html",context)

def objectbuild_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild,id=id)
  form=ObjectBuildForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "更新參考物件",
  }
  return render(request, "objectbuild/objectbuild_form.html",context)

def objectbuild_delete(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild, id=id)
  if request.method == "POST":
    instance.delete()
    # messages.success(request, 'Data Deleted.')
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context = {
    "instance": instance,
    "instance_yfcase": instance_yfcase,
    "title": "刪除參考物件"
  }
  return render(request, "objectbuild/objectbuild_delete.html", context)

# ==========================  ScoreA  =========================
def score_a_adj(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild,id=id)
  form=ScoreAForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "調整勘查員A評分",
  }
  return render(request, "score/score_a_form.html",context)

def score_a_clean(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild,id=id)
  form=ScoreAForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "清除勘查員A評分",
  }
  return render(request, "score/score_a_delete.html",context)

# ==========================  ScoreB  =========================
def score_b_adj(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild,id=id)
  form=ScoreBForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "調整勘查員B評分",
  }
  return render(request, "score/score_b_form.html",context)

def score_b_clean(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild,id=id)
  form=ScoreBForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "清除勘查員B評分",
  }
  return render(request, "score/score_b_delete.html",context)

# ==========================  ScoreC  =========================
def score_c_adj(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild,id=id)
  form=ScoreCForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "調整勘查員C評分",
  }
  return render(request, "score/score_c_form.html",context)

def score_c_clean(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(ObjectBuild,id=id)
  form=ScoreCForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "清除勘查員C評分",
  }
  return render(request, "score/score_c_delete.html",context)

# ==========================  FinalDecision(regionalHead)  =========================
def finaldecision_create(request,yfcase_id=None):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = FinalDecisionForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增最終判定",
  }
  return render(request, "finaldecision/finaldecision_form.html",context)


def finaldecision_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(FinalDecision,id=id)
  form=FinalDecisionForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "變更最終判定",
  }
  return render(request, "finaldecision/finaldecision_form.html",context)

def finaldecision_delete(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(FinalDecision, id=id)
  if request.method == "POST":
    instance.delete()
    # messages.success(request, 'Data Deleted.')
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context = {
    "instance": instance,
    "instance_yfcase": instance_yfcase,
    "title": "刪除最終判定"
  }
  return render(request, "finaldecision/finaldecision_delete.html", context)

# ==========================  SubSigntrueA  =========================
def subsignture_a_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(FinalDecision,id=id)
  form=SubSigntrueAForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "新增/變更副署人員1的簽核",
  }
  return render(request, "finaldecision/subsignture_a_form.html",context)

def subsignture_a_delete(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(FinalDecision,id=id)
  form=SubSigntrueAForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "刪除副署人員1的簽核",
  }
  return render(request, "finaldecision/subsignture_a_delete.html",context)

# ==========================  SubSigntrueB  =========================
def subsignture_b_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(FinalDecision,id=id)
  form=SubSigntrueBForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "新增/變更副署人員2的簽核",
  }
  return render(request, "finaldecision/subsignture_b_form.html",context)

def subsignture_b_delete(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(FinalDecision,id=id)
  form=SubSigntrueBForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Update")
    # 這裡的instance_yfcase.id指的是父類的id(Yfcase)
    return redirect("yfcase:yfcase_detail", instance_yfcase.id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "刪除副署人員2的簽核",
  }
  return render(request, "finaldecision/subsignture_b_delete.html",context)

def load_townships(request):
  city_id = request.GET.get('city')
  townships = Township.objects.filter(city_id=city_id).order_by('name')
  return render(request, 'yfcase/township_dropdown_list_options.html', {'townships': townships})


# ==========================  Result  =========================
def result_create(request,yfcase_id=None):
  # 要配合url回傳的yfcase_id，來取得超類的資料
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = ResultForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    # messages.success(request,"successfully Created")
    # 把父類的yfcase_id(不可寫成instance.id，回傳到子類的id)回傳給yfcase_detail
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增執行結果",
  }
  return render(request, "result/result_form.html",context)

def result_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(Result,id=id)
  form=ResultForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:yfcase_detail", yfcase_id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "更新執行結果",
  }
  return render(request, "result/result_form.html",context)

# ==========================  PDF(評量表)  =========================
def font_path():
  pdfmetrics.registerFont(TTFont('yh', '{}/fonts/TaipeiSansTCBeta-Regular.ttf'.format(settings.STATICFILES_DIRS[0])))
  DEFAULT_FONT['helvetica'] = 'yh'


# PDFkit-評量表
class yfratingscalePDFView(PDFView):
  template_name = './pdf/yfratingscale_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    context.update({
        'yfcase': yfcase,
    })
    return context

# 契稅申請單-Modal(Form)
class DeedtaxUpdateView(UpdateView):
  model=Yfcase
  form_class = DeedtaxForm
  template_name="yfcase/afterwinner/Deedtax_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(DeedtaxUpdateView,self).get_context_data(**kwargs)
    if Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseDeedtaxClient:
      deedtax_user_id=Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseDeedtaxClient
      context['deedtax_clent_id'] =CustomUser.objects.get(userFullName=deedtax_user_id).id
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '契稅申請單相關資料'
    return context

# PDFkit-契稅申請書
class deedtaxPDFView(PDFView):
  template_name = './pdf/deedtax_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    users = CustomUser.objects.all()
    context.update({
        'yfcase': yfcase,
        'users': users,
    })
    return context

# Form(Edit)-不動產登記清冊  
class RealestateregistrationUpdateView(UpdateView):
  model=Yfcase
  form_class = RealestateregistrationForm
  template_name="yfcase/afterwinner/Realestateregistration_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(RealestateregistrationUpdateView,self).get_context_data(**kwargs)
    if Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseRealEstateRegistrationRegisteredAgent:
      realestateregistration_user_id=Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseRealEstateRegistrationRegisteredAgent
      context['realestateregistration_user_id'] =CustomUser.objects.get(userFullName=realestateregistration_user_id).id
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '不動產登記清冊相關資料'
    return context

# PDFkit-不動產土地登記申請書
class realestateregistrationPDFView(PDFView):
  template_name = './pdf/realestateregistration_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    yfcaseCreditor_phone =CustomUser.objects.get(userFullName=yfcase.yfcaseCompany).userMobilePhone
    users = CustomUser.objects.all()

    # landRecord1
    try:
      landRecord1 = yfcase.lands.order_by('id').filter(id__gt=0)[0]
    except:
      landRecord1 = None

    # landRecord2
    try:
      landRecord2 = yfcase.lands.order_by('id').filter(id__gt=0)[1]
    except:
      landRecord2 = None

    # landRecord3
    try:
      landRecord3 = yfcase.lands.order_by('id').filter(id__gt=0)[2]
    except:
      landRecord3 = None

    # landRecord4
    try:
      landRecord4 = yfcase.lands.order_by('id').filter(id__gt=0)[3]
    except:
      landRecord4 = None


    # buildRecord1
    try:
      buildRecord1 = yfcase.builds.order_by('id').filter(id__gt=0)[0]
    except:
      buildRecord1 = None

    # buildRecord2
    try:
      buildRecord2 = yfcase.builds.order_by('id').filter(id__gt=0)[1]
    except:
      buildRecord2 = None

    # buildRecord3
    try:
      buildRecord3 = yfcase.builds.order_by('id').filter(id__gt=0)[2]
    except:
      buildRecord3 = None

    # buildRecord4
    try:
      buildRecord4 = yfcase.builds.order_by('id').filter(id__gt=0)[3]
    except:
      buildRecord4 = None

    # 合計
    buildRecordTotal = yfcase.yfcaseDeedtaxBuildingTransferArea1+yfcase.yfcaseDeedtaxBuildingTransferArea2+yfcase.yfcaseDeedtaxBuildingTransferArea3+yfcase.yfcaseDeedtaxBuildingTransferArea4+yfcase.yfcaseDeedtaxBuildingTransferArea4

    # 縣市後面一碼判定為"市"或是"縣"
    cityLastJudgment = yfcase.yfcaseCity.name[2]

    # 跨區申請-鄉鎮對應到縣市
    try:
      yfcaseAcceptingAuthorityTownship_city = Township.objects.get(name=yfcase.yfcaseAcceptingAuthorityTownship).city.name
    except:
      yfcaseAcceptingAuthorityTownship_city = None

    # 跨區申請-鄉鎮對應到地政事務所
    try:
      yfcaseAcceptingAuthorityTownship_land_office = Township.objects.get(name=yfcase.yfcaseAcceptingAuthorityTownship).land_office
    except:
      yfcaseAcceptingAuthorityTownship_land_office = None

    # 跨區申請-鄉鎮對應到縣市(判斷最後一個字是"縣"還是"市")
    try:
      yfcaseAcceptingAuthorityTownship_city_lastWord = yfcaseAcceptingAuthorityTownship_city[2]
    except:
      yfcaseAcceptingAuthorityTownship_city_lastWord = None

    context.update({
      'yfcase': yfcase,
      'users': users,
      'yfcaseCreditor_phone': yfcaseCreditor_phone,
      'landRecord1': landRecord1,
      'landRecord2': landRecord2,
      'landRecord3': landRecord3,
      'landRecord4': landRecord4,
      'buildRecord1': buildRecord1,
      'buildRecord2': buildRecord2,
      'buildRecord3': buildRecord3,
      'buildRecord4': buildRecord4,
      'buildRecordTotal': buildRecordTotal,
      'cityLastJudgment': cityLastJudgment,
      'yfcaseAcceptingAuthorityTownship_city':yfcaseAcceptingAuthorityTownship_city,
      'yfcaseAcceptingAuthorityTownship_land_office':yfcaseAcceptingAuthorityTownship_land_office,
      'yfcaseAcceptingAuthorityTownship_city_lastWord':yfcaseAcceptingAuthorityTownship_city_lastWord,
    })
    return context

# Form(Edit)-訴訟狀
class ComplaintUpdateView(UpdateView):
  model=Yfcase
  form_class = ComplaintForm
  template_name="yfcase/afterwinner/Complaint_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    data = super(ComplaintUpdateView,self).get_context_data(**kwargs)
    if Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseComplaintLitigationAgent:
      complaint_user_id=Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseComplaintLitigationAgent
      data['complaint_clent_id'] =CustomUser.objects.get(userFullName=complaint_user_id).id
    data['instace'] =Yfcase.objects.get(pk=self.kwargs.get('pk'))
    data["author_id"]=self.request.user.id
    data['value'] = '編輯'
    data['title'] = '訴訟狀相關資料'
    return data 
  
# Form(Edit)-共有人資訊
def coownerinfo_create(request,yfcase_id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = CoOwnerInfoForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:coowner_edit", yfcase_id)
  context = {
    "form" : form, 
    "instance_yfcase": instance_yfcase,
    "title": "新增建號",
  }
  return render(request, "coowner/coowner_form.html",context)

def coownerinfo_update(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(CoOwnerInfo,id=id)
  form=CoOwnerInfoForm(request.POST or None,instance=instance)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:coowner_edit", yfcase_id)
  context={
    "instance" : instance,
    "instance_yfcase" : instance_yfcase,
    "form" : form,
    "title": "新增/變更共有人資訊",
  }
  return render(request, "coowner/coowner_form.html",context)

def coownerinfo_delete(request,yfcase_id=None,id=None):
  instance_yfcase = get_object_or_404(Yfcase,id=yfcase_id)
  instance = get_object_or_404(CoOwnerInfo, id=id)
  if request.method == "POST":
    instance.delete()
    return redirect("yfcase:coowner_edit", instance_yfcase.id)
  context = {
    "instance": instance,
    "instance_yfcase": instance_yfcase,
    "title": "刪除共有人"
  }
  return render(request, "coowner/coowner_delete.html", context)

# Form(Edit)-共有人之繼承人資訊
def coownerheir_create(request,coowner_id=None):
  instance_coowner = get_object_or_404(CoOwnerInfo,id=coowner_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = CoOwnerHeirForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:coowner_edit", instance_coowner.yfcase_id)
  context = {
    "form" : form, 
    "instance_coowner": instance_coowner,
    "title": "新增共有人之繼承人",
  }
  return render(request, "coownerheir/coowner_heir_form.html",context)

def coownerheir_update(request,coowner_id=None,id=None):
  instance_coowner = get_object_or_404(CoOwnerInfo,id=coowner_id)
  instance_coowner_heir = get_object_or_404(CoOwnerHeir,id=id)
  form=CoOwnerHeirForm(request.POST or None,instance=instance_coowner_heir)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:coowner_edit", instance_coowner.yfcase_id)
  context={
    "instance_coowner_heir" : instance_coowner_heir,
    "instance_coowner" : instance_coowner,
    "form" : form,
    "title": "變更共有人之繼承人",
  }
  return render(request, "coownerheir/coowner_heir_form.html",context)

def coownerheir_delete(request,coowner_id=None,id=None):
  instance_coowner = get_object_or_404(CoOwnerInfo,id=coowner_id)
  instance_coowner_heir = get_object_or_404(CoOwnerHeir,id=id)
  if request.method == "POST":
    instance_coowner_heir.delete()
    return redirect("yfcase:coowner_edit", instance_coowner.yfcase_id)
  context = {
    "instance_coowner_heir" : instance_coowner_heir,
    "instance_coowner" : instance_coowner,
    "title": "刪除共有人之繼承人"
  }
  return render(request, "coownerheir/coowner_heir_delete.html", context)


# Form(Edit)-承受訴訟人之繼承人資訊
def coownerlitigation_create(request,coowner_heir_id=None):
  instance_coowner_heir = get_object_or_404(CoOwnerHeir,id=coowner_heir_id)
  instance_coowner =CoOwnerInfo.objects.get(id=instance_coowner_heir.coowner_id)
  if not request.user.is_staff or not request.user.is_superuser:
    raise Http404
  form = CoOwnerLitigationForm(request.POST or None)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:coowner_edit", instance_coowner.yfcase_id)
  context = {
    "form" : form, 
    "instance_coowner_heir": instance_coowner_heir,
    "instance_coowner": instance_coowner,
    "title": "新增承受訴訟人之繼承人",
  }
  return render(request, "coownerlitigation/coowner_litigation_form.html",context)
  

def coownerlitigation_update(request,coowner_heir_id=None,id=None):
  instance_coowner_heir = get_object_or_404(CoOwnerHeir,id=coowner_heir_id)
  instance_coowner_litigation = get_object_or_404(CoOwnerLitigation,id=id)
  instance_coowner =CoOwnerInfo.objects.get(id=instance_coowner_heir.coowner_id)
  form=CoOwnerLitigationForm(request.POST or None,instance=instance_coowner_litigation)
  if form.is_valid():
    instance=form.save(commit=False)
    instance.save()
    return redirect("yfcase:coowner_edit", instance_coowner.yfcase_id)
  context={
    "instance_coowner_heir" : instance_coowner_heir,
    "instance_coowner_litigation" : instance_coowner_litigation,
    "instance_coowner" : instance_coowner,
    "form" : form,
    "title": "變更承受訴訟人之繼承人",
  }
  return render(request, "coownerlitigation/coowner_litigation_form.html",context)

def coownerlitigation_delete(request,coowner_heir_id=None,id=None):
  instance_coowner_heir = get_object_or_404(CoOwnerHeir,id=coowner_heir_id)
  instance_coowner_litigation = get_object_or_404(CoOwnerLitigation,id=id)
  instance_coowner =CoOwnerInfo.objects.get(id=instance_coowner_heir.coowner_id)
  if request.method == "POST":
    instance_coowner_litigation.delete()
    return redirect("yfcase:coowner_edit", instance_coowner.yfcase_id)
  context = {
    "instance_coowner_heir" : instance_coowner_heir,
    "instance_coowner_litigation" : instance_coowner_litigation,
    "instance_coowner" : instance_coowner,
    "title": "刪除承受訴訟人之繼承人"
  }
  return render(request, "coownerlitigation/coowner_litigation_delete.html", context)


# PDFkit-訴訟狀
class complaintPDFView(PDFView):
  template_name = './pdf/complaint_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    users = CustomUser.objects.all()
    context.update({
        'yfcase': yfcase,
        'users': users,
    })
    return context

# Form(Edit)-存證信函
class LetterUpdateView(UpdateView):
  model=Yfcase
  form_class = LetterForm
  template_name="yfcase/afterwinner/Letter_edit.html"
  success_url = reverse_lazy('yfcase:home')

  def get_context_data(self, **kwargs):
    context = super(LetterUpdateView,self).get_context_data(**kwargs)
    if Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseLetterAgent:
      letter_user_id=Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseLetterAgent
      context['letter_clent_id'] =CustomUser.objects.get(userFullName=letter_user_id).id
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '存證信函相關資料'
    return context

# Form(Edit)-共有人
class CoownertUpdateView(UpdateView):
  model=Yfcase
  form_class = CoOwnerForm
  template_name="yfcase/afterwinner/Coowner_edit.html"
  success_url = reverse_lazy('yfcase:home')
  
  def get_context_data(self, **kwargs):
    context = super(CoownertUpdateView,self).get_context_data(**kwargs)
    yfcase=Yfcase.objects.get(pk=self.kwargs.get('pk'))
    if Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseCownerAgent:
      cowner_user_id=Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseCownerAgent
      context['cowner_clent_id'] =CustomUser.objects.get(userFullName=cowner_user_id).id
    context["author_id"]=self.request.user.id
    context['value'] = '編輯'
    context['title'] = '共有人資訊'
    return context

# PDFkit-存證信函
class letterPDFView(PDFView):
  template_name = './pdf/letter_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    if Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseLetterAgent:
      letter_agent_name=Yfcase.objects.get(pk=self.kwargs.get('pk')).yfcaseLetterAgent
      context['letter_agent_phone'] =CustomUser.objects.get(userFullName=letter_agent_name).userMobilePhone
    users = CustomUser.objects.all()
    context.update({
        'yfcase': yfcase,
        'users': users,
    })
    return context

# PDFkit-共有人
class coownerPDFView(PDFView):
  template_name = './pdf/coowner_pdf.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    pk = kwargs.get('pk')
    yfcase = Yfcase.objects.get(pk=pk)
    coowners = yfcase.coownerinfos.filter(yfcase_id=yfcase.id)
    if yfcase.yfcaseCownerAgent:
      yfcasecowneragent = CustomUser.objects.get(userFullName=yfcase.yfcaseCownerAgent)
    else:
      yfcasecowneragent = ''
  
    
    # coowners = yfcases.coownerinfos.all()
    # coowner_life = list(yfcases.coownerinfos.filter(coOwnerLifeOrDie="殁").values_list('id', flat=True)) 
    # context['coownerheir'] = CoOwnerHeir.objects.filter(id=coowner_life)

    users = CustomUser.objects.all()
    context.update({
        'yfcase': yfcase,
        'coowners': coowners,
        'yfcasecowneragent': yfcasecowneragent,
        'users': users,
    })
    return context