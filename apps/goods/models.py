from django.db import models

from db.base_model import BaseModel

from tinymce.models import HTMLField

#商品种类模型类
class GoodsType(BaseModel):
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20,verbose_name='标识')
    image = models.ImageField(upload_to='type',verbose_name='商品类型图片')
    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#商品SKU模型类

class GoodsSKU(BaseModel):
    #状态选择
    status_chices = (
        (0,'下线'),
        (0, '上线')

    )
    #商品种类的外键
    type = models.ForeignKey('GoodsType',verbose_name='商品种类')
    #商品SPU类型的外键
    goods = models.ForeignKey('Goods',verbose_name='商品SPU')
    name = models.CharField(max_length=20,verbose_name='商品的名称')
    desc = models.CharField(max_length=256,verbose_name='商品的简介')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品的价格')
    unite = models.CharField(max_length=20,verbose_name='商品单位')
    image = models.ImageField(upload_to='goods',verbose_name='商品的图片')
    stock = models.IntegerField(default=1,verbose_name='商品的库存')
    sales = models.IntegerField(default=0,verbose_name='商品的销量')
    status = models.SmallIntegerField(default=1,choices=status_chices,verbose_name='商品的状态')


    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


#商品SPU模型类
class Goods(BaseModel):
    name = models.CharField(max_length=20,verbose_name='商品spu名称')
    detail = HTMLField(blank=True,verbose_name='商品的详情')

    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品spu'
        verbose_name_plural = verbose_name


#商品图片模型类
class GoodsImage(BaseModel):
    sku = models.ForeignKey('GoodsSKU',verbose_name='商品')
    image = models.ImageField(upload_to='goods',verbose_name='图片的路径')
    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


#首页轮播商品展示模型类
class IndexGoodsBanner(BaseModel):

    sku = models.ForeignKey('GoodsSKU',verbose_name='商品')
    image = models.ImageField(upload_to='banner',verbose_name='图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示的顺序')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name


#首页分类商品展示
class IndexTypeGoodsBanner(BaseModel):
    DISPLAY_TYPE_CHOICES = (
        (0,'标题'),
        (1, '图片')
    )

    type = models.ForeignKey('GoodsType',verbose_name='商品的类型')
    sku = models.ForeignKey('GoodsSKU',verbose_name='商品sku')
    display_type = models.SmallIntegerField(default=1,choices=DISPLAY_TYPE_CHOICES,verbose_name='展示的类型')
    index = models.SmallIntegerField(default=0,verbose_name='展示顺序')


    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name='主页分类商品展示'
        verbose_name_plural = verbose_name
#首页促销活动模型类
class IndexPromotionBanner(BaseModel):
    name = models.CharField(max_length=20,verbose_name='活动名称')
    url = models.URLField(verbose_name='活动连接')
    image = models.ImageField(upload_to='banner',verbose_name='活动的图片')
    index = models.SmallIntegerField(default=0,verbose_name='展示的顺序')

    class Meta:
        db_table = 'df_index_promtion'
        verbose_name = '主页促销活动'
        verbose_name_plural = verbose_name







