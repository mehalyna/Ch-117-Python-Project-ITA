# Generated by Django 3.0 on 2021-05-30 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MongoUser',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(default='user', max_length=10)),
                ('status', models.CharField(default='active', max_length=10)),
                ('reviews', djongo.models.fields.JSONField(default=[])),
                ('recommended_books', djongo.models.fields.JSONField(default=[])),
                ('wishlist', djongo.models.fields.JSONField(default=[])),
                ('rated_books', djongo.models.fields.JSONField(default={})),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('birthdate', models.CharField(default='', max_length=15)),
                ('death_date', models.CharField(default='', max_length=15)),
                ('status', models.CharField(default='active', max_length=50)),
                ('books', djongo.models.fields.JSONField(default=[])),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=100)),
                ('year', models.CharField(default='', max_length=20)),
                ('publisher', models.CharField(default='', max_length=200)),
                ('language', models.CharField(default='', max_length=20)),
                ('description', models.CharField(default='', max_length=10000)),
                ('link_img', models.CharField(default='', max_length=1000)),
                ('pages', models.IntegerField(default=1)),
                ('genres', djongo.models.fields.JSONField(default=[])),
                ('status', models.CharField(default='active', max_length=100)),
                ('store_links', djongo.models.fields.JSONField(default=[])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Author')),
            ],
        ),
        migrations.CreateModel(
            name='BookStatistic',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('rating', models.FloatField(default=2.5)),
                ('total_read', models.IntegerField(default=0)),
                ('reading_now', models.IntegerField(default=0)),
                ('stars', djongo.models.fields.JSONField(default=[0, 0, 0, 0, 0])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(verbose_name=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('firstname', models.CharField(default='', max_length=50)),
                ('lastname', models.CharField(default='', max_length=50)),
                ('status', models.CharField(default='active', max_length=10)),
                ('comment', models.CharField(default='', max_length=5000)),
                ('date', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='statistic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.BookStatistic'),
        ),
    ]
