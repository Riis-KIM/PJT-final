# accounts/migrations/0002_create_default_site.py
from django.db import migrations

def update_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(id=1).update(
        domain='localhost:5173',
        name='Seedly'
    )

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(update_site),
    ]