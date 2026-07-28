import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smallscapesapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(
                default=5,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created_at']},
        ),
        # Backfill: reviews that already existed (the seeded testimonials + any
        # real reviews submitted before this migration) are marked approved so
        # they don't silently disappear from the public page after upgrade.
        migrations.RunSQL(
            sql="UPDATE smallscapesapp_review SET is_approved = 1;",
            reverse_sql="UPDATE smallscapesapp_review SET is_approved = 0;",
        ),
    ]
