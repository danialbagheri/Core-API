from django.utils.cache import get_cache_key
from django.core.cache import caches
from rest_framework import throttling
from redis import exceptions


class SafeCacheUserRateThrottle(throttling.UserRateThrottle):
    def allow_request(self, request, view):
        try:
            return super().allow_request(request, view)
        except exceptions.ConnectionError:
            return True


class SafeCacheAnonRateThrottle(throttling.AnonRateThrottle):
    def allow_request(self, request, view):
        try:
            return super().allow_request(request, view)
        except exceptions.ConnectionError:
            return True


class PutAnonymousRateThrottle(throttling.AnonRateThrottle):
    scope = 'put_anon'
    cache = caches['default']
    # TODO: Check if this works with a cache like mamched on the live server

    def get_cache_key(self, request, view):
        return get_cache_key(request, key_prefix="PUT", method='PUT')

    def allow_request(self, request, view):
        if self.rate is None:
            return True
        try:
            self.key = self.get_cache_key(request, view)
        except exceptions.ConnectionError:
            return True
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if request.method == "PUT" and len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return self.throttle_success()
