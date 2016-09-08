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

# Ubuntu Xenial 16.04 [LTS]
FROM ubuntu:16.04

# Install Deps
RUN apt-get update -yqq && \
    apt-get install -yqq python3-dev python3-pip qt5-default && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt /opt/userale

WORKDIR /opt

# Install requirements
RUN pip3 install -r requirements.txt

#CMD ["python", "./setup.py", "develop"]

