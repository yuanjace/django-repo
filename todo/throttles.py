# throttles.py
from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import Throttled

from datetime import datetime, timedelta
from django.core.cache import cache


class CustomThrottled(Throttled):
    default_detail = "好了啦，API不要打這麼急躁。慢慢來比較快"


class secondThrottle(BaseThrottle):
    def allow_request(self, request, view):
        key = (
            f"request_{request.user.id}"
            if request.user.is_authenticated
            else f"request_{request.META['REMOTE_ADDR']}"
        )
        last_request_time = cache.get(key)

        if not last_request_time or datetime.now() - last_request_time > timedelta(
            seconds=1
        ):
            cache.set(key, datetime.now(), timeout=1)  # 設置下一次請求的有效期為5秒
            return True

        raise CustomThrottled()
