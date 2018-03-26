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


def search_results_number_draw(request):
    if request.method == 'POST':
        draw_from = request.POST['draw_from']
        draw_to = request.POST['draw_to']

        date = 0
        result_list = []
        for draw_index in range(int(draw_from), int(draw_to) + 1):
            lotto_numbers = LottoNumber.objects.filter(draw=draw_index, is_bonus_number=False)
            winning_num = []
            odd_even = []
            group_1_10 = 0
            group_11_20 = 0
            group_21_30 = 0
            group_31_40 = 0
            group_41_50 = 0
            for lotto_num in lotto_numbers:
                winning_num.append(str(lotto_num.winning_number))
                date = lotto_num.date
                odd_even.append(lotto_num.odd_even)
                if lotto_num.group == '1~10':
                    group_1_10 += 1
                elif lotto_num.group == '11~20':
                    group_11_20 += 1
                elif lotto_num.group == '21~30':
                    group_21_30 += 1
                elif lotto_num.group == '31~40':
                    group_31_40 += 1
                elif lotto_num.group == '41~50':
                    group_41_50 += 1
            # print(','.join(winning_num))
            odd_cnt = odd_even.count('odd')
            even_cnt = odd_even.count('even')
            bonus_numbers = LottoNumber.objects.filter(draw=draw_index, is_bonus_number=True)
            # print(bonus_numbers[0].winning_number)
            data = {
                'draw': draw_index,
                'date': date,
                'winning_num': ','.join(winning_num),
                'bonus_num': bonus_numbers[0].winning_number,
                'odd_even': f'홀수:{odd_cnt} / 짝수:{even_cnt}',
                'group_1_10': group_1_10,
                'group_11_20': group_11_20,
                'group_21_30': group_21_30,
                'group_31_40': group_31_40,
                'group_41_50': group_41_50,
            }
            result_list.append(data)
        context = {
            'result_list': result_list,
        }
        return render(request, 'search-results-draw.html', context)
    return render(request, 'search-results-draw.html')


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
