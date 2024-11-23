from django.db import migrations

def create_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    Site.objects.create(
        id=1,
        domain='localhost:5173',
        name='Seedly'
    )

class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(create_site),
    ]