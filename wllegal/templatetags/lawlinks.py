#
# Copyright © Michal Čihař <michal@weblate.org>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from django import template
from django.utils.html import format_html

register = template.Library()

LINKS = {
    (2012, 89): "http://obcanskyzakonik.justice.cz/images/pdf/Civil-Code.pdf",
    (2000, 101): "https://www.uoou.cz/en/vismo/zobraz_dok.asp?id_ktg=1107",
    (2000, 121): "http://www.wipo.int/wipolex/en/text.jsp?file_id=126153",
    (
        2004,
        480,
    ): "https://www.uoou.cz/en/vismo/zobraz_dok.asp?id_org=200156&id_ktg=1155&archiv=0",
}

EU_LINK = "https://eur-lex.europa.eu/legal-content/ALL/?uri=celex:3{}R0{}"

GDPR_LANGS = {
    "bg",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "es",
    "et",
    "fi",
    "fr",
    "ga",
    "hr",
    "hu",
    "it",
    "lt",
    "lv",
    "mt",
    "nl",
    "pl",
    "pt",
    "ro",
    "sk",
    "sl",
    "sv",
}
GDPR_LINK = "http://www.privacy-regulation.eu/{}/{}.htm"


@register.simple_tag(takes_context=True)
def law_url(context, coll, year=None, scope=None):
    if scope == "EU":
        return EU_LINK.format(year, coll)

    if scope == "GDPR":
        lang = context["LANGUAGE_CODE"]
        if lang not in GDPR_LANGS:
            lang = "en"
        return GDPR_LINK.format(lang, coll)

    # Czech version by default
    url = f"https://www.zakonyprolidi.cz/cs/{year}-{coll}"

    # Use translation if available
    key = (year, coll)
    if context["LANGUAGE_CODE"] != "cs" and key in LINKS:
        url = LINKS[key]
    return url


@register.simple_tag(takes_context=True)
def law_link(context, coll, year=None, scope=None):
    url = law_url(context, coll, year, scope)
    return format_html('<a href="{}">{}/{}</a>', url, coll, year)
