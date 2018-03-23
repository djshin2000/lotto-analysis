from django.core.management import BaseCommand

from lotto.models import LottoNumber


class Command(BaseCommand):
    def handle(self, *args, **options):
        for index in range(100, 799):
            print('index: ', index)
            LottoNumber.objects.update_or_create_from_naver(draw=index)
