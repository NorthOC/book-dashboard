# Generated by Django 4.2.3 on 2023-08-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_book_pagecount_book_pubdate_alter_book_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pubdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]