import gettext
from typing import Optional

from fastapi import Query, Request

SUPPORTED_LANGUAGES = ["en", "fa"]
DEFAULT_LANGUAGE = "en"


def get_language(request: Request, lang: Optional[str] = Query(None)):
    if lang and lang in SUPPORTED_LANGUAGES:
        return lang

    accept_language = request.headers.get("Accept-Language", DEFAULT_LANGUAGE)
    for lang_code in accept_language.split(","):
        lang_code = lang_code.split(";")[0].strip().split("-")[0]
        if lang_code in SUPPORTED_LANGUAGES:
            return lang_code

    return DEFAULT_LANGUAGE


def get_translator(lang: str):
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    translation = gettext.translation(
        "messages", localedir="app/translations", languages=[lang]
    )
    translation.install()
    return translation.gettext
