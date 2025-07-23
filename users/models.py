from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
  userFirstName=models.CharField(u'姓氏',max_length=50,null=True,blank=True)
  userLastName=models.CharField(u'名字',max_length=50,null=True,blank=True)
  userFullName=models.CharField(u'全名',max_length=50,null=True,blank=True)
  userWorkArea=models.CharField(u'工作轄區',max_length=50,null=True,blank=True)
  userRole=models.PositiveIntegerField(u'權限',default=0)
  userIdentityCard=models.CharField(u'身分証號',max_length=50,null=True,blank=True)
  userBirthday=models.DateField(u'生日',null=True,blank=True)
  userLocalPhone=models.CharField(u'市話',max_length=50,null=True,blank=True)
  userMobilePhone=models.CharField(u'手機',max_length=50,null=True,blank=True)
  userCountry=models.CharField(u'縣市',max_length=50,null=True,blank=True)
  userTownship=models.CharField(u'鄉鎮',max_length=50,null=True,blank=True)
  userVillage=models.CharField(u'村里',max_length=50,null=True,blank=True)
  userNeighbor=models.CharField(u'鄰',max_length=50,null=True,blank=True)
  userStreet=models.CharField(u'街路',max_length=50,null=True,blank=True)
  userSection=models.CharField(u'段',max_length=50,null=True,blank=True)
  userLane=models.CharField(u'巷',max_length=50,null=True,blank=True)
  userAlley=models.CharField(u'弄',max_length=50,null=True,blank=True)
  userNumber=models.CharField(u'號',max_length=50,null=True,blank=True)
  userFloor=models.CharField(u'樓',max_length=50,null=True,blank=True)
  userPublicOrPrivate=models.CharField(u'身分別',max_length=50,null=True,blank=True)
  
  def __str__(self):
    # 要寫成str(self.userFullName)要不然在/admin執行時會出現"__str__ returned non-string (type NoneType)"
    return str(self.userFullName)
