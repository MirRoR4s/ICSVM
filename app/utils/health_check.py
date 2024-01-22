#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import ceil

from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.routing import APIRoute

from app.common.exception import errors


def ensure_unique_route_names(app: FastAPI) -> None:
    temp_routes = set()
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.name in temp_routes:
                raise ValueError(f'Non-unique route name: {route.name}')
            temp_routes.add(route.name)


async def http_limit_callback(request: Request, response: Response, expire: int):
    """
    请求限制时的默认回调函数
    """
    expires = ceil(expire / 1000)
    raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, detail='请求过于频繁，请稍后重试',headers={'Retry-After': str(expires)})

