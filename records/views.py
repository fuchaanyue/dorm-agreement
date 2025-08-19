# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from records.cos_utils import COSClient
import base64
import time
import json

def index(request):
    """
    渲染前端页面，并传入表格循环范围变量
    """
    return render(request, "index.html", {
        "range_10": range(1, 11),  # 主表 10 行
        "range_5": range(1, 6)     # 补充表 5 行
    })
@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        try:
            # 获取前端传来的图片数据

            data = json.loads(request.body)
            image_data = data.get('image')
            if not image_data:
                return JsonResponse({'error': '未提供图片数据'}, status=400)

            # 解析 base64 数据
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            # 生成唯一文件名
            timestamp = int(time.time())
            filename = f"agreements/agreement_{timestamp}.{ext}"

            # 解码成 bytes
            file_content = base64.b64decode(imgstr)

            # 上传到 COS
            cos_client = COSClient()
            file_url = cos_client.upload_image(file_content, filename)

            return JsonResponse({
                'success': True,
                'url': file_url,
                'filename': filename
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': '无效的请求方法'}, status=405)


