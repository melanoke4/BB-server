# Generated by Django 4.1.3 on 2024-09-13 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bottomlessboxapi', '0005_alter_user_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='lore',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_lore', to='bottomlessboxapi.lore'),
        ),
        migrations.AddField(
            model_name='item',
            name='review',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_review', to='bottomlessboxapi.review'),
        ),
        migrations.AlterField(
            model_name='lore',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lore_item', to='bottomlessboxapi.item'),
        ),
        migrations.AlterField(
            model_name='review',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_item', to='bottomlessboxapi.item'),
        ),
    ]
