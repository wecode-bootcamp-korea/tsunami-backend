# Generated by Django 3.1.5 on 2021-01-15 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productoption_name'),
        ('users', '0002_auto_20210114_0612'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='user',
            name='user_product_likes',
            field=models.ManyToManyField(through='users.UserProductLike', to='products.Product'),
        ),
    ]
