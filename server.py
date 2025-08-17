import asyncio
import aiohttp
from more_itertools import chunked
from models import Session, SwapiPeople, init_orm, close_orm


async def get_people(id,session):
    try:
        response = await session.get(f"https://www.swapi.tech/api/people/{id}")
        if response.status == 200:
            json_data = await response.json()
            properties = json_data['result']["properties"]
            filtered_data = {
                "id": f'{id}',
                "birth_year": properties["birth_year"],
                "eye_color": properties["eye_color"],
                "gender": properties["gender"],
                "hair_color": properties["hair_color"],
                "homeworld": properties["homeworld"],
                "mass": properties["mass"],
                "name": properties["name"],
                "skin_color": properties["skin_color"]

            }
            #print(filtered_data)
            return filtered_data

    except Exception:
        print(f"Error fetching character {id}")
        return None

async def add_people(people_json_list):
    pass
    async with Session() as session:
        all_people = [SwapiPeople(json=person_json) for person_json in people_json_list]
        session.add_all(all_people)
        await session.commit()

MAX_REQUEST = 15

async def main():
    await init_orm()
    async with aiohttp.ClientSession() as session:
        for person_chunk in chunked(range(1,100),MAX_REQUEST):
            coros = []
            for person_id in person_chunk:
                coro = get_people(person_id, session)
                coros.append(coro)

            gather_coro = asyncio.gather(*coros, return_exceptions=True)
            result = await gather_coro
            add_people_coro = add_people(result)
            add_people_task = asyncio.create_task(add_people_coro)

    print(coros)
    await  add_people_task
    await  close_orm()

asyncio.run(main())