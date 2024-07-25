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


from typing import Optional

from pydantic import Field
from src.models.schemas.base import BaseSchemaModel


class NeuralnetsResponse(BaseSchemaModel):
    name: str = Field(..., title="Neural Network Name", description="Neural Network Name")
    description: Optional[str] = Field(default="Neural nets", title="Description", description="Description")
    modules: Optional[list[str]] = Field(default=["Embedding(65, 65)"], title="Modules", description="Modules")
