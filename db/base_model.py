from django.db import models

#定义模型抽象的基类，（只定义，不实力对象，在子类里实力对象）

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add= True,verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    is_delete = models.BooleanField(default=False,verbose_name='删除标记')

    class Meta:
        #说明是一个抽象的模型类
        abstract = True
