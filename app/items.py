from fastapi import APIRouter, Depends, status, HTTPException
from app.db import get_user_db, get_async_session, Item, ShoppingList
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
import app.schemas as schemas
from app.users import current_active_user, User

router = APIRouter(
    prefix='/lists',
    tags=['Items']
)

@router.post('/{listId}/items',
             response_model=schemas.ItemRead,
             status_code=status.HTTP_201_CREATED)
async def create_item(listId: int,
                      request: schemas.ItemCreate,
                      db: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    async with db.begin():
        shopping_list = await db.execute(selectinload(ShoppingList.items).filter_by(id=listId))
        shopping_list = shopping_list.scalars().first()
    if not shopping_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Shopping List doesn't exist")
    new_item = Item(name=request.name, quantity=request.quantity, shopping_list=listId, unit_price=request.unit_price)
    new_item.shopping_list = shopping_list
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return new_item

@router.get('/{listId}/items/{itemId}',
            response_model=schemas.ItemRead,
            status_code=status.HTTP_200_OK)
async def get_item(listId: int,
                   itemId: int,
                   db: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_active_user)):
    item = await db.get(Item, itemId)
    if not item or item.shopping_list_id != listId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item doesn't exist in the shopping list")

    return item

@router.put('/{listId}/items/{itemId}',
            response_model=schemas.ItemRead,
            status_code=status.HTTP_202_ACCEPTED)
async def update_item(listId: int,
                      itemId: int,
                      request: schemas.ItemRead,
                      db: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    item = await db.get(Item, itemId)
    if not item or item.shopping_list_id != listId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item doesn't exist in the shopping list")

    item.unit_price = request.unit_price
    item.name = request.name
    item.quantity = request.quantity

    await db.commit()

    return item

@router.delete('/{listId}/items/{itemId}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(listId: int,
                      itemId: int,
                      db: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    item = await db.get(Item, itemId)
    if not item or item.shopping_list_id != listId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item doesn't exist in the shopping list")

    await db.delete(item)
    await db.commit()

    return {'Delete Item': 'Done'}
