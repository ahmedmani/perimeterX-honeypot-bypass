from mitmproxy import http






def request(flow: http.HTTPFlow) -> None:
    pass

def response(flow):
    fd = open('modifiedinit.js', 'r')
    if flow.request.url == 'https://www.walmart.com/px/PXu6b0qd2S/init.js':
        data = flow.response.get_text()
        flow.response.text = fd.read()


