from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .models import *
from users.models import *
from django.forms.models import inlineformset_factory
from .custom_layout_object import *

COMPANY_LIST = [
  ("",""),
  ("揚富開發有限公司","揚富開發有限公司"),
  ("鉅鈦開發有限公司","鉅鈦開發有限公司"),
]

BUILD_TYPE_USE= [
  ("",""),
  ("公設","公設"),
  ("公寓-5樓含以下無電梯","公寓-5樓含以下無電梯"),
  ("透天厝","透天厝"),
  ("店面-店舖","店面-店舖"),
  ("辦公商業大樓","辦公商業大樓"),
  ("住宅大樓-11層含以上有電梯","住宅大樓-11層含以上有電梯"),
  ("華廈-10層含以下有電梯","華廈-10層含以下有電梯"),
  ("套房","套房"),
  ("農舍","農舍"),
  ("增建-持分後坪數打對折","增建-持分後坪數打對折")
]

AREA_LIST = [
  ("",""),
  ("第一種住宅區","第一種住宅區"),
  ("第二種住宅區","第二種住宅區"),
  ("第三種住宅區","第三種住宅區"),
  ("第四種住宅區","第四種住宅區"),
  ("第五種住宅區","第五種住宅區"),
  ("第一種商業區","第一種商業區"),
  ("第二種商業區","第二種商業區"),
  ("第三種商業區","第三種商業區"),
  ("第四種商業區","第四種商業區"),
  ("第二種工業區","第二種工業區"),
  ("第三種工業區","第三種工業區"),
  ("行政區","行政區"),
  ("文教區","文教區"),
  ("倉庫區","倉庫區"),
  ("風景區","風景區"),
  ("農業區","農業區"),
  ("保護區","保護區"),
  ("行水區","行水區"),
  ("保存區","保存區"),
  ("特定專用區","特定專用區")
]

STATUS_LIST= (
  ("",""),
  ("實價登錄","實價登錄"),
  ("好時價","好時價"),
)

JUDGMENT_LIST=[
  ("未判定","未判定"),
  ("1拍進場","1拍進場"),
  ("2拍進場","2拍進場"),
  ("3拍進場","3拍進場"),
  ("4拍進場","4拍進場"),
  ("放棄","放棄"),
  ("4拍流標","4拍流標"),
]

BIDAUCTION_LIST=[
  ("",""),
  ("1拍","1拍"),
  ("2拍","2拍"),
  ("3拍","3拍"),
  ("4拍","4拍")
]

ACTIONRESULT_CHOICES = [
  ("",""),
  ("撤回","撤回"),
  ("第三人搶標","第三人搶標"),
  ("等待優購","等待優購"),
  ("遭優購","遭優購"),
  ("無人優購","無人優購")
]

CASESTATUS_CHOICES = [
  ("在途","在途"),
  ("結案","結案"),
]

DEED_TAX_RECLAIM_METHOD_LIST =[
  ("",""),
  ("親領","親領"),
  ("郵寄","郵寄"), 
]

DEED_TAX_CLOSING_NEWSLETTER_LIST =[
  ("",""),
  ("需要","需要"),
  ("不需要","不需要"), 
]

DEED_TAX_REPORT_ATTACHED_LIST =[
  ("",""),
  ("申請","申請"),
  ("不申請","不申請"), 
]

REAL_ESTATE_REGISTRATION_REASON_FOR_REGISTRATION = [
  ("",""),
  ("買賣","買賣"),
  ("拍賣","拍賣"), 
  ("調解","調解"), 
]

