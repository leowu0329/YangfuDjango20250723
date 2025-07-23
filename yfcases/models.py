from django.db import models
from decimal import *
from django.urls import reverse
from datetime import datetime
import math
import datetime
from django.utils import timezone

# ======= 縣市 =======
class City(models.Model):
  name = models.CharField(u'城市',max_length=30)

  def __str__(self):
    return self.name

  class Meta:
    # managed = True
    db_table = 'yfcase_city'

# ======= 鄉鎮 =======
class Township(models.Model):
  city = models.ForeignKey(City, on_delete=models.CASCADE)
  name = models.CharField(u'鄉鎮',max_length=30)
  zip_code = models.CharField(u'郵遞區號',max_length=30)
  district_court = models.CharField(u'地方法院',max_length=30)
  land_office  = models.CharField(u'地政事務所',max_length=30)
  finance_and_tax_bureau = models.CharField(u'財政稅務局',max_length=30)
  police_station = models.CharField(u'警察局',max_length=30)
  irs = models.CharField(u'國稅局',max_length=30)
  home_office = models.CharField(u'戶政事務所',max_length=30)

  def __str__(self):
    return self.name
 
  class Meta:
    # managed = True
    db_table = 'yfcase_township'

# ======= Yfcase =======
class Yfcase(models.Model):
  yfcaseCaseNumber=models.CharField(u'案號(*)',max_length=100)
  yfcaseCompany=models.CharField(u'所屬公司',max_length=50,null=True,blank=True)
  yfcaseCity=models.ForeignKey(City,verbose_name = u'縣市',on_delete=models.SET_NULL,null=True)
  yfcaseTownship=models.ForeignKey(Township,verbose_name = u'鄉鎮區里', on_delete=models.SET_NULL, null=True)
  yfcaseBigSection=models.CharField(u'段號',max_length=10,null=True,blank=True)
  yfcaseSmallSection=models.CharField(u'小段',max_length=10,null=True,blank=True)
  yfcaseVillage=models.CharField(u'村里',max_length=100,null=True,blank=True)
  yfcaseNeighbor=models.CharField(u'鄰',max_length=100,null=True,blank=True)
  yfcaseStreet=models.CharField(u'街路',max_length=100,null=True,blank=True)
  yfcaseSection=models.CharField(u'段',max_length=100,null=True,blank=True)
  yfcaseLane=models.CharField(u'巷',max_length=100,null=True,blank=True)
  yfcaseAlley=models.CharField(u'弄',max_length=100,null=True,blank=True)
  yfcaseNumber=models.CharField(u'號',max_length=100,null=True)
  yfcaseFloor=models.CharField(u'樓(含之幾)',max_length=100,null=True,blank=True)
  yfcaseDebtor=models.CharField(u'債務人',max_length=100,null=True,blank=True)
  yfcaseCreditor=models.CharField(u'債權人',max_length=100,null=True,blank=True)
  yfcaseCreditorMobilePhone=models.CharField(u'債權人電話',max_length=20,null=True,blank=True)
  yfcaseCityWithTownship = models.CharField(u'縣市鄉鎮',max_length=20,null=True,blank=True)
  yfcaseCaseStatus = models.CharField(u'案件狀態',max_length=10,null=True,blank=True)
  yfcaseSealUrl = models.URLField(max_length=255,null=True,blank=True)
  yfcaseUpdated = models.DateTimeField(u'案件最後更新時間',auto_now=True,auto_now_add=False)
  yfcaseTimestamp = models.DateTimeField(u'案件建立時間',auto_now=False,auto_now_add=True)
  user = models.ForeignKey('users.CustomUser',verbose_name = u'區域負責人', on_delete=models.CASCADE)
  # 契稅申請單欄位
  yfcaseDeedtaxHouseTaxRegistrationNumber=models.CharField(u'房屋稅籍編號',max_length=100,null=True,blank=True)
  yfcaseDeedtaxEstablishmentDate=models.DateField(u'契稅建立日期',null=True,blank=True)
  yfcaseDeedtaxDeclarationDate=models.DateField(u'契稅申報日期',null=True,blank=True)
  yfcaseDeedtaxClient=models.CharField(u'契稅委託人',max_length=100,null=True,blank=True)
  yfcaseDeedtaxTransferPrice= models.DecimalField(u'契稅移轉價格',default=0,max_digits=10,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxReclaimMethod=models.CharField(u'契稅領回方式',max_length=100,null=True,blank=True)
  yfcaseDeedtaxClosingNewsletter=models.CharField(u'契稅結案簡訊',max_length=100,null=True,blank=True)
  yfcaseDeedtaxRemarks=models.CharField(u'契稅備註',max_length=100,null=True,blank=True)
  yfcaseDeedtaxReportAttached=models.CharField(u'契稅報附聯',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorIdentityCard=models.CharField(u'身分証或統一編號',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorBirthday=models.DateField(u'生日',null=True,blank=True)
  yfcaseDeedtaxDebtorLocalPhone=models.CharField(u'市話',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorMobilePhone=models.CharField(u'手機',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorCity=models.CharField(u'縣市',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorTownship=models.CharField(u'鄉鎮區',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorVillage=models.CharField(u'村里',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorNeighbor=models.CharField(u'鄰',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorStreet=models.CharField(u'街路',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorSection=models.CharField(u'段',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorLane=models.CharField(u'巷',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorAlley=models.CharField(u'弄',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorNumber=models.CharField(u'號',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorFloor=models.CharField(u'樓(含之幾)',max_length=100,null=True,blank=True)
  yfcaseDeedtaxDebtorLandHoldingPointPersonal=models.DecimalField(u'土地個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxDebtorLandHoldingPointAll=models.DecimalField(u'土地所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxDebtorBuildHoldingPointPersonal=models.DecimalField(u'建物個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxDebtorBuildHoldingPointAll=models.DecimalField(u'建物所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxCreditorIdentityCard=models.CharField(u'身分証或統一編號',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorBirthday=models.DateField(u'生日',null=True,blank=True)
  yfcaseDeedtaxCreditorLocalPhone=models.CharField(u'市話',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorMobilePhone=models.CharField(u'手機',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorCity=models.CharField(u'縣市',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorTownship=models.CharField(u'鄉鎮區',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorVillage=models.CharField(u'村里',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorNeighbor=models.CharField(u'鄰',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorStreet=models.CharField(u'街路',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorSection=models.CharField(u'段',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorLane=models.CharField(u'巷',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorAlley=models.CharField(u'弄',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorNumber=models.CharField(u'號',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorFloor=models.CharField(u'樓(含之幾)',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCreditorLandHoldingPointPersonal=models.DecimalField(u'土地個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxCreditorLandHoldingPointAll=models.DecimalField(u'土地所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxCreditorBuildHoldingPointPersonal=models.DecimalField(u'建物個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseDeedtaxCreditorBuildHoldingPointAll=models.DecimalField(u'建物所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  # 契稅申請書-(12)移轉情形
  yfcaseDeedtaxBuildingTransferLevel1 = models.CharField(u'移轉情形-層次1',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferLevel2 = models.CharField(u'移轉情形-層次2',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferLevel3 = models.CharField(u'移轉情形-層次3',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferLevel4 = models.CharField(u'移轉情形-層次4',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferLevel5 = models.CharField(u'移轉情形-層次5',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferLevel6 = models.CharField(u'移轉情形-層次6',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferStructure1 = models.CharField(u'移轉情形-構造1',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferStructure2 = models.CharField(u'移轉情形-構造2',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferStructure3 = models.CharField(u'移轉情形-構造3',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferStructure4 = models.CharField(u'移轉情形-構造4',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferStructure5 = models.CharField(u'移轉情形-構造5',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferStructure6 = models.CharField(u'移轉情形-構造6',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferArea1 = models.DecimalField(u'移轉情形-面積(平方公尺)-1',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferArea2 = models.DecimalField(u'移轉情形-面積(平方公尺)-2',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferArea3 = models.DecimalField(u'移轉情形-面積(平方公尺)-3',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferArea4 = models.DecimalField(u'移轉情形-面積(平方公尺)-4',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferArea5 = models.DecimalField(u'移轉情形-面積(平方公尺)-5',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferArea6 = models.DecimalField(u'移轉情形-面積(平方公尺)-6',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicBuildingNumber1 = models.CharField(u'移轉情形-公設建號1',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicBuildingNumber2 = models.CharField(u'移轉情形-公設建號2',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicBuildingNumber3 = models.CharField(u'移轉情形-公設建號3',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicBuildingNumber4 = models.CharField(u'移轉情形-公設建號4',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicHoldings1 = models.CharField(u'移轉情形-持分比例1',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicHoldings2 = models.CharField(u'移轉情形-持分比例2',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicHoldings3 = models.CharField(u'移轉情形-持分比例3',max_length=100,null=True,blank=True)
  yfcaseDeedtaxBuildingTransferPublicHoldings4 = models.CharField(u'移轉情形-持分比例4',max_length=100,null=True,blank=True)
  yfcaseDeedtaxCoOwnerMatch=models.BooleanField(u'共有人一致',default=True)

  # 不動產登記(Real Estate Registration)
  yfcaseRealEstateRegistrationRegisteredAgent = models.CharField(u'登記代理人',max_length=100,null=True,blank=True)
  yfcaseRealEstateRegistrationDateOfCause = models.DateField(u'原因發生日期',null=True,blank=True)
  yfcaseRealEstateRegistrationReasonForRegistration = models.CharField(u'登記原因',max_length=100,null=True,blank=True)
  yfcaseRealEstateRegistrationRegistrationNote = models.CharField(u'登記備註',max_length=100,null=True,blank=True)
  yfcaseApplyAcrossInstitutions = models.BooleanField(u'跨所申請',default=False)
  yfcaseAcceptingAuthorityTownship = models.CharField(u'鄉鎮區里',max_length=100,null=True,blank=True)

  # 訢訟狀  
  yfcaseComplaintComplaintDate = models.DateField(u'起訴狀填寫日期',null=True,blank=True)
  yfcaseComplaintLitigationAgent= models.CharField(u'訴訟代理人',max_length=100,null=True,blank=True)
  yfcaseComplaintPresentValueOfLandAnnouncement = models.DecimalField(u'土地公告現值',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseComplaintPresentValueOfHouseTax= models.DecimalField(u'房屋課稅現值',default=0,max_digits=8,decimal_places=2,null=True,blank=True)
  yfcaseComplaintRefereeFee = models.DecimalField(u'裁判費',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  yfcaseComplaintUnsuccessfulDate = models.DateField(u'分割未果日期',null=True,blank=True)
  yfcaseComplaintLandWidth = models.DecimalField(u'土地面寬',default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  yfcaseComplaintLandDepth = models.DecimalField(u'土地深度',default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  yfcaseComplaintExhibit1 = models.CharField(u'證物1',max_length=100,null=True,blank=True)
  yfcaseComplaintExhibit2 = models.CharField(u'證物2',max_length=100,null=True,blank=True)
  yfcaseComplaintExhibit3 = models.CharField(u'證物3',max_length=100,null=True,blank=True)
  yfcaseComplaintExhibit4 = models.CharField(u'證物4',max_length=100,null=True,blank=True)

  # 存證信函
  yfcaseLetterAgent = models.CharField(u'存證信函代理人',max_length=100,null=True,blank=True)
  yfcaseLetterSender = models.CharField(u'存證信函寄件人',max_length=100,null=True,blank=True)

  
  # 共有人
  yfcaseCownerAgent = models.CharField(u'共有人代理人',max_length=100,null=True,blank=True)
  yfcasecoOwnerLandHPPersonnal=models.DecimalField(u'土地個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcasecoOwnerLandHPAll=models.DecimalField(u'土地所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseAllCoOwnerLandHPPersonnal=models.DecimalField(u'所有共有人應土地持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcaseAllCoOwnerLandHPAll=models.DecimalField(u'所有土地持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcasecoOwnerBuildHPPersonnal=models.DecimalField(u'建物個人持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  yfcasecoOwnerBuildHPAll=models.DecimalField(u'建物所有持分',default=0,max_digits=8,decimal_places=0,null=True,blank=True)
  
  def __str__(self):
    return self.yfcaseCaseNumber
    
  class Meta:
    # managed = True
    db_table = 'yfcase_yfcase'
    ordering = ["-yfcaseUpdated"]


  def fullAddress(self):
    # 變數名稱 = 自身欄名 判定自身欄名為None就空白，要不然返回自身的變數
    city = self.yfcaseCity if self.yfcaseCity is not None else ""
    township = self.yfcaseTownship if self.yfcaseTownship is not None else ""
    # bigSection = self.yfcaseBigSection if self.yfcaseBigSection is not None else ""
    # smallSection = self.yfcaseSmallSection if self.yfcaseSmallSection is not None else ""
    village = self.yfcaseVillage if self.yfcaseVillage is not None else ""
    neighbor = self.yfcaseNeighbor + "鄰" if self.yfcaseNeighbor is not None else ""
    street = self.yfcaseStreet if self.yfcaseStreet is not None else ""
    section = self.yfcaseSection + "段" if self.yfcaseSection is not None else ""
    lane = self.yfcaseLane + "巷" if self.yfcaseLane is not None else ""
    alley = self.yfcaseAlley + "弄" if self.yfcaseAlley is not None else ""
    number = self.yfcaseNumber + "號" if self.yfcaseNumber is not None else ""
    floor = self.yfcaseFloor if self.yfcaseFloor is not None else ""
    # 將各個欄位合併
    result = str(city)+str(township)+str(village)+str(neighbor)+str(street)+str(section)+str(lane)+str(alley)+str(number)+str(floor)
    return result

  # 在編輯Land設定
  # 得到所有地號面積的總和
  def get_land_holding_point_area_total(self):
    newlist=[]
    try:
      landTotal = 0
      for land_item in self.lands.exclude(landHoldingPointAll=0):
        landTotal += land_item.landArea * land_item.landHoldingPointPersonal / land_item.landHoldingPointAll
      return landTotal
    except:
      newlist.append(0)

  # 在編輯Build設定
  # 第一筆建物(非公設、非增建)各別面積
  def get_build_first_not_add_and_not_public_area(self):
    try:
      return self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().get_build_holding_point_area()
    except ZeroDivisionError:
      return 0

  # 取得第一筆非公設、非增建的持分比
  def get_first_not_add_and_not_public_holding_point_rate(self):
    try:
      if self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first():
        getFirstNotAddAndNotPublicHoldingPointPersonnal = self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().buildHoldingPointPersonal
        getFirstNotAddAndNotPublicHoldingPointAll = self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().buildHoldingPointAll
        return getFirstNotAddAndNotPublicHoldingPointPersonnal / getFirstNotAddAndNotPublicHoldingPointAll
    except ZeroDivisionError:
      return 0
      
  # (1)建物(非公設、非增建)持分後總面積
  def get_build_holding_point_area_group_total(self):
    newlist=[]
    try:
      getBuildHoldingPointAreaGroupTotal=0
      for getBuildHoldingPointAreaGroup in self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設"):
        getBuildHoldingPointAreaGroupTotal = getBuildHoldingPointAreaGroupTotal + getBuildHoldingPointAreaGroup.get_build_holding_point_area()
      return getBuildHoldingPointAreaGroupTotal
    except:
      newlist.append(0)

  # (2)建物(公設)持分後總面積
  def get_build_holding_point_public_group_total(self):
    getBuildHoldingPointPublicGroupTotal=0
    for getBuildHoldingPointPublicGroup in self.builds.filter(buildTypeUse="公設"):
      getBuildHoldingPointPublicGroupTotal = getBuildHoldingPointPublicGroupTotal + getBuildHoldingPointPublicGroup.get_build_first_not_add_and_not_public_holding_point_area()
    return getBuildHoldingPointPublicGroupTotal

  # (3)建物(增建)持分後總面積
  def get_build_holding_point_add_group_total(self):
    try:
      getBuildHoldingPointAddGroupTotal=0
      for getBuildHoldingPointAddGroup in self.builds.filter(buildTypeUse="增建-持分後坪數打對折"):
        getBuildHoldingPointAddGroupTotal = getBuildHoldingPointAddGroupTotal + getBuildHoldingPointAddGroup.get_after_add_holding_point_area()
      return getBuildHoldingPointAddGroupTotal
    except ZeroDivisionError:
      return 0

  # 上述(1)+(2)+(3)
  def get_build_holding_point_after_group_total(self):
    newlist=[]
    try:
      return self.get_build_holding_point_area_group_total() + self.get_build_holding_point_public_group_total() + self.get_build_holding_point_add_group_total()
    except:
      newlist.append(0)

  # 在編輯Auction設定
  # 計算時價
  def pbk(self):
    newlist=[]
    try:
      sumpbk=0
      countbk=0
      if self.auctions.all().filter(auctionFloorPriceFirst__gt=1000000):
        for objectbuild_item in self.objectbuilds.all():
          sumpbk += objectbuild_item.get_objectbuild_ping_price_abc_calculation()
          countbk += 1
        return sumpbk / countbk
      else:
        for objectbuild_item in self.objectbuilds.all():
          sumpbk += objectbuild_item.get_objectbuild_ping_price_ab_calculation()
          countbk += 1
        return sumpbk / countbk
    except:
      newlist.append(0)
  
  # 取得當前最後一拍對應的底價
  def get_floor_price_from_auction_date(self):
    auctionDateFirst_day = self.auctions.first().auctionDateFirst
    auctionDateSecond_day = self.auctions.first().auctionDateSecond
    auctionDateThird_day = self.auctions.first().auctionDateThird
    auctionDateFourth_day = self.auctions.first().auctionDateFourth
    auctionDateFirst_price = self.auctions.first().auctionFloorPriceFirst
    auctionDateSecond_price = self.auctions.first().auctionFloorPriceSecond
    auctionDateThird_price = self.auctions.first().auctionFloorPriceThird
    auctionDateFourth_price = self.auctions.first().auctionFloorPriceFourth
    if auctionDateFourth_price > 0 and auctionDateFourth_day != "":
      return auctionDateFourth_price
    elif auctionDateThird_price > 0 and auctionDateThird_day != "":
      return auctionDateThird_price
    elif auctionDateSecond_price > 0 and auctionDateSecond_day != "":
      return auctionDateSecond_price
    elif auctionDateFirst_price > 0 and auctionDateFirst_day != "":
      return auctionDateFirst_price
    else:
      return 0

  # 判斷是否為兩週內
  def two_weeks(self):
    # 取得目前的日期，要用form dateteim import datetime,不可用import datetime
    today = datetime.now()
    finaldecision_content = self.finaldecisions.first().finalDecision
    auctionDateFirst_day = self.auctions.first().auctionDateFirst
    auctionDateSecond_day = self.auctions.first().auctionDateSecond
    auctionDateThird_day = self.auctions.first().auctionDateThird
    auctionDateFourth_day = self.auctions.first().auctionDateFourth
    if finaldecision_content == "1拍進場" and auctionDateFirst_day != None:
      # 取得要計算的日期，要用form dateteim import datetime,不可用import datetime
      other_day = datetime.strptime(auctionDateFirst_day,'%Y-%m-%d')
      return (other_day-today).days + 1
    elif finaldecision_content == "2拍進場" and auctionDateSecond_day != None:
      # 取得要計算的日期，要用form dateteim import datetime,不可用import datetime
      other_day = datetime.strptime(auctionDateSecond_day,'%Y-%m-%d')
      return (other_day-today).days + 1
    elif finaldecision_content == "3拍進場" and auctionDateThird_day != None:
      # 取得要計算的日期，要用form dateteim import datetime,不可用import datetime
      other_day = datetime.strptime(auctionDateThird_day,'%Y-%m-%d')
      return (other_day-today).days + 1
    elif finaldecision_content == "4拍進場" and auctionDateFourth_day != None:
      # 取得要計算的日期，要用form dateteim import datetime,不可用import datetime
      other_day = datetime.strptime(auctionDateFourth_day,'%Y-%m-%d')
      return (other_day-today).days + 1
    else:
      return ""

  # auction 第一拍底價大於0的資料(get)
  def get_auction_1st(self):
    return self.auctions.all().get(auctionFloorPriceFirst__gt=0) 

  # auction 第二拍底價大於0的資料(get)
  def get_auction_2nd(self):
    return self.auctions.all().get(auctionFloorPriceSecond__gt=0)  

  # auction 第三拍底價大於0的資料(get)
  def get_auction_3rd(self):
    return self.auctions.all().get(auctionFloorPriceThird__gt=0)

  # auction 第四拍底價大於0的資料(get)
  def get_auction_4th(self):
    return self.auctions.all().get(auctionFloorPriceFourth__gt=0)    

  # result 篩選買止日不為空(filter)
  def get_result_stopBuyDate(self):
    return self.results.all().filter(stopBuyDate__isnull=False)

  # 在編輯finalDecision設定
  # 取得區域負責人的全名
  # def get_regionalHead_username(self):
  #     return self.finaldecisions.regionalHead

  # 取得當前登錄人員的全名
  # def get_user_username(self):
  #   return self.user.userFullName

  # 在編輯Build設定
  # 第一筆建物(非公設、非增建)各別面積
  def get_build_first_not_add_and_not_public_area(self):
    try:
      return self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().get_build_holding_point_area()
    except ZeroDivisionError:
      return 0

  # 取得第一筆非公設、非增建的個人持分
  def get_first_not_add_and_not_public_holding_point_personnal_rate(self):
    try:
      if self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first():
        getFirstNotAddAndNotPublicHoldingPointPersonnal = self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().buildHoldingPointPersonal
        return getFirstNotAddAndNotPublicHoldingPointPersonnal
    except ZeroDivisionError:
      return 0
      
  # 取得第一筆非公設、非增建的所有持分
  def get_first_not_add_and_not_public_holding_point_all_rate(self):
    try:
      if self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first():
        getFirstNotAddAndNotPublicHoldingPointAll = self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().buildHoldingPointAll
        return getFirstNotAddAndNotPublicHoldingPointAll
    except ZeroDivisionError:
      return 0

  # 取得第一筆非公設、非增建的持分比
  def get_first_not_add_and_not_public_holding_point_rate(self):
    try:
      if self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first():
        getFirstNotAddAndNotPublicHoldingPointPersonnal = self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().buildHoldingPointPersonal
        getFirstNotAddAndNotPublicHoldingPointAll = self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設").first().buildHoldingPointAll
        return getFirstNotAddAndNotPublicHoldingPointPersonnal / getFirstNotAddAndNotPublicHoldingPointAll
    except ZeroDivisionError:
      return 0
      
  # (1)建物(非公設、非增建)持分後總面積
  def get_build_holding_point_area_group_total(self):
    newlist=[]
    try:
      getBuildHoldingPointAreaGroupTotal=0
      for getBuildHoldingPointAreaGroup in self.builds.exclude(buildTypeUse="增建-持分後坪數打對折").exclude(buildTypeUse="公設"):
        getBuildHoldingPointAreaGroupTotal = getBuildHoldingPointAreaGroupTotal + getBuildHoldingPointAreaGroup.get_build_holding_point_area()
      return getBuildHoldingPointAreaGroupTotal
    except:
      newlist.append(0)

  # (2)建物(公設)持分後總面積
  def get_build_holding_point_public_group_total(self):
    getBuildHoldingPointPublicGroupTotal=0
    for getBuildHoldingPointPublicGroup in self.builds.filter(buildTypeUse="公設"):
      getBuildHoldingPointPublicGroupTotal = getBuildHoldingPointPublicGroupTotal + getBuildHoldingPointPublicGroup.get_build_first_not_add_and_not_public_holding_point_area()
    return getBuildHoldingPointPublicGroupTotal

  # (3)建物(增建)持分後總面積
  def get_build_holding_point_add_group_total(self):
    try:
      getBuildHoldingPointAddGroupTotal=0
      for getBuildHoldingPointAddGroup in self.builds.filter(buildTypeUse="增建-持分後坪數打對折"):
        getBuildHoldingPointAddGroupTotal = getBuildHoldingPointAddGroupTotal + getBuildHoldingPointAddGroup.get_after_add_holding_point_area()
      return getBuildHoldingPointAddGroupTotal
    except ZeroDivisionError:
      return 0

  # 上述(1)+(2)+(3)
  def get_build_holding_point_after_group_total(self):
    newlist=[]
    try:
      return self.get_build_holding_point_area_group_total() + self.get_build_holding_point_public_group_total() + self.get_build_holding_point_add_group_total()
    except:
      newlist.append(0)
      
  # 訴訟標的價額  
  def get_litigation_subject_price(self):
    newlist=[]
    try:
      # 土地公告現值
      PresentValueOfLandAnnouncement = self.yfcaseComplaintPresentValueOfLandAnnouncement
      # 土地總面積 * 土地原告應有持分
      LandHPTotalArea = self.get_land_holding_point_area_total()
      # 系爭房屋課稅現值
      PresentValueOfHouseTax = self.yfcaseComplaintPresentValueOfHouseTax
      # 房屋原告應有持分
      BuildHP = self.get_first_not_add_and_not_public_holding_point_personnal_rate() / self.get_first_not_add_and_not_public_holding_point_all_rate()
      return (PresentValueOfLandAnnouncement * LandHPTotalArea) + (PresentValueOfHouseTax * BuildHP)
    except:
      newlist.append(0)

    # ⺠事起訴狀（裁判分割共有物）
  # 共有人+債權人土地持分合計
  def get_coownerinfo_land_holding_point_total(self):
    newlist=[]
    try:
      getCoOwnerInfosLandHPPersonnalTotal=0
      for getCoOwnerLandHP in self.coownerinfos.filter(coOwnerLandHPPersonnal__gt=0).filter(coOwnerLandHPAll__gt=0):
        getCoOwnerInfosLandHPPersonnalTotal = getCoOwnerInfosLandHPPersonnalTotal + ( getCoOwnerLandHP.coOwnerLandHPPersonnal / getCoOwnerLandHP.coOwnerLandHPAll )
      return getCoOwnerInfosLandHPPersonnalTotal + ( self.yfcasecoOwnerLandHPPersonnal / self.yfcasecoOwnerLandHPAll )
    except:
      newlist.append(0)
    
  # 共有人+債權人建物持分合計
  def get_coownerinfo_build_holding_point_total(self):
    newlist=[]
    try:
      getCoOwnerInfosBuildHPPersonnalTotal=0
      for getCoOwnerBuildHP in self.coownerinfos.filter(coOwnerBuildHPPersonnal__gt=0).filter(coOwnerBuildHPAll__gt=0):
        getCoOwnerInfosBuildHPPersonnalTotal = getCoOwnerInfosBuildHPPersonnalTotal + ( getCoOwnerBuildHP.coOwnerBuildHPPersonnal / getCoOwnerBuildHP.coOwnerBuildHPAll )
      return getCoOwnerInfosBuildHPPersonnalTotal + ( self.yfcasecoOwnerBuildHPPersonnal / self.yfcasecoOwnerBuildHPAll )
    except:
      newlist.append(0)

  # 存証信函-所有共有人的土地持分總計
  def get_all_coowner_land_HP(self):
    newlist=[]
    try:
      return self.yfcaseAllCoOwnerLandHPPersonnal / self.yfcaseAllCoOwnerLandHPAll
    except:
      newlist.append(0)

# ======= Land =======
class Land(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='lands',on_delete=models.CASCADE)
  landNumber=models.CharField(u'地號',max_length=100,null=True)
  landUrl=models.URLField(u'謄本',max_length=200,null=True,blank=True)
  landArea=models.DecimalField(u'地坪(平方公尺)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  landHoldingPointPersonal=models.DecimalField(u'個人持分',default=0,max_digits=10,decimal_places=0,null=True,blank=True)
  landHoldingPointAll=models.DecimalField(u'所有持分',default=0,max_digits=10,decimal_places=0,null=True,blank=True)
  landRemark=models.CharField(u'備註',max_length=100,null=True,blank=True)
  landUpdated = models.DateTimeField(u'案件最後更新時間',auto_now=True,auto_now_add=False)
  
  def __str__(self):
    return self.landNumber

  class Meta:
    # managed = True
    db_table = 'yfcase_land'
    ordering = ["-landUpdated",]

  def get_land_holding_point_area(self):
    return self.landArea * ( self.landHoldingPointPersonal / self.landHoldingPointAll)

# ======= Build =======
class Build(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='builds',on_delete=models.CASCADE)
  buildNumber=models.CharField(u'建號',max_length=100,null=True)
  buildUrl=models.URLField(u'謄本',max_length=200,null=True,blank=True)
  buildArea=models.DecimalField(u'建坪(平方公尺)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  buildHoldingPointPersonal=models.DecimalField(u'個人持分',default=0,max_digits=10,decimal_places=0,null=True,blank=True)
  buildHoldingPointAll=models.DecimalField(u'所有持分',default=0,max_digits=10,decimal_places=0,null=True,blank=True)
  buildTypeUse=models.CharField(u'建物型',max_length=100,null=True,blank=True)
  buildUsePartition=models.CharField(u'使用分區',max_length=100,null=True,blank=True)
  buildRemark=models.CharField(u'備註',max_length=100,null=True,blank=True)
  buildAncillaryBuildingUseBy=models.CharField(u'附屬建物用途',max_length=100,null=True,blank=True)
  buildAncillaryBuildingArea=models.DecimalField(u'附屬建物面積',default=0,max_digits=6,decimal_places=2,null=True,blank=True)

  def __str__(self):
    return self.buildNumber

  # 建物(非公設、非增建)各別面積
  def get_build_holding_point_area(self):
    newlist=[]
    try:
      return self.buildArea * ( self.buildHoldingPointPersonal / self.buildHoldingPointAll)
    except:
      newlist.append(0)

  # 建物(增建)各別面積
  def get_after_add_holding_point_area(self):
    newlist=[]
    try:
      return self.get_build_holding_point_area() / 2
    except:
      newlist.append(0)

  # 建物(公設)各別面積
  def get_build_first_not_add_and_not_public_holding_point_area(self):
    try:
      return self.buildArea * (self.buildHoldingPointPersonal / self.buildHoldingPointAll) * self.yfcase.get_first_not_add_and_not_public_holding_point_rate()
    except ZeroDivisionError:
      return 0

# ======= Auction =======
class Auction(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='auctions',on_delete=models.CASCADE)
  auctionDateFirst = models.CharField(u'拍賣日(第一拍)',max_length=100,null=True,blank=True)
  auctionDateSecond = models.CharField(u'拍賣日(第二拍)',max_length=100,null=True,blank=True)
  auctionDateThird = models.CharField(u'拍賣日(第三拍)',max_length=100,null=True,blank=True)
  auctionDateFourth = models.CharField(u'拍賣日(第四拍)',max_length=100,null=True,blank=True)
  auctionFloorPriceFirst = models.DecimalField(u'底價(第一拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionFloorPriceSecond = models.DecimalField(u'底價(第二拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionFloorPriceThird = models.DecimalField(u'底價(第三拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionFloorPriceFourth = models.DecimalField(u'底價(第四拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionClickFirst = models.DecimalField(u'點閱(第一拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionClickSecond = models.DecimalField(u'點閱(第二拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionClickThird = models.DecimalField(u'點閱(第三拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionClickFourth = models.DecimalField(u'點閱(第四拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorFirst = models.DecimalField(u'監控(第一拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorSecond = models.DecimalField(u'監控(第二拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorThird = models.DecimalField(u'監控(第三拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMonitorFourth = models.DecimalField(u'監控(第四拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionCaseCountFirst = models.DecimalField(u'成交件數(第一拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionCaseCountSecond = models.DecimalField(u'成交件數(第二拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionCaseCountThird = models.DecimalField(u'成交件數(第三拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionCaseCountFourth = models.DecimalField(u'成交件數(第四拍)',default=0,max_digits=4,decimal_places=0,null=True,blank=True)
  auctionMarginFirst = models.DecimalField(u'保証金(第一拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionMarginSecond = models.DecimalField(u'保証金(第二拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionMarginThird = models.DecimalField(u'保証金(第三拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  auctionMarginFourth = models.DecimalField(u'保証金(第四拍)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)

  def get_ping_first_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceFirst / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_ping_second_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceSecond / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_ping_third_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceThird / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_ping_fourth_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceFourth / (self.yfcase.get_build_holding_point_after_group_total()* Decimal(0.3025))
    except:
      newlist.append(0)

  def get_first_cp(self):
    newlist=[]
    try:
      return  self.yfcase.pbk() / self.get_ping_first_price()
    except:
      newlist.append(0)

  def get_second_cp(self):
    newlist=[]
    try:
      return self.yfcase.pbk() / self.get_ping_second_price()
    except:
      newlist.append(0)

  def get_third_cp(self):
    newlist=[]
    try:
      return self.yfcase.pbk() / self.get_ping_third_price()
    except:
      newlist.append(0)

  def get_fourth_cp(self):
    newlist=[]
    try:
      return self.yfcase.pbk() / self.get_ping_fourth_price()
    except:
      newlist.append(0)

  def get_suggestedincreaseFirst(self):
    newlist=[]
    try:
      suggestedincreaseFirst = (math.ceil(self.auctionClickFirst / 100)+self.auctionMonitorFirst) * 3 / 100
      if suggestedincreaseFirst > 0.15:
        return 0.15
      else:
        return suggestedincreaseFirst
    except:
      newlist.append(0)

  def get_suggestedincreaseSecond(self):
    newlist=[]
    try:
      suggestedincreaseSecond = (math.ceil(self.auctionClickSecond / 100)+self.auctionMonitorSecond) * 3 / 100
      if suggestedincreaseSecond > 0.15:
        return 0.15
      else:
        return suggestedincreaseSecond
    except:
      newlist.append(0)

  def get_suggestedincreaseThird(self):
    newlist=[]
    try:
      suggestedincreaseThird = (math.ceil(self.auctionClickThird / 100)+self.auctionMonitorThird) * 3 / 100
      if suggestedincreaseThird > 0.15:
        return 0.15
      else:
        return suggestedincreaseThird
    except:
      newlist.append(0)

  def get_suggestedincreaseFouth(self):
    newlist=[]
    try:
      suggestedincreaseFouth = (math.ceil(self.auctionClickFourth / 100)+self.auctionMonitorFourth) * 3 / 100
      if suggestedincreaseFouth > 0.15:
        return 0.15
      else:
        return suggestedincreaseFouth
    except:
      newlist.append(0)

  # 建議加價(第一拍)
  def get_suggestedincreaseFirst_floor_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceFirst * Decimal( 1 + self.get_suggestedincreaseFirst())
    except:
      newlist.append(0)


  # 建議加價CP(第一拍)
  def get_suggestedincreaseFirst_cp(self):
    newlist=[]
    try:
      return self.get_first_cp() / Decimal( 1 + self.get_suggestedincreaseFirst())
    except:
      newlist.append(0)


  # 建議加價(第二拍)
  def get_suggestedincreaseSecond_floor_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceSecond * Decimal( 1 + self.get_suggestedincreaseSecond())
    except:
      newlist.append(0)

  # 建議加價CP(第二拍)
  def get_suggestedincreaseSecond_cp(self):
    newlist=[]
    try:
      return self.get_second_cp() / Decimal( 1 + self.get_suggestedincreaseSecond())
    except:
      newlist.append(0)

  # 建議加價(第三拍)
  def get_suggestedincreaseThird_floor_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceThird * Decimal( 1 + self.get_suggestedincreaseThird())
    except:
      newlist.append(0)
      
      
  # 建議加價CP(第三拍)
  def get_suggestedincreaseThird_cp(self):
    newlist=[]
    try:
      return self.get_third_cp() / Decimal( 1 + self.get_suggestedincreaseThird())
    except:
      newlist.append(0)

  # 建議加價(第四拍)
  def get_suggestedincreaseFourth_floor_price(self):
    newlist=[]
    try:
      return self.auctionFloorPriceFourth * Decimal( 1 + self.get_suggestedincreaseFouth())
    except:
      newlist.append(0)


  # 建議加價CP(第四拍)
  def get_suggestedincreaseFourth_cp(self):
    newlist=[]
    try:
      return self.get_fourth_cp() / Decimal( 1 + self.get_suggestedincreaseFouth())
    except:
      newlist.append(0)

# ======= Survey =======
class Survey(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='surveys',on_delete=models.CASCADE)
  surveyFirstDay = models.CharField(u'初勘日',max_length=100,null=True,blank=True)
  surveySecondDay = models.CharField(u'會勘日',max_length=100,null=True,blank=True)
  surveyForeclosureAnnouncementLink = models.URLField(u'法拍公告(證物三)',max_length=1000,null=True,blank=True)
  survey988Link = models.URLField(u'998連結',max_length=1000,null=True,blank=True)
  surveyObjectPhotoLink = models.URLField(u'物件照片(證物四)',max_length=1000,null=True,blank=True)
  surveyNetMarketPriceLink = models.URLField(max_length=1000,null=True,blank=True)
  surveyForeclosureRecordLink = models.URLField(u'法拍記錄(證物七)',max_length=1000,null=True,blank=True)
  surveyObjectViewLink = models.URLField(u'標的物(現場勘查)',max_length=1000,null=True,blank=True)
  surveyPagesViewLink = models.URLField(u'收發文薄',max_length=1000,null=True,blank=True)
  surveyMoneytViewLink = models.URLField(u'流水帳',max_length=1000,null=True,blank=True)

# ======= ObjectBuild =======
class ObjectBuild(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='objectbuilds',on_delete=models.CASCADE)
  objectBuildAddress = models.CharField(u'地址',max_length=100,null=True,blank=True)
  objectBuildTotalPrice=models.DecimalField(u'總價(NT)',default=0,max_digits=10,decimal_places=0,null=True,blank=True)
  objectBuildBuildArea=models.DecimalField(u'建坪(坪)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  objectBuildSubBuildArea=models.DecimalField(u'增建坪數(坪)',default=0,max_digits=10,decimal_places=2,null=True,blank=True)
  objectBuildHouseAge=models.DecimalField(u'屋齡(年)',default=0,max_digits=5,decimal_places=2,null=True,blank=True)
  objectBuildFloorHeight = models.CharField(u'樓高',max_length=100,null=True,blank=True)
  objectBuildStatus = models.CharField(u'狀態',max_length=100,null=True,blank=True)
  objectBuildTransactionDate = models.CharField(u'成交日期',max_length=100,null=True,blank=True)
  objectBuildUrl =models.URLField(u'附件',max_length=1000,null=True,blank=True)
  objectBuildScorerA = models.CharField(u'勘查員A',max_length=100,null=True,blank=True)
  objectBuildScorerB = models.CharField(u'勘查員B',max_length=100,null=True,blank=True)
  objectBuildScorerC = models.CharField(u'勘查員C',max_length=100,null=True,blank=True)
  objectBuildScorRateA=models.DecimalField(u'加成A',default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  objectBuildScorRateB=models.DecimalField(u'加成B',default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  objectBuildScorRateC=models.DecimalField(u'加成C',default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  objectBuildScorReasonA = models.CharField(u'加成原因A',max_length=100,null=True,blank=True)
  objectBuildScorReasonB = models.CharField(u'加成原因B',max_length=100,null=True,blank=True)
  objectBuildScorReasonC = models.CharField(u'加成原因C',max_length=100,null=True,blank=True)
  plusItemA1 = models.CharField(max_length=100,null=True,blank=True)
  plusItemA2 = models.CharField(max_length=100,null=True,blank=True)
  plusItemA3 = models.CharField(max_length=100,null=True,blank=True)
  plusItemA4 = models.CharField(max_length=100,null=True,blank=True)
  plusItemA5 = models.CharField(max_length=100,null=True,blank=True)
  plusItemOtherA = models.CharField(max_length=100,null=True,blank=True)
  plusValueA1 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueA2 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueA3 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueA4 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueA5 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueOtherA = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusItemB1 = models.CharField(max_length=100,null=True,blank=True)
  plusItemB2 = models.CharField(max_length=100,null=True,blank=True)
  plusItemB3 = models.CharField(max_length=100,null=True,blank=True)
  plusItemB4 = models.CharField(max_length=100,null=True,blank=True)
  plusItemB5 = models.CharField(max_length=100,null=True,blank=True)
  plusItemOtherB = models.CharField(max_length=100,null=True,blank=True)
  plusValueB1 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueB2 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueB3 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueB4 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueB5 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueOtherB = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusItemC1 = models.CharField(max_length=100,null=True,blank=True)
  plusItemC2 = models.CharField(max_length=100,null=True,blank=True)
  plusItemC3 = models.CharField(max_length=100,null=True,blank=True)
  plusItemC4 = models.CharField(max_length=100,null=True,blank=True)
  plusItemC5 = models.CharField(max_length=100,null=True,blank=True)
  plusItemOtherC = models.CharField(max_length=100,null=True,blank=True)
  plusValueC1 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueC2 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueC3 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueC4 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueC5 = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
  plusValueOtherC = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)


  def get_objectbuild_ping_price(self):
    newlist=[]
    try:
      return self.objectBuildTotalPrice / (self.objectBuildBuildArea + (self.objectBuildSubBuildArea / 2))
    except:
      newlist.append(0)


  def get_a_plus_value(self):
    newlist=[]
    try:
      return (1 + self.plusValueA1) * (1 + self.plusValueA2) * (1 + self.plusValueA3) * (1 + self.plusValueA4) * (1 + self.plusValueA5) * (1 + self.plusValueOtherA)
    except:
      newlist.append(0)

  def get_b_plus_value(self):
    newlist=[]
    try:
      return (1 + self.plusValueB1) * (1 + self.plusValueB2) * (1 + self.plusValueB3) * (1 + self.plusValueB4) * (1 + self.plusValueB5) * (1 + self.plusValueOtherB)
    except:
      newlist.append(0)

  def get_c_plus_value(self):
    newlist=[]
    try:
      return (1 + self.plusValueC1) * (1 + self.plusValueC2) * (1 + self.plusValueC3) * (1 + self.plusValueC4) * (1 + self.plusValueC5) * (1 + self.plusValueOtherC)
    except:
      newlist.append(0)

  def get_a_plus_value_total(self):
    newlist=[]
    try:
      return self.get_objectbuild_ping_price() * ( 1 + self.plusValueA1) * ( 1 + self.plusValueA2) * ( 1 + self.plusValueA3) * ( 1 + self.plusValueA4) * ( 1 + self.plusValueA5) * ( 1 + self.plusValueOtherA)
    except:
      newlist.append(0)

  def get_b_plus_value_total(self):
    newlist=[]
    try:
      return self.get_objectbuild_ping_price() * ( 1 + self.plusValueB1) * ( 1 + self.plusValueB2) * ( 1 + self.plusValueB3) * ( 1 + self.plusValueB4) * ( 1 + self.plusValueB5) * ( 1 + self.plusValueOtherB)
    except:
      newlist.append(0)

  def get_c_plus_value_total(self):
    newlist=[]
    try:
      return self.get_objectbuild_ping_price() * ( 1 + self.plusValueC1) * ( 1 + self.plusValueC2) * ( 1 + self.plusValueC3) * ( 1 + self.plusValueC4) * ( 1 + self.plusValueC5) * ( 1 + self.plusValueOtherC)
    except:
      newlist.append(0)

  # 當最新一拍底價>=1000000的平均加成(ABC)
  def get_score_plus_abc_rate_average_calculation(self):
    score_rate_average=0
    # A+B+C
    if self.objectBuildScorerA != None and self.objectBuildScorerB != None and self.objectBuildScorerC != None:
      score_rate_average = (self.get_a_plus_value()+self.get_b_plus_value()+self.get_c_plus_value()) / 3
    # A+B+0
    elif self.objectBuildScorerA != None and self.objectBuildScorerB != None :
      score_rate_average = (self.get_a_plus_value()+self.get_b_plus_value()) / 2
    # A+0+C
    elif self.objectBuildScorerA != None and self.objectBuildScorerC != None :
      score_rate_average = (self.get_a_plus_value()+self.get_c_plus_value()) / 2
    # A+0+0
    elif self.objectBuildScorerA != None:
      score_rate_average = self.get_a_plus_value()
    # 0+B+C
    elif self.objectBuildScorerB != None and self.objectBuildScorerC != None :
      score_rate_average = (self.get_b_plus_value()+self.get_c_plus_value()) / 2
    # 0+B+0
    elif self.objectBuildScorerB != None:
      score_rate_average = self.get_b_plus_value()
    # 0+0+C
    elif self.objectBuildScorerC != None:
      score_rate_average = self.get_c_plus_value()
    # 0+0+0
    else:
      score_rate_average = 1
    return score_rate_average

  # 當最新一拍底價<1000000的平均加成(AB)
  def get_score_plus_ab_rate_average_calculation(self):
    score_rate_average=0
    # A+B+0
    if self.objectBuildScorerA != None and self.objectBuildScorerB != None :
      score_rate_average = (self.get_a_plus_value()+self.get_b_plus_value()) / 2
    # A+0+0
    elif self.objectBuildScorerA != None:
      score_rate_average = self.get_a_plus_value()
    # 0+B+0
    elif self.objectBuildScorerB != None:
      score_rate_average = self.get_b_plus_value()
    # 0+0+0
    else:
      score_rate_average = 1
    return score_rate_average

  # 當最新一拍底價>=1000000的計算(ABC)
  def get_objectbuild_ping_price_abc_calculation(self):
    newlist=[]
    try:
      return self.get_score_plus_abc_rate_average_calculation() * self.get_objectbuild_ping_price()
    except:
      newlist.append(0)

  # 當最新一拍底價<1000000的計算(AB)
  def get_objectbuild_ping_price_ab_calculation(self):
    newlist=[]
    try:
      return self.get_score_plus_ab_rate_average_calculation() * self.get_objectbuild_ping_price()
    except:
      newlist.append(0)

  
# ======= FinalDecision =======
class FinalDecision(models.Model):
  yfcase=models.ForeignKey(Yfcase,related_name='finaldecisions',on_delete=models.CASCADE)
  finalDecision = models.CharField(u'最終判定',max_length=10,null=True,blank=True)
  finalDecisionRemark = models.CharField(u'備註',max_length=3000,null=True,blank=True)
  regionalHead = models.CharField(u'區域負責人',max_length=10,null=True,blank=True)
  regionalHeadDate = models.CharField(u'區域負責人簽核日期',max_length=10,null=True,blank=True)
  regionalHeadAddDate = models.DateTimeField(u'區域負責人存檔日期',default = timezone.now)
  regionalHeadWorkArea = models.CharField(u'區域負責人轄區',max_length=10,null=True,blank=True)
  subSigntrueA = models.CharField(u'副署人員A',max_length=10,null=True,blank=True)
  subSigntrueDateA = models.CharField(u'副署日期A',max_length=10,null=True,blank=True)
  subSigntrueWorkAreaA = models.CharField(u'副署轄區A',max_length=10,null=True,blank=True)
  subSigntrueB = models.CharField(u'副署人員B',max_length=10,null=True,blank=True)
  subSigntrueDateB = models.CharField(u'副署日期B',max_length=10,null=True,blank=True)
  subSigntrueWorkAreaB = models.CharField(u'副署轄區B',max_length=10,null=True,blank=True)

  def __str__(self):
    return self.finalDecision

  def other_day_to_today(self):
    # 取得目前的日期，要用form dateteim import datetime,不可用import datetime
    today = datetime.now()
    # 取得要計算的日期，要用form dateteim import datetime,不可用import datetime
    other_day = datetime.strptime(self.regionalHeadAddDate,'%m/%d/%Y')
    result = other_day - today
    return str(result.days)

# ======= Result =======
class Result(models.Model):
  yfcase = models.ForeignKey(Yfcase,related_name='results',on_delete=models.CASCADE)
  stopBuyDate = models.CharField(u'應買止日',max_length=20,null=True,blank=True)
  actionResult = models.CharField(u'執行結果',max_length=20,null=True,blank=True)
  bidAuctionTime = models.CharField(u'搶標拍別',max_length=20,null=True,blank=True)
  bidMoney = models.DecimalField(u'搶標金額',default=0,max_digits=10,decimal_places=0,null=True,blank=True)
  objectNumber = models.CharField(u'標的編號',max_length=20,null=True,blank=True)
