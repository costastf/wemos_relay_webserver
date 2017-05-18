# -*- coding: utf-8 -*-
# Micropython code to manage a relay through a webserver on a esp8266
# Copyright (C) 2017  Costas Tyfoxylos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ujson


class RelayHandler(object):
    def __init__(self, relay_object):
        self.relay = relay_object

    def get(self, api_request):
        return {'state': self.relay.state,
                'status': self.relay.status}

    def post(self, api_request):
        try:
            http = api_request.get('http')
            body = http.get('body').decode('utf-8')
            response = ujson.loads(body)
            state = response.get('state', 'NoState')
            if state == 'NoState':
                raise ValueError(api_request)
            self.relay.activate() if state else self.relay.deactivate()
            result = {'result': 'success'}
        except Exception as e:
            result = {'result': 'failure',
                      'exception': e}
        return result
