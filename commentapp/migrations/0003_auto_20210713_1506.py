# Generated by Django 3.2.4 on 2021-07-13 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commentapp', '0002_auto_20210706_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_level_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_comment_level_1', to='commentapp.comment', verbose_name='родитель первого уровня'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_comment_to', to='commentapp.comment', verbose_name='родитель'),
        ),
    ]
