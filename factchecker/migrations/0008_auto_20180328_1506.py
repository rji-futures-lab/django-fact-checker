# Generated by Django 2.0.3 on 2018-03-28 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factchecker', '0007_auto_20180319_2209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='claimrating',
            options={'ordering': ['sort_order'], 'verbose_name': 'rating'},
        ),
        migrations.AddField(
            model_name='claimrating',
            name='sort_order',
            field=models.IntegerField(default=0, help_text='Order in which this item appears.'),
        ),
        migrations.AlterField(
            model_name='claimrating',
            name='image',
            field=models.ImageField(blank=True, help_text='Image file representing the rating of a claim.', upload_to='claim-rating-images/'),
        ),
        migrations.AlterField(
            model_name='claimsource',
            name='image',
            field=models.ImageField(blank=True, help_text='Image file representing the source.', upload_to='claim-source-images/'),
        ),
    ]