ACCEPTING_AUTHORITY_TOWNSHIP_LIST = [
  ("",""),
  ("中正區","中正區"),
  ("大同區","大同區"),
  ("中山區","中山區"),
  ("松山區","松山區"),
  ("大安區","大安區"),
  ("萬華區","萬華區"),
  ("信義區","信義區"),
  ("士林區","士林區"),
  ("北投區","北投區"),
  ("內湖區","內湖區"),
  ("南港區","南港區"),
  ("文山區","文山區"),
  ("仁愛區","仁愛區"),
  ("信義區","信義區"),
  ("中正區","中正區"),
  ("中山區","中山區"),
  ("安樂區","安樂區"),
  ("暖暖區","暖暖區"),
  ("七堵區","七堵區"),
  ("萬里區","萬里區"),
  ("金山區","金山區"),
  ("板橋區","板橋區"),
  ("汐止區","汐止區"),
  ("深坑區","深坑區"),
  ("石碇區","石碇區"),
  ("瑞芳區","瑞芳區"),
  ("平溪區","平溪區"),
  ("雙溪區","雙溪區"),
  ("貢寮區","貢寮區"),
  ("新店區","新店區"),
  ("坪林區","坪林區"),
  ("烏來區","烏來區"),
  ("永和區","永和區"),
  ("中和區","中和區"),
  ("土城區","土城區"),
  ("三峽區","三峽區"),
  ("樹林區","樹林區"),
  ("鶯歌區","鶯歌區"),
  ("三重區","三重區"),
  ("新莊區","新莊區"),
  ("泰山區","泰山區"),
  ("林口區","林口區"),
  ("蘆洲區","蘆洲區"),
  ("五股區","五股區"),
  ("八里區","八里區"),
  ("淡水區","淡水區"),
  ("三芝區","三芝區"),
  ("石門區","石門區"),
  ("南竿鄉","南竿鄉"),
  ("北竿鄉","北竿鄉"),
  ("莒光鄉","莒光鄉"),
  ("東引鄉","東引鄉"),
  ("宜蘭市","宜蘭市"),
  ("頭城鎮","頭城鎮"),
  ("礁溪鄉","礁溪鄉"),
  ("壯圍鄉","壯圍鄉"),
  ("員山鄉","員山鄉"),
  ("羅東鎮","羅東鎮"),
  ("三星鄉","三星鄉"),
  ("大同鄉","大同鄉"),
  ("五結鄉","五結鄉"),
  ("冬山鄉","冬山鄉"),
  ("蘇澳鎮","蘇澳鎮"),
  ("南澳鄉","南澳鄉"),
  ("東區","東區"),
  ("北區","北區"),
  ("香山區","香山區"),
  ("竹北市","竹北市"),
  ("湖口鄉","湖口鄉"),
  ("新豐鄉","新豐鄉"),
  ("新埔鎮","新埔鎮"),
  ("關西鎮","關西鎮"),
  ("芎林鄉","芎林鄉"),
  ("寶山鄉","寶山鄉"),
  ("竹東鎮","竹東鎮"),
  ("五峰鄉","五峰鄉"),
  ("橫山鄉","橫山鄉"),
  ("尖石鄉","尖石鄉"),
  ("北埔鄉","北埔鄉"),
  ("峨眉鄉","峨眉鄉"),
  ("中壢區","中壢區"),
  ("平鎮區","平鎮區"),
  ("龍潭區","龍潭區"),
  ("楊梅區","楊梅區"),
  ("新屋區","新屋區"),
  ("觀音區","觀音區"),
  ("桃園區","桃園區"),
  ("龜山區","龜山區"),
  ("八德區","八德區"),
  ("大溪區","大溪區"),
  ("復興區","復興區"),
  ("大園區","大園區"),
  ("蘆竹區","蘆竹區"),
  ("竹南鎮","竹南鎮"),
  ("頭份市","頭份市"),
  ("三灣鄉","三灣鄉"),
  ("南庄鄉","南庄鄉"),
  ("獅潭鄉","獅潭鄉"),
  ("後龍鎮","後龍鎮"),
  ("通霄鎮","通霄鎮"),
  ("苑裡鎮","苑裡鎮"),
  ("苗栗市","苗栗市"),
  ("造橋鄉","造橋鄉"),
  ("頭屋鄉","頭屋鄉"),
  ("公館鄉","公館鄉"),
  ("大湖鄉","大湖鄉"),
  ("泰安鄉","泰安鄉"),
  ("銅鑼鄉","銅鑼鄉"),
  ("三義鄉","三義鄉"),
  ("西湖鄉","西湖鄉"),
  ("卓蘭鎮","卓蘭鎮"),
  ("中區","中區"),
  ("東區","東區"),
  ("南區","南區"),
  ("西區","西區"),
  ("北區","北區"),
  ("北屯區","北屯區"),
  ("西屯區","西屯區"),
  ("南屯區","南屯區"),
  ("太平區","太平區"),
  ("大里區","大里區"),
  ("霧峰區","霧峰區"),
  ("烏日區","烏日區"),
  ("豐原區","豐原區"),
  ("后里區","后里區"),
  ("石岡區","石岡區"),
  ("東勢區","東勢區"),
  ("和平區","和平區"),
  ("新社區","新社區"),
  ("潭子區","潭子區"),
  ("大雅區","大雅區"),
  ("神岡區","神岡區"),
  ("大肚區","大肚區"),
  ("沙鹿區","沙鹿區"),
  ("龍井區","龍井區"),
  ("梧棲區","梧棲區"),
  ("清水區","清水區"),
  ("大甲區","大甲區"),
  ("外埔區","外埔區"),
  ("大安區","大安區"),
  ("彰化市","彰化市"),
  ("芬園鄉","芬園鄉"),
  ("花壇鄉","花壇鄉"),
  ("秀水鄉","秀水鄉"),
  ("鹿港鎮","鹿港鎮"),
  ("福興鄉","福興鄉"),
  ("線西鄉","線西鄉"),
  ("和美鎮","和美鎮"),
  ("伸港鄉","伸港鄉"),
  ("員林市","員林市"),
  ("社頭鄉","社頭鄉"),
  ("永靖鄉","永靖鄉"),
  ("埔心鄉","埔心鄉"),
  ("溪湖鎮","溪湖鎮"),
  ("大村鄉","大村鄉"),
  ("埔鹽鄉","埔鹽鄉"),
  ("田中鎮","田中鎮"),
  ("北斗鎮","北斗鎮"),
  ("田尾鄉","田尾鄉"),
  ("埤頭鄉","埤頭鄉"),
  ("溪州鄉","溪州鄉"),
  ("竹塘鄉","竹塘鄉"),
  ("二林鎮","二林鎮"),
  ("大城鄉","大城鄉"),
  ("芳苑鄉","芳苑鄉"),
  ("二水鄉","二水鄉"),
  ("南投市","南投市"),
  ("中寮鄉","中寮鄉"),
  ("草屯鎮","草屯鎮"),
  ("國姓鄉","國姓鄉"),
  ("埔里鎮","埔里鎮"),
  ("仁愛鄉","仁愛鄉"),
  ("名間鄉","名間鄉"),
  ("集集鎮","集集鎮"),
  ("水里鄉","水里鄉"),
  ("魚池鄉","魚池鄉"),
  ("信義鄉","信義鄉"),
  ("竹山鎮","竹山鎮"),
  ("鹿谷鄉","鹿谷鄉"),
  ("東區","東區"),
  ("西區","西區"),
  ("番路鄉","番路鄉"),
  ("梅山鄉","梅山鄉"),
  ("竹崎鄉","竹崎鄉"),
  ("阿里山鄉","阿里山鄉"),
  ("中埔鄉","中埔鄉"),
  ("大埔鄉","大埔鄉"),
  ("水上鄉","水上鄉"),
  ("鹿草鄉","鹿草鄉"),
  ("太保市","太保市"),
  ("朴子市","朴子市"),
  ("東石鄉","東石鄉"),
  ("六腳鄉","六腳鄉"),
  ("新港鄉","新港鄉"),
  ("民雄鄉","民雄鄉"),
  ("大林鎮","大林鎮"),
  ("溪口鄉","溪口鄉"),
  ("義竹鄉","義竹鄉"),
  ("布袋鎮","布袋鎮"),
  ("斗南鎮","斗南鎮"),
  ("大埤鄉","大埤鄉"),
  ("虎尾鎮","虎尾鎮"),
  ("土庫鎮","土庫鎮"),
  ("褒忠鄉","褒忠鄉"),
  ("東勢鄉","東勢鄉"),
  ("臺西鄉","臺西鄉"),
  ("崙背鄉","崙背鄉"),
  ("麥寮鄉","麥寮鄉"),
  ("斗六市","斗六市"),
  ("林內鄉","林內鄉"),
  ("古坑鄉","古坑鄉"),
  ("莿桐鄉","莿桐鄉"),
  ("西螺鎮","西螺鎮"),
  ("二崙鄉","二崙鄉"),
  ("北港鎮","北港鎮"),
  ("水林鄉","水林鄉"),
  ("口湖鄉","口湖鄉"),
  ("四湖鄉","四湖鄉"),
  ("元長鄉","元長鄉"),
  ("中西區","中西區"),
  ("東區","東區"),
  ("南區","南區"),
  ("北區","北區"),
  ("安平區","安平區"),
  ("安南區","安南區"),
  ("永康區","永康區"),
  ("歸仁區","歸仁區"),
  ("新化區","新化區"),
  ("左鎮區","左鎮區"),
  ("玉井區","玉井區"),
  ("楠西區","楠西區"),
  ("南化區","南化區"),
  ("仁德區","仁德區"),
  ("關廟區","關廟區"),
  ("龍崎區","龍崎區"),
  ("官田區","官田區"),
  ("麻豆區","麻豆區"),
  ("佳里區","佳里區"),
  ("西港區","西港區"),
  ("七股區","七股區"),
  ("將軍區","將軍區"),
  ("學甲區","學甲區"),
  ("北門區","北門區"),
  ("新營區","新營區"),
  ("後壁區","後壁區"),
  ("白河區","白河區"),
  ("東山區","東山區"),
  ("六甲區","六甲區"),
  ("下營區","下營區"),
  ("柳營區","柳營區"),
  ("鹽水區","鹽水區"),
  ("善化區","善化區"),
  ("大內區","大內區"),
  ("山上區","山上區"),
  ("新市區","新市區"),
  ("安定區","安定區"),
  ("新興區","新興區"),
  ("前金區","前金區"),
  ("苓雅區","苓雅區"),
  ("鹽埕區","鹽埕區"),
  ("鼓山區","鼓山區"),
  ("旗津區","旗津區"),
  ("前鎮區","前鎮區"),
  ("三民區","三民區"),
  ("楠梓區","楠梓區"),
  ("小港區","小港區"),
  ("左營區","左營區"),
  ("仁武區","仁武區"),
  ("大社區","大社區"),
  ("岡山區","岡山區"),
  ("路竹區","路竹區"),
  ("阿蓮區","阿蓮區"),
  ("田寮區","田寮區"),
  ("燕巢區","燕巢區"),
  ("橋頭區","橋頭區"),
  ("梓官區","梓官區"),
  ("彌陀區","彌陀區"),
  ("永安區","永安區"),
  ("湖內區","湖內區"),
  ("鳳山區","鳳山區"),
  ("大寮區","大寮區"),
  ("林園區","林園區"),
  ("鳥松區","鳥松區"),
  ("大樹區","大樹區"),
  ("旗山區","旗山區"),
  ("美濃區","美濃區"),
  ("六龜區","六龜區"),
  ("內門區","內門區"),
  ("杉林區","杉林區"),
  ("甲仙區","甲仙區"),
  ("桃源區","桃源區"),
  ("那瑪夏區","那瑪夏區"),
  ("茂林區","茂林區"),
  ("茄萣區","茄萣區"),
  ("東沙群島","東沙群島"),
  ("南沙群島","南沙群島"),
  ("馬公市","馬公市"),
  ("西嶼鄉","西嶼鄉"),
  ("望安鄉","望安鄉"),
  ("七美鄉","七美鄉"),
  ("白沙鄉","白沙鄉"),
  ("湖西鄉","湖西鄉"),
  ("金沙鎮","金沙鎮"),
  ("金湖鎮","金湖鎮"),
  ("金寧鄉","金寧鄉"),
  ("金城鎮","金城鎮"),
  ("烈嶼鄉","烈嶼鄉"),
  ("烏坵鄉","烏坵鄉"),
  ("屏東市","屏東市"),
  ("三地門鄉","三地門鄉"),
  ("霧臺鄉","霧臺鄉"),
  ("瑪家鄉","瑪家鄉"),
  ("九如鄉","九如鄉"),
  ("里港鄉","里港鄉"),
  ("高樹鄉","高樹鄉"),
  ("鹽埔鄉","鹽埔鄉"),
  ("長治鄉","長治鄉"),
  ("麟洛鄉","麟洛鄉"),
  ("竹田鄉","竹田鄉"),
  ("內埔鄉","內埔鄉"),
  ("萬丹鄉","萬丹鄉"),
  ("潮州鎮","潮州鎮"),
  ("泰武鄉","泰武鄉"),
  ("來義鄉","來義鄉"),
  ("萬巒鄉","萬巒鄉"),
  ("崁頂鄉","崁頂鄉"),
  ("新埤鄉","新埤鄉"),
  ("南州鄉","南州鄉"),
  ("林邊鄉","林邊鄉"),
  ("東港鎮","東港鎮"),
  ("琉球鄉","琉球鄉"),
  ("佳冬鄉","佳冬鄉"),
  ("新園鄉","新園鄉"),
  ("枋寮鄉","枋寮鄉"),
  ("枋山鄉","枋山鄉"),
  ("春日鄉","春日鄉"),
  ("獅子鄉","獅子鄉"),
  ("車城鄉","車城鄉"),
  ("牡丹鄉","牡丹鄉"),
  ("恆春鎮","恆春鎮"),
  ("滿州鄉","滿州鄉"),
  ("臺東市","臺東市"),
  ("綠島鄉","綠島鄉"),
  ("蘭嶼鄉","蘭嶼鄉"),
  ("延平鄉","延平鄉"),
  ("卑南鄉","卑南鄉"),
  ("鹿野鄉","鹿野鄉"),
  ("關山鎮","關山鎮"),
  ("海端鄉","海端鄉"),
  ("池上鄉","池上鄉"),
  ("東河鄉","東河鄉"),
  ("成功鎮","成功鎮"),
  ("長濱鄉","長濱鄉"),
  ("太麻里鄉","太麻里鄉"),
  ("金峰鄉","金峰鄉"),
  ("大武鄉","大武鄉"),
  ("達仁鄉","達仁鄉"),
  ("花蓮市","花蓮市"),
  ("新城鄉","新城鄉"),
  ("秀林鄉","秀林鄉"),
  ("吉安鄉","吉安鄉"),
  ("壽豐鄉","壽豐鄉"),
  ("鳳林鎮","鳳林鎮"),
  ("光復鄉","光復鄉"),
  ("豐濱鄉","豐濱鄉"),
  ("瑞穗鄉","瑞穗鄉"),
  ("萬榮鄉","萬榮鄉"),
  ("玉里鎮","玉里鎮"),
  ("卓溪鄉","卓溪鄉"),
  ("富里鄉","富里鄉")
]

