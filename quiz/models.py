
from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.name)


class Question(models.Model):
    tags = models.ManyToManyField(Tag)
    ques = models.TextField()
    summary = models.TextField(blank=True, null=True)
    weightage = models.PositiveIntegerField()
    negative_marks = models.IntegerField(blank=True, null=True)
    option1 = models.CharField(max_length=10000,)
    option2 = models.CharField(max_length=10000, blank=True, null=True)
    option3 = models.CharField(max_length=10000, blank=True, null=True)
    option4 = models.CharField(max_length=10000, blank=True, null=True)
    # choices = (
    #     (option1, 'option 1'),
    #     (option2, 'option 2'),
    #     (option3, 'option 3'),
    #     (option4, 'option 4'),
    # )
    correct_answer = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return str(self.ques)


class Test(models.Model):
    tags = models.ManyToManyField(Tag)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    instructions = models.TextField()
    total_ques = models.PositiveIntegerField(blank=True, null=True)
    duration = models.DurationField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return str(self.course) + str(self.name)

    # def get_max_marks(self):
    #     max_marks = 0
    #     for question in self.questions:
    #         max_marks += question.weightage
    #     return max_marks


class UserTest(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.test) + str(self.user)


class Submission(models.Model):
    test = models.ForeignKey(UserTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
    choices = (
        ('Wrong', 'Wrong'),
        ('Correct', 'Correct'),
    )
    status = models.CharField(choices=choices,max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.test) + str(self.question)
