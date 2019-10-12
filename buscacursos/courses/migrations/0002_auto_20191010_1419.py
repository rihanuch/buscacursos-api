# Generated by Django 2.2.6 on 2019-10-10 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.IntegerField()),
                ('nrc', models.IntegerField(unique=True)),
                ('retiro', models.BooleanField(default=True)),
                ('ingles', models.BooleanField(default=False)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Campus')),
                ('profesores', models.ManyToManyField(to='courses.Profesor')),
                ('ramo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secciones', to='courses.Ramo')),
                ('semestre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Semestre')),
            ],
            options={
                'unique_together': {('ramo', 'seccion', 'semestre')},
            },
        ),
        migrations.DeleteModel(
            name='SeccionRamo',
        ),
    ]