LIFEORDIE_LIST=[
  ("存","存"),
  ("殁","殁")
]

class YfcaseForm(forms.ModelForm):
  # 多加了widget=forms.Select(attrs={'class': 'form-select'})是要欄位在右側出現了向下的箭頭所設定
  yfcaseCompany = forms.ChoiceField(label="所屬公司",choices=COMPANY_LIST, widget=forms.Select(attrs={'class': 'form-select'}))
  yfcaseCaseStatus = forms.ChoiceField(label="案件狀態",choices=CASESTATUS_CHOICES)
  class Meta:
    model=Yfcase
    fields =['yfcaseCaseNumber','yfcaseCompany','yfcaseCity','yfcaseTownship','yfcaseBigSection','yfcaseSmallSection',"yfcaseVillage","yfcaseNeighbor","yfcaseStreet","yfcaseSection","yfcaseLane","yfcaseAlley","yfcaseNumber","yfcaseFloor",'yfcaseDebtor','yfcaseCreditor','yfcaseCreditorMobilePhone','yfcaseCityWithTownship','yfcaseCaseStatus','yfcaseSealUrl','user'] 
    

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.fields['yfcaseTownship'].queryset = Township.objects.none()
      
      if 'city' in self.data:
        try:
          city_id = int(self.data.get('city'))
          self.fields['yfcaseTownship'].queryset = Township.objects.filter(city_id=city_id).order_by('name')
        except (ValueError, TypeError):
          pass  # invalid input from the client; ignore and fallback to empty City queryset
      elif self.instance.pk:
        self.fields['yfcaseTownship'].queryset = self.instance.city.city_set.order_by('name')

class LandForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  class Meta:
    model=Land
    fields =['yfcase','landNumber','landUrl','landArea','landHoldingPointPersonal','landHoldingPointAll','landRemark'] 

class BuildForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  buildTypeUse = forms.ChoiceField(label="建物型",choices=BUILD_TYPE_USE, required=False)
  buildUsePartition = forms.ChoiceField(label="使用分區",choices=AREA_LIST, required=False)
  class Meta:
    model=Build
    fields ='__all__'

class AuctionForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  auctionDateFirst = forms.CharField(label="拍賣日(第一拍)",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)
  auctionDateSecond = forms.CharField(label="拍賣日(第二拍)",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)
  auctionDateThird = forms.CharField(label="拍賣日(第三拍)",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)
  auctionDateFourth = forms.CharField(label="拍賣日(第四拍)",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)

  class Meta:
    model=Auction
    fields ='__all__' 

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class SurveyForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  surveyFirstDay = forms.CharField(label="初勘日",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)
  surveySecondDay = forms.CharField(label="會勘日",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)
  class Meta:
    model=Survey
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class ObjectBuildForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  objectBuildStatus = forms.ChoiceField(label="狀態",choices=STATUS_LIST, required=False)
  objectBuildTransactionDate = forms.CharField(label="成交日期",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)
  class Meta:
    model=ObjectBuild
    fields =['yfcase','objectBuildAddress','objectBuildTotalPrice','objectBuildBuildArea','objectBuildHouseAge','objectBuildFloorHeight','objectBuildStatus','objectBuildTransactionDate','objectBuildUrl','objectBuildSubBuildArea']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

