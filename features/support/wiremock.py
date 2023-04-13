
import functools

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def wiremock(uri, *fields):
    methods = ['get', 'post', 'delete']
    generate_functions = lambda url: type(
        'Requests',
        (),
        {method: functools.partial(getattr(requests, method), url, verify=False) for method in methods},
    )
    actions = dict(
        mappings="mappings",
        requests="requests",
        count="requests/count",
        remove_requests="requests/remove",
        find="requests/find",
    )
    build_url = lambda field: f'{uri}/__admin/{actions[field]}'

    return type(
        'WireMock',
        (),
        {f: generate_functions(build_url(f)) if f != 'maps' else mapper(build_url('mappings')) for f in fields},
    )


def mapper(url):
    def require_json_response(requester, request, body=None, status=200):
        response = requester(
            json=(
                dict(
                    request=request,
                    response=dict(
                        status=status,
                        jsonBody=body or {},
                        headers={"Content-Type": "application/json;charset=UTF-8"},
                    ),
                )
            )
        )
        response.raise_for_status()
        return response.json()

    def add_mapping(requester, method, uri, params=None, body=None):
        request = dict(method=method.upper())
        request['urlPath' if params else 'url'] = uri
        if params:
            request['queryParameters'] = {k: dict(equalTo=v) for k, v in params.items()}
        if body:
            # TODO: support recursive definitions
            request['bodyPatterns'] = [
                {
                    'matchesJsonPath': {
                        'expression': f'.{k}',
                        'equalTo': str(v).replace("'", '"'),
                    }
                }
                for k, v in body.items()
            ]
        return type(
            '',
            (),
            dict(json=functools.partial(require_json_response, requester, request)),
        )

    return type(
        '',
        (),
        dict(
            remove=lambda: requests.delete(url),
            add=type(
                '',
                (),
                {
                    k: functools.partial(add_mapping, functools.partial(requests.post, url), k)
                    for k in ('get', 'post', 'patch', 'put', 'delete')
                },
            ),
        ),
    )
