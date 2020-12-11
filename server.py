import json
from aiohttp import web
from lxml import etree


routes = web.RouteTableDef()


@routes.get("/{path:.*}")
async def handle_get(request):
    return await request_handler(request)


@routes.post("/{path:.*}")
async def handle_post(request):
    return await request_handler(request)


async def request_handler(request):
    print("<<<<<< Logging raw request:")
    print(
        f"{request.method} {request.path_qs} HTTP/{request.version.major}.{request.version.minor}"
    )
    for header in request.headers:
        print(f"{header}: {request.headers[header]}")
    body = await request.read()
    if request.content_type.startswith('text/xml') or request.content_type.startswith('application/xml'):
        parser = etree.XMLParser(remove_blank_text=True)
        body = etree.tostring(
            etree.XML(body, parser).getroottree(), pretty_print=True, xml_declaration=True
        ).decode("utf-8")
    elif request.content_type == "application/json":
        body = json.dumps(json.loads(body), indent=2)
    else:
        body = body.decode(request.charset or "utf-8")
    print(f"\n{body}")
    print(">>>>>>>>> Sending response")
    print("HTTP 200 OK\nOK")
    print("====================")
    return web.Response(text="OK")


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8888)
