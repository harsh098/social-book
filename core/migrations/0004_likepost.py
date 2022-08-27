# Generated by Django 3.2.5 on 2022-08-19 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
                ('post_object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
            ],
        ),
    ]