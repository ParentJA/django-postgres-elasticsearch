from django.contrib.postgres.operations import TrigramExtension
from django.db import connection, migrations


def update_wine_search_word(apps, schema_editor):
    sql = """
        INSERT INTO catalog_winesearchword (word)
        SELECT word FROM ts_stat('
          SELECT to_tsvector(''simple'', winery) ||
                 to_tsvector(''simple'', coalesce(description, ''''))
            FROM catalog_wine
        ');
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_winesearchword'),
    ]

    operations = [
        TrigramExtension(),
        migrations.RunSQL(sql="""
            CREATE INDEX IF NOT EXISTS wine_search_word_trigram_index
                ON catalog_winesearchword
             USING gin (word gin_trgm_ops);
        """, elidable=True),
        migrations.RunPython(update_wine_search_word, elidable=True),
    ]
