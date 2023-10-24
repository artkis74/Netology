import json
import re

from aiohttp import web


async def validate_post_user(data: dict) -> dict:
    if "password" not in data or len(data["password"]) < 6:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'password is too short or missing'}),
                               content_type='application/json')
    elif "email" not in data or not re.match(r'[^@]+@[^@]+\.[^@+]', data["email"]):
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'your email is uncorrected or missing'}),
                               content_type='application/json')
    return data


async def validate_patch_user(data: dict) -> dict:
    if 'password' in data and len(data['password']) < 6:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'password is too short'}),
                               content_type='application/json')
    elif "email" in data and not re.match(r'[^@]+@[^@]+\.[^@+]', data["email"]):
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'your email is uncorrected.'}),
                               content_type='application/json')
    return data


async def validate_post_ad(data: dict) -> dict:
    if 'description'not in data or len(data["description"]) < 6:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'description is too short or missing'}),
                               content_type='application/json')
    elif 'title' not in data or len(data["description"]) < 2:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'title is too short or missing'}),
                               content_type='application/json')
    elif 'owner' not in data:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'specify the owner'}),
                               content_type='application/json')
    return data


async def validate_patch_ad(data: dict) -> dict:
    if 'description' in data and len(data['description']) < 6:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'description is too short'}),
                               content_type='application/json')
    elif 'title' in data and len(data['title']) < 2:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'title is too short or missing'}),
                               content_type='application/json')
    elif 'owner' in data:
        raise web.HTTPConflict(text=json.dumps({'status_code': 400, 'error': 'you cannot change the owner of the ad'}),
                               content_type='application/json')
    return data
