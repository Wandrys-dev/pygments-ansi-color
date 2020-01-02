# -*- coding: utf-8 -*-
"""Pygments lexer for text containing ANSI color codes."""
from __future__ import absolute_import
from __future__ import unicode_literals

import itertools
import re

import pygments.lexer
import pygments.token


C = pygments.token.Token.C
Color = pygments.token.Token.Color


_ansi_code_to_color = {
    0: 'Black',
    1: 'Red',
    2: 'Green',
    3: 'Yellow',
    4: 'Blue',
    5: 'Magenta',
    6: 'Cyan',
    7: 'White',
}

_256_colors = {
    0: '#000000',
    1: '#800000',
    2: '#008000',
    3: '#808000',
    4: '#000080',
    5: '#800080',
    6: '#008080',
    7: '#c0c0c0',
    8: '#808080',
    9: '#ff0000',
    10: '#00ff00',
    11: '#ffff00',
    12: '#0000ff',
    13: '#ff00ff',
    14: '#00ffff',
    15: '#ffffff',
    16: '#000000',
    17: '#00005f',
    18: '#000087',
    19: '#0000af',
    20: '#0000d7',
    21: '#0000ff',
    22: '#005f00',
    23: '#005f5f',
    24: '#005f87',
    25: '#005faf',
    26: '#005fd7',
    27: '#005fff',
    28: '#008700',
    29: '#00875f',
    30: '#008787',
    31: '#0087af',
    32: '#0087d7',
    33: '#0087ff',
    34: '#00af00',
    35: '#00af5f',
    36: '#00af87',
    37: '#00afaf',
    38: '#00afd7',
    39: '#00afff',
    40: '#00d700',
    41: '#00d75f',
    42: '#00d787',
    43: '#00d7af',
    44: '#00d7d7',
    45: '#00d7ff',
    46: '#00ff00',
    47: '#00ff5f',
    48: '#00ff87',
    49: '#00ffaf',
    50: '#00ffd7',
    51: '#00ffff',
    52: '#5f0000',
    53: '#5f005f',
    54: '#5f0087',
    55: '#5f00af',
    56: '#5f00d7',
    57: '#5f00ff',
    58: '#5f5f00',
    59: '#5f5f5f',
    60: '#5f5f87',
    61: '#5f5faf',
    62: '#5f5fd7',
    63: '#5f5fff',
    64: '#5f8700',
    65: '#5f875f',
    66: '#5f8787',
    67: '#5f87af',
    68: '#5f87d7',
    69: '#5f87ff',
    70: '#5faf00',
    71: '#5faf5f',
    72: '#5faf87',
    73: '#5fafaf',
    74: '#5fafd7',
    75: '#5fafff',
    76: '#5fd700',
    77: '#5fd75f',
    78: '#5fd787',
    79: '#5fd7af',
    80: '#5fd7d7',
    81: '#5fd7ff',
    82: '#5fff00',
    83: '#5fff5f',
    84: '#5fff87',
    85: '#5fffaf',
    86: '#5fffd7',
    87: '#5fffff',
    88: '#870000',
    89: '#87005f',
    90: '#870087',
    91: '#8700af',
    92: '#8700d7',
    93: '#8700ff',
    94: '#875f00',
    95: '#875f5f',
    96: '#875f87',
    97: '#875faf',
    98: '#875fd7',
    99: '#875fff',
    100: '#878700',
    101: '#87875f',
    102: '#878787',
    103: '#8787af',
    104: '#8787d7',
    105: '#8787ff',
    106: '#87af00',
    107: '#87af5f',
    108: '#87af87',
    109: '#87afaf',
    110: '#87afd7',
    111: '#87afff',
    112: '#87d700',
    113: '#87d75f',
    114: '#87d787',
    115: '#87d7af',
    116: '#87d7d7',
    117: '#87d7ff',
    118: '#87ff00',
    119: '#87ff5f',
    120: '#87ff87',
    121: '#87ffaf',
    122: '#87ffd7',
    123: '#87ffff',
    124: '#af0000',
    125: '#af005f',
    126: '#af0087',
    127: '#af00af',
    128: '#af00d7',
    129: '#af00ff',
    130: '#af5f00',
    131: '#af5f5f',
    132: '#af5f87',
    133: '#af5faf',
    134: '#af5fd7',
    135: '#af5fff',
    136: '#af8700',
    137: '#af875f',
    138: '#af8787',
    139: '#af87af',
    140: '#af87d7',
    141: '#af87ff',
    142: '#afaf00',
    143: '#afaf5f',
    144: '#afaf87',
    145: '#afafaf',
    146: '#afafd7',
    147: '#afafff',
    148: '#afd700',
    149: '#afd75f',
    150: '#afd787',
    151: '#afd7af',
    152: '#afd7d7',
    153: '#afd7ff',
    154: '#afff00',
    155: '#afff5f',
    156: '#afff87',
    157: '#afffaf',
    158: '#afffd7',
    159: '#afffff',
    160: '#d70000',
    161: '#d7005f',
    162: '#d70087',
    163: '#d700af',
    164: '#d700d7',
    165: '#d700ff',
    166: '#d75f00',
    167: '#d75f5f',
    168: '#d75f87',
    169: '#d75faf',
    170: '#d75fd7',
    171: '#d75fff',
    172: '#d78700',
    173: '#d7875f',
    174: '#d78787',
    175: '#d787af',
    176: '#d787d7',
    177: '#d787ff',
    178: '#d7af00',
    179: '#d7af5f',
    180: '#d7af87',
    181: '#d7afaf',
    182: '#d7afd7',
    183: '#d7afff',
    184: '#d7d700',
    185: '#d7d75f',
    186: '#d7d787',
    187: '#d7d7af',
    188: '#d7d7d7',
    189: '#d7d7ff',
    190: '#d7ff00',
    191: '#d7ff5f',
    192: '#d7ff87',
    193: '#d7ffaf',
    194: '#d7ffd7',
    195: '#d7ffff',
    196: '#ff0000',
    197: '#ff005f',
    198: '#ff0087',
    199: '#ff00af',
    200: '#ff00d7',
    201: '#ff00ff',
    202: '#ff5f00',
    203: '#ff5f5f',
    204: '#ff5f87',
    205: '#ff5faf',
    206: '#ff5fd7',
    207: '#ff5fff',
    208: '#ff8700',
    209: '#ff875f',
    210: '#ff8787',
    211: '#ff87af',
    212: '#ff87d7',
    213: '#ff87ff',
    214: '#ffaf00',
    215: '#ffaf5f',
    216: '#ffaf87',
    217: '#ffafaf',
    218: '#ffafd7',
    219: '#ffafff',
    220: '#ffd700',
    221: '#ffd75f',
    222: '#ffd787',
    223: '#ffd7af',
    224: '#ffd7d7',
    225: '#ffd7ff',
    226: '#ffff00',
    227: '#ffff5f',
    228: '#ffff87',
    229: '#ffffaf',
    230: '#ffffd7',
    231: '#ffffff',
    232: '#080808',
    233: '#121212',
    234: '#1c1c1c',
    235: '#262626',
    236: '#303030',
    237: '#3a3a3a',
    238: '#444444',
    239: '#4e4e4e',
    240: '#585858',
    241: '#626262',
    242: '#6c6c6c',
    243: '#767676',
    244: '#808080',
    245: '#8a8a8a',
    246: '#949494',
    247: '#9e9e9e',
    248: '#a8a8a8',
    249: '#b2b2b2',
    250: '#bcbcbc',
    251: '#c6c6c6',
    252: '#d0d0d0',
    253: '#dadada',
    254: '#e4e4e4',
    255: '#eeeeee',
}


