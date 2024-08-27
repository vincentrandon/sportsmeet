import csv
import os

from django.core.management import CommandError, BaseCommand

from planner.models import Player


class Command(BaseCommand):
    help = 'Import players from CSV)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if not os.path.exists(csv_file):
            raise CommandError(f"The file {csv_file} does not exist")

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip the header row

            for row in reader:

                name, licence_number = row

                player, created = Player.objects.get_or_create(
                    name=name,
                    licence_number=licence_number
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Successfully added player: {name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Failed creating: {name}"))

        self.stdout.write(self.style.SUCCESS('CSV file imported successfully'))