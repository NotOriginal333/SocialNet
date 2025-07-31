from flask import Blueprint, request, Response, current_app
from urllib.parse import urlparse, urljoin

import requests

bp = Blueprint("proxy", __name__)


@bp.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    base_url = current_app.config['DJANGO_BACKEND_URL']
    backend_url = urljoin(base_url + '/', path)

    parsed_url = urlparse(current_app.config['DJANGO_BACKEND_URL'])
    host_without_port = parsed_url.hostname

    headers = dict(request.headers)
    headers["Host"] = host_without_port
    method = request.method.lower()

    func = getattr(requests, method)
    resp = func(backend_url, headers=headers, data=request.get_data(), params=request.args)

    print("proxy path:", path)
    print("backend_url:", backend_url)

    return Response(resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type"))
