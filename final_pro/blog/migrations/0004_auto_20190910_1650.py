# Generated by Django 2.2.2 on 2019-09-10 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_content_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_time',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_time',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
    ]