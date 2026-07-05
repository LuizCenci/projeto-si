from django.contrib.auth.hashers import make_password
from django.db import migrations


def criar_contas(apps, schema_editor):
    Usuario = apps.get_model("core", "Usuario")
    contas = [
        ("universidade@academica.edu", "Universidade Demo", "UNIVERSIDADE", "Universidade@123", False),
        ("123456", "Estudante Demo", "ESTUDANTE", "Estudante@123", False),
        ("admin", "Administrador", "ADMIN", "Admin@123", True),
    ]
    for username, nome, role, senha, staff in contas:
        Usuario.objects.create(
            username=username,
            first_name=nome,
            role=role,
            password=make_password(senha),
            is_staff=staff,
            is_superuser=staff,
        )


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [migrations.RunPython(criar_contas, migrations.RunPython.noop)]
