import typing
import sqlalchemy

from src.models.db.file import UploadedFile
from src.repository.crud.base import BaseCRUDRepository
from src.utilities.verifier.file import file_verifier # type: ignore
from src.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist


class UploadedFileCRUDRepository(BaseCRUDRepository):
    async def create_uploadfile(self, file_name: str) -> UploadedFile:

        file_name_stmt = sqlalchemy.select(UploadedFile.name).select_from(UploadedFile).where(UploadedFile.name == file_name)
        file_name_query = await self.async_session.execute(file_name_stmt)
        db_file_name = file_name_query.scalar()
                
        if not file_verifier.is_file_available(name=db_file_name):
            raise EntityAlreadyExists(f"The file_name `{file_name}` is already file_name!")  
   
   
        uploaded_file = UploadedFile(name=file_name)

        self.async_session.add(instance=uploaded_file)
        await self.async_session.commit()
        await self.async_session.refresh(instance=uploaded_file)

        return uploaded_file

    async def read_uploadedfiles(self) -> typing.Sequence[UploadedFile]:
        stmt = sqlalchemy.select(UploadedFile)
        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def read_uploadedfiles_by_id(self, id: int) -> UploadedFile:
        stmt = sqlalchemy.select(UploadedFile).where(UploadedFile.id == id)
        query = await self.async_session.execute(statement=stmt)
        fileinfo = query.scalar()
        if fileinfo is None:
            raise EntityDoesNotExist("File with id `{id}` does not exist!")

        return fileinfo# type: ignore

    async def delete_file_by_id(self, id: int) -> str:
        select_stmt = sqlalchemy.select(UploadedFile).where(UploadedFile.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        delete_file = query.scalar()

        if not delete_file:
            raise EntityDoesNotExist(f"File with id `{id}` does not exist!")  # type: ignore

        stmt = sqlalchemy.delete(table=UploadedFile).where(UploadedFile.id == delete_file.id)

        await self.async_session.execute(statement=stmt)
        await self.async_session.commit()

        return f"Filewith id '{id}' is successfully deleted!"
