from django.db import models
from django.core.validators import RegexValidator
from django.core.files import File
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.urls import reverse
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw



# import uuid

# Create your models here.

# new_uuid = uuid.uuid4()

#Strands:
ABM = 'ABM'
GAS = 'GAS'
HUMSS = 'HUMSS'
STEM = 'STEM'
TVL = 'TVL'


STRAND = (
    (ABM, "Accountancy Business Management"),
    (GAS, "General Academics Strand"),
    (HUMSS, "Humanities and Social Sciences"),
    (STEM, "Science Technology Engineering and Mathematics"),
    (TVL, "Technical Vocational Livelihood"),

)

#Grade Level:

grade_11 = '11'
grade_12 = '12'

grade_level = (
    (grade_11, 'Grade 11'),
    (grade_12, 'Grade 12')
)

#School Year:
SCHOOL_YEAR_CHOICES = [
    ('2023-24', '2023-24'),
    ('2024-25', '2024-25'),
    ('2025-26', '2025-26'),
    ('2026-27', '2026-27'),
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, studentNumber=None, coachNumber=None, idNumber=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, studentNumber=studentNumber, coachNumber=coachNumber, idNumber=idNumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, studentNumber=None, coachNumber=None, idNumber=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, studentNumber, coachNumber, idNumber, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    studentNumber = models.CharField(max_length=50, unique=True, blank=True, null=True)
    coachNumber = models.CharField(max_length=50, unique=True, blank=True, null=True)
    idNumber = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Add related_name='custom_users' to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.email
    




# Strand and Subjects models
class Strand(models.Model):
    name = models.CharField(max_length=50, choices=STRAND)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=100)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

class Student(models.Model):
    school_year = models.CharField(max_length=50, choices=SCHOOL_YEAR_CHOICES, default='2023-24')
    studentNumber = models.CharField(max_length=50, unique=True, editable=False)
    LRN = models.PositiveIntegerField()
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    addrs = models.CharField(max_length=100)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE)
    gradeLevel = models.CharField(max_length=50, choices=grade_level)
    section = models.CharField(max_length=3, validators=[RegexValidator(r'^\d{1,3}$')])
    picture = models.ImageField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.studentNumber:
            current_year = str(self.created_at.year) if self.created_at else str(timezone.now().year)
            student_count = Student.objects.filter(created_at__year=current_year).count() + 1
            self.studentNumber = f"{current_year}{student_count:03d}"

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Student: {self.firstName} {self.lastName}"
    
class Coaches(models.Model):

    coachNumber = models.CharField(max_length=50, unique=True, editable=False)
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=10, blank=True)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    addrs = models.CharField(max_length=50)
    cpNum = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{1,12}$')], blank=True)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject, related_name='coaches')

    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.coachNumber:
            current_year = str(self.created_at.year) if self.created_at else str(timezone.now().year)
            coach_count = Coaches.objects.filter(created_at__year=current_year).count() + 1
            self.coachNumber = f"{current_year}{coach_count:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Coach: {self.firstName} {self.lastName}"

class Attendance(models.Model):
    coach = models.ForeignKey(Coaches, on_delete=models.CASCADE)
    strand = models.ForeignKey(Strand, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    qr_code = models.ImageField(upload_to='Attendance', blank=True)

    class Meta:
        verbose_name_plural = 'Attendance QR'

    def coach_name(self):
        return self.coach
    
    def __str__(self):
        return f"Attendance for {self.coach} on {self.date}"

    
    def save(self, *args, **kwargs):
        # Generate QR code data
        base_url = "http://192.168.3.31:8000/"  # Update with your actual domain
        qr_data = base_url + reverse('attendance_login')
        
        # Generate QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code image to model field
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_file = File(img_io, name=f"qr_code-{self.date}.png")
        self.qr_code.save(img_file.name, img_file, save=False)

        super().save(*args, **kwargs)


    
    def get_att_url(self):
        return reverse('attendance_list', args=[self.coach])

class Attendance_List(models.Model):
    coach = models.ForeignKey(Coaches, on_delete=models.CASCADE)
    qrcode = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    user = models.ForeignKey(                                                                                                                                                   User, on_delete=models.CASCADE)
    loginid = models.CharField(max_length=100, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Attendance List'

    def __str__(self):
        return str(self.loginid)


