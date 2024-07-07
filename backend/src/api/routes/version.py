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


import fastapi
from src.models.schemas.version import ServiceVersionResponse
from src.config.manager import settings

router = fastapi.APIRouter(prefix="/version", tags=["version"])

@router.get(
    path="",
    name="version:get-version",
    response_model=ServiceVersionResponse,
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_version() -> ServiceVersionResponse:
    """
    Get the version of the service
    
    ```bash
    curl http://localhost:8000/api/version -> {"llamacpp":"server--b1-a8d49d8","milvus":"v2.3.12","kirin":"v0.1.8"}
    ```
    
    Return ServiceVersionResponse: 
    - **kirin**: The version of the API aggregator
    - **milvus**: The version of the vector database
    - **llamacpp**: The version of the inference engine 
    """

    return ServiceVersionResponse(
        kirin=settings.VERSION,
        milvus=settings.MILVUS_VERSION,
        llamacpp=settings.INFERENCE_ENG_VERSION
  )
