from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import os
from .model import CustomEncoder
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def solve_problem(request):
    # 获取文本数据
    text_data = request.data.get('text_field')

    # 获取文件对象
    file_obj = request.FILES.get('file_field')

    result = CustomEncoder(file_obj, text_data)

    # 假设最终结果存储在变量`result`中
    return JsonResponse({'result': result})


def my_form_view(request):
    return render(request, 'form_template.html')


# Create your views here.
