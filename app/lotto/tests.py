from django.test import TestCase

# Create your tests here.

# test_num = 11
# if test_num in range(1, 11):
#     print('true')
# else:
#     print('false')


class LottoNumber:
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


test = LottoNumber()
print(test.CHOICES_GROUP_TYPE[0][0])
