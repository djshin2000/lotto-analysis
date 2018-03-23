from django.db import models

from crawler.lotto_number import LottoNumberData


class LottoNumberManager(models.Manager):
    def update_or_create_from_naver(self):
        lotto_number_data = LottoNumberData()
        lotto_number_data.get_data()
        draw = lotto_number_data.draw
        win_number_list = lotto_number_data.win_num_list
        bonus_number = lotto_number_data.bonus_num
        date = lotto_number_data.date

        # group 필드의 값 구하기
        def lotto_number_match_group(num):
            num = int(num)
            if num in range(1, 11):
                group = LottoNumber.CHOICES_GROUP_TYPE[0][0]
            elif num in range(11, 21):
                group = LottoNumber.CHOICES_GROUP_TYPE[1][0]
            elif num in range(21, 31):
                group = LottoNumber.CHOICES_GROUP_TYPE[2][0]
            elif num in range(31, 41):
                group = LottoNumber.CHOICES_GROUP_TYPE[3][0]
            elif num in range(41, 51):
                group = LottoNumber.CHOICES_GROUP_TYPE[4][0]
            return group

        # odd_even 필드의 값 구하기
        def lotto_number_match_odd_even(num):
            num = int(num)
            if num % 2 == 1:
                odd_even = LottoNumber.CHOICES_ODD_EVEN[0][0]
            else:
                odd_even = LottoNumber.CHOICES_ODD_EVEN[1][0]
            return odd_even

        # 당첨번호 데이터 생성 및 업데이트(보너스 번호 제외)
        for win_number in win_number_list:
            self.update_or_create(
                draw=draw,
                winning_number=win_number,
                is_bonus_number=False,
                group=lotto_number_match_group(win_number),
                odd_even=lotto_number_match_odd_even(win_number),
                date=date,
            )

        # 보너스 번호 생성 및 업데이트
        self.update_or_create(
            draw=draw,
            winning_number=bonus_number,
            is_bonus_number=True,
            group=lotto_number_match_group(bonus_number),
            odd_even=lotto_number_match_odd_even(bonus_number),
            date=date,
        )


class LottoNumber(models.Model):
    CHOICES_GROUP_TYPE = (
        ('1~10', '1그룹(1~10)'),
        ('11~20', '2그룹(11~20)'),
        ('21~30', '3그룹(21~30)'),
        ('31~40', '4그룹(31~40)'),
        ('41~50', '5그룹(41~50)'),
    )
    CHOICES_ODD_EVEN = (
        ('odd', '홀수'),
        ('even', '짝수'),
    )

    draw = models.PositiveIntegerField('회차')
    winning_number = models.PositiveSmallIntegerField('당첨번호')
    is_bonus_number = models.BooleanField('보너스번호 유무')
    group = models.CharField('그룹', choices=CHOICES_GROUP_TYPE, max_length=15)
    odd_even = models.CharField('홀짝', choices=CHOICES_ODD_EVEN, max_length=15)
    date = models.DateField('추첨일')

    objects = LottoNumberManager()

    class Meta:
        unique_together = ('draw', 'winning_number')

    def __str__(self):
        return f'{self.draw}회차 {self.winning_number}'
