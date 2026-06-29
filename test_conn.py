import urllib.request
req = urllib.request.Request('http://litellm-proxy:4000/v1/models')
req.add_header('Authorization', 'Bearer sk-horizonai-litellm-2026')
try:
    code = urllib.request.urlopen(req).getcode()
    print('SUCCESS CODE:', code)
except Exception as e:
    print('FAILED:', str(e))
