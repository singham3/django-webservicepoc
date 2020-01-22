# Generated by Django 2.2.5 on 2019-11-12 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogoFavIconsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('field_type', models.CharField(max_length=200)),
                ('manager', models.CharField(max_length=200)),
                ('favlogo_value', models.CharField(default='1_favlogo_value', max_length=200, unique=True)),
                ('config_value_file', models.FileField(upload_to='LogoFav/')),
                ('createdat', models.DateTimeField(auto_now_add=True)),
                ('updatedat', models.DateTimeField(auto_now_add=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
