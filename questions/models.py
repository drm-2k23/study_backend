# # Create your models here.
# from __future__ import unicode_literals

# import os
# import re
# import uuid

# from decimal import Decimal
# from datetime import datetime

# from django.db import models
# from django.utils.translation import gettext_lazy as _

# from utils.validator import DECIMAL_VALIDATOR
# from utils.basemodel import BaseTimeStampModel
# from django_resized import ResizedImageField
# from django.contrib.auth import get_user_model

# User = get_user_model()

# def clean_image_name(name):
#     if name:
#         unique_id = uuid.uuid4().hex[:5].lower()
#         name = name + " " + unique_id
#         clean_name = re.sub('[^A-Za-z0-9\s]+', '', name)
#         add_underscore_to_space = re.sub('[\s]+', '_', clean_name)
#         return add_underscore_to_space
#     else:
#         return ""


# def document_directory_path(self, file_name):
#     basename = os.path.basename(file_name)
#     name, ext = os.path.splitext(basename)
#     if ext == '.apng':
#         ext = '.png'
#     name = self.product_name
#     image_list = ['.jpeg', '.jpg', '.gif', '.bmp', '.svg', '.psd', 'cpt', ".png",
#                   'psp', 'cxf', 'pdn', 'jfif', 'exif', 'tiff', 'ppm', 'pgm ', 'pnm']
#     if ext.lower() in image_list:
#         file_type = "images"
#     else:
#         file_type = "others"
#     cleaned_file_name = clean_image_name(name)
#     path = "media/" + '/{}/{}{}'.format(file_type, cleaned_file_name, ext)
#     return datetime.now().strftime(path)


# # Create your models here.
# class Subject(BaseTimeStampModel):
#     name = models.CharField(max_length=50)

#     class Meta:
#         verbose_name = _('Subject')
#         verbose_name_plural = _('Subjects')

#     def __str__(self):
#         return self.name


# class Chapter(BaseTimeStampModel):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# class Source(BaseTimeStampModel):
#     name =  models.CharField(max_length=50)

#     def __str__(self):
#         return self.name



# class QuestionTypes(BaseTimeStampModel):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name




# class AddQuestions(BaseTimeStampModel):
#     product_name = models.CharField(
#         _("Product Name"),
#         max_length=255,
#     )
#     added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     question_image = ResizedImageField(size=[500, 500],
#                                       quality=100,
#                                       help_text=_("Question Image"),
#                                       upload_to=document_directory_path, null=True, blank=True
#                                       )
#     answer_image = ResizedImageField(size=[500, 500],
#                                       quality=100,
#                                       help_text=_("Answer Image"),
#                                       upload_to=document_directory_path, null=True, blank=True
#                                       )

    
                                    
#     price = models.DecimalField(
#         max_digits=15, decimal_places=2, blank=True, null=True, validators=[DECIMAL_VALIDATOR], default=Decimal('0.00'))
#     quantity = models.PositiveSmallIntegerField()
#     description = models.TextField(
#         help_text=_("Detailed description."),
#     )
#     product_image = ResizedImageField(size=[500, 500],
#                                       quality=100,
#                                       help_text=_("Upload Image"),
#                                       upload_to=document_directory_path, null=True, blank=True
#                                       )

#     def __str__(self):
#         return self.product_name


# class Order(BaseTimeStampModel):
#     product_details = models.ManyToManyField(Product)
#     total_amount = models.DecimalField(
#             max_digits=15, decimal_places=2, blank=True, null=True, validators=[DECIMAL_VALIDATOR],
#             default=Decimal('0.00'))
#     user_detail = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return str(self.id)