def _token_from_lexer_state(bold, faint, fg_color, bg_color):
    """Construct a token given the current lexer state.

    We can only emit one token even though we have a multiple-tuple state.
    To do work around this, we construct tokens like "Bold.Red".
    """
    components = ()

    if bold:
        components += ('Bold',)

    if faint:
        components += ('Faint',)

    if fg_color:
        components += (fg_color,)

    if bg_color:
        components += ('BG' + bg_color,)

    if len(components) == 0:
        return pygments.token.Text
    else:
        token = Color
        for component in components:
            token = getattr(token, component)
        return token


def color_tokens(fg_colors, bg_colors, enable_256color=False):
    """Return color tokens for a given set of colors.

    Pygments doesn't have a generic "color" token; instead everything is
    contextual (e.g. "comment" or "variable"). That doesn't make sense for us,
    where the colors actually *are* what we care about.

    This function will register combinations of tokens (things like "Red" or
    "Bold.Red.BGGreen") based on the colors passed in.

    You can also define the tokens yourself, but note that the token names are
    *not* currently guaranteed to be stable between releases as I'm not really
    happy with this approach.

    Optionally, you can enable 256-color support by passing
    `enable_256color=True`. This will (very slightly) increase the CSS size,
    but enable the use of 256-color in text. The reason this is optional and
    non-default is that it requires patching the Pygments formatter you're
    using, using the ExtendedColorHtmlFormatterMixin provided by this file.
    For more details on why and how, see the README.

    Usage:

        fg_colors = bg_colors = {
            'Black': '#000000',
            'Red': '#EF2929',
            'Green': '#8AE234',
            'Yellow': '#FCE94F',
            'Blue': '#3465A4',
            'Magenta': '#c509c5',
            'Cyan': '#34E2E2',
            'White': '#ffffff',
        }
        class MyStyle(pygments.styles.SomeStyle):
            styles = dict(pygments.styles.SomeStyle.styles)
            styles.update(color_tokens(fg_colors, bg_colors))
    """
    styles = {}

    if enable_256color:
        styles[pygments.token.Token.C.Bold] = 'bold'
        styles[pygments.token.Token.C.Faint] = ''
        for i, color in _256_colors.items():
            styles[getattr(pygments.token.Token.C, 'C{}'.format(i))] = color
            styles[getattr(pygments.token.Token.C, 'BGC{}'.format(i))] = 'bg:{}'.format(color)

        for color, value in fg_colors.items():
            styles[getattr(C, color)] = value

        for color, value in bg_colors.items():
            styles[getattr(C, 'BG{}'.format(color))] = 'bg:{}'.format(value)
    else:
        for bold, faint, fg_color, bg_color in itertools.product(
                (False, True),
                (False, True),
                {None} | set(fg_colors),
                {None} | set(bg_colors),
        ):
            token = _token_from_lexer_state(bold, faint, fg_color, bg_color)
            if token is not pygments.token.Text:
                value = []
                if bold:
                    value.append('bold')
                if fg_color:
                    value.append(fg_colors[fg_color])
                if bg_color:
                    value.append('bg:' + bg_colors[bg_color])
                styles[token] = ' '.join(value)

    return styles


