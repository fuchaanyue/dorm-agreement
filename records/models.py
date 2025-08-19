from django.db import models

class AgreementRecord(models.Model):
    """宿舍公约达成记录卡"""
    serial_number = models.IntegerField()                  # 序号
    event_name = models.CharField(max_length=100)           # 事件名称
    agreement_content = models.TextField()                  # 公约内容
    achievement = models.CharField(max_length=100, blank=True)  # 宿舍成就，可空
    created_at = models.DateTimeField(auto_now_add=True)    # 创建时间

    def __str__(self):
        return f"{self.serial_number} - {self.event_name}"

class AgreementSupplement(models.Model):
    """宿舍公约补充"""
    serial_number = models.IntegerField()                   # 序号
    consensus = models.TextField()                          # 宿舍共识
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"补充 {self.serial_number}"

class Document(models.Model):
    file = models.FileField(upload_to="docs/")
