#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2016 The Charles Stark Draper Laboratory, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.auth import AuthBase

import json

# Logger will need to optinally handle authorization 
# through basic http auth, proxy, and SOCKS

class StructuredMessage (object):
	"""
	"""
	def __init__(self, data):
		self.data = data

	def __str__(self):
		return '%s' % (json.dumps (self.data, sort_keys=False, indent=4))
