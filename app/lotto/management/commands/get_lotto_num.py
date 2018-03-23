from django.core.management import BaseCommand

from crawler.lotto_number import LottoNumberData


class Command(BaseCommand):
    def handle(self, *args, **options):
        lotto_num = LottoNumberData()
        lotto_num.get_data()
