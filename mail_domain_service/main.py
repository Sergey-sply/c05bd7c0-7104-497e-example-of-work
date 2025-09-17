import logging
import platform
from typing import Literal

import uvicorn

from mail_domain_service.config.settings import settings
from mail_domain_service.setup.setup_fastapi import create_fastapi_app

app = create_fastapi_app()


def configure_webserver() -> uvicorn.Server:

    loop: Literal["auto", "uvloop"]
    if platform == "linux":
        try:
            import uvloop

            uvloop.install()
            loop = "uvloop"
        except ModuleNotFoundError:
            loop = "auto"
    else:
        loop = "auto"
    # ===============================

    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host="0.0.0.0",
            port=settings.DOMAIN_PORT,
            workers=settings.WEBHOOK_WORKERS,
            reload=False,
            forwarded_allow_ips="*",
            proxy_headers=True,
            server_header=False,
            date_header=False,
            log_level=logging.DEBUG,
            loop=loop,
        ),
    )
    return server

if __name__ == '__main__':
    server = configure_webserver()
    server.run()