from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

import config
from src.auth.entrypoints.routers.users import users
from src.auth.entrypoints.routers.verifications import verifications

app_config = config.get_app_settings()

app = FastAPI(
    title=app_config.title,
    version=app_config.version,
    description=app_config.description,
)


@app.on_event('startup')
async def startup() -> None:
    config.start_mappers()
    config.logger.debug('[DEBUG] Mappers have been mapped')

    config.metadata.create_all(bind=config.engine)
    config.logger.debug('[DEBUG] All metadata has been created')


@app.on_event('shutdown')
async def shutdown() -> None:
    clear_mappers()
    config.logger.debug('[DEBUG] Mappers have been cleared')

    config.metadata.drop_all(bind=config.engine)
    config.logger.debug('[DEBUG] All metadata has been dropped')


app.include_router(verifications, prefix=config.get_api_url())
app.include_router(users, prefix=config.get_api_url())
