import os
import asyncio
from .app import app
from .seed import create_products

def run() -> None:
    # app.run(host='0.0.0.0', port=4332)
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))

def seed() -> None:
    asyncio.get_event_loop().run_until_complete(create_products())
 