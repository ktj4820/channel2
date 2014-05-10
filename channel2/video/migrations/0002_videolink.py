# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('video', models.ForeignKey(to='video.Video', to_field='id')),
                ('key', models.CharField(max_length=64, db_index=True)),
                ('ip_address', models.CharField(max_length=64)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
            ],
            options={
                'db_table': 'video_link',
            },
            bases=(models.Model,),
        ),
    ]
