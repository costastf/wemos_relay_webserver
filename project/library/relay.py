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

from machine import Pin


class Relay(object):
    def __init__(self, pin_number=5):
        self._pin = Pin(pin_number, Pin.OUT)

    @property
    def status(self):
        return 'on' if self.state else 'off'

    @property
    def state(self):
        return self._pin.value()

    @state.setter
    def state(self, status):
        self._pin.high() if status else self._pin.low()

    def toggle(self):
        self.state = not self.state

    def activate(self):
        self.state = True

    def deactivate(self):
        self.state = False
