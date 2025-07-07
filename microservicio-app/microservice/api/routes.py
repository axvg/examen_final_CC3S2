from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from microservice.services import business_logic

router = APIRouter(
    prefix="/api/notes",
    tags=["notes"]
)


class ItemIn(BaseModel):
    name: str = Field(..., example="sample note", description="Nombre único de nota")
    description: Optional[str] = Field(
        None, example="optional description", description="Descripción opcional de la nota"
    )


class ItemOut(ItemIn):
    id: int = Field(..., description="Identificador único de la nota")


@router.post(
    "/",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva nota"
)
def create_note(item: ItemIn) -> ItemOut:
    try:
        created = business_logic.create_note(item.name, item.description)
        return created
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )


@router.get(
    "/",
    response_model=List[ItemOut],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las notas"
)
def list_notes() -> List[ItemOut]:
    try:
        return business_logic.get_all_notes()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener notas"
        )
