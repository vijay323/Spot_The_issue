from django.db import migrations, models
import core.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_id', models.CharField(default=core.models.generate_issue_id, max_length=20, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='issues/')),
                ('category', models.CharField(choices=[('Pothole', 'Pothole'), ('Garbage', 'Garbage'), ('Broken Streetlight', 'Broken Streetlight'), ('Waterlogging', 'Waterlogging'), ('Damaged Road', 'Damaged Road'), ('Other', 'Other')], default='Other', max_length=50)),
                ('priority', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', max_length=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Sent to Authority', 'Sent to Authority'), ('Resolved', 'Resolved')], default='Pending', max_length=30)),
                ('location', models.CharField(default='', max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('confidence', models.IntegerField(default=0)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-reported_at']},
        ),
    ]
