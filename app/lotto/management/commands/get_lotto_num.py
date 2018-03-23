from django.core.management import BaseCommand
from django.db.models import Max

from lotto.models import LottoNumber


class Command(BaseCommand):
    def handle(self, *args, **options):
        aggregate_data = LottoNumber.objects.all().aggregate(Max('draw'))
        search_draw = aggregate_data['draw__max']
        if search_draw is None:
            search_draw = 1
            print('search_draw :', search_draw)
        else:
            search_draw += 1
            print('search_draw :', search_draw)
        LottoNumber.objects.update_or_create_from_naver(draw=search_draw)
