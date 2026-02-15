
from .models import File
import csv

def import_books(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            File.objects.create(
                name1= row["name1"],
                email1=row["email1"],
                contact1=row["contact1"],
                squad=row["squad"],
                language = row["language"]
            )
