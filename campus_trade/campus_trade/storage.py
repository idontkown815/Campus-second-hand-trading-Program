import oss2
from django.core.files.storage import Storage
from django.conf import settings

class AliyunOSSStorage(Storage):
    def __init__(self):
        self.access_key_id = settings.ALIYUN_OSS_ACCESS_KEY_ID
        self.access_key_secret = settings.ALIYUN_OSS_ACCESS_KEY_SECRET
        self.bucket_name = settings.ALIYUN_OSS_BUCKET_NAME
        self.endpoint = settings.ALIYUN_OSS_ENDPOINT
        
        # 创建OSS认证对象
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        # 创建Bucket对象
        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)
    
    def _save(self, name, content):
        # 上传文件到OSS
        self.bucket.put_object(name, content)
        return name
    
    def _open(self, name, mode='rb'):
        # 从OSS获取文件
        return self.bucket.get_object(name)
    
    def exists(self, name):
        # 检查文件是否存在
        return self.bucket.object_exists(name)
    
    def url(self, name):
        # 返回文件的URL
        if hasattr(settings, 'ALIYUN_OSS_CUSTOM_DOMAIN') and settings.ALIYUN_OSS_CUSTOM_DOMAIN:
            return f"https://{settings.ALIYUN_OSS_CUSTOM_DOMAIN}/{name}"
        else:
            return f"https://{self.bucket_name}.{self.endpoint}/{name}"
    
    def delete(self, name):
        # 删除OSS上的文件
        self.bucket.delete_object(name)
    
    def get_available_name(self, name, max_length=None):
        # 生成可用的文件名
        return super().get_available_name(name, max_length)
