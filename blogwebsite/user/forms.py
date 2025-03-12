from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import SimpleUser,Blog, Creator, ContactUs
import re

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        error_messages={'invalid': 'Enter a valid email address.'}
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=100,  # Prevents unrealistic age input
        required=True,
        error_messages={'invalid': 'Enter a valid age between 1 and 100.'}
    )
    country = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Country is required.'}
    )
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': 'Upload a valid image file.'}
    )

    class Meta:
        model = SimpleUser
        fields = ('username', 'email', 'age', 'country', 'image', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if SimpleUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters long.")
        return username


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        error_messages={'required': 'Username is required.'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        error_messages={'required': 'Password is required.'}
    )


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        error_messages={'invalid': 'Enter a valid email address.'}
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=True,
        error_messages={'invalid': 'Enter a valid age between 1 and 100.'}
    )
    country = forms.CharField(
        max_length=100,
        required=True,
        error_messages={'required': 'Country is required.'}
    )
    image = forms.ImageField(
        required=False,
        error_messages={'invalid': 'Upload a valid image file.'}
    )

    class Meta:
        model = SimpleUser
        fields = ('age', 'country', 'image', 'email')

  
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'description', 'photo', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write something only paragraph...', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


COUNTRIES = [
    ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'),
    ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'),
    ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'),
    ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'),
    ('BO', 'Bolivia'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'),
    ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'),
    ('CV', 'Cabo Verde'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('KY', 'Cayman Islands'),
    ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'),
    ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'),
    ('CD', 'Congo, Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'),
    ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Curaçao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'),
    ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'),
    ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'),
    ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'),
    ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'),
    ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'),
    ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'),
    ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'),
    ('VA', 'Holy See'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'),
    ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'),
    ('IM', 'Isle of Man'),('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'),
    ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'),
    ('KP', 'Korea, North'), ('KR', 'Korea, South'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Laos'),
    ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'),
    ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MG', 'Madagascar'),
    ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'),
    ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'),
    ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'), ('MC', 'Monaco'), ('MN', 'Mongolia'),
    ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'),
    ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'),
    ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'),
    ('NF', 'Norfolk Island'), ('MK', 'North Macedonia'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'),
    ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine'), ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'),
    ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Réunion'),
    ('RO', 'Romania'), ('RU', 'Russia'), ('RW', 'Rwanda'), ('BL', 'Saint Barthélemy'),
    ('SH', 'Saint Helena'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'),
    ('MF', 'Saint Martin'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'),
    ('SX', 'Sint Maarten'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'),
    ('ZA', 'South Africa'), ('GS', 'South Georgia'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SE', 'Sweden'), ('CH', 'Switzerland'),
    ('SY', 'Syria'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'),
    ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'),
    ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('VG', 'Virgin Islands, British'),
    ('VI', 'Virgin Islands, U.S.'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'),
    ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'),
]

# Education levels
EDUCATION_LEVELS = [
    ('', 'Select Education Level'),  
    ('MATRIC', 'Matriculation (10th Grade)'),
    ('INTER', 'Intermediate (12th Grade)'),
    ('GRAD', 'Graduate (Bachelor’s Degree)'),
    ('POSTGRAD', 'Postgraduate (Master’s Degree)'),
    ('PHD', 'Doctorate (PhD)'),
    ('DIPLOMA', 'Diploma'),
    ('CERT', 'Certificate'),
    ('VOC', 'Vocational Training'),
    ('OTHER', 'Other'),
]

class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['first_name', 'last_name', 'email', 'bio', 'education', 'country', 'phone_number', 'password', 'photo', 'background_photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write something about you...', 'rows': 4}),
            'education': forms.Select(attrs={'class': 'form-control'}, choices=EDUCATION_LEVELS),
            'country': forms.Select(attrs={'class': 'form-control'}, choices=COUNTRIES),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'background_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
class CreatorLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        required=True,
        error_messages={
            'required': 'Password is required.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    

ISSUES = [
    ('', 'Select Issue'),  
    ('LOGIN', 'Unable to Login'),
    ('REGISTER', 'Registration Issues'),
    ('POST', 'Unable to Post a Blog'),
    ('COMMENT', 'Cannot Comment on Blogs'),
    ('EDIT', 'Editing or Deleting Blog Issues'),
    ('PROFILE', 'Profile Update Issues'),
    ('SLOW', 'Website Loading Slowly'),
    ('RESPONSIVE', 'Mobile Responsiveness Problems'),
    ('BROKEN_LINK', 'Broken Links on Website'),
    ('OTHER', 'Other'),
]
    

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['email','phone_number','issue','problem']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'issue': forms.Select(attrs={'class': 'form-control'}, choices=ISSUES),
            'problem': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your problem...', 'rows': 4}),
        }    

        labels = {
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'issue': 'Issue Type',
            'problem': 'Problem Description',
        }