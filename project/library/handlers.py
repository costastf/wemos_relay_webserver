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

    def _get_state(self):
        state = True if self.relay.state else False
        return {'state': state}

    def get(self, api_request):
        _ = api_request
        return self._get_state()

    def post(self, api_request):
        try:
            http = api_request.get('http')
            body = http.get('body').decode('utf-8')
            response = ujson.loads(body)
            state = response.get('state', 'NoState')
            if state == 'NoState':
                raise ValueError(api_request)
            self.relay.activate() if state else self.relay.deactivate()
            result = self._get_state()
        except Exception as e:
            result = {'state': 'unknown',
                      'exception': e}
        return result
