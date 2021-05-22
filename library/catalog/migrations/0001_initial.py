# Generated by Django 3.0 on 2021-05-20 15:42

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('genres', djongo.models.fields.JSONField(default=[])),
                ('authors', djongo.models.fields.JSONField(default=[])),
                ('rating', models.FloatField(default=2.5)),
                ('years', djongo.models.fields.JSONField(default=[], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='MongoUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
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
                ('preference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Preference')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
