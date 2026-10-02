from django.db import migrations, models


TUTORIAL_VIEW_KEY = "epolyscat:manual-tutorials"
CASE_IDS = ("test01", "test04", "test08", "test12", "test36")


def assign_tutorial_keys(apps, _schema_editor):
    View = apps.get_model("epolyscat_django_app", "View")
    Run = apps.get_model("epolyscat_django_app", "Run")

    tutorial_views = list(
        View.objects.filter(owner=None, type="tutorial").order_by("pk")
    )
    if tutorial_views:
        canonical_view = tutorial_views[0]
        for duplicate_view in tutorial_views[1:]:
            canonical_view.runs.add(*duplicate_view.runs.all())
            duplicate_view.delete()
        canonical_view.tutorial_key = TUTORIAL_VIEW_KEY
        canonical_view.save(update_fields=["tutorial_key"])

    for case_id in CASE_IDS:
        filepath = f"data/epolyscat/manual_tutorials/{case_id}"
        tutorial_runs = list(
            Run.objects.filter(owner=None, filepath=filepath).order_by("pk")
        )
        if not tutorial_runs:
            continue
        canonical_run = tutorial_runs[0]
        for duplicate_run in tutorial_runs[1:]:
            canonical_run.views.add(*duplicate_run.views.all())
            duplicate_run.delete()
        canonical_run.tutorial_key = f"epolyscat:manual-tutorial:{case_id}"
        canonical_run.save(update_fields=["tutorial_key"])


def clear_tutorial_keys(apps, _schema_editor):
    View = apps.get_model("epolyscat_django_app", "View")
    Run = apps.get_model("epolyscat_django_app", "Run")
    View.objects.filter(tutorial_key=TUTORIAL_VIEW_KEY).update(tutorial_key=None)
    Run.objects.filter(
        tutorial_key__startswith="epolyscat:manual-tutorial:"
    ).update(tutorial_key=None)


class Migration(migrations.Migration):

    dependencies = [
        ("epolyscat_django_app", "0027_run_workflow_source_run"),
    ]

    operations = [
        migrations.AddField(
            model_name="view",
            name="tutorial_key",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=80,
                null=True,
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="run",
            name="tutorial_key",
            field=models.CharField(
                blank=True,
                editable=False,
                max_length=80,
                null=True,
                unique=True,
            ),
        ),
        migrations.RunPython(assign_tutorial_keys, clear_tutorial_keys),
    ]
