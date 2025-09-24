from typing import Type, List, Optional
from sqlalchemy import nulls_last, asc, BinaryExpression, desc, delete, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.strategy_options import _AbstractLoad
from sqlalchemy.sql import select

from app.api.dependencies.base import PaginationParam, SortParam
from app.db.models.base import Base


async def create_entity(session: AsyncSession, entity, commit: bool = True, refresh: bool = True):
    session.add(entity)
    if commit:
        await session.commit()
        if refresh:
            await session.refresh(entity)
    elif refresh:
        await session.flush()

    return entity


async def update_entity(
        session: AsyncSession,
        entity_type: Type[Base],
        to_update: dict,
        commit: bool = True,
        update_time: bool = True,
        filters: List[BinaryExpression] = None,
):
    from app.utils.utils import now_datetime_with_timezone
    if not to_update:
        raise ValueError()
    if filters is None:
        filters = list()
    if update_time:
        to_update[entity_type.update_time] = now_datetime_with_timezone()
    query = update(entity_type).values(to_update).returning(entity_type)
    for query_filter in filters:
        query = query.where(query_filter)
    result = await session.execute(query)
    if commit:
        await session.commit()
    entity = result.scalar()
    if not entity:
        raise NoResultFound()
    await session.refresh(entity)
    return entity


async def delete_entity(
        session: AsyncSession,
        entity_type: Type[Base],
        filters: List[BinaryExpression] = None,
        commit: bool = True
):
    query = delete(entity_type)
    for query_filter in filters:
        query = query.where(query_filter)
    result = await session.execute(query)
    if commit:
        await session.commit()
    else:
        await session.flush()
    if result.rowcount == 0:
        raise NoResultFound


async def get_entity_by_filters(
        session: AsyncSession,
        entity_type: object,
        filters: List[BinaryExpression] = None
):
    query = select(entity_type)
    for filter in filters:
        query = query.where(filter)
    result = await session.execute(query)
    entity = result.scalars().first()
    if not entity:
        raise NoResultFound()
    return entity


async def get_list_of_entities(
        session: AsyncSession,
        entity_type: Type[Base],
        filters: Optional[List[BinaryExpression]] = None,
        sort: Optional[SortParam] = None,
        pagination: PaginationParam = None,
        columns: Optional[List[object]] = None,
        load_options: Optional[List[_AbstractLoad]] = None,
):
    if filters is None:
        filters = list()
    sort_by = []
    if sort:
        if isinstance(sort.by, list):
            sort_by.extend(sort.by)
        else:
            sort_by.append(sort.by)
    sort_func = asc if sort and sort.order == "asc" else desc
    if columns:
        query = select(*columns)
    else:
        query = select(entity_type)

    if load_options:
        for option in load_options:
            query = query.options(option)

    for query_filter in filters:
        query = query.where(query_filter)
    query = query.offset(pagination.offset).limit(pagination.limit) if pagination else query
    if sort_by:
        sort_columns = [nulls_last(sort_func(column)) for column in sort_by]
        query = query.order_by(*sort_columns)
    result = await session.execute(query)
    if columns:
        entities = result.all()
    else:
        entities = result.scalars().unique().all()
    return entities
