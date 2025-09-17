from fastapi import FastAPI

from mail_domain_service.api.v1.endpoints.mail_usage import mail_usage_router


def register_routers(app: FastAPI):
    app.include_router(mail_usage_router)