import jinja2
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment

from project.utils import consts


def build_jinja2_environment(**options) -> Environment:
    opts = options.copy()
    opts.update(
        {
            "auto_reload": True,
            # "enable_async": True,
            "undefined": (
                jinja2.DebugUndefined if settings.DEBUG else jinja2.ChainableUndefined
            ),
        }
    )

    env = Environment(**opts)

    global_names = {
        "debug": settings.DEBUG,
        "project_name": consts.PROJECT_NAME.capitalize(),
        "static": static,
        "url": reverse,
    }

    env.globals.update(**global_names)

    return env
