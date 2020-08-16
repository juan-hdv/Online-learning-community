# Generated by Django 3.0.8 on 2020-08-02 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='provider',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='courses.CourseProvider'),
        ),
    ]