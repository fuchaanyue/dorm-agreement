import base64
import os
from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    """
    渲染前端页面，并传入表格循环范围变量
    """
    return render(request, "index.html", {
        "range_10": range(1, 11),  # 主表 10 行
        "range_5": range(1, 6)     # 补充表 5 行
    })

@api_view(["POST"])
def save_image(request):
    """
    接收前端传来的 base64 图片并保存到 MEDIA_ROOT/agreements/
    """
    image_data = request.data.get("image")
    if not image_data:
        return Response({"error": "缺少图片数据"}, status=400)

    try:
        # 去掉 data:image/png;base64, 头
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        # 文件名加上时间戳避免覆盖
        from datetime import datetime
        file_name = f"dorm_agreement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"

        # 确保目录存在
        save_dir = os.path.join(settings.MEDIA_ROOT, "agreements")
        os.makedirs(save_dir, exist_ok=True)

        # 保存文件
        file_full_path = os.path.join(save_dir, file_name)
        with open(file_full_path, "wb") as f:
            f.write(base64.b64decode(imgstr))

        return Response({
            "status": "success",
            "message": "图片已保存",
            "path": f"{settings.MEDIA_URL}agreements/{file_name}"
        })
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)
