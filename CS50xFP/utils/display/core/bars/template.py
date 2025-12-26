"""
BarTemplate: Template for user/site/SCP/MTF display bars
"""

from rich.console import Console
from typing import Literal

from .lines import print_piped_line, format_centered_text as fc_text
from ....general.display_config import Bars, Styles, Terminal as Terminal
from ....general.exceptions import field_error



class BarTemplate:
    """
    Template for rendering user/site/SCP/MTF display bars

    Parameters
    ----------
    console : Console | None
        Console to print to
    has_center_column : bool
        does the bar has a center column
    width : int, default=General.MIN_TERM_WIDTH
        Total width of the bar
    triple_top : bool
        whether or not to use the ACS/MTF top bar style
        (3 columns on the top row)
    double_sep_top : bool
        alternate render for ACS/MTF top row separator
        ** NOT IMPLEMENTED **
    """

    def __init__(self,
                 console: Console | None = None,
                 has_center_column: bool = False,
                 width: int = Terminal.MIN_TERM_WIDTH,
                 triple_top: bool = False,
                 double_sep_top: bool = False
                ) -> None:

        # === Validation ===

        if double_sep_top:
            raise NotImplementedError(
                'double_sep_top ACS/MTF bar not yet implemented'
            )

        if triple_top and has_center_column:
            raise ValueError(
                             'ACS & MTF bars must not have center columns'
                            )



        # === Init basic self vars ===

        self.triple_top = triple_top                              # whether or not to use the ACS/MTF top bar style
        self.width = width - 2                                    # width of bar text area
        self.console = console if console else Console()          # Console to print to
        self.cols: Literal[2, 3] = 3 if has_center_column else 2  # number of columns
        self.double_sep_top = False                               # alternate render for ACS/MTF top row separator
        self.sides: list[Literal['l', 'c', 'r']]                  # sides to use for piped lines

        if has_center_column:
            self.sides = ['l', 'c', 'r']
        else:
            self.sides = ['l', 'r']


        # === Handle length calculation ===
        pipe_space = 1 if self.cols == 3 else 2  # space taken by pipes in the bar
        col_len = (self.width - pipe_space) // self.cols


        # validation
        if (col_len * self.cols) + pipe_space != self.width:
            raise field_error(
                             'width', width,
                             f'a multiple of {self.cols} plus {pipe_space}'
                            )

        self.lengths = [col_len] * self.cols  # lengths of each column
        rept = '═' * col_len

        # adjust middle col to preserve total width
        if self.cols == 3:
            middle_col_len = col_len - 1


            middle = '═' * middle_col_len
            self.middle_col_len = middle_col_len
            self.lengths[1] = middle_col_len

        # make pylance happy
        else:
            middle = rept



        # === Handle column stuff ===

        if triple_top: # ACS & MTF bars
            l_r    = '═' * Bars.TOP_SECTIONS[0]              # left & right seps
            center = '═' * ((Bars.TOP_SECTIONS[1] - 2) // 2) # account for pipes

            if self.double_sep_top:
                self.sep = {
                            't':  f'╔{l_r}╗╔{center}══{center}╗╔{l_r}╗',
                            'lt': f'╠{l_r}╝╚{center}╗╔{center}╝╚{l_r}╣',
                            'm':  f'╠{l_r}══{center}╣╠{l_r}══{center}╣',
                            'b':  f'╚{l_r}══{center}╝╚{l_r}══{center}╝'
                           }

            else:
                self.sep = {
                            't':  f'╔{l_r}╦{center}══{center}╦{l_r}╗',
                            'lt': f'╠{l_r}╩{center}╗╔{center}╩{l_r}╣',
                            'm':  f'╠{l_r}═{center}╣╠{l_r}═{center}╣',
                            'b':  f'╚{l_r}═{center}╝╚{l_r}═{center}╝'
                           }

        elif self.cols == 3: # User bars
            self.sep = {
                        't': f'╔{rept}═{middle}═{rept}╗',
                        'm': f'╠{rept}╦{middle}╦{rept}╣',
                        'b': f'╚{rept}╩{middle}╩{rept}╝'
                       }

        else: # Site bars
            self.sep = {
                        't': f'╔{rept}══{rept}╗',
                        'm': f'╠{rept}╗╔{rept}╣',
                        'b': f'╚{rept}╝╚{rept}╝'
                       }




    # === Helper Method ===

    def _render_sep(self,
                    pos: Literal['t', 'lt', 'm', 'b']
                   ) -> None:
        """
        Renders a separator line

        Parameters
        ----------
        pos : {'t', 'lt', 'm', 'b'}
            Position of separator
            (Can not be 'lt' if `self.triple_top = False`)
        """

        # validation
        if pos == 'lt' and not self.triple_top:
            raise field_error(
                'pos', pos,
                "'t', 'm', or 'b' ('lt' only valid for triple_top bars)"
            )

        if pos not in self.sep:
            if self.triple_top:
                raise field_error('pos', pos, "'t', 'lt', 'm', or 'b'")
            else:
                raise field_error('pos', pos, "'t', 'm', or 'b'")

        # render
        self.console.print(f'{Terminal.LEFT_PADDING}{self.sep[pos]}')



    # === Main Methods ===

    def render_top_line(self,
                        text_styles: list[tuple[str, str | None]]
                       ) -> None:
        """
        Renders the top line for bars

        Parameters
        ----------
        text_styles: list[tuple[str, str | None]]
            Texts and their styles for the columns of the top bar (left, center, right)

        Raises
        ------
        ValueError
            - If `len(text_styles)` is not 3 when `triple_top` is True
            - If `len(text_styles)` is not 1 when `triple_top` is False
            - If any tuple in `text_styles` does not have length 2
        """
        t_s = text_styles
        expected_len = 3 if self.triple_top else 1

        # Validation
        if len(t_s) != expected_len:
            raise field_error(
                            'text_styles', t_s,
                            f'{expected_len} tuples, got {len(t_s)}'
                            )

        if not all(len(t) == 2 for t in t_s):
            raise field_error(
                            'text_styles', t_s,
                            f'All tuples must have length 2'
                            )


        # === Render ===

        if not self.triple_top:
            self.console.print(
                Terminal.LEFT_PADDING, "║",
                *fc_text(t_s[0][0], 'c', t_s[0][1], self.width),
                sep=''
            )

        else:
            self.console.print(
                Terminal.LEFT_PADDING, '║',

                *fc_text(t_s[0][0], 'l', t_s[0][1], Bars.TOP_SECTIONS[0]),
                *fc_text(t_s[1][0], 'c', t_s[1][1], Bars.TOP_SECTIONS[1]),
                *fc_text(t_s[2][0], 'r', t_s[2][1], Bars.TOP_SECTIONS[2]),

                sep=''
            )

    def render_lines(self,
                    text_styles: list[tuple[str, str | None]],
                   ) -> None:
        """
        Renders lines with provided texts and stylings
        using print_piped_line from ./lines.py

        Parameters
        ----------
        text_styles : list[tuple[str, str | None]]
            Texts to render and their styles
        """

        # === Input Validation ===
        if len(text_styles) % self.cols != 0:
            raise field_error(
                             'text_styles', text_styles,
                             f'a multiple of {self.cols}'
                            )

        if not all(len(t) == 2 for t in text_styles):
            raise field_error(
                            'text_styles', text_styles,
                            f'All tuples must have length 2'
                            )


        # === Render ===
        for i in range(len(text_styles)):
            tmp = i % len(self.sides)

            print_piped_line(
                             console=self.console,
                             string=text_styles[i][0],
                             side=self.sides[tmp],
                             style=text_styles[i][1],
                             content_width=self.lengths[tmp],
                             cols=self.cols,
                            )
