import aiohttp
import asyncio
from db import People, Session
import time

async def call_api(i, session):
    async with session.get(f'https://swapi.dev/api/people/{i}') as response:
        if response.status == 200:
            response = await response.json()
            response['id'] = i
            return response


async def add_records(records):
    session = Session()
    for record in records:
        if record:
            session.add(People(
                id = record['id'],
                name = record['name'],
                birth_year = record['birth_year'],
                eye_color = record['eye_color'],
                films = ','.join(record['films']) if record['films'] else None,
                gender = record['gender'],
                hair_color = record['hair_color'],
                height = None if record['height'] == 'unknown' else float(record['height'].replace(',', '.')),
                homeworld = record['homeworld'],
                mass = None if record['mass'] == 'unknown' else float(record['mass'].replace(',', '.')),
                skin_color = record['skin_color'],
                species = ','.join(record['species']) if record['species'] else None,
                starships = ','.join(record['starships']) if record['starships'] else None,
                vehicles = ','.join(record['vehicles']) if record['vehicles'] else None,
            ))
    session.commit()


async def main():
    async with aiohttp.ClientSession() as session:
        coros = []
        i = 1
        flag = True
        cnt = 1
        while flag:
            coro = call_api(i, session)
            coros.append(coro)
            if i % 10 == 0:
                api_responses = await asyncio.gather(*coros)
                asyncio.create_task(add_records(api_responses))
                coros = []
                while cnt < len(api_responses):
                    if api_responses[cnt] == None and cnt == len(api_responses)-1:
                        flag = False
                        break
                    cnt += 1
                cnt = 1            
            i += 1


if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main())
    print(time.time() - t1)