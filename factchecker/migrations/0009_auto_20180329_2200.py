# Generated by Django 2.0.3 on 2018-03-29 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factchecker', '0008_auto_20180328_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='claim',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='last_modified_at',
        ),
        migrations.RemoveField(
            model_name='claim',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='claimrating',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='claimrating',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='claimrating',
            name='last_modified_at',
        ),
        migrations.RemoveField(
            model_name='claimrating',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='claimreview',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='claimreview',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='claimreview',
            name='last_modified_at',
        ),
        migrations.RemoveField(
            model_name='claimreview',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='claimsource',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='claimsource',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='claimsource',
            name='last_modified_at',
        ),
        migrations.RemoveField(
            model_name='claimsource',
            name='last_modified_by',
        ),
    ]