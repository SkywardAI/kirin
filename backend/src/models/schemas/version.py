# coding=utf-8

# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from src.models.schemas.base import BaseSchemaModel
from pydantic import Field


class ServiceVersionResponse(BaseSchemaModel):
    """
    The version of the service

    - **kirin**: The version of the API aggregator
    - **inference_engine**: The version of the inference engine
    """

    inference_engine: str | None = Field(
        ..., title="infernece engine version", description="infernece engine version", examples=["server--b1-a8d49d8"]
    )
    kirin: str | None = Field(
        ..., title="backend service version", description="backend service version", examples=["v0.1.8"]
    )