# ======= ScoreAForm =======
class ScoreAForm(forms.ModelForm):
  class Meta:
    model=ObjectBuild
    fields =['objectBuildScorerA','objectBuildScorRateA','objectBuildScorReasonA','plusItemA1','plusItemA2','plusItemA3','plusItemA4','plusItemA5','plusItemOtherA','plusValueA1','plusValueA2','plusValueA3','plusValueA4','plusValueA5','plusValueOtherA']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

# ======= ScoreBForm =======
class ScoreBForm(forms.ModelForm):
  class Meta:
    model=ObjectBuild
    fields =['objectBuildScorerB','objectBuildScorRateB','objectBuildScorReasonB','plusItemB1','plusItemB2','plusItemB3','plusItemB4','plusItemB5','plusItemOtherB','plusValueB1','plusValueB2','plusValueB3','plusValueB4','plusValueB5','plusValueOtherB']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

# ======= ScoreCForm =======
class ScoreCForm(forms.ModelForm):
  class Meta:
    model=ObjectBuild
    fields =['objectBuildScorerC','objectBuildScorRateC','objectBuildScorReasonC','plusItemC1','plusItemC2','plusItemC3','plusItemC4','plusItemC5','plusItemOtherC','plusValueC1','plusValueC2','plusValueC3','plusValueC4','plusValueC5','plusValueOtherC']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
