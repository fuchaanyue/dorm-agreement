from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cos_utils import COSClient
import base64
import time


@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        try:
            # 获取前端传来的图片数据
            image_data = request.POST.get('image')
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
