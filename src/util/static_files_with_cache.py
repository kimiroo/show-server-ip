from fastapi import Response
from fastapi.staticfiles import StaticFiles

class StaticFilesWithCache(StaticFiles):
    def __init__(self, *args, cache_timeout: int = 31536000, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_timeout = cache_timeout

    def file_response(self, *args, **kwargs) -> Response:
        response = super().file_response(*args, **kwargs)
        # Set Cache-Control header
        response.headers["Cache-Control"] = f"public, max-age={self.cache_timeout}"
        return response