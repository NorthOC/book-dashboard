# Generated by Django 4.2.3 on 2023-08-05 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_book_created_alter_book_pubdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pubdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
