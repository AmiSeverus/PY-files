from aiohttp import web
from asyncpg import UniqueViolationError
from gino import Gino
import json

PG_DSN = 'postgres://postgres:postgres@127.0.0.1:5432/flask'

app = web.Application()
db = Gino()

class HTTPException(web.HTTPClientError):
    def __init__(self, *args, error='', **kwargs):
        kwargs['text'] = json.dumps({'error':error})
        super().__init__(*args, **kwargs, content_type='application/json')


class BadRequest(HTTPException):
    status_code = 400


class NotFound(HTTPException):
    status_code = 404


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)

    _idx1 = db.Index('app_users_name', 'name', unique=True)


class AdvModel(db.Model):
    __tablename__='advs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    _idx1 = db.Index('app_advs_title', 'title', unique=True)


class UserView(web.View):

    async def post(self):
        user_data = await self.request.json()
        try:
            new_user = await UserModel.create(name=user_data['name'])
        except UniqueViolationError:
            raise BadRequest(error='name не уникальный')

        return web.json_response(
            {
                'user_id':new_user.id
            }
        )

class AdvView(web.View):

    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await AdvModel.get(adv_id)
        if adv is None:
            raise NotFound(error='adv не найден')
        return web.json_response({
            'id':adv.id,
            'title':adv.title,
            'text':adv.text,
            'created_at':adv.created_at,
            'user':adv.user_id
        })

    async def post(self):
        adv_data = await self.request.json()
        try:
            new_adv = await AdvModel.create(
                title = adv_data['title'],
                text = adv_data['text'],
                user_id = adv_data['user_id']
            )
        except UniqueViolationError:
            raise BadRequest(error='post не уникальный')

        return web.json_response(
            {
                'adv_id':new_adv.id
            }
        )

    async def destroy(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv = await AdvModel.get(adv_id)
        if adv is None:
            raise NotFound(error='adv не найден')
        await adv.delete()
        return web.json_response(
            {
                'response':'Adv удалено'
            }
        )

async def test(request):
    return web.json_response(
        {'hello':'world'}
    )


async def init_orm(app):
    print('start')
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
    print('finish')


app.router.add_route('GET', '/', test)
app.router.add_route('POST', '/users/', UserView)
app.router.add_route('GET', '/advs/{adv_id:\d+}', AdvView)
app.router.add_route('POST', '/advs', AdvView)
app.router.add_route('DELETE', '/advs/{adv_id:\d+}', AdvView)


app.cleanup_ctx.append(init_orm)

web.run_app(app)