# Generated by Django 3.2.5 on 2022-08-19 09:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_likepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='post_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post'),
        ),
        migrations.AddConstraint(
            model_name='likepost',
            constraint=models.UniqueConstraint(fields=('like_usr', 'post_object'), name='likes_constraint'),
        ),
    ]
