from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_update_wine_search_word'),
    ]

    operations = [
        CreateExtension(name='fuzzystrmatch'),
    ]
