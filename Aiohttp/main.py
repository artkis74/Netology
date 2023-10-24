import json

from aiohttp import web
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from db import engine, Session
from models import Base, User, Ads
from shema import validate_post_user, validate_patch_user, validate_post_ad, validate_patch_ad

app = web.Application()


async def app_context(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print('Выход')


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response


async def login(request: web.Request):
    json_data = await request.json()
    async with Session() as session:
        query = select(User).where(User.email == json_data['email'])
        result = await session.execute(query)
        user = result.scalar()
        if user and 'password' in json_data:
            is_password_correct = checkpw(json_data['password'].encode(), user.password.encode())
            if is_password_correct:
                return web.json_response({'status': 'ok'})
        raise web.HTTPUnauthorized(text=json.dumps({'error': "user or password is uncorrected"}),
                                   content_type='application/json')


async def get_user(user_id: int, session: Session):
    user = await session.get(User, user_id)
    if user is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': "user not found"}),
                               content_type='application/json')
    return user


async def get_ad(ad_id: int, session: Session):
    ad = await session.get(Ads, ad_id)
    if ad is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'message': "ad not found"}),
                               content_type='application/json')
    return ad


class UserView(web.View):
    async def get(self):
        user = await get_user(int(self.request.match_info['user_id']), self.request['session'])
        return web.json_response({"id": user.user_id, 'email': user.email,
                                  'created_time': int(user.registered_at.timestamp())})

    async def post(self):
        json_data = await validate_post_user(await self.request.json())
        json_data['password'] = hashpw(json_data['password'].encode(), salt=gensalt()).decode()
        async with Session() as session:
            user = User(**json_data)
            session.add(user)
            try:
                await session.commit()
            except IntegrityError:
                raise web.HTTPConflict(text=json.dumps({'error': 'user already exist'}),
                                       content_type='application/json')
            return web.json_response({'id': user.user_id})

    async def patch(self):
        user = await get_user(int(self.request.match_info['user_id']), self.request['session'])
        json_data = await self.request.json()
        json_data_valid = await validate_patch_user(json_data)
        json_data_valid['password'] = hashpw(json_data_valid['password'].encode(), salt=gensalt()).decode()
        for field, value in json_data_valid.items():
            setattr(user, field, value)
            self.request['session'].add(user)
            await self.request['session'].commit()
        return web.json_response({'status': 'patched'})

    async def delete(self):
        user = await get_user(int(self.request.match_info['user_id']), self.request['session'])
        await self.request['session'].delete(user)
        await self.request['session'].commit()
        return web.json_response({'status': 'deleted'})


class AdsView(web.View):
    async def get(self):
        ad = await get_ad(int(self.request.match_info['ad_id']), self.request['session'])
        return web.json_response({"id": ad.ads_id, 'title': ad.title,
                                  'created_time': int(ad.created_at.timestamp()),
                                  'description': ad.description,
                                  'owner': ad.owner})

    async def post(self):
        json_data = await validate_post_ad(await self.request.json())
        async with Session() as session:
            json_data['owner'] = int(json_data['owner'])
            ad = Ads(**json_data)
            session.add(ad)
            try:
                await session.commit()
            except IntegrityError:
                raise web.HTTPConflict(text=json.dumps({'error': 'ad already exist'}),
                                       content_type='application/json')
            return web.json_response({'id': ad.ads_id})

    async def patch(self):
        ad = await get_ad(int(self.request.match_info['ad_id']), self.request['session'])
        json_data = await self.request.json()
        json_data_valid = await validate_patch_ad(json_data)
        for field, value in json_data_valid.items():
            setattr(ad, field, value)
            self.request['session'].add(ad)
            await self.request['session'].commit()
        return web.json_response({'status': 'patched'})

    async def delete(self):
        ad = await get_ad(int(self.request.match_info['ad_id']), self.request['session'])
        await self.request['session'].delete(ad)
        await self.request['session'].commit()
        return web.json_response({'status': 'deleted'})


app.middlewares.append(session_middleware)
app.cleanup_ctx.append(app_context)
app.add_routes(
    [
        web.get('/users/{user_id:\d+}', UserView),
        web.post('/users/', UserView),
        web.patch('/users/{user_id:\d+}', UserView),
        web.delete('/users/{user_id:\d+}', UserView),
        web.get('/ads/{ad:\d+}', AdsView),
        web.post('/ads/', AdsView),
        web.patch('/ads/{ad_id:\d+}', AdsView),
        web.delete('/ads/{ad_id:\d+}', AdsView),
        web.post('/login/', login)
    ]
)

if __name__ == "__main__":
    web.run_app(app)
