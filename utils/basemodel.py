from django.db import models

# Create your models here.


class BaseCreateTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created_at)


class BaseTimeStampModel(BaseCreateTimeStampModel):
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.updated_at)



