"""
Corporate network SSL patch — disables certificate verification globally.
Import this module before any network calls in environments with SSL inspection.
"""
import os
import ssl
import warnings

# Suppress SSL warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
os.environ["PYTHONWARNINGS"] = "ignore:Unverified HTTPS request"

# Patch Python ssl module
ssl._create_default_https_context = ssl._create_unverified_context

# Patch requests.Session so ALL requests calls skip SSL verification
try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    _orig_request = requests.Session.request

    def _no_verify_request(self, method, url, **kwargs):
        kwargs.setdefault("verify", False)
        return _orig_request(self, method, url, **kwargs)

    requests.Session.request = _no_verify_request
except Exception:
    pass

# Patch httpx clients so openai SDK skips SSL verification
try:
    import httpx
    _orig_client_init = httpx.Client.__init__
    _orig_async_client_init = httpx.AsyncClient.__init__

    def _client_no_verify(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_client_init(self, *args, **kwargs)

    def _async_client_no_verify(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_async_client_init(self, *args, **kwargs)

    httpx.Client.__init__ = _client_no_verify
    httpx.AsyncClient.__init__ = _async_client_no_verify
except Exception:
    pass
