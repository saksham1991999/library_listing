# Generated by Django 2.2 on 2020-04-15 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques', models.TextField()),
                ('summary', models.TextField(blank=True, null=True)),
                ('weightage', models.PositiveIntegerField()),
                ('negative_marks', models.IntegerField(blank=True, null=True)),
                ('option1', models.CharField(max_length=10000)),
                ('option2', models.CharField(blank=True, max_length=10000, null=True)),
                ('option3', models.CharField(blank=True, max_length=10000, null=True)),
                ('option4', models.CharField(blank=True, max_length=10000, null=True)),
                ('correct_answer', models.CharField(blank=True, max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('instructions', models.TextField()),
                ('total_ques', models.PositiveIntegerField(blank=True, null=True)),
                ('duration', models.DurationField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Course')),
                ('questions', models.ManyToManyField(to='quiz.Question')),
                ('tags', models.ManyToManyField(to='quiz.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1000)),
                ('status', models.CharField(blank=True, choices=[('Wrong', 'Wrong'), ('Correct', 'Correct')], max_length=1000, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Question')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.UserTest')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='quiz.Tag'),
        ),
    ]