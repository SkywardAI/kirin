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

from src.api.routes.account import router as account_router
from src.api.routes.authentication import router as auth_router
from src.api.routes.chat import router as chat_router
from src.api.routes.version import router as version_router
from src.api.routes.health import router as health_router
from src.api.routes.rag_datasets import router as datasets_router
from src.api.routes.neural_nets import router as neural_nets_router

router = fastapi.APIRouter()

router.include_router(router=account_router)
router.include_router(router=auth_router)
router.include_router(router=chat_router)
router.include_router(router=version_router)
router.include_router(router=health_router)
router.include_router(router=datasets_router)
router.include_router(router=neural_nets_router)
