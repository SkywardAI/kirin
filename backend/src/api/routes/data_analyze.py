import fastapi

from src.models.schemas.data_analyze import DataViewResponse

router = fastapi.APIRouter(prefix="/dataview", tags=["dataview"])


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
    file_path = "somewhere/" + session_id + ".html"
    return DataViewResponse(filePath=file_path)
