from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect

from lotto.models import LottoNumber


def lotto_analysis_home(request):
    aggregate_data = LottoNumber.objects.all().aggregate(Max('draw'))
    draw_max = aggregate_data['draw__max']
    last_lotto_win_num_list = LottoNumber.objects.filter(draw=draw_max)
    print(last_lotto_win_num_list)
    last_win_num_list = []
    last_bonus_num = 0
    for last_win_num in last_lotto_win_num_list:
        if last_win_num.is_bonus_number:
            last_bonus_num = last_win_num.winning_number
        else:
            last_win_num_list.append(last_win_num.winning_number)

    context = {
        'draw_max': draw_max,
        'last_draw_date': last_lotto_win_num_list[0].date,
        'last_win_num_list': last_win_num_list,
        'last_bonus_num': last_bonus_num,
    }
    return render(request, 'index.html', context)


def get_number_frequency(request):
    num_frequency_list = []
    total = 0
    for num in range(1, 46):
        win_num_cnt = LottoNumber.objects.filter(winning_number=num, is_bonus_number=False).count()
        bonus_num_cnt = LottoNumber.objects.filter(winning_number=num, is_bonus_number=True).count()
        num_overall = win_num_cnt + bonus_num_cnt
        total += num_overall
        data = {
            'num': num,
            'win_num_cnt': win_num_cnt,
            'bonus_num_cnt': bonus_num_cnt,
            'num_overall': num_overall,
        }
        num_frequency_list.append(data)
    context = {
        'num_list': num_frequency_list,
    }
    # print(context)
    # print(f'total >> {total}')
    return render(request, 'number-frequency.html', context)


def lotto_number_list(request):
    lotto_num_list = LottoNumber.objects.all()
    context = {
        'lotto_list': lotto_num_list,
    }
    return render(request, 'index.html', context)


# def lotto_number_add_from_naver(request):
#     if request.method == 'GET':
#         draw = 1
#         LottoNumber.objects.update_or_create_from_naver(draw=draw)
#         return redirect('lotto:lotto-list')
