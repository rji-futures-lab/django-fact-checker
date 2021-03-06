# Generated by Django 2.0.3 on 2018-04-05 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factchecker', '0011_auto_20180401_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='submitter',
            field=models.ForeignKey(blank=True, help_text='Refers to the person who submitted the claim.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claims_submitted', to='factchecker.ClaimSubmitter'),
        ),
    ]
