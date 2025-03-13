from django import forms
import re
from user.models import Blog, Creator
from .models import Story

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
    

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'description', 'category', 'photo']  # Removed 'status', added fields from your model
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blog Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write something only paragraph...', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BlogStatusForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('delete', 'Delete')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )    


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['content','text']
        widgets = {
            'content': forms.FileInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write something....'}),
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
        fields = [
            'first_name',
            'last_name',
            'email',
            'bio',
            'education',
            'country',
            'phone_number',
            'photo',
            'background_photo'
        ]

        widgets = {
            'education': forms.Select(attrs={'class': 'form-control'}, choices=EDUCATION_LEVELS),
            'country': forms.Select(attrs={'class': 'form-control'}, choices=COUNTRIES),
        }
        exclude = ['password', 'created_at', 'updated_at']  

    
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})