import app.services.perchai as perchai_service
from app import env


def add_first_user():
    super_admins = perchai_service.members.get_super_admins()

    if super_admins:
        return

    perchai_service.members.init_first_member(
        env.get_env(env.EnvKeys.FIRST_USER_GMAIL),
        env.get_env(env.EnvKeys.FIRST_USER_FIRST_NAME),
        env.get_env(env.EnvKeys.FIRST_USER_FIRST_NAME),
    )
