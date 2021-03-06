import csv

from django.core.management.base import BaseCommand

from phones.models import Phone

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as csvfile:
            phone_reader = csv.reader(csvfile, delimiter=';')
            # пропускаем заголовок
            next(phone_reader)

            for line in phone_reader:
                if line[5] == 'True':
                    lte_exists = True
                else:
                    lte_exists = False
                slug = "".join(line[1].split())
                phone_item = Phone(name=line[1], price=int(line[3]), image=line[2], release_date=line[4], lte_exists=lte_exists, slug=slug)
                phone_item.save()
