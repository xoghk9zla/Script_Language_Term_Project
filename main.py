import urllib
url = 'http://openapi.copyright.or.kr/openapi/service/rest/ShrWrtgService/getTxtExpWrtgDetail'
queryParams = '?' + urllib.urlencode({ urllib.quote_plus('ServiceKey') : 'CJQ9nAHb49w9WHrlkk0MT5t2V69kTMcq4Js5RoW6kTsYJIhX%2FpMWTNueiXNVjNuHwnKoXBQl2FOov8euaabf%2FA%3D%3D', urllib.quote_plus('writingSeq') : '9008053' })

request = urllib.Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urllib.urlopen(request).read()
print(response_body)