class AnsiColorLexer(pygments.lexer.RegexLexer):
    name = 'ANSI Color'
    aliases = ('ansi-color', 'ansi', 'ansi-terminal')
    flags = re.DOTALL | re.MULTILINE

    def __init__(self, *args, **kwargs):
        super(AnsiColorLexer, self).__init__(*args, **kwargs)
        self.reset_state()

    def reset_state(self):
        self.bold = False
        self.faint = False
        self.fg_color = None
        self.bg_color = None

    @property
    def current_token(self):
        return _token_from_lexer_state(
            self.bold, self.faint, self.fg_color, self.bg_color,
        )

    def process(self, match):
        """Produce the next token and bit of text.

        Interprets the ANSI code (which may be a color code or some other
        code), changing the lexer state and producing a new token. If it's not
        a color code, we just strip it out and move on.

        Some useful reference for ANSI codes:
          * http://ascii-table.com/ansi-escape-sequences.php
        """
        # "after_escape" contains everything after the start of the escape
        # sequence, up to the next escape sequence. We still need to separate
        # the content from the end of the escape sequence.
        after_escape = match.group(1)

        # TODO: this doesn't handle the case where the values are non-numeric.
        # This is rare but can happen for keyboard remapping, e.g.
        # '\x1b[0;59;"A"p'
        parsed = re.match(
            r'([0-9;=]*?)?([a-zA-Z])(.*)$',
            after_escape,
            re.DOTALL | re.MULTILINE,
        )
        if parsed is None:
            # This shouldn't ever happen if we're given valid text + ANSI, but
            # people can provide us with utter junk, and we should tolerate it.
            text = after_escape
        else:
            value, code, text = parsed.groups()
            if code == 'm':  # "m" is "Set Graphics Mode"
                # Special case \x1b[m is a reset code
                if value == '':
                    self.reset_state()
                else:
                    try:
                        values = [int(v) for v in value.split(';')]
                    except ValueError:
                        # Shouldn't ever happen, but could with invalid ANSI.
                        values = []

                    while len(values) > 0:
                        value = values.pop(0)
                        fg_color = _ansi_code_to_color.get(value - 30)
                        bg_color = _ansi_code_to_color.get(value - 40)
                        if fg_color:
                            self.fg_color = fg_color
                        elif bg_color:
                            self.bg_color = bg_color
                        elif value == 1:
                            self.bold = True
                        elif value == 2:
                            self.faint = True
                        elif value == 22:
                            self.bold = False
                            self.faint = False
                        elif value == 39:
                            self.fg_color = None
                        elif value == 49:
                            self.bg_color = None
                        elif value == 0:
                            self.reset_state()
                        elif value in (38, 48):
                            try:
                                five = values.pop(0)
                                color = values.pop(0)
                            except IndexError:
                                continue
                            else:
                                if five != 5:
                                    continue
                                if not 0 <= color <= 255:
                                    continue
                                color = 'C{}'.format(color)
                                if value == 38:
                                    self.fg_color = color
                                else:
                                    self.bg_color = color

        yield match.start(), self.current_token, text

    tokens = {
        # states have to be native strings
        str('root'): [
            (r'\x1b\[([^\x1b]*)', process),
            (r'[^\x1b]+', pygments.token.Text),
        ],
    }


class ExtendedColorHtmlFormatterMixin(object):

    def _get_css_classes(self, token):
        classes = super(ExtendedColorHtmlFormatterMixin, self)._get_css_classes(token)
        if token[0] == 'Color':
            classes += ' ' + ' '.join(
                self._get_css_class(getattr(C, part))
                for part in token[1:]
            )
        return classes
