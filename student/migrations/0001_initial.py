# Generated by Django 2.1.5 on 2024-03-05 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lecturer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseFeedback',
            fields=[
                ('feedbackId', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('overall', models.IntegerField()),
                ('difficulty', models.IntegerField()),
                ('usefulness', models.IntegerField()),
                ('workload', models.IntegerField()),
                ('examFormat', models.CharField(max_length=50)),
                ('evaluationMethod', models.CharField(max_length=250)),
                ('lecturerRating', models.IntegerField()),
                ('gradeReceived', models.CharField(max_length=2)),
                ('recommendCourse', models.BooleanField()),
                ('textFeedback', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('reported', models.IntegerField(default=0)),
                ('approved', models.BooleanField(default=True)),
                ('feedbackDateTime', models.DateTimeField(auto_now_add=True)),
                ('courseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturer.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('guid', models.CharField(max_length=7, primary_key=True, serialize=False, unique=True)),
                ('email', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('password', models.TextField()),
                ('programType', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='StudentFeedbackLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedbackId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.CourseFeedback')),
                ('guid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.AddField(
            model_name='coursefeedback',
            name='guid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
    ]
