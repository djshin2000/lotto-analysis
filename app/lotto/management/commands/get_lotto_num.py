from django.core.management import BaseCommand

from lotto.models import LottoNumber


class Command(BaseCommand):
    def handle(self, *args, **options):
        LottoNumber.objects.update_or_create_from_naver()
