from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from microservice.services import business_logic

router = APIRouter(
    prefix="/api/items",
    tags=["items"]
)


class ItemIn(BaseModel):
    name: str = Field(..., example="sample item", description="Nombre único del ítem")
    description: Optional[str] = Field(
        None, example="optional description", description="Descripción opcional del ítem"
    )


class ItemOut(ItemIn):
    id: int = Field(..., description="Identificador único del ítem")


@router.post(
    "/",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo ítem"
)
def create_item(item: ItemIn) -> ItemOut:
    try:
        created = business_logic.create_item(item.name, item.description)
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
    summary="Listar todos los ítems"
)
def list_items() -> List[ItemOut]:
    try:
        return business_logic.get_all_items()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al obtener los ítems"
        )
