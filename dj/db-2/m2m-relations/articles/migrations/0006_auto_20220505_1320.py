# Generated by Django 3.1.2 on 2022-05-05 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20220505_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articletag',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_link', to='articles.article'),
        ),
        migrations.AlterField(
            model_name='articletag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_link', to='articles.tag'),
        ),
    ]
