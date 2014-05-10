# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import channel2.core.uploads


class Migration(migrations.Migration):

    dependencies = [
        ('label', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('file', models.FileField(null=True, blank=True, upload_to=channel2.core.uploads.video_file_upload_to)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(editable=False, max_length=100)),
                ('views', models.IntegerField(default=0)),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='label.Label', to_field='id', null=True)),
                ('cover', models.FileField(null=True, blank=True, upload_to=channel2.core.uploads.video_cover_upload_to)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'video',
            },
            bases=(models.Model,),
        ),
    ]
