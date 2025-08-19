from django.core.files.storage import Storage
from django.conf import settings
from qcloud_cos import CosConfig, CosS3Client
from urllib.parse import urljoin


class TencentCOSStorage(Storage):
    """
    自定义腾讯云 COS 存储后端
    """

    def __init__(self, option=None):
        self.secret_id = settings.TENCENT_SECRET_ID
        self.secret_key = settings.TENCENT_SECRET_KEY
        self.region = settings.TENCENT_REGION
        self.bucket = settings.TENCENT_BUCKET
        self.domain = settings.TENCENT_BUCKET_DOMAIN  # 访问域名，最好用 CDN 加速过的

        config = CosConfig(
            Region=self.region,
            SecretId=self.secret_id,
            SecretKey=self.secret_key,
            Token=None,
            Scheme="https"
        )
        self.client = CosS3Client(config)

    def _open(self, name, mode="rb"):
        raise NotImplementedError("暂不支持直接打开文件")

    def _save(self, name, content):
        # 上传文件
        self.client.put_object(
            Bucket=self.bucket,
            Body=content.read(),
            Key=name,
            StorageClass="STANDARD",
            EnableMD5=False
        )
        return name

    def url(self, name):
        return urljoin(self.domain, name)
