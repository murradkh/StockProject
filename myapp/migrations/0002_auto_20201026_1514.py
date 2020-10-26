# Generated by Django 3.1.1 on 2020-10-26 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='primaryExchange',
        ),
        migrations.AddField(
            model_name='stock',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='primary_exchange',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='change',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='change_percent',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='market_cap',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='top_rank',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watchlist', models.ManyToManyField(blank=True, to='myapp.Stock')),
            ],
        ),
    ]
