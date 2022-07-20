from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

import config
from src.auth.entrypoints.routers.users import users
from src.auth.entrypoints.routers.verifications import verifications

app_config = config.get_app_settings()
mongo_config = config.get_mongo_settings()

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

    verifications_table = config.mongo_client[mongo_config.name].create_collection(
        config.MongoTables.verifications.name,
    )
    verifications_table.create_index(config.MongoTables.verifications.uuid, unique=True)
    verifications_table.create_index(config.MongoTables.verifications.email, unique=True)
    config.logger.debug('[DEBUG] Mongo tables has been created')


@app.on_event('shutdown')
async def shutdown() -> None:
    clear_mappers()
    config.logger.debug('[DEBUG] Mappers have been cleared')

    config.metadata.drop_all(bind=config.engine)
    config.logger.debug('[DEBUG] All metadata has been dropped')

    config.mongo_client.drop_database(mongo_config.name)
    config.logger.debug('[DEBUG] Mongo tables has been dropped')


app.include_router(verifications, prefix=config.get_api_url())
app.include_router(users, prefix=config.get_api_url())
