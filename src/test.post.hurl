POST https://httpbin.org/post
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
[FormParams]
default: false
email: hi@example.com
number: 33611223344
[BasicAuth]
alice: secret
[QueryStringParams]
id: 4567
order: newest

HTTP *
[Asserts]
status < 300
status >= 200
header "server" contains "gunicorn"
jsonpath "$.url" contains "https://httpbin.org/post"
jsonpath "$.form.email" == "hi@example.com"