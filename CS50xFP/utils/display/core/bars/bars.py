"""
BarTemplate implementations for rendering bars

Contains
--------
- acs_bar: Renders an ACS bar
- mtf_bar: Renders an MTF bar
- site_bar: Renders a Site bar
- user_bar: Renders a User bar
"""


from .template import BarTemplate
from ...config import CLEAR_LVL_COLOURS
from ....sql.null_processors import ProcessedData as PD

from rich.console import Console

# === Bar Implementations ===

def acs_bar(
            info: PD.SCP,
            console: Console | None = None
           ) -> None:
    """
    Displays an ACS-style bar for provided SCP info

    Args:
        info (ProcessedData.SCP): SCP info to display
        console (Console | None): Console to print to
    """

    # init base render class
    base = BarTemplate(console, triple_top=True)

    # === Render ===

    base._render_sep('t')

    base.render_top_line([
                          (info.id_str, None),
                          (info.name_str, None),
                          (info.clear_lvl_str,
                           CLEAR_LVL_COLOURS[info.clear_lvl_id])
                        ])

    base._render_sep('lt')

    base.render_lines(
                      [
                       base._gen_classification_args('Containment',
                                                     info.cnt_class),
                       (f'Disruption Class: {info.disrupt_class}',
                        info.disrupt_class_hex),
                       base._gen_classification_args('Secondary',
                                                     info.scnd_class),
                       (f'Risk Class: {info.risk_class}',
                        info.risk_class_hex)
                      ],
    )

    base._render_sep('m')

    base.render_lines([
                       (f'Site Responsible: {info.site_resp}', None),
                       (f'Assigned MTF: {info.mtf_str}', None)
                     ])

    base._render_sep('b')


def mtf_bar(
            info: PD.MTF,
            console: Console | None = None
           ) -> None:
    """
    Displays a bar for provided MTF info
    Args:
        info (ProcessedData.MTF): MTF info to display
        console (Console | None): Console to print to
    """

    # init base render class
    base = BarTemplate(console, triple_top=True)

    # === Render ===
    base._render_sep('t')

    base.render_top_line([
                          (info.name_str, None),
                          (info.nickname, None),
                          (info.active, None)
                        ])

    base._render_sep('lt')

    base.render_lines([
                       (f'Assigned Site: {info.site}', None),
                       (f'Leader: {info.leader_str}', None)
                     ])

    base._render_sep('b')


def site_bar(
            info: PD.Site,
            loc: str,
            console: Console | None = None
           ) -> None:
    """
    Displays a bar for provided Site info
    Args:
        info (ProcessedData.Site): Site info to display
        loc (str): Location of the site
        console (Console | None): Console to print to
    """

    # init base render class
    base = BarTemplate(console)

    # === Render ===
    base._render_sep('t')

    base.render_top_line([(info.name_str, None)])

    base._render_sep('m')

    base.render_lines([
                       (f'Director: {info.director_str}', None),
                       (f'Location: {loc}', None)
                     ])

    base._render_sep('b')


def user_bar(
             info: PD.User,
             console: Console | None = None
            ) -> None:
    """
    Displays a bar for provided User info
    Args:
        info (ProcessedData.User): User info to display
        console (Console | None): Console to print to
    """

    # init base render class
    base = BarTemplate(console)

    # === Render ===
    base._render_sep('t')

    base.render_top_line([(info.name_str, None)])

    base._render_sep('m')

    base.render_lines([
                       (f'Assigned Site: {info.site}', None),
                       (f'Clearance Level: {info.clearance_str}',
                        CLEAR_LVL_COLOURS[info.clearance_id])
                     ])

    base._render_sep('b')
