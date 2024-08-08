# Generated by Django 5.0.7 on 2024-08-08 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_review_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='books.book'),
        ),
    ]
