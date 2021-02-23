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
from library import Relay, RelayHandler
import http_api_handler
import uhttpd
import time
import machine


def main():
    try:
        relay = Relay()
        exception_timeout = configuration.get('exception_reset_timeout')
        api_handler = http_api_handler.Handler([(['relay'],
            RelayHandler(relay, configuration.get('http_authorization_token')))]
        )
        server = uhttpd.Server([('/api', api_handler)])
        server.run()
    except Exception as e:
        print(('Caught exception, {}'
               'resetting in {} seconds...').format(e, exception_timeout))
        time.sleep(exception_timeout)
        machine.reset()


if __name__ == '__main__':
    main()
