# Generated by Django 3.0.8 on 2020-08-02 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20200802_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='provider',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='courses.CourseProvider'),
        ),
        migrations.AlterField(
            model_name='coursecategory',
            name='courses',
            field=models.ManyToManyField(null=True, related_name='categories', to='courses.Course'),
        ),
    ]
