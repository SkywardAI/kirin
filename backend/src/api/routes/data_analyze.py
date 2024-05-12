from fastapi import Request
from fastapi.templating import Jinja2Templates
import fastapi

from bokeh.embed import server_document

from src.models.schemas.data_analyze import DataViewResponse

router = fastapi.APIRouter(prefix="/dataview", tags=["dataview"])
templates = Jinja2Templates(directory="templates")

@router.post(
    "",
    name="data_analyze:dataview",
    response_model=DataViewResponse,
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def dataview(
    session_id: str,
) -> DataViewResponse:
    # TODO generate dataview by searching of session_id
    script = server_document('http://localhost:5006/sample')
    return DataViewResponse(script=script)

@router.get(
    "",
    name="data_analyze:sample",
    status_code=fastapi.status.HTTP_201_CREATED,
)
async def sample_plot(
    request: Request,
):
    script = server_document('http://localhost:5006/sample')
    print(script)
    return templates.TemplateResponse("bokeh.html", {
        "request": request,
        "title": "Bokeh Plot",
        "bokeh_script": script,
    })