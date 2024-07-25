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
from fastapi.security import OAuth2PasswordBearer
from src.api.dependencies.repository import get_repository
from src.models.schemas.neural_nets import NeuralnetsResponse


router = fastapi.APIRouter(prefix="/nn", tags=["Neural network templates"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/verify")



@router.get(
    path="/list",
    name="nn:get-neural-net-list",
    response_model=list[NeuralnetsResponse],
    status_code=fastapi.status.HTTP_200_OK,
)
async def get_neural_net_list(
    token: str = fastapi.Depends(oauth2_scheme),
) -> list[NeuralnetsResponse]:
    """
    Get all the pre-processed neural network list.
    """

    return [
        {
            "name": "GPT",
            "description": "GPT is a transformer-based model",
            "modules": ["BigramLanguageModel((token_embedding_table): Embedding(65, 65))","Embedding(65, 65)"]
        },
        {
            "name": "Makemore",
            "description": "Makemore is a character-level language model",
            "modules": ["Makemore((token_embedding_table): Embedding(65, 65))","Embedding(65, 65)"]
        }
    ]