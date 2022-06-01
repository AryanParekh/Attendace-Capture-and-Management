# Generated by Django 3.1.5 on 2022-06-01 02:59

import att_man.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('starting_year', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('ending_year', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('b_id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('COMPS', 'Computer'), ('IT', 'Information Technology'), ('EXTC', 'Electronics & Telecommunication'), ('MECH', 'Mechanical'), ('BIO', 'Biomedical'), ('ELEX', 'Electronics'), ('CHEM', 'Chemical')], max_length=5)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='att_man.batch')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_number', models.CharField(max_length=4)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='att_man.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=200)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='att_man.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('sap_id', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=att_man.models.get_upload_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='att_man.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_no', models.CharField(max_length=4)),
                ('teacher_name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('starting_time', models.TimeField()),
                ('ending_time', models.TimeField()),
                ('topic', models.CharField(blank=True, max_length=150, null=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='att_man.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('attended', models.BooleanField(default=False)),
                ('lecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='att_man.lecture')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='att_man.student')),
            ],
        ),
    ]
