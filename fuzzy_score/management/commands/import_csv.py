import csv

from collections import defaultdict
from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from fuzzy_score.models import PPIScore


class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """
    i = 1

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []
        print(self.i)
        self.i = self.i + 1

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("filename", nargs=1)
        parser.add_argument("--delete", action="store_true")

    def handle(self, *args, **options):
        if options["delete"]:
           self.stdout.write("Deleting")
           PPIScore.objects.all().delete()
        bulk_mgr = BulkCreateManager(chunk_size=500000)
        with open(options["filename"][0], "r") as csvfile:
            self.stdout.write(self.style.SUCCESS("Importowanie..."))
            reader = csv.reader(csvfile, delimiter=",")
            # reader = csv.DictReader(csvfile, delimiter=",")
            for i, row in enumerate(reader, start=0):
                prot1 = row[0]
                prot2 = row[1]
                score = float(row[2])
                ppi_score = PPIScore(protein1=prot1, protein2=prot2, score=score)
                bulk_mgr.add(ppi_score)
                ppi_score = PPIScore(protein1=prot2, protein2=prot1, score=score)
                bulk_mgr.add(ppi_score)
            bulk_mgr.done()
                
        self.stdout.write(self.style.SUCCESS("Gotowe!"))

# python3 manage.py import_csv /media/jsroka/linux/fuzzyppi/test.csv
# python3 manage.py import_csv /media/jsroka/linux/fuzzyppi/Norm-MR_All_Iter.csv

