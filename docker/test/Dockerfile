# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Python 3.5 Base Image
FROM python:3.5
MAINTAINER Michelle Beard <msbeard@apache.org>

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code
ADD test_requirements.txt /code

# Install requirements
RUN pip3 install -r requirements.txt
RUN pip3 install -r test_requirements.txt

ADD . /code/

RUN python3 setup.py test || exit 0
RUN pylint userale/ --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > /code/pylint.log || exit 0
