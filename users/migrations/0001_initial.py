# Generated by Django 3.1.5 on 2021-01-12 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=60, unique=True)),
                ('phone_number', models.CharField(max_length=11, unique=True)),
                ('birthday', models.CharField(max_length=12, null=True)),
                ('is_sms_agreed', models.BooleanField()),
                ('is_email_agreed', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=11)),
                ('is_default', models.BooleanField()),
                ('zipcode', models.CharField(max_length=5)),
                ('street_name', models.CharField(max_length=100)),
                ('detail_address', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'destinations',
            },
        ),
        migrations.CreateModel(
            name='UserProductLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'user_product_likes',
            },
        ),
    ]