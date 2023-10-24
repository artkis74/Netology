import asyncio
import aiohttp

from db import Session, SwapiPeople, engine, Base


async def download_links(links_list, client_session):
    coros = [client_session.get(link) for link in links_list]
    http_responces = await asyncio.gather(*coros)
    json_coros = [http_response.json() for http_response in http_responces]
    return await asyncio.gather(*json_coros)


async def paste_to_db(people_list):
    async with Session() as session:
        orm_objects = [SwapiPeople(json=item) for item in people_list]
        session.add_all(orm_objects)
        await session.commit()


async def get_people(people_id, client_session):
    async with client_session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json()
        film_links = json_data.get('films', [])
        species_links = json_data.get('species', [])
        starships_links = json_data.get('starships', [])
        vehicles_links = json_data.get('vehicles', [])
        films_coro = download_links(film_links, client_session)
        vehicles_coro = download_links(vehicles_links, client_session)
        starships_coro = download_links(starships_links, client_session)
        species_coro = download_links(species_links, client_session)
        fields = await asyncio.gather(films_coro, vehicles_coro, starships_coro, species_coro)
        films, vehicles, starships, species = fields
        json_data['films'] = [film['title'] for film in films]
        json_data['vehicles'] = [vehicle["name"] for vehicle in vehicles]
        json_data['species'] = [specie["name"] for specie in species]
        json_data['starships'] = [starship["name"] for starship in starships]
        return json_data


async def main():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)

    async with aiohttp.ClientSession() as client_session:
        coros = [get_people(i, client_session) for i in range(1, 21)]
        results = await asyncio.gather(*coros)

    asyncio.create_task(paste_to_db(people_list=results))

    async with aiohttp.ClientSession() as client_session:
        coros = [get_people(i, client_session) for i in range(21, 41)]
        results = await asyncio.gather(*coros)

    asyncio.create_task(paste_to_db(people_list=results))

    async with aiohttp.ClientSession() as client_session:
        coros = [get_people(i, client_session) for i in range(41, 61)]
        results = await asyncio.gather(*coros)

    asyncio.create_task(paste_to_db(people_list=results))

    async with aiohttp.ClientSession() as client_session:
        coros = [get_people(i, client_session) for i in range(61, 84)]
        results = await asyncio.gather(*coros)

    asyncio.create_task(paste_to_db(people_list=results))

    all_tasks = asyncio.all_tasks()
    all_tasks = all_tasks - {asyncio.current_task()}
    await asyncio.gather(*all_tasks)

if __name__ == "__main__":
    asyncio.run(main())


