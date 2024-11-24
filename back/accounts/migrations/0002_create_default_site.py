# accounts/migrations/0002_create_default_site.py
from django.db import migrations

def update_site(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    # create 대신 update_or_create 사용
    Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': 'localhost:5173',
            'name': '금융상품 비교 서비스'
        }
    )

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),  # accounts 앱의 initial 마이그레이션 의존성 추가
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(update_site),
    ]