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
from ....general.display_config import Styles
from ....sql.transformers import Models, get_scp_colours

from rich.console import Console



# === Bar Implementations ===

def acs_bar(
            info: Models.SCP,
            console: Console | None = None
           ) -> None:
    """
    Displays an ACS-style bar for provided SCP info

    Parameters
    ----------
    info : Models.SCP
        SCP info to display
    console : Console | None, default=None
        Console to print to
    """

    # validation
    if not isinstance(info, Models.SCP):
        raise TypeError('info must be an instance of Models.SCP')
    if not isinstance(console, (Console, type(None))):
        raise TypeError('console must be an instance of Console or None')

    # inits
    base = BarTemplate(console, triple_top=True)
    colours = get_scp_colours(info)


    # === Render ===

    base._render_sep('t')

    base.render_top_line([
                          (info.display_id, None),
                          (info.display_name, None),
                          (info.display_clearance,
                           colours.clear_lvl)
                        ])

    base._render_sep('lt')

    base.render_lines([
                       (f'Containment Class: {info.display_containment}',
                        colours.cont_class),
                       (f'Disruption Class: {info.display_disruption}',
                        colours.disrupt_class),
                       (f'Secondary Class: {info.display_secondary}',
                        colours.scnd_class),
                       (f'Risk Class: {info.display_risk}',
                        colours.risk_class)
                     ])

    base._render_sep('m')

    base.render_lines([
                       (f'Assigned Site: {info.display_site}', None),
                       (f'Assigned MTF: {info.display_mtf}', None),
                     ])

    base._render_sep('b')


def mtf_bar(
            info: Models.MTF,
            console: Console | None = None
           ) -> None:
    """
    Displays a bar for provided MTF info
    Parameters
    ----------
    info : Models.MTF
        MTF info to display
    console : Console | None, default=None
        Console to print to
    """

    # validation
    if not isinstance(info, Models.MTF):
        raise TypeError('info must be an instance of Models.MTF')
    if not isinstance(console, (Console, type(None))):
        raise TypeError('console must be an instance of Console or None')

    # init base render class
    base = BarTemplate(console, triple_top=True)

    # === Render ===
    base._render_sep('t')

    base.render_top_line([
                          (info.display_name, None),
                          (info.display_nickname, None),
                          (info.display_active, None)
                        ])

    base._render_sep('lt')

    base.render_lines([
                       (f'Assigned Site: {info.display_site}', None),
                       (f'Leader: {info.display_leader}', None)
                     ])

    base._render_sep('b')


def site_bar(
            info: Models.Site,
            loc: str,
            console: Console | None = None
           ) -> None:
    """
    Displays a bar for provided Site info

    Parameters
    ----------
    info : Models.Site
        Site info to display
    loc : str
        Site location string
    console : Console | None, default=None
        Console to print to
    """

    # validation
    if not isinstance(info, Models.Site):
        raise TypeError('info must be an instance of Models.Site')
    if not isinstance(console, (Console, type(None))):
        raise TypeError('console must be an instance of Console or None')

    # init base render class
    base = BarTemplate(console)

    # === Render ===
    base._render_sep('t')

    base.render_top_line([(info.display_name, None)])

    base._render_sep('m')

    base.render_lines([
                       (f'Director: {info.display_director}', None),
                       (f'Location: {loc}', None)
                     ])

    base._render_sep('b')


def user_bar(
             info: Models.User,
             console: Console | None = None
            ) -> None:
    """
    Displays a bar for provided User info

    Parameters
    ----------
    info : Models.User
        User info to display
    console : Console | None, default=None
        Console to print to
    """

    # validation
    if not isinstance(info, Models.User):
        raise TypeError('info must be an instance of Models.User')
    if not isinstance(console, (Console, type(None))):
        raise TypeError('console must be an instance of Console or None')

    # init base render class
    base = BarTemplate(console, has_center_column=True)

    # === Render ===
    base._render_sep('t')

    base.render_top_line([(info.display_name, None)])

    base._render_sep('m')

    base.render_lines([
                       (f'Assigned Site: {info.display_site}', None),
                       (info.display_active, None),
                       (info.display_clearance,
                        Styles.CLEAR_LVL[info.clearance_lvl.id]),
                     ])

    base._render_sep('b')
