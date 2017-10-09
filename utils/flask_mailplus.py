from typing import Optional

from flask import render_template

from world_manager.extensions import mail


def send_template_message(template,
                          context: Optional[dict]=None, *args, **kwargs):

    if context is None:
        context = {}

    if template is not None:
        if 'body' in kwargs or 'html' in kwargs:
            raise ValueError('Only one of template or body may be specified')
        kwargs['body'] = _try_render_template(template, **context)
        kwargs['html'] = _try_render_template(template,
                                              extension='html',
                                              **context)

    mail.send_message(*args, **kwargs)


def _try_render_template(template_path: str, extension='txt', **kwargs):
    try:
        return render_template(f'{template_path}.{extension}', **kwargs)
    except IOError:
        pass
