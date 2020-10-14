from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
Weekdays_Choices = (
    ('M', 'Monday'),
    ('Tu', 'Tuesday'),
    ('W', 'Wednesday'),
    ('Th', 'Thursday'),
    ('F', 'Friday'),
    ('Sa', 'Saturday'),
    ('Su', 'Sunday'),
)
class User(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_owner = models.BooleanField(default=False)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class ammenities(models.Model):
    title = models.CharField(max_length=50)
    quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Ammenities'


class payment_methods(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Payment Methods'


class weekday(models.Model):
    day = models.CharField(max_length=20)

    def __str__(self):
        return self.day

    class Meta:
        verbose_name_plural = 'Weekdays'


refund_policy_choices = (
    ('Yes', "Yes"),
    ('No', 'No'),
)
class library(models.Model):
    name = models.CharField(max_length=50)
    location = models.PointField(srid=4326, geography=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    owner_fname = models.CharField(max_length=50)
    owner_lname = models.CharField(max_length=50)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15)

    addr1 = models.CharField(max_length=50)
    addr2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    state = models.CharField(max_length=50)

    landline = models.CharField(max_length=12, blank=True, null=True)

    amenities = models.ManyToManyField(ammenities, blank=True)
    library_description = models.TextField(max_length=500)
    past_record_of_students = models.TextField(max_length=500, blank=True, null=True)
    payment_methods = models.ManyToManyField(payment_methods)
    fb_url = models.CharField(max_length=200, blank=True, null=True)
    insta = models.CharField(max_length=100, blank=True, null=True)
    google_map = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    main_image = models.ImageField()

    no_of_seats = models.PositiveSmallIntegerField()
    opening_days = models.ManyToManyField(weekday)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    non_refundable_charges = models.PositiveSmallIntegerField(blank=True, null=True)
    refund_policy = models.CharField(max_length=3, choices=refund_policy_choices)
    min_price_range = models.PositiveSmallIntegerField(blank=True, null=True)
    max_price_range = models.PositiveSmallIntegerField(blank=True, null=True)

    verified = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    views = models.PositiveSmallIntegerField(default=0)
    rejected = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Libraries'

    def get_images(self):
        images = library_images.objects.filter(library=self)
        return images

    def get_rating(self):
        ratings = library_ratings.objects.filter(library=self)

        if ratings.exists():
            total_rating = 0
            total = 0
            for rating_qs in ratings:
                total += 1
                total_rating += rating_qs.rating
            avg = total_rating/total
            return str(avg)
        else:
            return ''

class library_images(models.Model):
    image = models.ImageField()
    library = models.ForeignKey('core.library', on_delete=models.CASCADE)

    def __str__(self):
        return self.library.name

    class Meta:
        verbose_name_plural = 'Library Images'


class library_videos(models.Model):
    video = models.FileField()
    youtube_url = models.CharField(max_length=250)
    library = models.ForeignKey('core.library', on_delete=models.CASCADE)

    def __str__(self):
        return self.library.name

    class Meta:
        verbose_name_plural = 'Library Videos'


class library_ratings(models.Model):
    library = models.ForeignKey('core.library', on_delete=models.PROTECT)
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.library)


class bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    libraries = models.ManyToManyField('core.library')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Bookmarks'


class comparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    libraries = models.ManyToManyField('core.library')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Comparison of Libraries'

    '''

    name, owner_first_name, owner_last_name, addr_line1, addr_line2, area, zipcode, state, email, mobile_no, landline, no_of_seats, opening_time, closing_time, ammenities, library_description, image_1, image_2, image_3, image_4, more_images, payment_methods, verified
    '''


class testimonial(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Testimonials'


class enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_no = models.CharField(max_length=12)
    preferred_joining_date = models.DateField()
    preferred_time_slot = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Enquiries'


class newsletter(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Newsletter Subscribers'


class bug_report(models.Model):
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=12)
    email = models.EmailField()
    issue = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Bug Reports'


class faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'FAQ'

    def get_short_content(self):
        if len(self.answer) > 500:
            content = self.answer[:500]
            return content
        else:
            return self.answer

    def if_short_content(self):
        if len(self.answer) > 500:
            return 'True'
        else:
            return False


class TermsAndConditions(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'Terms And Conditions'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Contact Us Form'


#
# class library(models.Model):
#     location = models.PointField(srid=4326,  geography=True)
#     name = models.CharField(max_length=100)