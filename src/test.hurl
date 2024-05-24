POST https://httpbin.org/post
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
[QueryStringParams]
id: 4567
order: newest
[BasicAuth]
alice: secret
{
    "id": "4568",
    "evaluate": true
}

HTTP *
[Asserts]
status < 300
status >= 200
header "server" contains "gunicorn"
jsonpath "$.url" contains "https://httpbin.org/post"
jsonpath "$.json.id" == "4568"