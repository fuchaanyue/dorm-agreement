# cos_utils.py
from qcloud_cos import CosConfig, CosS3Client
import os
import time


class COSClient:
    def __init__(self):
        # 从环境变量获取配置
        self.config = CosConfig(
            Region=os.getenv('COS_REGION'),
            SecretId=os.getenv('COS_SECRET_ID'),
            SecretKey=os.getenv('COS_SECRET_KEY'),
            Scheme="https"
        )
        self.bucket = os.getenv('COS_BUCKET')

        # 创建客户端
        self.client = CosS3Client(self.config)

        # 验证配置
        if not all([
            os.getenv('COS_REGION'),
            os.getenv('COS_SECRET_ID'),
            os.getenv('COS_SECRET_KEY'),
            os.getenv('COS_BUCKET')
        ]):
            raise ValueError("请设置必要的环境变量：COS_REGION, COS_SECRET_ID, COS_SECRET_KEY, COS_BUCKET")

    def upload_image(self, file_content: bytes, file_path: str):
        """
        上传图片到COS
        :param file_content: 二进制图片数据
        :param file_path: COS中的文件路径
        :return: 图片的访问URL
        """
        try:
            # 上传文件
            self.client.put_object(
                Bucket=self.bucket,
                Key=file_path,
                Body=file_content
            )

            # 构建访问URL
            return f"https://{self.bucket}.cos.{self.config._region}.myqcloud.com/{file_path}"

        except Exception as e:
            raise Exception(f"图片上传失败: {str(e)}")
