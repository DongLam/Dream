# Generated by Django 3.2.9 on 2021-11-25 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0003_alter_match_datetimestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['team1']},
        ),
        migrations.AddField(
            model_name='match',
            name='team1_tmp',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='match',
            name='team2_tmp',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]