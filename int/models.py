from __future__ import unicode_literals

from django.db import models

class Post(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    date = models.DateTimeField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    thread = models.IntegerField(blank=True, null=True)
    country_code = models.TextField(blank=True, null=True, db_index=True)
    country_path = models.TextField(blank=True, null=True)
    main_post = models.NullBooleanField(db_index=True)

    class Meta:
        db_table = 'post'
