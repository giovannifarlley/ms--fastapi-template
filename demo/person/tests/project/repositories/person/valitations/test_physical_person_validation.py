from bson.objectid import ObjectId
import pytest
from datetime import datetime
from project.infrastructure.constants.mongo_collections import Collections
from project.repositories.person.models.physical_person import PhysicalPerson
from project.infrastructure.data_layer.data_layer_general import DataLayer
from project.repositories.person.valitations.physical_person import ValidatePhysicalPerson


data_layer = DataLayer(Collections.physical_person)

base_data = {
    "status": "active",
    "name": "teste",
    "last_name": "teste",
    "age": 12,
    "birthdate": datetime.now(),
    "gender": "",
    "personal_document_id": "11122233344",
    "email": "teste@teste.com",
    "phone": "+5534988887777",
}


async def create_mongo_object(input_data=base_data):
    physical_person = PhysicalPerson(**input_data)
    result = await data_layer.save(physical_person.dict(exclude_unset=True))
    return result


async def delete_mongo_object(_id: ObjectId):
    result = await data_layer.delete({"_id": _id})
    return result


@pytest.mark.asyncio
async def test_this_physical_person_has_exist():

    physical_person = await create_mongo_object()

    result = await ValidatePhysicalPerson.this_physical_person_has_exist(physical_person)

    if result:
        await delete_mongo_object(physical_person["_id"])

    assert result


@pytest.mark.asyncio
async def test_this_physical_person_has_not_exist():

    result = await ValidatePhysicalPerson.this_physical_person_has_exist({"name": "abacaxiazul"})

    assert not result


@pytest.mark.asyncio
async def test_this_physical_person_is_active():

    physical_person = await create_mongo_object()

    result = await ValidatePhysicalPerson.this_physical_person_is_active(physical_person["_id"])
    if result:
        await delete_mongo_object(physical_person["_id"])

    assert result


@pytest.mark.asyncio
async def test_this_physical_person_is_inactive():

    base_data = {
        "status": "inactive",
        "name": "teste",
        "last_name": "teste",
        "age": 12,
        "birthdate": datetime.now(),
        "gender": "",
        "personal_document_id": "33344455566",
        "email": "teste@teste.com",
        "phone": "+5534988887777",
    }

    physical_person = await create_mongo_object(base_data)

    result = await ValidatePhysicalPerson.this_physical_person_is_active(physical_person["_id"])

    if result:
        await delete_mongo_object(physical_person["_id"])

    assert not result


@pytest.mark.asyncio
async def test_this_email_exist_in_store():

    physical_person = await create_mongo_object()

    result = await ValidatePhysicalPerson.this_email_exist_in_store(base_data["email"])
    if result:
        await delete_mongo_object(physical_person["_id"])

    assert result


@pytest.mark.asyncio
async def test_this_email_not_exist_in_store():

    physical_person = await create_mongo_object()

    result = await ValidatePhysicalPerson.this_email_exist_in_store("a@a.com")
    if result:
        await delete_mongo_object(physical_person["_id"])

    assert not result


@pytest.mark.asyncio
async def test_this_document_id_exist_in_store():

    physical_person = await create_mongo_object()

    result = await ValidatePhysicalPerson.this_document_id_exist_in_store(base_data["personal_document_id"])
    if result:
        await delete_mongo_object(physical_person["_id"])

    assert result


@pytest.mark.asyncio
async def test_this_document_id_not_exist_in_store():

    physical_person = await create_mongo_object()

    result = await ValidatePhysicalPerson.this_document_id_exist_in_store("05237147000114")
    if result:
        await delete_mongo_object(physical_person["_id"])

    assert not result
