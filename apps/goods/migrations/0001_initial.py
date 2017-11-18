# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(verbose_name='商品spu名称', max_length=20)),
                ('detail', tinymce.models.HTMLField(blank=True, verbose_name='商品的详情')),
            ],
            options={
                'verbose_name': '商品spu',
                'verbose_name_plural': '商品spu',
                'db_table': 'df_goods',
            },
        ),
        migrations.CreateModel(
            name='GoodsImage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('image', models.ImageField(upload_to='goods', verbose_name='图片的路径')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'db_table': 'df_goods_image',
            },
        ),
        migrations.CreateModel(
            name='GoodsSKU',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(verbose_name='商品的名称', max_length=20)),
                ('desc', models.CharField(verbose_name='商品的简介', max_length=256)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品的价格')),
                ('unite', models.CharField(verbose_name='商品单位', max_length=20)),
                ('image', models.ImageField(upload_to='goods', verbose_name='商品的图片')),
                ('stock', models.IntegerField(default=1, verbose_name='商品的库存')),
                ('sales', models.IntegerField(default=0, verbose_name='商品的销量')),
                ('status', models.SmallIntegerField(default=1, verbose_name='商品的状态', choices=[(0, '下线'), (0, '上线')])),
                ('goods', models.ForeignKey(verbose_name='商品SPU', to='goods.Goods')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'db_table': 'df_goods_sku',
            },
        ),
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(verbose_name='种类名称', max_length=20)),
                ('logo', models.CharField(verbose_name='标识', max_length=20)),
                ('image', models.ImageField(upload_to='type', verbose_name='商品类型图片')),
            ],
            options={
                'verbose_name': '商品种类',
                'verbose_name_plural': '商品种类',
                'db_table': 'df_goods_type',
            },
        ),
        migrations.CreateModel(
            name='IndexGoodsBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('image', models.ImageField(upload_to='banner', verbose_name='图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示的顺序')),
                ('sku', models.ForeignKey(verbose_name='商品', to='goods.GoodsSKU')),
            ],
            options={
                'verbose_name': '首页轮播商品',
                'verbose_name_plural': '首页轮播商品',
                'db_table': 'df_index_banner',
            },
        ),
        migrations.CreateModel(
            name='IndexPromotionBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(verbose_name='活动名称', max_length=20)),
                ('url', models.URLField(verbose_name='活动连接')),
                ('image', models.ImageField(upload_to='banner', verbose_name='活动的图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示的顺序')),
            ],
            options={
                'verbose_name': '主页促销活动',
                'verbose_name_plural': '主页促销活动',
                'db_table': 'df_index_promtion',
            },
        ),
        migrations.CreateModel(
            name='IndexTypeGoodsBanner',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('display_type', models.SmallIntegerField(default=1, verbose_name='展示的类型', choices=[(0, '标题'), (1, '图片')])),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('sku', models.ForeignKey(verbose_name='商品sku', to='goods.GoodsSKU')),
                ('type', models.ForeignKey(verbose_name='商品的类型', to='goods.GoodsType')),
            ],
            options={
                'verbose_name': '主页分类商品展示',
                'verbose_name_plural': '主页分类商品展示',
                'db_table': 'df_index_type_goods',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(verbose_name='商品种类', to='goods.GoodsType'),
        ),
        migrations.AddField(
            model_name='goodsimage',
            name='sku',
            field=models.ForeignKey(verbose_name='商品', to='goods.GoodsSKU'),
        ),
    ]
