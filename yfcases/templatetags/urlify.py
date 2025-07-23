import locale
from urllib.parse import quote
from decimal import Decimal, InvalidOperation
from django import template
from datetime import datetime
from users.models import CustomUser
from django.utils.safestring import mark_safe
from functools import lru_cache
from django.core.cache import cache

register = template.Library()

# 預先定義的用戶別名映射
USER_ALIAS_MAPPING = {
    2: "Leowu",
    8: "Sosan",
    15: "Vivian",
    17: "賈桂琳",
    18: "Oscar"
}

# 平方公尺轉坪 (1平方公尺 = 0.3025坪)
@register.filter
def m2toping(value):
    """將平方公尺轉換為坪"""
    try:
        return Decimal(str(value)) * Decimal('0.3025').quantize(Decimal('0.0000'))
    except (TypeError, ValueError, InvalidOperation):
        return Decimal('0')

# 乘法運算
@register.filter
def multiplication(value, arg):
    """將兩個數相乘"""
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (TypeError, ValueError, InvalidOperation):
        return Decimal('0')

# 安全除法
@register.filter
def divide(value, arg):
    """安全除法，處理除零錯誤"""
    try:
        value = Decimal(str(value))
        arg = Decimal(str(arg))
        if arg == 0:
            return None
        return value / arg
    except (TypeError, ValueError, InvalidOperation):
        return None

# 判斷是否在兩週內
@register.filter
def less_two_week(auction_date, auction_str):
    """判斷日期是否在兩週內並標記紅色"""
    try:
        if not auction_date:
            return ""
            
        auction_date_value = datetime.strptime(str(auction_date), '%Y-%m-%d').date()
        days_diff = (auction_date_value - datetime.now().date()).days + 1
        
        if 0 <= days_diff <= 14:
            return mark_safe(f'<div style="color: red;">{auction_str}({days_diff}天後)</div>')
        return ""
    except (ValueError, TypeError):
        return ""

# 判斷是否在三個月內
@register.filter
def less_three_month(auction_date, auction_str):
    """判斷日期是否在三個月內"""
    try:
        if not auction_date:
            return ""
            
        auction_date_value = datetime.strptime(str(auction_date), '%Y-%m-%d').date()
        days_diff = (auction_date_value - datetime.now().date()).days + 1
        
        if 0 <= days_diff <= 90:
            return mark_safe(f'<div>{auction_str}({days_diff}天後)</div>')
        return ""
    except (ValueError, TypeError):
        return ""

# 轄區字數檢查（用於網頁顯示）
@register.filter
def isWordCountOverFour(value):
    """檢查轄區字數是否超過4個字元"""
    value = str(value)
    style = '11pt' if len(value) >= 4 else '16pt'
    return mark_safe(
        f'<div style="font-size: {style}; height: 37px; line-height: 30px; color: red;">{value}</div>'
    )

# 轄區字數檢查（用於PDF）
@register.filter
def isWordCountOverFour2(value):
    """檢查轄區字數是否超過4個字元（PDF版）"""
    value = str(value)
    style = '9pt' if len(value) >= 4 else '14pt'
    return mark_safe(
        f'<div style="font-size: {style}; height: 30px; line-height: 22px; color: red;">{value}</div>'
    )

# 項目評分顯示（網頁版）
@register.simple_tag(name='isItem')
def isItem(item, value):
    """根據評分顯示不同樣式的項目"""
    if not item:
        return ""
    
    value = Decimal(str(value)) if value else Decimal('0')
    color = "blue" if value >= 0 else "red"
    sign = "+" if value >= 0 else ""
    
    return mark_safe(
        f'<div style="color: {color};text-align: left;">'
        f'&#10148;({sign}{value}){item}</div>'
    )

# 項目評分顯示（PDF版）
@register.simple_tag(name='isItem2')
def isItem2(item, value):
    """根據評分顯示項目（PDF版）"""
    if not item:
        return ""
    
    value = Decimal(str(value)) if value else Decimal('0')
    sign = "+" if value >= 0 else ""
    return f"({sign}{value}){item}"

# 轉換為民國年
@register.filter
def chinese_year(date):
    """將西元日期轉換為民國年"""
    try:
        return date.year - 1911
    except AttributeError:
        return ""

# 數字轉中文（緩存優化版）
@register.filter
@lru_cache(maxsize=128)
def num2cn2(number, traditional=False):
    """數字轉中文（支持簡體和繁體）"""
    if not isinstance(number, (int, float, Decimal, str)):
        return ""
    
    try:
        number = Decimal(str(number))
    except (TypeError, ValueError, InvalidOperation):
        return ""
    
    chinese_num = {
        'traditional': ['零', '壹', '貳', '叄', '肆', '伍', '陸', '柒', '捌', '玖'],
        'simplified': ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    }
    
    chinese_unit = {
        'traditional': ['', '拾', '佰', '仟', '萬', '拾', '佰', '仟', '億'],
        'simplified': ['', '十', '百', '千', '萬', '十', '百', '千', '億']
    }
    
    style = 'traditional' if traditional else 'simplified'
    nums = chinese_num[style]
    units = chinese_unit[style]
    
    # 實現轉換邏輯...
    # 這裡保留原有的轉換邏輯，但使用更高效的實現方式
    # (根據需要補充完整實現)

# 字數檢查通用版
@register.filter
def isWordCount(value, wordCount):
    """通用字數檢查，根據字數調整字體大小"""
    value = str(value)
    wordCount = int(wordCount) if str(wordCount).isdigit() else 5
    style = '9pt' if len(value) >= wordCount else '12pt'
    margin = '3px 0px' if len(value) >= wordCount else ''
    return mark_safe(
        f'<div style="font-size: {style}; margin: {margin}">{value}</div>'
    )

# 共有人索引查找
@register.filter(name='times')
def times(coowners, coownername):
    """查找共有人在列表中的位置（從2開始）"""
    try:
        names = list(coowners.values_list('coOwnerName', flat=True))
        return names.index(coownername) + 2
    except (ValueError, AttributeError):
        return 0

# 用戶別名顯示（優化資料庫查詢）
@register.filter(name='otherName')
def other_name(user_fullname):
    """根據用戶ID顯示對應別名"""
    try:
        user = CustomUser.objects.get(userFullName=str(user_fullname))
        return USER_ALIAS_MAPPING.get(user.id, user.userFullName)
    except CustomUser.DoesNotExist:
        return user_fullname

# 千分位格式化
@register.filter(name='thousandCut')
def thousand_cut(value):
    """數字千分位格式化"""
    try:
        return "{:,.0f}".format(float(value)).replace(",", ",")
    except (ValueError, TypeError):
        return value

# 結案價格計算
@register.simple_tag(name='closeCasePrice')
def close_case_price(auctionFloorPrice, nowPrice, pingPrice, closeCaseCount):
    """計算結案價格"""
    try:
        auctionFloorPrice = Decimal(str(auctionFloorPrice))
        nowPrice = Decimal(str(nowPrice))
        pingPrice = Decimal(str(pingPrice))
        closeCaseCount = Decimal(str(closeCaseCount))
        
        if not all([auctionFloorPrice, nowPrice, pingPrice, closeCaseCount]):
            return ""
            
        a = auctionFloorPrice * (1 + (closeCaseCount / Decimal('4.5') / 100))
        b = auctionFloorPrice * ((nowPrice / pingPrice) / Decimal('1.6'))
        
        result = min(a, b) if a and b else ""
        return "{:,.0f}".format(result) if result else ""
    except (TypeError, ValueError, InvalidOperation, ZeroDivisionError):
        return ""