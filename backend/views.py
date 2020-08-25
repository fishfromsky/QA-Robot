from django.shortcuts import render
from .models import Line, Station, Time
from django.views.decorators.http import require_http_methods
import json
from django.http import JsonResponse
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ManyToManyField
import os
from ChineseNER.tensorflow.test import print_result


def to_dict(self, fields=None, exclude=None):
    data = {}
    for f in self._meta.concrete_fields + self._meta.many_to_many:
        value = f.value_from_object(self)

        if fields and f.name not in fields:
            continue

        if exclude and f.name in exclude:
            continue

        if isinstance(f, ManyToManyField):
            value = [i.id for i in value] if self.pk else None

        if isinstance(f, DateTimeField):
            value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

        data[f.name] = value

    return data


@require_http_methods(['GET'])
def search_time(request):
    response = {'code': 20000, 'message': 'success', 'data': []}
    line = request.GET.get('line')
    station = request.GET.get('station')
    ser = request.GET.get('service')
    if Line.objects.filter(name=line).count() == 0:
        response['code'] = 50000
        response['message'] = '不存在该线路'
    else:
        lines = Line.objects.filter(name=line)
        for line_item in lines:
            line_num = line_item.number
            if Station.objects.filter(name=station, line_id=Line(number=line_num)).count() == 0:
                response['code'] = 50000
                response['message'] = line + '不存在该站点'
            else:
                sta = Station.objects.get(name=station, line_id=Line(number=line_num))
                sta_id = sta.id
                time = Time.objects.filter(station_id=Station(id=sta_id))
                for item in time:
                    response['data'].append(to_dict(item))

    return JsonResponse(response, safe=False)


def judge_question(request):
    response = {'code': 20000, 'message': 'success', 'data': []}
    sentence = request.GET.get('question')
    res = print_result(sentence)
    if '_line' not in res:
        response['code'] = 50000
        response['message'] = '缺少线路'
    elif '_station' not in res:
        response['code'] = 50000
        response['message'] = '缺少站点'
    else:
        response['data'].append(res)

    return JsonResponse(response, safe=False)
