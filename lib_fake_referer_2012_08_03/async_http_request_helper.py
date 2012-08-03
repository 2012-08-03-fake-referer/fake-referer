# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2011, 2012 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

assert unicode is not str
assert str is bytes

import urllib, urllib2, json
from .daemon_async import daemon_async

REQUEST_TIMEOUT = 20.0
RESPONSE_BODY_LENGTH_LIMIT = 10000000

class Response:
    pass

@daemon_async
def async_fetch(url, data=None, header_list=None, proxies=None, use_json=None):
    if isinstance(data, dict):
        data = urllib.urlencode(data)
    if use_json is None:
        use_json = False
    
    build_opener_args = []
    if proxies is not None:
        build_opener_args.append(
                urllib2.ProxyHandler(proxies=proxies))
    
    opener = urllib2.build_opener(*build_opener_args)
    
    if header_list is not None:
        opener.addheaders = tuple(header_list)
    
    f = opener.open(url, data=data, timeout=REQUEST_TIMEOUT)
    
    response = Response()
    response.code = f.getcode()
    response.body = f.read(RESPONSE_BODY_LENGTH_LIMIT)
    
    if use_json:
        response = json.loads(response.body)
    
    return response