# ======= FinalDecisionForm(regionalHead) =======
class FinalDecisionForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  regionalHead = forms.CharField(widget=forms.HiddenInput())
  finalDecision = forms.ChoiceField(label="最終判定",choices=JUDGMENT_LIST, required=False)
  regionalHeadDate = forms.CharField(label="簽核日期",widget=forms.TextInput(attrs={'class': 'form-control datepicker'}),required=False)
  # regionalHead = forms.ModelChoiceField(CustomUser.objects.all(), widget=forms.HiddenInput())
  class Meta:
    model=FinalDecision
    fields = ['yfcase','finalDecision','regionalHeadAddDate','finalDecisionRemark','regionalHead','regionalHeadDate','regionalHeadWorkArea']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

# ======= FinalDecisionForm(SubSigntrueA) =======
class SubSigntrueAForm(forms.ModelForm):
  class Meta:
    model=FinalDecision
    fields =['subSigntrueA','subSigntrueDateA','subSigntrueWorkAreaA']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

# ======= FinalDecisionForm(SubSigntrueB) =======
class SubSigntrueBForm(forms.ModelForm):
  class Meta:
    model=FinalDecision
    fields =['subSigntrueB','subSigntrueDateB','subSigntrueWorkAreaB']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

# ======= Result =======
class ResultForm(forms.ModelForm):
  yfcase = forms.ModelChoiceField(Yfcase.objects.all(), widget=forms.HiddenInput())
  bidAuctionTime = forms.ChoiceField(label="搶標拍別",choices=BIDAUCTION_LIST, required=False)
  actionResult = forms.ChoiceField(label="執行結果",choices=ACTIONRESULT_CHOICES, required=False)
  caseStatus = forms.ChoiceField(label="執行結果",choices=CASESTATUS_CHOICES, required=False)
  class Meta:
    model=Result
    fields =['yfcase', 'stopBuyDate', 'actionResult', 'bidAuctionTime', 'bidMoney', 'objectNumber']
    # fields =['yfcase', 'stopBuyDate', 'withdraw', 'bidAuctionTime', 'bidMoney', 'waitBuy', 'otherBuy', 'noOneBuy', 'objectNumber']

