from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Candidate", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200)), ("email", models.EmailField(max_length=254, unique=True)), ("party", models.CharField(blank=True, max_length=200)), ("votes", models.PositiveIntegerField(default=0))]),
        migrations.CreateModel(name="Voter", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("name", models.CharField(max_length=200)), ("email", models.EmailField(max_length=254, unique=True)), ("has_voted", models.BooleanField(default=False))]),
        migrations.CreateModel(name="Vote", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="vote_records", to="voting.candidate")), ("voter", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="vote", to="voting.voter"))]),
    ]
