#!/usr/bin/env python3
'''style_check.py - flag places where a physics-paper draft drifts from the house style.

The style is that of five papers from Daniel Whiteson's group (TOP 2311.00121, CHARM 2609.32054,
TIME 2605.11071, HNL 2510.16107, TRACK 2505.02937). Each threshold and word list is tied to a
measured norm of those papers; README.md gives the numbers and the limits of every check.

Usage
  python3 style_check.py draft.tex                 Markdown report on stdout
  python3 style_check.py draft.md --max-words 35
  python3 style_check.py - < draft.txt             read stdin (the format is sniffed)
  python3 style_check.py draft.tex --only long,verb,acronyms
  python3 style_check.py draft.tex --json > report.json
  python3 style_check.py draft.tex --dump          print the sentences the checker saw

Checks (give the number or the name to --only)
  1 long        sentences above --max-words (default 40), and the length distribution
  2 verb        main verb after word 12 (a long opening phrase or a long subject)
  3 connectors  sentence-initial Moreover/Furthermore/Thus/..., stock phrases, 'in order to'
  4 vocab       inflated words and phrases (utilize, leverage, ...) with plain alternatives
  5 hype        hype and intensifiers (novel, crucial, very, ...); 'significant' with no number
  6 vague       improve/better/enhance/outperform/gain with no number and no named baseline
  7 acronyms    acronyms used before their definition, or never defined
  8 terms       one term in several forms: hyphen/space/closed, capitals, US/UK spelling
  9 figures     figure and table references: first-citation order, unreferenced or missing labels
  10 passive    passive-voice share by part (report); flags an abstract above 30 percent

Python 3 standard library only.
'''
import argparse
import json
import os
import re
import statistics
import sys
import unicodedata
from collections import Counter, defaultdict

# =============================================================================================
# Corpus norms (five reference papers). Sources: analysis/lens-sentences.md (tables 2.1, 2.2,
# 2.6), analysis/lens-layering.md (sections 4-5) and analysis/connector_counts_output.md.
# =============================================================================================
# part: (sentences, median, mean, p90, % <=12 words, % >30, % >40)
CORPUS_LEN = {
    'abstract': (33, 25, 26.8, 43, 6.1, 33.3, 15.2),
    'intro': (126, 23, 25.3, 39, 10.3, 27.8, 8.7),
    'body': (616, 23, 25.4, 41, 10.4, 27.4, 10.6),
    'concl': (90, 26, 27.1, 42, 8.9, 31.1, 12.2),
    'app': (120, 22, 23.9, 41, 15.8, 26.7, 10.8),
    'prose': (985, 23, 25.4, 41, 10.8, 27.9, 10.7),
    'caption': (169, 18, 19.5, 33, 27.2, 14.2, 2.4),
}
# % of sentences with a passive, by part
CORPUS_PASSIVE = {'abstract': 18.2, 'intro': 28.6, 'body': 39.9, 'concl': 26.7, 'app': 29.2,
                  'prose': 35.2, 'caption': 22.5}
CORPUS_WE_PER_1K = 13.6
# How a figure reference sits in a body sentence (64 references in the corpus bodies)
CORPUS_FIG_FORMS = [('passive', 'X is shown in Fig. N', 26), ('see', 'claim; see Fig. N', 13),
                    ('subject', 'Figure N shows X', 7), ('in_we', 'In Fig. N, we show X', 6),
                    ('as_seen', 'as can be seen in Fig. N', 1), ('paren', 'bare (Fig. N)', 1),
                    ('other', 'other or prepositional', 10)]
# Flags per 1,000 words when this script runs on the plain text of the five papers
# (pdftotext output, 28,112 words, 235 flags; see README.md, Validation).
CORPUS_RATE = {1: 3.3, 2: 0.9, 3: 0.4, 4: 0.4, 5: 1.6, 6: 0.1, 7: 0.2, 8: 1.1, 9: 0.3, 10: 0.0}
CORPUS_RATE_TOTAL = 8.4

CHECKS = [
    (1, 'long', 'Long sentences'),
    (2, 'verb', 'Late main verb'),
    (3, 'connectors', 'Stock connectors and filler openers'),
    (4, 'vocab', 'Inflated words and phrases'),
    (5, 'hype', 'Hype and intensifiers'),
    (6, 'vague', 'Vague result claims'),
    (7, 'acronyms', 'Acronyms'),
    (8, 'terms', 'Terminology variants'),
    (9, 'figures', 'Figure and table references'),
    (10, 'passive', 'Passive voice'),
]

PART_LABEL = {'abstract': 'abstract', 'intro': 'introduction', 'body': 'body', 'concl': 'conclusions',
              'app': 'appendix', 'caption': 'caption', 'footnote': 'footnote', 'prose': 'all prose'}

# =============================================================================================
# Placeholders (math, citations, references, code) and structure markers
# =============================================================================================
PH_O, PH_C = '\ue000', '\ue001'
PH_RE = re.compile('\ue000(\\d+)\ue001')
MK_O, MK_C = '\ue010', '\ue011'
MK_RE = re.compile('\ue010([^\ue011]*)\ue011')
MK_BR = MK_O + 'B' + MK_C


def mk_head(level, title):
    title = re.sub('[\n\ue010\ue011|]', ' ', title)
    return '%sH%d|%s%s' % (MK_O, level, re.sub(r'\s+', ' ', title).strip(), MK_C)


def mk_part(part):
    return MK_O + 'P' + part + MK_C


FILL = '\ue012'      # marks a line kept only for line numbering; it does not end a paragraph


def keep_nl(s):
    return ('\n' + FILL) * s.count('\n')


def blank_nl(s):
    return '\n' * s.count('\n')


class Store:
    '''Holds what each placeholder stands for.'''

    def __init__(self):
        self.items = []

    def add(self, kind, content='', **kw):
        d = dict(kind=kind, content=content, weight=1)
        d.update(kw)
        self.items.append(d)
        return '%s%d%s' % (PH_O, len(self.items) - 1, PH_C)

    def __getitem__(self, i):
        return self.items[int(i)]


MATH_SPLIT = re.compile(
    r'\\(?:to|rightarrow|leftarrow|leftrightarrow|longrightarrow|mapsto|times|cdot|pm|mp|sim|approx|'
    r'simeq|lesssim|gtrsim|le|ge|leq|geq|ll|gg|ne|neq|propto|equiv|in|otimes|oplus|quad|qquad)(?![A-Za-z])'
    r'|[=<>+\-−/,;]|\s+')
SUBSUP = re.compile(r'[_^]\s*(?:\{[^{}]*\}|\\[A-Za-z]+|.)')


def math_weight(c):
    '''Approximate number of words the expression adds (the corpus counted math tokens as words).'''
    c = re.sub(r'\\(?:mathrm|mathbf|mathit|mathcal|mathsf|mathbb|text|textrm|textit|rm|bf|it|'
               r'operatorname|boldsymbol|bm)(?![A-Za-z])', '', c)
    c = SUBSUP.sub('', c)
    c = re.sub(r'\\(?:left|right|bigl|bigr|Bigl|Bigr|big|Big|bigg|Bigg)', '', c)
    k = sum(1 for p in MATH_SPLIT.split(c) if p and re.search(r'[A-Za-z0-9]', p))
    return max(1, min(k, 8))


def math_has_value(c):
    '''True when the expression holds a number outside sub- and superscripts.'''
    if re.search(r'\\sqrt\s*\{?\s*s\s*\}?\s*=|fb\s*\}?\s*\^\s*\{?\s*-\s*1|\\(?:i|inv)fb', c):
        return False                      # collision energy or luminosity: context, not a result
    c = SUBSUP.sub('', c)
    c = re.sub(r'\\[A-Za-z]+', '', c)
    return bool(re.search(r'\d', c))


def shorten(s, n):
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(' ', 1)[0]
    if len(cut) < n * 0.6:
        cut = s[:n]
    return cut + ' …'


def render(s, store, mode):
    '''mode 'plain': text the checks read; mode 'show': text the report prints.'''
    def rep(m):
        it = store[m.group(1)]
        k = it['kind']
        if mode == 'plain':
            if k == 'M':
                return '0' if it.get('value') else 'x'
            if k == 'E':
                return 'x'
            if k == 'C':
                return it.get('plain', '')
            if k == 'R':
                return it.get('plain', 'N')
            return 'x'
        if k == 'M':
            return '$' + shorten(it['content'], 30) + '$'
        if k == 'E':
            return '[equation]'
        if k == 'C':
            return it.get('show', '[cite]')
        if k == 'R':
            return it.get('show', '[ref]')
        return shorten(it.get('show', it['content']), 30)
    return PH_RE.sub(rep, s)


# =============================================================================================
# LaTeX
# =============================================================================================
CMD_RE = re.compile(r'\\([A-Za-z@]+|.)', re.S)
BEGIN_RE = re.compile(r'\\begin\s*\{([^}]*)\}')
ENV_RE = re.compile(r'\\(begin|end)\s*\{([^}]*)\}')

CITE_CMDS = {'cite', 'citep', 'citet', 'citealp', 'citealt', 'citeauthor', 'citeyear', 'citenum', 'Cite',
             'Citep', 'Citet', 'parencite', 'Parencite', 'textcite', 'Textcite', 'autocite', 'Autocite',
             'footcite', 'supercite', 'fullcite', 'smartcite', 'cites', 'citealias'}
TEXT_CITE = {'citet', 'Citet', 'citeauthor', 'textcite', 'Textcite'}
REF_CMDS = {'ref', 'eqref', 'autoref', 'Autoref', 'cref', 'Cref', 'vref', 'Vref', 'pageref', 'nameref',
            'subref', 'labelcref', 'cpageref', 'Cpageref', 'fref', 'Fref', 'figref', 'Figref', 'tabref',
            'secref', 'eqnref', 'appref', 'crefrange', 'Crefrange'}
NAMED_REF = {'autoref', 'Autoref', 'cref', 'Cref', 'vref', 'Vref', 'fref', 'Fref', 'figref', 'Figref',
             'tabref', 'secref', 'eqnref', 'appref', 'labelcref', 'crefrange', 'Crefrange'}
SECTION_LEVELS = {'part': 0, 'chapter': 0, 'section': 1, 'subsection': 2, 'subsubsection': 3,
                  'paragraph': 4, 'subparagraph': 5}
KEEP_ARG = {'textbf', 'textit', 'emph', 'textsl', 'textsc', 'texttt', 'textrm', 'textsf', 'textup',
            'textmd', 'textnormal', 'underline', 'uline', 'mbox', 'hbox', 'fbox', 'text', 'textsuperscript',
            'textsubscript', 'enquote', 'hl', 'ul', 'mathrm', 'mathbf', 'mathit', 'boldsymbol', 'bm',
            'MakeUppercase', 'MakeLowercase', 'uppercase', 'lowercase', 'NoCaseChange', 'textls', 'strong',
            'centerline', 'leftline', 'rightline', 'emphasize', 'makebox', 'framebox', 'noindent'}
KEEP_LAST = {'textcolor': 2, 'colorbox': 2, 'foreignlanguage': 2, 'raisebox': 2, 'scalebox': 2,
             'resizebox': 3, 'rotatebox': 2, 'parbox': 2, 'fcolorbox': 3}
DROP_ARGS = {'vspace': 1, 'hspace': 1, 'includegraphics': 1, 'input': 1, 'include': 1, 'bibliography': 1,
             'bibliographystyle': 1, 'setlength': 2, 'addtolength': 2, 'setcounter': 2, 'addtocounter': 2,
             'stepcounter': 1, 'refstepcounter': 1, 'usepackage': 1, 'RequirePackage': 1, 'documentclass': 1,
             'pagestyle': 1, 'thispagestyle': 1, 'pagenumbering': 1, 'color': 1, 'fontsize': 2,
             'linespread': 1, 'graphicspath': 1, 'hypersetup': 1, 'affiliation': 1, 'altaffiliation': 1,
             'author': 1, 'email': 1, 'date': 1, 'title': 1, 'keywords': 1, 'pacs': 1, 'preprint': 1,
             'thanks': 1, 'collaboration': 1, 'institute': 1, 'received': 1, 'accepted': 1, 'published': 1,
             'address': 1, 'phantom': 1, 'hphantom': 1, 'vphantom': 1, 'rule': 2, 'todo': 1, 'marginpar': 1,
             'sout': 1, 'xout': 1, 'addbibresource': 1, 'nocite': 1, 'newcounter': 1, 'definecolor': 3,
             'captionsetup': 1, 'setstretch': 1, 'tikzset': 1, 'pgfplotsset': 1, 'urlstyle': 1,
             'hyphenation': 1, 'theoremstyle': 1, 'newtheorem': 2, 'numberwithin': 2, 'bibitem': 1,
             'titlerunning': 1, 'authorrunning': 1, 'newlength': 1, 'settowidth': 2, 'arxiv': 1, 'doi': 1,
             'tnotetext': 1, 'fntext': 1, 'cortext': 1, 'ead': 1, 'orcid': 1, 'subjclass': 1,
             'shorttitle': 1, 'shortauthors': 1, 'enlargethispage': 1, 'affil': 1, 'noaffiliation': 0,
             'vskip': 0, 'hskip': 0, 'kern': 0, 'putbib': 0, 'subfile': 1, 'externaldocument': 1,
             'pdfbookmark': 2, 'bookmark': 1, 'graphicspath*': 1, 'adjustbox': 1, 'pgfmathsetmacro': 2}
DIMEN_CMDS = {'vskip', 'hskip', 'kern', 'mskip'}
DROP0 = set('''centering raggedright raggedleft indent maketitle clearpage cleardoublepage newpage
pagebreak nopagebreak linebreak nolinebreak allowbreak smallskip medskip bigskip hfill vfill hfil vfil
protect relax xspace nonumber notag leavevmode null ignorespaces displaystyle textstyle scriptstyle bf it
em rm sf tt sc sl up md bfseries itshape mdseries rmfamily sffamily ttfamily scshape slshape upshape
normalfont small footnotesize scriptsize tiny large Large LARGE huge Huge normalsize boldmath unboldmath
FloatBarrier printbibliography tableofcontents listoffigures listoftables frontmatter mainmatter
backmatter onecolumngrid twocolumngrid balance sloppy fussy selectfont strut hline toprule midrule
bottomrule linenumbers nolinenumbers makeatletter makeatother endinput noaffiliation footnotemark
newline quad qquad enspace thinspace negthinspace hspacefill break nobreak samepage raggedbottom
flushbottom appendixpage addappheadtotoc clearpage pagebreak'''.split())
SPACE0 = {'newline', 'quad', 'qquad', 'enspace', 'thinspace', 'break', 'hfill'}
TEXT_SYMBOLS = {
    'ldots': '…', 'dots': '…', 'textellipsis': '…', 'textbackslash': '\\', 'LaTeX': 'LaTeX', 'TeX': 'TeX',
    'textendash': '–', 'textemdash': '—', 'textdegree': '°', 'degree': '°', 'textmu': 'µ', 'textpm': '±',
    'texttimes': '×', 'ie': 'i.e.', 'eg': 'e.g.', 'etal': 'et al.', 'cf': 'cf.', 'vs': 'vs.', 'wrt': 'w.r.t.',
    'ss': 'ß', 'o': 'ø', 'O': 'Ø', 'ae': 'æ', 'AE': 'Æ', 'oe': 'œ', 'OE': 'Œ', 'aa': 'å', 'AA': 'Å',
    'l': 'ł', 'L': 'Ł', 'i': 'ı', 'j': 'ȷ', 'S': '§', 'P': '¶', 'dag': '†', 'ddag': '‡', 'copyright': '©',
    'textregistered': '®', 'texttrademark': '™', 'checkmark': '✓', 'textquotedblleft': '“',
    'textquotedblright': '”', 'textquoteleft': '‘', 'textquoteright': '’', 'slash': '/', 'textless': '<',
    'textgreater': '>', 'textbar': '|', 'today': 'today', 'percent': '%', 'textpercent': '%',
    'GeV': 'GeV', 'TeV': 'TeV', 'MeV': 'MeV', 'keV': 'keV', 'eV': 'eV', 'PeV': 'PeV', 'fb': 'fb', 'pb': 'pb',
    'nb': 'nb', 'ifb': 'fb−1', 'ipb': 'pb−1', 'invfb': 'fb−1', 'invpb': 'pb−1', 'fbinv': 'fb−1',
    'pbinv': 'pb−1', 'iab': 'ab−1', 'mm': 'mm', 'cm': 'cm', 'ns': 'ns', 'ps': 'ps', 'GeVc': 'GeV/c',
    'TeVc': 'TeV/c', 'ttbar': 'tt̄', 'textasciitilde': '~', 'textunderscore': '_', 'textasciicircum': '^',
    'xspace': '', 'acknowledgments': '', 'acknowledgements': '',
}
UNIT_MAP = {'giga': 'G', 'tera': 'T', 'mega': 'M', 'kilo': 'k', 'milli': 'm', 'micro': 'µ', 'nano': 'n',
            'pico': 'p', 'femto': 'f', 'atto': 'a', 'centi': 'c', 'peta': 'P', 'exa': 'E',
            'electronvolt': 'eV', 'eV': 'eV', 'GeV': 'GeV', 'TeV': 'TeV', 'MeV': 'MeV', 'keV': 'keV',
            'barn': 'b', 'metre': 'm', 'meter': 'm', 'second': 's', 'percent': '%', 'radian': 'rad',
            'tesla': 'T', 'kelvin': 'K', 'hertz': 'Hz', 'gram': 'g', 'kilogram': 'kg', 'joule': 'J',
            'watt': 'W', 'volt': 'V', 'ampere': 'A', 'degree': '°', 'minute': 'min', 'hour': 'h', 'day': 'd',
            'year': 'yr', 'fb': 'fb', 'pb': 'pb', 'per': '/', 'inverse': '', 'squared': '^2', 'cubic': '^3',
            'square': '', 'clight': 'c', 'speedoflight': 'c', 'mm': 'mm', 'cm': 'cm', 'ns': 'ns'}
SIUNITX = {'SI', 'qty', 'si', 'unit', 'num', 'SIrange', 'qtyrange', 'numrange', 'ang', 'SIlist', 'numlist'}
ACCENTS = {'\'': '\u0301', '`': '\u0300', '^': '\u0302', '\x22': '\u0308', '~': '\u0303', '=': '\u0304',
           '.': '\u0307', 'u': '\u0306', 'v': '\u030c', 'H': '\u030b', 'c': '\u0327', 'k': '\u0328',
           'r': '\u030a', 'b': '\u0331', 'd': '\u0323'}
SPECIAL = {'\\': ' ', ',': ' ', ';': ' ', ':': ' ', '!': '', ' ': ' ', '\n': ' ', '\t': ' ', '%': '%',
           '&': '&', '#': '#', '_': '_', '$': '$', '{': '{', '}': '}', '-': '', '/': '', '@': '', '|': '‖',
           '>': ' ', '<': ' ', '*': ''}
MACRO_DEF_CMDS = {'newcommand', 'renewcommand', 'providecommand', 'DeclareRobustCommand', 'def', 'gdef',
                  'edef', 'xdef', 'let', 'newenvironment', 'renewenvironment', 'DeclareMathOperator', 'newif',
                  'NewDocumentCommand', 'RenewDocumentCommand', 'DeclareDocumentCommand',
                  'ProvideDocumentCommand', 'newrobustcmd', 'renewrobustcmd'}
MATH_ENVS = {'equation', 'align', 'alignat', 'eqnarray', 'gather', 'multline', 'flalign', 'displaymath',
             'math', 'dmath', 'dgroup', 'IEEEeqnarray', 'empheq', 'darray', 'dseries'}
FLOAT_ENVS = {'figure': 'fig', 'wrapfigure': 'fig', 'sidewaysfigure': 'fig', 'SCfigure': 'fig',
              'figwindow': 'fig', 'table': 'tab', 'wraptable': 'tab', 'sidewaystable': 'tab', 'SCtable': 'tab',
              'longtable': 'tab', 'tabwindow': 'tab'}
BLANK_ENVS = {'tabular', 'tabularx', 'tabulary', 'array', 'supertabular', 'xtabular', 'verbatim', 'Verbatim',
              'lstlisting', 'minted', 'comment', 'thebibliography', 'tikzpicture', 'pgfpicture', 'picture',
              'axis', 'filecontents', 'titlepage', 'keyword', 'keywords', 'tabu', 'tblr', 'algorithm',
              'algorithmic', 'algorithm2e', 'pycode', 'code', 'fmffile', 'feynman', 'circuitikz',
              'references', 'bibliography', 'frontmatter', 'IEEEkeywords', 'CCSXML', 'tikzcd'}
LIST_ENVS = {'itemize', 'enumerate', 'description', 'list', 'compactitem', 'compactenum', 'asparaenum',
             'asparaitem', 'compactdesc'}
DROP_PART_ENVS = {'acknowledgments', 'acknowledgements', 'acknowledgment', 'acknowledgement', 'acks',
                  'funding'}
APPENDIX_ENVS = {'appendices', 'appendix', 'subappendices'}
ENV_ARGS = {'minipage': 1, 'multicols': 1, 'wrapfigure': 2, 'wraptable': 2, 'subfigure': 1, 'subtable': 1,
            'adjustbox': 1, 'list': 2, 'alignat': 1, 'tabularx': 2, 'tabular': 1, 'array': 1, 'tcolorbox': 0,
            'longtable': 1, 'figwindow': 1, 'mdframed': 0}
PREFIX_KIND = {'fig': 'fig', 'figure': 'fig', 'tab': 'tab', 'table': 'tab', 'tbl': 'tab', 'eq': 'eq',
               'eqn': 'eq', 'equation': 'eq', 'sec': 'sec', 'section': 'sec', 'ssec': 'sec', 'subsec': 'sec',
               'chap': 'sec', 'ch': 'sec', 'app': 'app', 'appx': 'app', 'apx': 'app', 'appendix': 'app'}
KIND_WORD = {'fig': 'Fig.', 'tab': 'Table', 'eq': 'Eq.', 'sec': 'Sec.', 'app': 'App.'}


def strip_tex_comments(t):
    out = []
    for line in t.split('\n'):
        i, n, cut = 0, len(line), None
        while i < n:
            ch = line[i]
            if ch == '\\':
                i += 2
                continue
            if ch == '%':
                cut = i
                break
            i += 1
        if cut is None:
            out.append(line)
        else:
            out.append(line[:cut] if line[:cut].strip() else FILL)
    return '\n'.join(out)


def match_brace(s, i):
    '''s[i] == '{'. Index just past the matching '}', or -1.'''
    depth, n, j = 0, len(s), i
    while j < n:
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return -1


def match_bracket(s, i):
    '''s[i] == '['. Index just past the matching ']' (braces inside are skipped), or -1.'''
    n, j = len(s), i + 1
    while j < n:
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            k = match_brace(s, j)
            if k < 0:
                return -1
            j = k
            continue
        if c == ']':
            return j + 1
        if c == '\n' and s[j + 1:j + 2] == '\n':
            return -1
        j += 1
    return -1


def skip_ws(s, j):
    n, nl = len(s), 0
    while j < n and s[j] in ' \t\n':
        if s[j] == '\n':
            nl += 1
            if nl > 1:
                break
        j += 1
    return j


def read_opt(s, j):
    if j < len(s) and s[j] == '[':
        e = match_bracket(s, j)
        if e > 0:
            return s[j + 1:e - 1], e
    return None, j


def read_arg(s, j):
    k = skip_ws(s, j)
    if k < len(s) and s[k] == '{':
        e = match_brace(s, k)
        if e > 0:
            return s[k + 1:e - 1], e
    return None, j


def read_tok_or_arg(s, j):
    a, e = read_arg(s, j)
    if a is not None:
        return a, e
    k = skip_ws(s, j)
    if k < len(s) and s[k] == '\\':
        m = CMD_RE.match(s, k)
        return m.group(0), m.end()
    if k < len(s) and not s[k].isspace():
        return s[k], k + 1
    return None, j


def find_seq(s, seq, j):
    '''Next unescaped occurrence of seq (which starts with a backslash) at or after j.'''
    n = len(s)
    while j < n:
        c = s[j]
        if c == '\\':
            if s.startswith(seq, j):
                return j
            j += 2
            continue
        j += 1
    return -1


def find_dollar(s, j, double=False):
    n = len(s)
    while j < n:
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '$':
            if not double:
                return j
            if s.startswith('$$', j):
                return j
        j += 1
    return -1


def find_env_end(t, name, start):
    depth = 1
    for m in ENV_RE.finditer(t, start):
        if m.group(2).strip() != name:
            continue
        if m.group(1) == 'begin':
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return m.start(), m.end()
    return None, None


def unit_text(u):
    u = (u or '').strip()
    t = re.sub(r'\\([A-Za-z]+)', lambda m: UNIT_MAP.get(m.group(1), ''), u)
    t = re.sub(r'[{}~]', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def parse_macros(t):
    '''User macros: name -> (number of arguments, default of the optional one or None, body).'''
    macros = {}
    for m in re.finditer(r'\\(?:re|provide)?newcommand\*?|\\DeclareRobustCommand\*?|\\newrobustcmd\*?', t):
        j = m.end()
        k = skip_ws(t, j)
        if t[k:k + 1] == '{':
            e = match_brace(t, k)
            if e < 0:
                continue
            nm, j = t[k + 1:e - 1].strip(), e
        else:
            mm = CMD_RE.match(t, k)
            if not mm:
                continue
            nm, j = mm.group(0), mm.end()
        if not re.fullmatch(r'\\[A-Za-z@]+', nm):
            continue
        nargs, default = 0, None
        k = skip_ws(t, j)
        if t[k:k + 1] == '[':
            e = match_bracket(t, k)
            if e < 0:
                continue
            try:
                nargs = int(t[k + 1:e - 1].strip())
            except ValueError:
                nargs = 0
            j = e
            k = skip_ws(t, j)
            if t[k:k + 1] == '[':
                e2 = match_bracket(t, k)
                if e2 > 0:
                    default, j = t[k + 1:e2 - 1], e2
        body, _ = read_arg(t, j)
        if body is not None:
            macros[nm[1:]] = (nargs, default, body)
    for m in re.finditer(r'\\[gex]?def\s*\\([A-Za-z@]+)((?:#\d)*)\s*\{', t):
        e = match_brace(t, m.end() - 1)
        if e > 0:
            macros[m.group(1)] = (len(m.group(2)) // 2, None, t[m.end():e - 1])
    return macros


def macro_def_end(t, name, j):
    '''End of a macro definition whose command name (\\newcommand, \\def, ...) ends at j.'''
    n = len(t)
    if name in ('newcommand', 'renewcommand', 'providecommand', 'DeclareRobustCommand', 'newrobustcmd',
                'renewrobustcmd', 'DeclareMathOperator'):
        if t[j:j + 1] == '*':
            j += 1
        k = skip_ws(t, j)
        if t[k:k + 1] == '{':
            e = match_brace(t, k)
            j = e if e > 0 else k + 1
        else:
            mm = CMD_RE.match(t, k)
            j = mm.end() if mm else k
        for _ in range(2):
            k = skip_ws(t, j)
            if t[k:k + 1] == '[':
                e = match_bracket(t, k)
                if e > 0:
                    j = e
        a, j2 = read_arg(t, j)
        return j2 if a is not None else j
    if name in ('def', 'gdef', 'edef', 'xdef'):
        k = skip_ws(t, j)
        mm = CMD_RE.match(t, k)
        j = mm.end() if mm else k
        b = t.find('{', j)
        if b < 0 or b - j > 40:
            return j
        e = match_brace(t, b)
        return e if e > 0 else j
    if name == 'let':
        k = skip_ws(t, j)
        mm = CMD_RE.match(t, k)
        j = mm.end() if mm else k
        k = skip_ws(t, j)
        if t[k:k + 1] == '=':
            k = skip_ws(t, k + 1)
        mm = CMD_RE.match(t, k)
        return mm.end() if mm else min(n, k + 1)
    if name in ('newenvironment', 'renewenvironment'):
        _, j = read_arg(t, j)
        for _ in range(2):
            k = skip_ws(t, j)
            if t[k:k + 1] == '[':
                e = match_bracket(t, k)
                if e > 0:
                    j = e
        for _ in range(2):
            _, j = read_arg(t, j)
        return j
    if name in ('NewDocumentCommand', 'RenewDocumentCommand', 'DeclareDocumentCommand',
                'ProvideDocumentCommand'):
        k = skip_ws(t, j)
        if t[k:k + 1] == '{':
            e = match_brace(t, k)
            j = e if e > 0 else k + 1
        else:
            mm = CMD_RE.match(t, k)
            j = mm.end() if mm else k
        for _ in range(2):
            _, j = read_arg(t, j)
        return j
    if name == 'newif':
        k = skip_ws(t, j)
        mm = CMD_RE.match(t, k)
        return mm.end() if mm else j
    return j


def remove_macro_defs(t):
    out, pos = [], 0
    pat = re.compile(r'\\(%s)(?![A-Za-z@])' % '|'.join(sorted(MACRO_DEF_CMDS, key=len, reverse=True)))
    while True:
        m = pat.search(t, pos)
        if not m:
            out.append(t[pos:])
            break
        out.append(t[pos:m.start()])
        e = macro_def_end(t, m.group(1), m.end())
        out.append(keep_nl(t[m.start():e]))
        pos = max(e, m.end())
    return ''.join(out)


class TexConv:
    '''Turns LaTeX (or the LaTeX bits of Markdown) into text with placeholders.
    Every conversion keeps the number of newlines, so line numbers stay those of the input.'''

    def __init__(self, store, macros=None, md=False):
        self.store = store
        self.macros = macros or {}
        self.md = md
        self.labels = []      # dict(key, line, kind, num)
        self.refs = []        # dict(keys, line, cmd, ctx, seq)
        self.footnotes = []   # (line, text)
        self.captions = []    # dict(line, text, kind, num, sub)
        self.floats = []      # dict(kind, nums, line, keys)
        self.bugs = []        # (line, message)
        self.appendices = []  # dict(num, title, line)
        self.counters = {'fig': 0, 'tab': 0}
        self.in_app = False
        self.app_count = 0
        self.after_heading = False
        self.pending = None
        self.seq = 0
        self.depth = 0

    # -- environments -------------------------------------------------------------------------
    def envpass(self, t, line0=1):
        out, pos = [], 0
        while True:
            m = BEGIN_RE.search(t, pos)
            if not m:
                out.append(t[pos:])
                break
            out.append(t[pos:m.start()])
            name = m.group(1).strip()
            base = name.rstrip('*')
            es, ee = find_env_end(t, name, m.end())
            if es is None:
                out.append(keep_nl(m.group(0)))
                pos = m.end()
                continue
            k = m.end()
            if base in ENV_ARGS:
                _, k = read_opt(t, k)
                for _ in range(ENV_ARGS[base]):
                    a, k2 = read_arg(t, k)
                    if a is None:
                        break
                    k = k2
                    _, k = read_opt(t, k)
            inner = t[k:es]
            line_in = line0 + t.count('\n', 0, k)
            head, tail, whole = t[m.start():k], t[es:ee], t[m.start():ee]
            if base in BLANK_ENVS or base in DROP_PART_ENVS:
                rep = keep_nl(whole)
            elif base in MATH_ENVS:
                rep = self.display_math(inner, line_in) + keep_nl(whole)
            elif base in FLOAT_ENVS:
                self.float_env(FLOAT_ENVS[base], inner, line_in)
                rep = keep_nl(whole)
            elif base == 'abstract':
                rep = (mk_part('abstract') + keep_nl(head) + self.envpass(inner, line_in) + mk_part('/abstract')
                       + keep_nl(tail))
            elif base in APPENDIX_ENVS:
                self.in_app = True
                rep = mk_part('app') + keep_nl(head) + self.envpass(inner, line_in) + keep_nl(tail)
            elif base in LIST_ENVS:
                rep = MK_BR + keep_nl(head) + self.envpass(inner, line_in) + MK_BR + keep_nl(tail)
            else:
                rep = keep_nl(head) + self.envpass(inner, line_in) + keep_nl(tail)
            out.append(rep)
            pos = ee
        return ''.join(out)

    def float_env(self, kind, inner, line0):
        subspans = []
        for m in re.finditer(r'\\begin\s*\{(sub(?:figure|table)\*?)\}', inner):
            es, ee = find_env_end(inner, m.group(1), m.end())
            if es is not None:
                subspans.append((m.start(), ee))

        def in_sub(p):
            return any(a <= p < b for a, b in subspans)
        events = []
        for m in re.finditer(r'\\(caption|captionof|subcaption|subcaptionbox|subfloat|subfigure|label)'
                             r'(?![A-Za-z@])\*?', inner):
            if m.group(1) == 'subfigure' and inner[m.end():m.end() + 1] != '[':
                continue
            events.append(m)
        mains = []    # (pos, num)
        labels = []   # (pos, key, line, sub)
        nums = []
        for m in events:
            cmd, j = m.group(1), m.end()
            line = line0 + inner.count('\n', 0, m.start())
            if cmd == 'label':
                a, _ = read_arg(inner, j)
                if a is not None:
                    labels.append((m.start(), a.strip(), line, in_sub(m.start())))
                continue
            if cmd == 'captionof':
                typ, j = read_arg(inner, j)
            if cmd in ('subfloat', 'subfigure'):
                arg, _ = read_opt(inner, j)
            elif cmd == 'subcaptionbox':
                arg, _ = read_arg(inner, j)
            else:
                opt, j = read_opt(inner, j)
                arg, _ = read_arg(inner, j)
            if arg is None:
                continue
            sub = cmd in ('subcaption', 'subcaptionbox', 'subfloat', 'subfigure') or in_sub(m.start())
            if sub:
                num = None
            else:
                self.counters[kind] += 1
                num = self.counters[kind]
                mains.append((m.start(), num))
                nums.append(num)
            text = self.conv(arg, line, 'fcaption')
            self.captions.append(dict(line=line, text=text, kind=kind, num=num, sub=sub))
        for c in self.captions:
            if c['sub'] and c['num'] is None and nums and c['kind'] == kind:
                c['num'] = nums[0]
        keys = []
        for pos, key, line, sub in labels:
            before = [n for p, n in mains if p < pos]
            after = [n for p, n in mains if p > pos]
            if sub:
                num = (after or before or [None])[0]
            elif before:
                num = before[-1]
            else:
                num = (after or [None])[0]
                if mains:
                    self.bugs.append((line, '\\label{%s} comes before \\caption in its float, so \\ref{%s} '
                                            'prints the section number, not the %s number. Move the \\label '
                                            'after the \\caption.' % (key, key,
                                                                      'figure' if kind == 'fig' else 'table')))
            keys.append(key)
            self.labels.append(dict(key=key, line=line, kind=kind, num=num))
        if nums:
            self.floats.append(dict(kind=kind, nums=nums, line=line0, keys=keys))

    # -- math ---------------------------------------------------------------------------------
    def display_math(self, content, line):
        for mm in re.finditer(r'\\label\s*\{([^}]*)\}', content):
            self.labels.append(dict(key=mm.group(1).strip(), line=line + content.count('\n', 0, mm.start()),
                                    kind='eq', num=None))
        c = re.sub(r'\\(?:label|tag)\s*\{[^}]*\}|\\(?:nonumber|notag)(?![A-Za-z])', '', content)
        c = re.sub(r'\\(?:left|right|bigl|bigr|Bigl|Bigr|big|Big|bigg|Bigg)\s*\.', '', c)
        c = re.sub(r'(?:\\\\|\\[,;:!]|\\q?quad(?![A-Za-z])|\s|&)+$', '', c.rstrip())
        c = re.sub(r'\\(?:text|mathrm|textrm)\s*\{\s*([.,;])\s*\}\s*$', r'\1', c)
        punct = c[-1] if c[-1:] in ('.', ',', ';') else ''
        return self.store.add('E', content.strip()) + punct

    def inline_math(self, content, line):
        for mm in re.finditer(r'\\label\s*\{([^}]*)\}', content):
            self.labels.append(dict(key=mm.group(1).strip(), line=line, kind='eq', num=None))
        c = content.strip()
        trail = ''
        if c[-1:] in ('.', ',', ';') and not c.endswith('\\' + c[-1]):
            trail, c = c[-1], c[:-1].rstrip()
        return self.store.add('M', c, weight=math_weight(c), value=math_has_value(c)) + trail

    def dollar(self, s, i, line):
        n = len(s)
        if s.startswith('$$', i):
            e = find_dollar(s, i + 2, double=True)
            if e < 0:
                return '$$', i + 2
            return self.display_math(s[i + 2:e], line), e + 2
        e = find_dollar(s, i + 1)
        if e < 0:
            return '$', i + 1
        content = s[i + 1:e]
        if re.search(r'\n[ \t]*\n', content):
            return '$', i + 1
        if self.md and (not content or content[0].isspace() or content[-1].isspace()
                        or (e + 1 < n and s[e + 1].isdigit())):
            return '$', i + 1
        return self.inline_math(content, line), e + 1

    # -- labels -------------------------------------------------------------------------------
    def add_label(self, key, line, ctx):
        if ctx == 'fcaption':
            return
        if self.pending:
            kind, num = self.pending
            self.pending = None
            self.labels.append(dict(key=key, line=line, kind=kind, num=num))
            for f in self.floats:
                if f['kind'] == kind and num in f['nums']:
                    f['keys'].append(key)
            return
        pre = key.split(':', 1)[0].lower() if ':' in key else ''
        kind = PREFIX_KIND.get(pre)
        if kind is None:
            kind = 'sec' if (ctx == 'heading' or self.after_heading) else 'other'
        num = None
        if kind == 'sec' and self.in_app:
            kind = 'app'
        if kind == 'app' and self.in_app and self.app_count:
            num = self.app_count
        self.labels.append(dict(key=key, line=line, kind=kind, num=num))

    # -- main scanner -------------------------------------------------------------------------
    def conv(self, s, line0=1, ctx='body'):
        self.depth += 1
        if self.depth > 30:
            self.depth -= 1
            return keep_nl(s)
        out = []
        i, n, line = 0, len(s), line0
        md = self.md
        while i < n:
            c = s[i]
            if c == '\n':
                out.append(c)
                line += 1
                i += 1
                continue
            if c == '\\':
                txt, j = self.command(s, i, line, ctx)
            elif c == '$':
                txt, j = self.dollar(s, i, line)
            elif not md and c in '{}':
                txt, j = '', i + 1
            elif not md and c == '~':
                txt, j = ' ', i + 1
            elif not md and c == '%':
                e = s.find('\n', i)
                txt, j = '', (n if e < 0 else e)
            elif not md and s.startswith('---', i):
                txt, j = '—', i + 3
            elif not md and s.startswith('--', i):
                txt, j = '–', i + 2
            elif not md and c == '`':
                txt, j = ('“', i + 2) if s.startswith('``', i) else ('‘', i + 1)
            elif not md and s.startswith('\'\'', i):
                txt, j = '”', i + 2
            elif not md and c == '&':
                txt, j = ' ', i + 1
            else:
                if not c.isspace():
                    self.after_heading = False
                out.append(c)
                i += 1
                continue
            k = s.count('\n', i, j)
            if k:
                txt += ('\n' + FILL) * max(0, k - txt.count('\n'))
                line += k
            if txt.strip() and not txt.startswith(MK_O):
                self.after_heading = False
            out.append(txt)
            i = j
        self.depth -= 1
        return ''.join(out)

    def command(self, s, i, line, ctx):
        m = CMD_RE.match(s, i)
        if not m:
            return '\\', i + 1
        name, j = m.group(1), m.end()
        n = len(s)
        if not (name[0].isalpha() or name[0] == '@'):
            return self.symbol(name, s, j, line)
        if self.md and name not in self.macros and not self.md_known(name):
            return '\\' + name, j
        if len(name) == 1 and name in ACCENTS and (s[j:j + 1] == '{' or s[j:j + 2].strip()[:1].isalpha()):
            return self.accent(name, s, j)
        if name in MACRO_DEF_CMDS:
            return '', macro_def_end(s, name, j)
        if name in self.macros:
            return self.expand(name, s, j, line, ctx)
        if j < n and s[j] == '*' and (name in SECTION_LEVELS or name in CITE_CMDS or name == 'caption'):
            j += 1
        argline = line
        if name in SECTION_LEVELS:
            _, j = read_opt(s, j)
            arg, j2 = read_arg(s, j)
            if arg is None:
                return '', j
            title = render(self.conv(arg, line, 'heading'), self.store, 'show').replace('\n', ' ')
            if self.in_app and SECTION_LEVELS[name] <= 1:
                self.app_count += 1
                self.appendices.append(dict(num=self.app_count, title=title.strip(), line=line))
            self.after_heading = True
            return mk_head(SECTION_LEVELS[name], title), j2
        if name == 'appendix':
            self.in_app = True
            return mk_part('app'), j
        if name in ('acknowledgments', 'acknowledgements', 'acknowledgment'):
            return mk_head(1, 'Acknowledgments'), j
        if name == 'item':
            opt, j = read_opt(s, j)
            lab = (self.conv(opt, line, ctx) + ' ') if opt else ''
            return MK_BR + lab, j
        if name == 'par':
            return MK_BR, j
        if name in CITE_CMDS:
            for _ in range(2):
                _, j = read_opt(s, j)
            arg, j2 = read_arg(s, j)
            if arg is None:
                return '', j
            if name in TEXT_CITE:
                return self.store.add('C', arg, plain='Ref.', show='[cite]'), j2
            return self.store.add('C', arg, plain='', show='[cite]'), j2
        if name in REF_CMDS:
            _, j = read_opt(s, j)
            arg, j2 = read_arg(s, j)
            if arg is None:
                return '', j
            keys = [k.strip() for k in arg.split(',') if k.strip()]
            if name in ('crefrange', 'Crefrange'):
                arg2, j3 = read_arg(s, j2)
                if arg2 is not None:
                    keys.append(arg2.strip())
                    j2 = j3
            self.seq += 1
            self.refs.append(dict(keys=keys, line=line, cmd=name, ctx=ctx, seq=self.seq))
            plain = 'N'
            if name in NAMED_REF and keys:
                pre = keys[0].split(':', 1)[0].lower() if ':' in keys[0] else ''
                word = KIND_WORD.get(PREFIX_KIND.get(pre, ''), '')
                plain = (word + ' N').strip()
            return self.store.add('R', arg, plain=plain, show='\\%s{%s}' % (name, arg)), j2
        if name == 'hyperref':
            opt, j = read_opt(s, j)
            arg, j2 = read_arg(s, j)
            if opt:
                self.seq += 1
                self.refs.append(dict(keys=[opt.strip()], line=line, cmd=name, ctx=ctx, seq=self.seq))
            return self.conv(arg or '', line, ctx), (j2 if arg is not None else j)
        if name == 'label':
            arg, j2 = read_arg(s, j)
            if arg is None:
                return '', j
            self.add_label(arg.strip(), line, ctx)
            return '', j2
        if name in ('footnote', 'footnotetext'):
            _, j = read_opt(s, j)
            arg, j2 = read_arg(s, j)
            if arg is None:
                return '', j
            self.footnotes.append((line, self.conv(arg, line, 'footnote')))
            return '', j2
        if name in ('caption', 'captionof', 'subcaption'):
            kind = 'fig'
            if name == 'captionof':
                typ, j = read_arg(s, j)
                kind = 'tab' if (typ or '').strip().startswith('tab') else 'fig'
            _, j = read_opt(s, j)
            arg, j2 = read_arg(s, j)
            if arg is None:
                return '', j
            num = None
            if name != 'subcaption':
                self.counters[kind] += 1
                num = self.counters[kind]
                self.pending = (kind, num)
                self.floats.append(dict(kind=kind, nums=[num], line=line, keys=[]))
            self.captions.append(dict(line=line, text=self.conv(arg, line, 'fcaption'), kind=kind, num=num,
                                      sub=name == 'subcaption'))
            return '', j2
        if name in ('url', 'path', 'nolinkurl'):
            arg, j2 = read_arg(s, j)
            return self.store.add('K', arg or '', show=arg or ''), (j2 if arg is not None else j)
        if name == 'href':
            _, j = read_arg(s, j)
            arg, j2 = read_arg(s, j)
            return self.conv(arg or '', line, ctx), (j2 if arg is not None else j)
        if name == 'verb':
            if j < n:
                d = s[j]
                e = s.find(d, j + 1)
                if e > 0 and '\n' not in s[j + 1:e]:
                    return self.store.add('K', s[j + 1:e], show=s[j + 1:e]), e + 1
            return '', j
        if name == 'ensuremath':
            arg, j2 = read_arg(s, j)
            return self.inline_math(arg or '', line), (j2 if arg is not None else j)
        if name in SIUNITX:
            return self.siunitx(name, s, j)
        if name == 'texorpdfstring':
            a, j = read_arg(s, j)
            _, j2 = read_arg(s, j)
            return self.conv(a or '', line, ctx), j2
        if name in KEEP_ARG:
            for _ in range(2):
                _, j = read_opt(s, j)
            arg, j2 = read_arg(s, j)
            if arg is None:
                return '', j
            return self.conv(arg, argline + s.count('\n', i, j), ctx), j2
        if name in KEEP_LAST:
            args = []
            for _ in range(KEEP_LAST[name]):
                _, j = read_opt(s, j)
                a, j2 = read_arg(s, j)
                if a is None:
                    break
                args.append((a, j))
                j = j2
            if not args:
                return '', j
            a, pos = args[-1]
            return self.conv(a, line + s.count('\n', i, pos), ctx), j
        if name in DIMEN_CMDS:
            mm = re.match(r'\s*[-+]?\d*\.?\d+\s*(?:pt|mm|cm|em|ex|in|bp|pc|sp|mu|\\[A-Za-z]+)'
                          r'(?:\s*(?:plus|minus)\s*[-+]?\d*\.?\d+\s*(?:pt|mm|cm|em|ex|fil+))*', s[j:])
            return '', j + (mm.end() if mm else 0)
        if name in DROP_ARGS:
            for _ in range(2):
                _, j = read_opt(s, j)
            for _ in range(DROP_ARGS[name]):
                a, j2 = read_arg(s, j)
                if a is None:
                    break
                j = j2
                _, j = read_opt(s, j)
            return '', j
        if name in ('begin', 'end'):
            arg, j2 = read_arg(s, j)
            return '', (j2 if arg is not None else j)
        if name in TEXT_SYMBOLS:
            return TEXT_SYMBOLS[name], j
        if name in DROP0:
            return (' ' if name in SPACE0 else ''), j
        # an unknown command: keep the text of its arguments, or its name if it looks like one
        if j < n and s[j] == '{':
            parts = []
            while j < n and s[j] == '{':
                e = match_brace(s, j)
                if e < 0:
                    break
                parts.append(self.conv(s[j + 1:e - 1], line + s.count('\n', i, j), ctx))
                j = e
            return ' '.join(parts), j
        if name[0].isupper() and re.fullmatch(r'[A-Za-z]+', name):
            return name, j
        return '', j

    def md_known(self, name):
        return (name in CITE_CMDS or name in REF_CMDS or name in KEEP_ARG or name in SIUNITX
                or name in TEXT_SYMBOLS or name in ('label', 'footnote', 'url', 'href', 'ensuremath', 'cite',
                                                    'text', 'emph', 'textbf', 'begin', 'end'))

    def symbol(self, name, s, j, line):
        if name in '([':
            seq = '\\)' if name == '(' else '\\]'
            e = find_seq(s, seq, j)
            if e < 0 or (self.md and (e - j > 2000 or re.fullmatch(r'[\d,\s–-]*', s[j:e]))):
                return name, j
            if name == '(':
                return self.inline_math(s[j:e], line), e + 2
            return self.display_math(s[j:e], line), e + 2
        if self.md:
            return name, j
        if name in ACCENTS:
            return self.accent(name, s, j)
        if name == '\\':
            if s[j:j + 1] == '*':
                j += 1
            if s[j:j + 1] == '[':
                e = match_bracket(s, j)
                if e > 0:
                    j = e
            return ' ', j
        return SPECIAL.get(name, ''), j

    def accent(self, name, s, j):
        comb = ACCENTS[name]
        if s[j:j + 1] == '{':
            e = match_brace(s, j)
            if e < 0:
                return '', j
            arg, j2 = s[j + 1:e - 1].strip(), e
        else:
            k = j
            if name.isalpha() and s[k:k + 1] == ' ':
                k += 1
            if s[k:k + 1] == '\\':
                mm = CMD_RE.match(s, k)
                arg, j2 = mm.group(0), mm.end()
            elif k < len(s):
                arg, j2 = s[k], k + 1
            else:
                return '', j
        if arg in ('\\i', '\\j'):
            arg = arg[1]
        if not arg or arg.startswith('\\'):
            return '', j2
        return unicodedata.normalize('NFC', arg[0] + comb) + arg[1:], j2

    def expand(self, name, s, j, line, ctx):
        nargs, default, body = self.macros[name]
        args = []
        if default is not None and nargs:
            opt, j = read_opt(s, j)
            args.append(default if opt is None else opt)
            nargs -= 1
        for _ in range(nargs):
            a, j2 = read_tok_or_arg(s, j)
            if a is None:
                break
            args.append(a)
            j = j2
        rep = body
        for k in range(len(args), 0, -1):
            rep = rep.replace('#%d' % k, args[k - 1])
        return self.conv(rep.replace('\n', ' '), line, ctx), j

    def siunitx(self, name, s, j):
        def arg():
            nonlocal j
            _, j = read_opt(s, j)
            a, j2 = read_arg(s, j)
            if a is not None:
                j = j2
            return (a or '').strip()
        if name in ('SI', 'qty'):
            a = arg()
            return a + ' ' + unit_text(arg()), j
        if name in ('si', 'unit'):
            return unit_text(arg()), j
        if name in ('num', 'SIlist', 'numlist'):
            return arg().replace(';', ','), j
        if name in ('SIrange', 'qtyrange'):
            a, b = arg(), arg()
            return '%s–%s %s' % (a, b, unit_text(arg())), j
        if name == 'numrange':
            a, b = arg(), arg()
            return '%s–%s' % (a, b), j
        return arg() + '°', j


def parse_tex(src, store):
    t = src.replace('\r\n', '\n').replace('\r', '\n')
    t = strip_tex_comments(t)
    t = re.sub(r'\\iffalse\b.*?\\fi\b', lambda m: keep_nl(m.group(0)), t, flags=re.S)
    macros = parse_macros(t)
    includes = re.findall(r'\\(?:input|include|subfile)\s*\{([^}]+)\}', t)
    mb = re.search(r'\\begin\s*\{document\}', t)
    if mb:
        t = keep_nl(t[:mb.end()]) + t[mb.end():]
    me = re.search(r'\\end\s*\{document\}', t)
    if me:
        t = t[:me.start()] + keep_nl(t[me.start():])
    t = remove_macro_defs(t)
    for name, (nargs, default, body) in macros.items():
        if nargs == 0 and re.search(r'\\(?:begin|end)\s*\{', body):
            flat = body.replace('\n', ' ')
            t = re.sub(r'\\%s(?![A-Za-z@])' % re.escape(name), lambda m, b=flat: b, t)
    conv = TexConv(store, macros)
    t = conv.envpass(t, 1)
    body = conv.conv(t, 1, 'body')
    blocks = build_blocks(body)
    for c in conv.captions:
        blocks.append(text_block(c['text'], c['line'], 'caption', fig=(c['kind'], c['num']), sub=c['sub']))
    for line, txt in conv.footnotes:
        blocks.append(text_block(txt, line, 'footnote'))
    return dict(blocks=blocks, conv=conv, includes=includes, vocab=None)


def text_block(text, line0, kind, **kw):
    pieces = [(line0 + k, seg.replace(FILL, '')) for k, seg in enumerate(text.split('\n'))
              if seg.replace(FILL, '').strip()]
    pieces = [(ln, MK_RE.sub(' ', seg)) for ln, seg in pieces]
    d = dict(kind=kind, part=kind, section='', pieces=pieces)
    d.update(kw)
    return d


# =============================================================================================
# Section structure shared by LaTeX and Markdown
# =============================================================================================
DROP_HEAD_RE = re.compile(r'^(?:acknowledge?ments?|references|bibliography|author contributions?|'
                          r'data availability(?: statement)?|code availability|funding|conflicts? of interest|'
                          r'competing interests|declaration of competing interests?|contents|table of contents)$')
INTRO_HEAD_RE = re.compile(r'^(?:introduction|motivation|introduction and motivation)$')
CONCL_HEAD_RE = re.compile(r'^(?:conclusions?|summary|outlook|concluding remarks|final remarks|'
                           r'summary and (?:conclusions?|outlook|discussion)|'
                           r'conclusions? and (?:outlook|discussion|future work|perspectives)|'
                           r'discussion and (?:conclusions?|outlook)|summary and future work)$')


def norm_title(title):
    t = title.strip().lower()
    t = re.sub(r'^(?:[a-z]|[ivx]+|\d+(?:\.\d+)*)(?:[.:)]\s*|\s+)', '', t)
    return re.sub(r'[\s.:;]+$', '', t)


def part_for_heading(title, level, st):
    raw = title.strip().lower()
    t = norm_title(title)
    if re.match(r'^(?:appendix|appendices|app\.\s)', raw) or re.match(r'^supplementa(?:l|ry)', t):
        st['in_app'] = True
        return 'app'
    if DROP_HEAD_RE.match(t):
        return 'drop'
    if t == 'abstract':
        return 'abstract'
    if st.get('in_app'):
        return 'app'
    if INTRO_HEAD_RE.match(t):
        return 'intro'
    if CONCL_HEAD_RE.match(t):
        return 'concl'
    if level > 1 and st['part'] in ('intro', 'body', 'concl'):
        return st['part']
    return 'body'


def build_blocks(text, top=1):
    '''Split marker-annotated, line-aligned text into paragraph blocks with part and section.'''
    blocks = []
    st = dict(part='body', section='', in_app=False)
    cur = [None]

    def close():
        if cur[0] and cur[0]['pieces']:
            blocks.append(cur[0])
        cur[0] = None

    def add(seg, ln):
        seg = seg.replace(FILL, '')
        if not seg.strip() or st['part'] in ('drop', 'front'):
            return
        if cur[0] is None:
            cur[0] = dict(kind='prose', part=st['part'], section=st['section'], pieces=[])
        cur[0]['pieces'].append((ln, seg))

    for ln, line in enumerate(text.split('\n'), 1):
        if not line.strip():
            close()
            continue
        pos = 0
        for m in MK_RE.finditer(line):
            add(line[pos:m.start()], ln)
            close()
            mk = m.group(1)
            if mk.startswith('P'):
                p = mk[1:]
                if p == 'abstract':
                    st['part'] = 'abstract'
                elif p == '/abstract':
                    st['part'] = 'intro'
                elif p == 'app':
                    st['part'] = 'app'
                    st['in_app'] = True
            elif mk.startswith('H'):
                lvl, _, title = mk[1:].partition('|')
                level = max(1, int(lvl) - top + 1)
                st['part'] = part_for_heading(title, level, st)
                st['section'] = title
            pos = m.end()
        add(line[pos:], ln)
    close()
    return blocks


# =============================================================================================
# Markdown
# =============================================================================================
MD_CAPTION_RE = re.compile(r'^\s*(?:\*\*|\*|_)?\s*(Figure|Fig\.|FIG\.|Table|TABLE|Tab\.)\s*(\d+|[IVX]+)'
                           r'\s*[.:|—]\s*(?:\*\*|\*|_)?\s*')
CROSSREF_KIND = {'fig': 'fig', 'tbl': 'tab', 'tab': 'tab', 'sec': 'sec', 'eq': 'eq', 'app': 'app'}


def parse_md(src, store):
    t = src.replace('\r\n', '\n').replace('\r', '\n')
    if t.startswith('---\n'):
        e = t.find('\n---', 4)
        if e > 0:
            e2 = t.find('\n', e + 4)
            e2 = len(t) if e2 < 0 else e2
            t = blank_nl(t[:e2]) + t[e2:]
    t = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$', lambda m: blank_nl(m.group(0)), t, flags=re.M | re.S)
    t = re.sub(r'<!--.*?-->', lambda m: keep_nl(m.group(0)) if m.group(0).count('\n') else '', t, flags=re.S)
    t = re.sub(r'(?<!`)`([^`\n]+)`(?!`)', lambda m: store.add('K', m.group(1), show=m.group(1)), t)
    conv = TexConv(store, {}, md=True)
    t = conv.envpass(t, 1)
    t = conv.conv(t, 1, 'body')
    lines = t.split('\n')
    n = len(lines)
    heads = []
    for i, line in enumerate(lines):
        m = re.match(r'^(#{1,6})\s+(.*?)\s*#*\s*$', line)
        if m:
            heads.append((i, len(m.group(1)), m.group(2)))
        elif (i + 1 < n and line.strip() and not re.match(r'^\s*([-*+]|\d+[.)])\s', line)
              and re.match(r'^\s*(=+|-{2,})\s*$', lines[i + 1])):
            heads.append((i, 1 if lines[i + 1].strip()[0] == '=' else 2, line.strip()))
    top = 1
    known = [lv for _, lv, title in heads
             if re.match(r'^(?:abstract|introduction|conclusions?|summary|references|appendix)', norm_title(title))]
    if known:
        top = min(known)
    elif heads:
        cnt = Counter(lv for _, lv, _ in heads)
        top = min(lv for lv, c in cnt.items() if c >= 2) if any(c >= 2 for c in cnt.values()) else 1
    headset = {i: (lv, title) for i, lv, title in heads}
    footnotes, captions = [], []
    out = []
    in_table = False
    for i, line in enumerate(lines):
        if i in headset:
            lv, title = headset[i]
            if lv < top:
                out.append('')
                continue
            out.append(mk_head(lv, render(title, store, 'show')))
            continue
        if i > 0 and (i - 1) in headset and re.match(r'^\s*(=+|-{2,})\s*$', line):
            out.append('')
            continue
        s = line
        if re.match(r'^\s*\|', s) or re.match(r'^\s*:?-{3,}:?\s*\|', s) or (in_table and '|' in s):
            in_table = bool(s.strip())
            out.append('')
            continue
        in_table = False
        if re.match(r'^\s*((\*\s*){3,}|(-\s*){3,}|(_\s*){3,})$', s):
            out.append(MK_BR)
            continue
        fm = re.match(r'^\s*\[\^([^\]]+)\]:\s*(.*)$', s)
        if fm:
            footnotes.append((i + 1, fm.group(2)))
            out.append('')
            continue
        if re.match(r'^\s*\[[^\]^]+\]:\s*\S+', s):
            out.append('')
            continue
        s = re.sub(r'^\s*>\s?', '', s)

        def image(m):
            alt, attr = m.group(1), m.group(3) or ''
            lab = re.search(r'#((?:fig|tbl|tab):[^\s}]+)', attr)
            if alt.strip() or lab:
                kind = 'tab' if lab and lab.group(1).startswith(('tbl', 'tab')) else 'fig'
                captions.append(dict(line=i + 1, text=alt, kind=kind, label=lab.group(1) if lab else None))
            return ''
        s = re.sub(r'!\[([^\]]*)\]\(([^)]*)\)(\{[^}]*\})?', image, s)
        s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
        s = re.sub(r'\[([^\]]+)\]\[[^\]]*\]', r'\1', s)
        s = re.sub(r'<(https?://[^>\s]+)>', lambda m: store.add('K', m.group(1), show=m.group(1)), s)
        s = re.sub(r'\[\^[^\]]+\]', '', s)
        s = re.sub(r'\{#[^}]*\}', '', s)

        def bracket_cite(m):
            inner = m.group(1)
            keys = re.findall(r'@([A-Za-z0-9_][\w:.#$%&\-+?<>~/]*)', inner)
            if not keys:
                return m.group(0)
            return md_cite(keys, i + 1, conv, store)
        s = re.sub(r'\[((?:[^\[\]]*?)@[^\[\]]*)\]', bracket_cite, s)
        s = re.sub(r'(?<![\w@.])@([A-Za-z][\w:.#$%&\-+?<>~/]*[\w])',
                   lambda m: md_cite([m.group(1)], i + 1, conv, store), s)
        lm = re.match(r'^(\s*)([-*+•]|\d+[.)])\s+', s)
        if lm:
            s = MK_BR + s[lm.end():]
        s = re.sub(r'(\*\*|__)(?=\S)(.+?)(?<=\S)\1', r'\2', s)
        s = re.sub(r'(?<![\w*\\])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])', r'\1', s)
        s = re.sub(r'(?<![\w\\])_(?=\S)(.+?)(?<=\S)_(?![\w])', r'\1', s)
        s = re.sub(r'~~(.+?)~~', '', s)
        s = re.sub(r'</?[A-Za-z][^>\n]*>', '', s)
        s = re.sub(r'\\([\\`*_{}\[\]()#+\-.!|>~])', r'\1', s)
        out.append(s)
    # caption paragraphs (Figure 1: ...)
    k = 0
    while k < len(out):
        cm = MD_CAPTION_RE.match(out[k]) if (k == 0 or not out[k - 1].strip() or out[k - 1] == MK_BR) else None
        if cm:
            e = k
            while e + 1 < len(out) and out[e + 1].strip() and not MK_RE.search(out[e + 1]):
                e += 1
            text = '\n'.join([out[k][cm.end():]] + out[k + 1:e + 1])
            kind = 'tab' if cm.group(1).lower().startswith('tab') else 'fig'
            captions.append(dict(line=k + 1, text=text, kind=kind, number=roman_or_int(cm.group(2))))
            for q in range(k, e + 1):
                out[q] = ''
            k = e + 1
            continue
        k += 1
    blocks = build_blocks('\n'.join(out), top=top)
    counters = {'fig': 0, 'tab': 0}
    floats = []
    for c in captions:
        if c.get('number'):
            num = c['number']
        else:
            counters[c['kind']] += 1
            num = counters[c['kind']]
        counters[c['kind']] = max(counters[c['kind']], num)
        if c.get('label'):
            conv.labels.append(dict(key=c['label'], line=c['line'], kind=c['kind'], num=num))
        floats.append(dict(kind=c['kind'], nums=[num], line=c['line'], keys=[c['label']] if c.get('label') else []))
        blocks.append(text_block(c['text'], c['line'], 'caption', fig=(c['kind'], num), sub=False))
    for line, txt in footnotes + conv.footnotes:
        blocks.append(text_block(txt, line, 'footnote'))
    conv.floats.extend(floats)
    return dict(blocks=blocks, conv=conv, includes=[], vocab=None, text_floats=floats)


def md_cite(keys, line, conv, store):
    refs = [k for k in keys if k.split(':', 1)[0] in CROSSREF_KIND and ':' in k]
    if refs and len(refs) == len(keys):
        conv.seq += 1
        conv.refs.append(dict(keys=refs, line=line, cmd='crossref', ctx='body', seq=conv.seq))
        word = KIND_WORD.get(CROSSREF_KIND[refs[0].split(':', 1)[0]], '')
        return store.add('R', ', '.join(refs), plain=(word + ' N').strip(), show='@' + refs[0])
    return store.add('C', ', '.join(keys), plain='', show='[@' + keys[0] + ']')


def roman_or_int(s):
    if s.isdigit():
        return int(s)
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    total, prev = 0, 0
    for ch in reversed(s.upper()):
        v = vals.get(ch, 0)
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


# =============================================================================================
# Plain text (also the pdftotext output of the reference papers)
# =============================================================================================
FW = set('''a an the of to in on for with by from at as and or but nor not no is are was were be been
being has have had do does did can could may might will would shall should must this that these those
which who whom whose what where when while if than then there here it its we our us they their them
such each both all any some many more most less other another into onto over under between among
through across about above below per via without within also only so very'''.split())
PUNCT = '.,;:!?()[]{}\x22“”\'’‘`'
WORD_RE = re.compile('^[A-Za-z]+(?:[-\'’][A-Za-z]+)*$')
EQNUM_RE = re.compile(r'^\(\s*[A-Z]?\d+[a-z]?\s*\)$')
TXT_CAP_RE = re.compile(r'^(FIG\.|FIGURE|Figure|Fig\.|TABLE|Table|Tab\.)\s*([0-9]+|[IVX]+)\s*[.:|—]')
MATHFUNC = {'sin', 'cos', 'tan', 'exp', 'log', 'ln', 'max', 'min', 'arg', 'lim', 'sup', 'inf'}
NUM_ONLY_RE = re.compile(r'^(?:[IVX]+\.|[A-H]\.|\d+(?:\.\d+)*\.)$')
NUMBERED_TITLE_RE = re.compile(r'^(?P<num>[IVX]+|[A-H]|\d+(?:\.\d+)*)[.)]?\s+(?P<title>\S.*)$')
APPENDIX_HEAD_RE = re.compile(r'^(?:Appendix|APPENDIX)(?:\s+[A-Z0-9]+)?\s*(?:[:.]|$)')
KNOWN_HEAD_RE = re.compile(r'^(?:abstract|introduction|conclusions?|summary|outlook|discussion|results|methods?|'
                           r'acknowledge?ments?|references|bibliography|appendix(?:\s+[a-z0-9]+)?|appendices|'
                           r'contents|background|related work|data availability|summary and outlook|'
                           r'conclusions? and outlook)\s*[:.]?$', re.I)


def real_words(line):
    out = []
    for t in line.split():
        t = t.strip(PUNCT)
        if len(t) >= 2 and WORD_RE.match(t) or t in ('a', 'A', 'I'):
            out.append(t)
    return out


LENIENT = [False]     # True for plain-text drafts that are not PDF extractions


def label(line):
    '''Label P for a prose-like line, S for figure junk, math or a heading (from style_metrics.py).'''
    s = line.strip()
    if s.startswith('•'):
        return 'P'
    if LENIENT[0] and ends_terminal(s) and len(real_words(s)) >= 3 and re.match(r'^[\W\d]*[A-Za-z\ue000]', s):
        return 'P'
    rw = real_words(s)
    nfw = sum(1 for w in rw if w.lower() in FW)
    nonspace = len(re.sub(r'\s', '', s)) or 1
    ratio = sum(len(w) for w in rw) / nonspace
    mixed = [w for w in rw if not w.isupper()]
    lower = sum(1 for w in mixed if w[0].islower()) / (len(mixed) or 1)
    return 'P' if (len(rw) >= 4 and ratio >= 0.45 and lower >= 0.4 and (nfw >= 2 or len(rw) >= 5)) else 'S'


def prose_like(line):
    s = line.strip()
    rw = [w for w in real_words(s) if w.lower() not in MATHFUNC]
    if not any(len(w) >= 2 for w in rw):
        return False
    nonspace = len(re.sub(r'\s', '', s)) or 1
    if sum(len(w) for w in rw) / nonspace < 0.5:
        return False
    has_fw = any(w.lower() in FW for w in rw)
    has_long_lower = any(len(w) >= 5 and w.islower() for w in rw) or (
        s.endswith(':') and any(len(w) >= 3 and w.islower() for w in rw))
    neutral = {'Fig', 'Figs', 'Eq', 'Eqs', 'Sec', 'Ref', 'Refs', 'Table', 'Tab', 'Section', 'Appendix', 'App'}
    return (has_fw or has_long_lower) and all(w[0].islower() or w.isupper() or w in neutral for w in rw)


def ends_terminal(s):
    return bool(re.search(r'[.?!][\x22”’)\]]*\s*$', s.strip()))


def build_section(lines, idxs, store):
    '''Pieces (line, text) of one section; drops figure junk and turns displayed math into a
    placeholder (logic from style_metrics.py, without its per-paper fixes).'''
    nb = [i for i in idxs if lines[i].strip()]
    labs = {i: label(lines[i]) for i in nb}
    runs = []
    for i in nb:
        if runs and runs[-1][0] == labs[i]:
            runs[-1][1].append(i)
        else:
            runs.append([labs[i], [i]])
    for k, (lab, ls) in enumerate(runs):
        if lab == 'P' and len(ls) <= 2:
            prev_junk = k == 0 or (runs[k - 1][0] == 'S' and len(runs[k - 1][1]) >= 3)
            next_junk = k == len(runs) - 1 or (runs[k + 1][0] == 'S' and len(runs[k + 1][1]) >= 3)
            s = lines[ls[-1]].strip()
            nfw_run = sum(1 for i in ls for w in real_words(lines[i]) if w.lower() in FW)
            keep = nfw_run >= 4 or (ends_terminal(s) and sum(1 for w in real_words(s) if w.lower() in FW) >= 3)
            if prev_junk and next_junk and not keep and len(runs) > 1:
                runs[k][0] = 'S'
    merged = []
    for lab, ls in runs:
        if merged and merged[-1][0] == lab:
            merged[-1][1].extend(ls)
        else:
            merged.append([lab, list(ls)])
    runs = merged
    pieces = []
    eq = lambda: store.add('E', '')
    for k, (lab, ls) in enumerate(runs):
        if lab == 'P':
            pieces.extend((i, lines[i].strip()) for i in ls)
            continue
        prevP = k > 0 and runs[k - 1][0] == 'P'
        nextP = k < len(runs) - 1 and runs[k + 1][0] == 'P'
        texts = [lines[i].strip() for i in ls]
        prev_text = pieces[-1][1] if pieces else ''
        nxt = lines[runs[k + 1][1][0]].strip() if nextP else ''
        if any(EQNUM_RE.match(t) for t in texts):
            out, seg = [], []

            def flush():
                if seg:
                    punct = ''
                    for t in reversed(seg):
                        if EQNUM_RE.match(t) or re.fullmatch(r'[\d.,\s]+', t):
                            continue
                        if re.search(r'(?<!\d)\.\s*$', t) or t.endswith('h.c.'):
                            punct = '.'
                            break
                        if t.endswith(','):
                            punct = ','
                            break
                    out.append((ls[0], eq() + punct))
                    seg.clear()
            for i, t in zip(ls, texts):
                if prose_like(t) and not EQNUM_RE.match(t):
                    flush()
                    out.append((i, t))
                else:
                    seg.append(t)
            flush()
            col = []
            for i, t in out:
                if col and PH_RE.fullmatch(col[-1][1].rstrip('.,')) and PH_RE.fullmatch(t.rstrip('.,')):
                    p = col[-1][1][-1] if col[-1][1][-1] in '.,' else ''
                    q = t[-1] if t[-1] in '.,' else p
                    col[-1] = (col[-1][0], col[-1][1].rstrip('.,') + q)
                else:
                    col.append((i, t))
            if col and PH_RE.fullmatch(col[-1][1]) and nxt[:1].isupper():
                col[-1] = (col[-1][0], col[-1][1] + '.')
            pieces.extend(col)
        elif prev_text.rstrip().endswith(':') and (nextP or k == len(runs) - 1) and len(ls) <= 15:
            pieces.append((ls[0], eq() + ('.' if nxt[:1].isupper() else '')))
        elif prevP and nextP and (len(ls) <= 2 or (len(ls) <= 4 and all(len(t) <= 40 for t in texts))):
            pieces.extend((i, t) for i, t in zip(ls, texts))
        elif k == 0 and nextP and len(ls) <= 2 and nxt[:1].islower():
            pieces.extend((i, t) for i, t in zip(ls, texts))
        elif prevP and k == len(runs) - 1 and len(ls) <= 2 and ends_terminal(texts[-1]):
            pieces.extend((i, t) for i, t in zip(ls, texts))
        else:
            pairs = list(zip(ls, texts))
            lead = []
            if prevP and not ends_terminal(prev_text):
                for i, t in pairs:
                    if prose_like(t) and t[:1].islower():
                        lead.append((i, t))
                    else:
                        break
            tail = []
            last_i, last_t = pairs[-1]
            if len(pairs) > len(lead) and prose_like(last_t) and ends_terminal(last_t):
                tail = [(last_i, last_t)]
            pieces.extend(lead)
            rest = [t for _, t in pairs[len(lead):len(pairs) - len(tail)]]
            open_sentence = prevP and not ends_terminal(lead[-1][1] if lead else prev_text)
            if (open_sentence and nextP and not (lead and lead[-1][1].rstrip().endswith(':'))
                    and len(pairs) <= 20 and any('=' in t for t in rest[:3])):
                pieces.append((pairs[len(lead)][0], eq() + ('.' if nxt[:1].isupper() else '')))
            if lead and lead[-1][1].rstrip().endswith(':') and len(pairs) > len(lead) + len(tail):
                pieces.append((lead[-1][0], eq() + ('.' if nxt[:1].isupper() else '')))
            pieces.extend(tail)
    return pieces


def join_pieces(pieces, vocab):
    '''Join lines with line-break hyphen repair; returns text and [(offset, line)].'''
    text, offs = '', []
    for i, t in pieces:
        t = re.sub(r'\s+', ' ', t).strip()
        if not t:
            continue
        if vocab is not None and text.endswith('-') and re.search(r'[A-Za-z]-$', text) and t[:1].islower():
            left = re.search(r'([A-Za-z]+)-$', text).group(1).lower()
            right = re.match(r'([A-Za-z]*)', t).group(1).lower()
            offs.append((len(text), i))
            if left in vocab and right in vocab and len(right) > 3:
                text += t
            else:
                text = text[:-1] + t
        elif vocab is None and text and re.search(r'[A-Za-z]-$', text) and t[:1].isalpha():
            offs.append((len(text), i))
            text += t
        else:
            if text:
                text += ' '
            offs.append((len(text), i))
            text += t
    return text, offs


def txt_inline(line, store):
    def cite(m):
        nums = [int(x) for x in re.findall(r'\d+', m.group(0))]
        after = line[m.end():m.end() + 8]
        if 0 in nums or re.match(r'\s*(?:GeV|TeV|MeV|eV|cm|mm|m\b|rad|fb|s\b|ns|µs|%)', after):
            return m.group(0)
        return store.add('C', m.group(0), plain='', show=m.group(0))
    line = re.sub(r'\[\s*\d{1,3}[a-z]?(?:\s*[,–\-]\s*\d{1,3}[a-z]?)*\s*\]', cite, line)
    line = re.sub(r'(?<![\\$\w])\$(?=\S)([^$\n]{1,200}?)(?<=\S)\$(?![\d$])',
                  lambda m: store.add('M', m.group(1), weight=math_weight(m.group(1)),
                                      value=math_has_value(m.group(1))), line)
    return line


def is_allcaps_heading(s):
    letters = [c for c in s if c.isalpha()]
    if len(letters) < 4 or len(s.split()) > 10 or re.search(r'[.?!=\[\]]$', s) or '=' in s:
        return False
    if sum(1 for c in letters if c.isupper()) / len(letters) < 0.85:
        return False
    words = re.findall(r'[A-Za-z]+', s)
    return any(len(w) >= 4 and w.upper() not in KNOWN_ACR for w in words)


def title_like(s):
    w = s.split()
    return (1 <= len(w) <= 10 and not re.search(r'[.?!,;=]$', s) and s[:1].isalpha()
            and len(re.findall(r'[A-Za-z]', s)) >= 3 and not TXT_CAP_RE.match(s))


def txt_headings(lines, skip_lines):
    n = len(lines) - 1
    heads, used = {}, set()

    def nb(i, step):
        j = i + step
        while 1 <= j <= n and not lines[j].strip():
            j += step
        return j if 1 <= j <= n else None

    def collect(i):
        title, got = lines[i].strip(), [i]
        j = i + 1
        while (j <= n and lines[j].strip() and len(got) < 3 and len(lines[j].split()) <= 6
               and not re.search(r'[.?!,;]$', lines[j].strip())
               and sum(c.isupper() for c in lines[j] if c.isalpha()) >= 0.85 * max(1, sum(c.isalpha() for c in lines[j]))
               and sum(c.isupper() for c in title if c.isalpha()) >= 0.85 * max(1, sum(c.isalpha() for c in title))):
            title += ' ' + lines[j].strip()
            got.append(j)
            j += 1
        return title, got

    seen_prose = False
    for i in range(1, n + 1):
        if i in skip_lines or i in used:
            continue
        s = lines[i].strip()
        if not s:
            continue
        if not seen_prose and label(s) == 'P' and len(s.split()) >= 8:
            seen_prose = True
        pi, ni = nb(i, -1), nb(i, 1)
        ps = lines[pi].strip() if pi else ''
        ns = lines[ni].strip() if ni else ''
        if NUM_ONLY_RE.match(s) and ni and ni - i <= 3 and ni not in skip_lines and title_like(ns):
            title, got = collect(ni)
            lvl = 2 if re.match(r'^(?:[A-H]\.|\d+\.\d)', s) else 1
            heads[i] = (s + ' ' + title, lvl)
            used.update(got)
            continue
        if APPENDIX_HEAD_RE.match(s) and len(s.split()) <= 14:
            heads[i] = (s, 1)
            continue
        core = re.sub(r'^(?:[IVX]+|[A-H]|\d+(?:\.\d+)*)[.)]?\s+', '', s)
        if KNOWN_HEAD_RE.match(core) and len(s.split()) <= 6:
            heads[i] = (s, 1)
            continue
        if is_allcaps_heading(s) and (seen_prose or KNOWN_HEAD_RE.match(core)) and not re.search(r'\d', s):
            title, got = collect(i)
            heads[i] = (title, 1)
            used.update(g for g in got if g != i)
            continue
        m = NUMBERED_TITLE_RE.match(s)
        if (m and title_like(m.group('title')) and len(s.split()) <= 8
                and not re.match(r'^\d+(?:\.\d+)?\s+(?:[a-z]|GeV|TeV|MeV|events?|fb)', s)
                and (pi is None or ends_terminal(ps) or pi in heads or not ps)
                and (m.group('title')[:1].isupper())):
            num = m.group('num')
            heads[i] = (s, 2 if ('.' in num or re.fullmatch(r'[A-H]', num)) else 1)
            continue
        if (seen_prose and title_like(s) and len(s.split()) <= 8 and not lines[i - 1].strip()
                and (i + 1 > n or not lines[i + 1].strip())
                and (pi is None or ends_terminal(ps) or pi in heads)
                and ns[:1].isupper()):
            heads[i] = (s, 2)
    return heads, used


def txt_captions(lines):
    '''Captions that start with FIG. N / Figure N: / TABLE N ... (logic from style_metrics.py).'''
    n = len(lines) - 1
    caps = []
    i = 1
    while i <= n:
        m = TXT_CAP_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        kind = 'tab' if m.group(1).lower().startswith('tab') else 'fig'
        got = [i]
        j = i + 1
        while j <= n and len(got) < 30:
            s = lines[j].strip()
            last = lines[got[-1]].strip()
            if TXT_CAP_RE.match(s):
                break
            if not s:
                if ends_terminal(last):
                    break
                j += 1
                continue
            if ends_terminal(last) and (label(s) == 'S' or s[:1].islower()):
                break
            got.append(j)
            j += 1
        caps.append(dict(kind=kind, num=roman_or_int(m.group(2)), line=i, idxs=got, prefix=m.end()))
        i = got[-1] + 1
    return caps


def looks_extracted(text):
    '''True for text that looks like pdftotext output: an arXiv stamp, or many hard-wrapped hyphenated lines.'''
    nonblank = [l for l in text.split('\n') if l.strip()]
    hyph_ends = sum(1 for l in nonblank if re.search(r'[a-z]-$', l.rstrip()))
    return bool(re.search(r'^\s*arXiv:\d{4}\.\d{4,5}', text, re.M) or (
        len(nonblank) > 100 and hyph_ends > 0.03 * len(nonblank)))


def parse_txt(src, store):
    t = src.replace('\r\n', '\n').replace('\r', '\n').replace('\f', '')
    raw = t.split('\n')
    LENIENT[0] = not looks_extracted(t)
    lines = [''] + [txt_inline(l, store) for l in raw]
    for k in range(1, len(lines)):
        lm = re.match(r'^(\s*)([-*+]|\d+[.)])\s+(?=\S)', lines[k])
        if lm and not NUM_ONLY_RE.match(lines[k].strip()) and not NUMBERED_TITLE_RE.match(lines[k].strip()):
            lines[k] = '• ' + lines[k][lm.end():]
    n = len(lines) - 1
    caps = txt_captions(lines)
    cap_lines = {i for c in caps for i in c['idxs']}
    heads, used = txt_headings(lines, cap_lines)
    ref_start = None
    for i in range(1, n + 1):
        if re.match(r'^\[1\]\s+\S', raw[i - 1].strip()) and any(
                re.match(r'^\[2\]\s', raw[j - 1].strip()) for j in range(i + 1, min(n, i + 40) + 1)):
            ref_start = i
            break
    vocab = set()
    for i in range(1, n + 1):
        if label(lines[i]) == 'P':
            vocab.update(w.lower() for w in real_words(lines[i]))
    sections = []
    st = dict(part='pre', section='', in_app=False)
    cur = []
    in_refs = False
    for i in range(1, n + 1):
        if ref_start and i == ref_start:
            if cur:
                sections.append((st['part'], st['section'], cur))
                cur = []
            in_refs = True
        if i in heads:
            title, lvl = heads[i]
            if in_refs and not APPENDIX_HEAD_RE.match(title):
                continue
            in_refs = False
            if cur:
                sections.append((st['part'], st['section'], cur))
            cur = []
            if st['part'] == 'pre':
                st['part'] = 'body'
            st['part'] = part_for_heading(title, lvl, st)
            st['section'] = title
            continue
        if in_refs or i in cap_lines or i in used or st['part'] == 'drop':
            continue
        s = lines[i].strip()
        if re.fullmatch(r'\d{1,3}', s):
            continue
        cur.append(i)
    if cur:
        sections.append((st['part'], st['section'], cur))
    have_heads = bool(heads)
    explicit_abstract = any(norm_title(h[0]) == 'abstract' for h in heads.values())
    blocks = []
    for part, section, idxs in sections:
        if part == 'pre':
            if explicit_abstract:
                continue
            if have_heads:
                part = 'abstract'
                nb = [i for i in idxs if lines[i].strip()]
                labs = [label(lines[i]) for i in nb]
                last_s = max((k for k in range(len(nb)) if labs[k] == 'S' and (k == 0 or labs[k - 1] == 'S')
                              and any(labs[q] == 'P' for q in range(k + 1, len(nb)))), default=None)
                if last_s is not None:
                    idxs = nb[last_s + 1:]
            else:
                part = 'body'
        pieces = build_section(lines, idxs, store)
        para = []
        for k, (ln, txt) in enumerate(pieces):
            if para:
                pl = para[-1][0]
                gap = any(not lines[q].strip() for q in range(pl + 1, ln)) if ln > pl else False
                if gap and ends_terminal(para[-1][1]) and (txt[:1].isupper() or txt.startswith(('•', PH_O))):
                    blocks.append(dict(kind='prose', part=part, section=section, pieces=para))
                    para = []
            para.append((ln, txt))
        if para:
            blocks.append(dict(kind='prose', part=part, section=section, pieces=para))
    floats = []
    for c in caps:
        first = lines[c['line']].strip()[c['prefix']:]
        pieces = [(c['line'], first)] + [(i, lines[i].strip()) for i in c['idxs'][1:]]
        blocks.append(dict(kind='caption', part='caption', section='', pieces=pieces,
                           fig=(c['kind'], c['num']), sub=False))
        floats.append(dict(kind=c['kind'], nums=[c['num']], line=c['line'], keys=[]))
    conv = TexConv(store)
    conv.floats = floats
    rawrefs = []
    for i in range(1, n + 1):
        if i in cap_lines or (ref_start and i >= ref_start and not any(
                APPENDIX_HEAD_RE.match(h[0]) and ref_start <= q <= i for q, h in heads.items())):
            continue
        if i in heads:
            continue
        for rx, kind in ((FIGWORD_RE, 'fig'), (TABWORD_RE, 'tab'), (APPWORD_RE, 'app')):
            for m in rx.finditer(raw[i - 1]):
                nums, _ = parse_numlist(raw[i - 1], m.end(), letters=(kind == 'app'), roman=(kind == 'tab'))
                rawrefs.extend((kind, v) for v in nums)
    return dict(blocks=blocks, conv=conv, includes=[], vocab=vocab, text_floats=floats, rawrefs=set(rawrefs),
                heads=[(i, h[0]) for i, h in sorted(heads.items())])


# =============================================================================================
# Sentences
# =============================================================================================
ABBR = {'fig.', 'figs.', 'eq.', 'eqs.', 'ref.', 'refs.', 'sec.', 'secs.', 'app.', 'apps.', 'tab.', 'tabs.',
        'e.g.', 'i.e.', 'al.', 'vs.', 'cf.', 'approx.', 'no.', 'nos.', 'eqn.', 'eqns.', 'resp.', 'ch.', 'chap.',
        'sect.', 'viz.', 'w.r.t.', 'a.u.', 'dr.', 'prof.', 'mr.', 'ms.', 'st.', 'jr.', 'phys.', 'rev.', 'lett.',
        'nucl.', 'proc.', 'mod.', 'int.', 'eur.', 'ibid.', 'op.', 'cit.', 'vol.', 'pp.', 'p.', 'ex.'}


def split_sentences(text):
    out = []
    chunks, pos = [], 0
    for m in re.finditer(r'\s*•\s*', text):
        chunks.append((pos, text[pos:m.start()]))
        pos = m.end()
    chunks.append((pos, text[pos:]))
    for base, chunk in chunks:
        start = 0
        for m in re.finditer(r'[.?!][\x22”’)\]]*(\s+)', chunk):
            nxt = chunk[m.end():m.end() + 1]
            if not nxt:
                continue
            if not (nxt.isupper() or nxt.isdigit() or nxt in '“\x22([‘' or nxt == PH_O
                    or (not nxt.isascii() and nxt.isalpha())):
                continue
            pre = chunk[start:m.start() + 1].split()
            tok = pre[-1].lstrip('([\x22“').lower() if pre else ''
            if tok in ABBR:
                continue
            s = chunk[start:m.start(1)].strip()
            if s:
                out.append((base + start, s))
            start = m.end()
        s = chunk[start:].strip()
        if s:
            out.append((base + start, s))
    return out


class Sent:
    __slots__ = ('i', 'line', 'part', 'kind', 'section', 'block', 'raw', 'plain', 'show', 'toks', 'low',
                 'rawtoks', 'words', 'fig')

    def excerpt(self, n=170):
        return shorten(self.show, n)


def make_sentences(blocks, store, vocab):
    sents = []
    for b_id, b in enumerate(blocks):
        pieces = [(ln, MK_RE.sub(' ', seg)) for ln, seg in b['pieces']]
        text, offs = join_pieces(pieces, vocab)
        if b['kind'] == 'caption':
            text = re.sub(r'^\s*(?:FIG\.|FIGURE|Figure|Fig\.|TABLE|Table|Tab\.)\s*(?:[0-9]+|[IVX]+)\s*[.:|—]\s*',
                          '', text)
        for off, raw in split_sentences(text):
            line = max((o for o in offs if o[0] <= off), default=(0, b['pieces'][0][0] if b['pieces'] else 0))[1]
            raw = re.sub(r'\s+', ' ', raw).strip()
            plain = re.sub(r'\s+', ' ', render(raw, store, 'plain')).strip()
            plain = re.sub(r'\s+([,.;:)])', r'\1', plain)
            plain = re.sub(r'\(\s*\)', '', plain)
            if not re.search(r'[A-Za-z]{2,}', plain):
                continue
            s = Sent()
            s.i = len(sents)
            s.line = line
            s.part = b['part'] if b['kind'] == 'prose' else b['kind']
            s.kind = b['kind']
            s.section = b.get('section', '')
            s.block = b_id
            s.raw = raw
            s.plain = plain
            s.show = render(raw, store, 'show')
            rt = []
            for t in plain.split():
                if re.search(r'[A-Za-z0-9µ\u0370-\u03ff]', t):
                    rt.append(t)
                elif rt and (',' in t or ';' in t):
                    rt[-1] += ','          # a comma printed as its own token ('Z ′ ,')
            s.rawtoks = rt
            s.toks = [t.strip(PUNCT) for t in s.rawtoks]
            s.low = [t.lower() for t in s.toks]
            extra = sum(store[m.group(1)]['weight'] - 1 for m in PH_RE.finditer(raw)
                        if store[m.group(1)]['kind'] == 'M')
            s.words = len(s.toks) + max(0, extra)
            s.fig = b.get('fig')
            if s.words == 0:
                continue
            sents.append(s)
    for k, s in enumerate(sents):
        s.i = k
    return sents


# =============================================================================================
# Shared word lists and helpers for the checks
# =============================================================================================
KNOWN_ACR = set('''LHC HL-LHC LEP LEP2 ILC CLIC FCC FCC-ee FCC-hh FCC-eh CEPC SPPC ATLAS CMS LHCB ALICE FASER
FASER2 FPF SND SND@LHC MATHUSLA CODEX ANUBIS MOEDAL TOTEM SHIP NA62 NA64 KOTO KEK BES BESIII CERN SLAC FNAL
BNL DESY PSI TRIUMF RHIC EIC HERA SPS DUNE NOVA T2K KATRIN LZ XENON XENONNT PANDAX CDMS CRESST DAMA ADMX CAST
IAXO AMS LIGO CMB BBN WMAP SM BSM QCD QED EW CP CPT CKM PMNS NLO NNLO N3LO LO LL NLL NNLL N3LL PDF MC ML NN
CL CLS GEV TEV MEV KEV EV PEV 1D 2D 3D 4D 5D GPU CPU TPU RAM UV IR RMS US USA UK EU DOE NSF ERC NASA STFC DFG
PYTHIA PYTHIA8 HERWIG SHERPA POWHEG GEANT GEANT4 DELPHES MADGRAPH MG5 ROOT HEPDATA RIVET FASTJET MCFM NNPDF
CTEQ MSTW LHAPDF TMVA CUDA API JSON CSV URL HTML PHD ID OK FAQ AI LLM CPU GPUS IEEE APS JHEP PRD PRL EPJC
ARXIV MB GB TB PB HZ MHZ GHZ KHZ PDFS NNS'''.upper().split())

AUX = {'is', 'are', 'was', 'were', 'am', 'has', 'have', 'had', 'do', 'does', 'did', 'can', 'could', 'may',
       'might', 'will', 'would', 'shall', 'should', 'must', 'cannot', 'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t',
       'doesn\'t', 'don\'t', 'didn\'t', 'can\'t', 'won\'t', 'wouldn\'t', 'shouldn\'t', 'couldn\'t', 'hasn\'t',
       'haven\'t', 'hadn\'t'}
VERB_BASES = '''accept account achieve act add address adjust adopt affect agree aim allow alter amount
analyze analyse appear apply approach approximate argue arise arrive assess assign assume attach attain
attempt attribute average avoid balance base become begin behave believe belong benefit bin blind boost
bound break bring build calculate calibrate call cancel capture carry cause center centre change
characterize characterise check choose cite claim classify cluster collect combine come compare compete
complement complete comprise compute concentrate conclude confirm conserve consider consist constitute
constrain construct contain continue contribute control converge convert correct correlate correspond
cost count couple cover create cross cut deal decay decide decline decouple decrease deduce define
degrade demand demonstrate denote depend deposit derive describe design detect determine develop deviate
differ diminish disappear discard discover discriminate discuss display distinguish distribute divide
dominate double draw drive drop emerge emit employ enable encode encounter end enforce enhance ensure
enter equal escape establish estimate evaluate evolve examine exceed exclude exhibit exist expand expect
experience explain exploit explore express extend extract extrapolate fail fall favor favour feature feed
fill filter find fit fix flip focus follow force form formulate fragment gain generate get give go govern
grow guarantee guide handle happen help hide highlight hold identify ignore illustrate imply impose
improve include incorporate increase indicate induce infer inform inherit initialize integrate interact
interfere interpolate interpret introduce invert investigate involve isolate join keep know label lack
lead learn leave lie limit link list locate look lose lower maintain make manage map match matter maximize
mean measure meet merge minimize miss mix model modify monitor motivate move multiply need normalize note
notice observe obtain occupy occur offer omit open operate optimize originate oscillate outline output
outperform overcome overestimate overlap parameterize parametrize pass peak perform permit pick place play
plot point populate pose possess predict prefer prepare present preserve prevent probe proceed process
produce project promise propagate propose prove provide publish pull push put quantify raise range rank
reach read realize receive reconstruct record recover reduce refer refine reflect regard regress reject
relate release rely remain remove render repeat replace report represent reproduce require rescale
resemble reside resolve respond restrict result retain return reveal reweight rise rotate run sample
satisfy saturate scale scan search see seek select send separate serve set shift show shrink sit smear
solve span specify split stand start state stay stem store study subtract succeed suffer suffice suggest
sum summarize supply support suppress surpass survive take target tend test think train transfer
transform translate travel treat trigger try tune turn undergo underestimate understand unfold update use
utilize validate vanish vary verify view violate wait want weaken weigh weight widen work write yield
outweigh leverage facilitate elucidate delve showcase underscore harness unveil'''.split()
IRREG_PAST = set('''found showed gave took made saw chose led began became held kept left lost met ran rose
fell grew knew drew wrote built brought thought sought sent spent came went got stood understood overcame
underwent arose meant dealt felt told said bound broke drove fed hid lay paid won wore shrank'''.split())
NOUN_BASES = set('''use study test fit model search decay result limit set cut work change increase decrease
range peak sample map list point plot form feature label weight bin trigger target record report process
project approach control cost count cover cross end fall focus gain help lack lead match mean need note
offer place play pass rank return rise run scale scan shift sum start state support turn balance boost
center centre design display double drop equal experience filter fix flip force fragment guide handle
link look lower mix monitor move output overlap pick pull push release regard repeat smear span split
stand stem store transfer travel tune update view wait want yield cluster average account aim amount
attempt bound call check claim cause couple deal demand deposit estimate exhibit feed fill measure
reach source step train track type value select'''.split())
DOUBLE_FINAL = {'fit', 'drop', 'plan', 'stop', 'submit', 'control', 'refer', 'prefer', 'occur', 'permit',
                'omit', 'commit', 'transfer', 'emit', 'admit', 'regret', 'label', 'model', 'travel', 'cancel',
                'scan', 'bin', 'flip', 'map', 'set', 'cut', 'run', 'split', 'put', 'sum', 'begin', 'shift'}


def inflect(base):
    forms = {base}
    if re.search(r'(?:s|sh|ch|x|z|o)$', base):
        forms.add(base + 'es')
    elif re.search(r'[^aeiou]y$', base):
        forms.add(base[:-1] + 'ies')
    else:
        forms.add(base + 's')
    if base.endswith('e'):
        forms.add(base + 'd')
    elif re.search(r'[^aeiou]y$', base):
        forms.add(base[:-1] + 'ied')
    else:
        forms.add(base + 'ed')
        if base in DOUBLE_FINAL:
            forms.add(base + base[-1] + 'ed')
    return forms


MORPH_VERB_RE = re.compile(r'^[a-z]{3,}(?:izes|ises|ates|ifies|yzes|yses|ized|ised|ated|ified|yzed|ysed|'
                           r'[^e]ed)$')
NOT_PART = {'need', 'indeed', 'speed', 'seed', 'feed', 'bed', 'red', 'shed', 'hundred', 'embed', 'proceed',
            'exceed', 'succeed', 'breed', 'weed', 'deed', 'greed', 'naked', 'wicked', 'sacred', 'kindred'}
PRONOUNS = {'we', 'they', 'you', 'i', 'which', 'that', 'who', 'it', 'he', 'she', 'one'}
NOT_PLURAL = set('''its this thus is was has as us bus gas plus minus versus focus basis analysis axis mass
class less process access loss cross previous various numerous continuous consensus status chaos bias
radius thesis hypothesis synthesis emphasis gauss always perhaps whereas does goes lens yes'''.split())
SUBORD = {'because', 'although', 'though', 'while', 'whereas', 'since', 'if', 'when', 'whenever', 'once',
          'unless', 'until', 'as', 'given', 'provided', 'after', 'before', 'assuming', 'whether', 'even'}
OPENER_PREP = {'in', 'for', 'at', 'with', 'by', 'from', 'on', 'to', 'using', 'under', 'within', 'among',
               'during', 'across', 'through', 'beyond', 'despite', 'unlike', 'compared', 'following', 'based',
               'depending', 'starting', 'combining', 'applying', 'assuming', 'taking'}

LABEL_NUM_RE = re.compile(
    r'(?:\b(?:Figs?|Figures?|figures?|Tabs?|Tables?|tables?|Secs?|Sects?|Sections?|sections?|Eqs?|Eqns?|'
    r'Equations?|equations?|Refs?|Apps?|Appendix|Appendices|appendix|Chapters?|Ch|Models?|Runs?|Cases?|'
    r'Scenarios?|Benchmarks?|Steps?|Panels?|Points?|Regions?|Categor(?:y|ies)|Options?|Versions?|'
    r'Algorithms?|Lines?|Rows?|Columns?|Layers?|Iterations?|Epochs?|Phase|Stage|Level|Model)\.?\s*~?\(?\s*'
    r'(?:N|\d+|[IVX]+|[A-H])\b\)?(?:\s*(?:,|and|&|–|-|to|or)\s*\(?(?:N|\d+|[IVX]+|[A-H])\b\)?)*)')
CONTEXT_NUM_RE = re.compile(r'(?:√s|\bs)\s*=\s*\d+(?:\.\d+)?\s*TeV|\b(?:at|of)\s+\d+(?:\.\d+)?\s*TeV\b|'
                            r'\b\d+(?:\.\d+)?\s*(?:fb|pb|ab|nb)\s*(?:\^?\s*\{?\s*[-−]\s*1\}?|⁻¹)')
YEAR_RE = re.compile(r'\b(?:19|20)\d\d\b')
NUM_TOKEN_RE = re.compile(r'(?<![A-Za-z0-9_])\d+(?:[.,]\d+)*(?![A-Za-z0-9])')
SPELLED_NUM_RE = re.compile(r'\b(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|'
                            r'forty|fifty|hundred|thousand|million|billion|twice|thrice|half|halve[sd]?|'
                            r'double[sd]?|doubling|tripled?|quadrupled?|tenfold|twofold|threefold|factor of|'
                            r'orders? of magnitude|percent|per cent|dozen)\b', re.I)
STAT_RE = re.compile(r'\b(?:statistical(?:ly)?|significance|sigma|σ|p-?values?|confidence|excess(?:es)?|'
                     r'deviations?|discovery|evidence|hypothes[ie]s|fluctuations?|test statistic)\b', re.I)
STAT_CS_RE = re.compile(r'\bCLs?\b')


def has_number(plain, strict=False):
    t = LABEL_NUM_RE.sub(' ', plain)
    t = YEAR_RE.sub(' ', t)
    if strict:
        t = CONTEXT_NUM_RE.sub(' ', t)
    return bool(NUM_TOKEN_RE.search(t) or SPELLED_NUM_RE.search(t))


class Flag(dict):
    pass


def flag(check, s, msg, line=None, part=None, text=None, info=False, **kw):
    f = Flag(check=check, line=line if line is not None else (s.line if s else 0),
             part=part if part is not None else (s.part if s else ''),
             text=text if text is not None else (s.excerpt() if s else ''), msg=msg, info=info)
    f.update(kw)
    return f


# =============================================================================================
# Check 1: long sentences
# =============================================================================================
SPLIT_POINTS = [r',\s+which\b', r',\s+(?:and|but)\s+(?:we|the|this|these|it|they|our)\b', r',\s+where\b',
                r',\s+while\b', r',\s+(?:so|thus|hence)\b', r',\s+(?:allowing|leading|resulting|making|giving)\b',
                r'\s+because\b', r',\s+although\b', r',\s+since\b', r',\s+whereas\b']


def long_hint(s):
    p = s.plain
    if ';' in p or re.search(r'\((?:i|ii|1|a)\)|\brespectively\b', p):
        return 'It has visible structure (a semicolon, an enumeration or *respectively*); check that every part is needed.'
    best = None
    for pat in SPLIT_POINTS:
        for m in re.finditer(pat, p):
            before = len(p[:m.start()].split())
            after = len(p[m.end():].split())
            if before >= 10 and after >= 6:
                if best is None or abs(before - s.words / 2) < abs(best[0] - s.words / 2):
                    best = (before, m.group(0).strip())
    if best:
        return 'No visible structure; one place to split is *%s* (after word %d).' % (best[1], best[0])
    return 'No visible structure; split it, or give the parts visible structure.'


def length_rows(sents):
    rows = []
    groups = [('abstract', lambda s: s.part == 'abstract'), ('intro', lambda s: s.part == 'intro'),
              ('body', lambda s: s.part == 'body'), ('concl', lambda s: s.part == 'concl'),
              ('app', lambda s: s.part == 'app'), ('prose', lambda s: s.kind == 'prose'),
              ('caption', lambda s: s.kind == 'caption')]
    for name, pred in groups:
        ls = [s.words for s in sents if pred(s)]
        if not ls:
            continue
        srt = sorted(ls)
        n = len(ls)
        rows.append(dict(part=name, n=n, words=sum(ls), median=statistics.median(ls),
                         mean=round(statistics.mean(ls), 1), p90=srt[min(n - 1, int(round(0.9 * (n - 1))))],
                         le12=round(100 * sum(1 for x in ls if x <= 12) / n, 1),
                         gt30=round(100 * sum(1 for x in ls if x > 30) / n, 1),
                         gt40=round(100 * sum(1 for x in ls if x > 40) / n, 1)))
    return rows


def check_long(doc, opts):
    mx = opts.max_words
    very = max(60, mx + 20)
    flags, info = [], []
    for s in doc.sents:
        if s.words > mx:
            hint = long_hint(s)
            structured = hint.startswith('It has visible structure')
            msg = '%d words%s. %s' % (s.words, ' (very long)' if s.words > very else '', hint)
            if structured and s.words <= very:
                info.append(flag(1, s, msg, words=s.words, info=True))
            else:
                flags.append(flag(1, s, msg, words=s.words))
    return dict(flags=flags, info=info, rows=length_rows(doc.sents))


# =============================================================================================
# Check 2: late main verb
# =============================================================================================
LATE_VERB = 12


def nounish(w):
    return (w.isalpha() and len(w) >= 3 and w not in FW and w not in AUX and not w.endswith('ly')
            and w not in PRONOUNS and w not in SUBORD)


DETS = set('''the a an this these those each every any some no our their its his her my your all both such
several many few other another either neither whose'''.split())
PREPS = set('''of in on at for with by from into onto over under between among through across about above
below per via without within after before during until against along around behind beyond near toward
towards upon throughout than as'''.split())
NUMWORDS = set('one two three four five six seven eight nine ten'.split())
LABEL_WORDS = {'fig', 'figs', 'figure', 'figures', 'table', 'tables', 'tab', 'eq', 'eqs', 'equation',
               'equations', 'section', 'sec', 'appendix', 'app', 'model', 'run', 'ref', 'refs', 'step'}
SUBJ_PRON = {'we', 'they', 'it', 'he', 'she', 'i', 'you'}
NOUN_S_ENDINGS = ('ss', 'us', 'is', 'ics', 'ous', 'ices', 'ions', 'ments', 'nesses', 'ities', 'ances', 'ences',
                  'ers', 'ors', 'ons', 'ists', 'isms', 'als', 'ings', 'ays', 'eys', 'ains', 'ets', 'ies')
ADJ_ENDINGS = ('ed', 'al', 'ic', 'ive', 'ous', 'ent', 'ant', 'ary', 'ble', 'ar', 'ful', 'less', 'ing')
CLAUSE_START = {'then', 'and', 'but', 'so', 'while', 'whereas', 'if', 'when', 'because', 'that', 'which', 'since',
                'although', 'though', 'or', 'nor', 'yet', 'where'}
AFTER_VERB = (PREPS - {'of', 'as', 'than'}) | (DETS - {'all', 'both', 'each', 'several', 'many', 'few'}) | {
    'to', 'that', 'not', 'also', 'only', 'well', 'more', 'less', 'much', 'very', 'up', 'out', 'down', 'off',
    'into', 'it', 'them', 'us', 'there', 'here'}
SKIP_ADV = {'also', 'then', 'first', 'further', 'now', 'only', 'still', 'thus', 'therefore', 'not', 'instead',
            'again', 'often', 'always', 'never', 'already', 'here', 'next', 'finally', 'all', 'both', 'each'}
FORM_BASE = {}
for _b in VERB_BASES:
    for _f in inflect(_b):
        FORM_BASE.setdefault(_f, _b)
for _f in IRREG_PAST:
    FORM_BASE.setdefault(_f, _f)


def is_finite(low, j):
    '''Generous test for a finite verb at position j: when unsure it says yes, so that the
    check flags fewer sentences rather than more.'''
    w = low[j]
    prev = low[j - 1] if j > 0 else ''
    prev2 = low[j - 2] if j > 1 else ''
    nxt = low[j + 1] if j + 1 < len(low) else ''
    if w in AUX:
        return not (prev == 'to' and w in ('have', 'do'))
    base = FORM_BASE.get(w)
    if base is None:
        if not w.isalpha() or w in FW or w in SUBORD:
            return False
        if MORPH_VERB_RE.match(w) and w not in NOT_PART:
            base = w
        elif (w.endswith('s') and len(w) >= 4 and not w.endswith(NOUN_S_ENDINGS)
              and prev not in CLAUSE_START and j > 0 and not prev.endswith(ADJ_ENDINGS)
              and (nxt in AFTER_VERB or nxt.endswith('ly') or not nxt)):
            base = w        # unknown word in -s before a function word: maybe a verb (it fades, X struggles)
        elif w.endswith('ed') and len(w) >= 5 and w not in NOT_PART and (nxt in AFTER_VERB or nxt.endswith('ly')):
            base = w
        else:
            return False
    noun = base in NOUN_BASES or base == w and w.endswith('s')
    if prev == 'to':
        return False
    if noun and w != base and w.endswith('s') and len(prev) > 3 and prev.endswith(ADJ_ENDINGS):
        return False                  # 'simulated samples', 'experimental results'
    if prev in DETS:
        return j == 1 and prev in ('this', 'these', 'that', 'those') and not noun and not w.endswith('ed')
    if prev in PREPS:
        return w.endswith('s') and not noun and not w.endswith('ed')
    if prev in NUMWORDS or re.match(r'^\d', prev) or prev == '0':
        if prev2.rstrip('.') in LABEL_WORDS:
            return True
        if noun and not (w.endswith('s') and nxt in AFTER_VERB):
            return False
    if w == base and base in NOUN_BASES and nounish(nxt):
        subj = (prev in PRONOUNS or prev in AUX or prev.endswith('ly')
                or (prev.endswith('s') and prev not in NOT_PLURAL and len(prev) > 3))
        if not subj:
            return False
    return True


def main_verb(s):
    '''(position of the main verb, the verb, words before the main clause, words of subject before the verb).'''
    low, raw = s.low, s.rawtoks
    if not low:
        return None
    start = 0
    for _ in range(4):
        w = low[start] if start < len(low) else ''
        w2 = low[start + 1] if start + 1 < len(low) else ''
        gerund = w.endswith('ing') and len(w) > 4 and w not in OPENER_PREP
        relative = start > 0 and w in ('which', 'where', 'whose', 'whereby')
        if (w in SUBORD or w in OPENER_PREP or w in CONNECTIVE_OPENERS or gerund or relative
                or (w.endswith('ly') and w2.endswith('ing'))):
            c = next((k for k in range(start, min(len(raw), start + 35)) if raw[k].endswith(',')), None)
            if gerund:
                end = c if c is not None else min(len(low), start + 30)
                if any(is_finite(low, k) for k in range(start + 1, end + 1 if c is not None else end)):
                    break            # a gerund subject: 'Predicting X requires ...'
            if w not in SUBORD and not relative:
                end = c if c is not None else min(len(low), start + 30)
                if any(low[k] in SUBJ_PRON and k + 1 < len(low) and low[k + 1].isalpha()
                       and (low[k + 1] not in FW or low[k + 1] in AUX) for k in range(start + 1, end)):
                    break            # 'In this paper we study ...': the main clause has started
            if c is None:
                if w in SUBORD or relative:
                    return None
                break
            start = c + 1
        else:
            break
    j = None
    for k in range(start, min(len(low), start + 45)):
        if low[k] in SUBJ_PRON:
            q = k + 1
            while q < len(low) and (low[q] in SKIP_ADV or (low[q].endswith('ly') and len(low[q]) > 3)):
                q += 1
            if q < len(low) and low[q].isalpha() and (low[q] not in FW or low[q] in AUX) and low[q] not in SUBORD:
                j = q
                break
        if is_finite(low, k):
            j = k
            break
    if j is None:
        return None
    commas = [k for k in range(start, j) if raw[k].endswith(',')]
    subj_start = max(start, commas[-1] + 1) if commas else start
    return j + 1, s.toks[j], start, j - subj_start


CONNECTIVE_OPENERS = {'however', 'thus', 'therefore', 'moreover', 'furthermore', 'additionally', 'finally',
                      'similarly', 'consequently', 'nevertheless', 'here', 'instead', 'again', 'first', 'next',
                      'then', 'hence', 'also', 'alternatively', 'specifically', 'unfortunately', 'indeed',
                      'importantly', 'notably', 'still', 'overall', 'practically', 'theoretically',
                      'historically', 'traditionally', 'experimentally', 'typically', 'generally', 'ideally'}
LATE_OPENER = 15
LATE_SUBJECT = 14


def check_verb(doc, opts):
    flags = []
    positions = []
    for s in doc.sents:
        if s.kind == 'caption' or len(s.toks) < 15:
            continue
        mv = main_verb(s)
        if not mv:
            continue
        pos, verb, o, d = mv
        positions.append(pos)
        if pos <= LATE_VERB or (o < LATE_OPENER and d < LATE_SUBJECT):
            continue
        if o >= LATE_OPENER:
            why = 'after an opening %s of %d words' % ('clause' if s.low[0] in SUBORD else 'phrase', o)
            fix = 'Start with the main clause, or move the opening part into its own sentence.'
        else:
            why = 'after a subject of %d words' % d
            fix = 'Shorten the subject (move its qualifiers after the verb), or split.'
        msg = 'Main verb *%s* at word %d, %s. %s' % (verb, pos, why, fix)
        flags.append(flag(2, s, msg, text=shorten(' '.join(s.show.split()[:max(pos + 3, 18)]), 170), pos=pos))
    return dict(flags=flags, median=statistics.median(positions) if positions else None, n=len(positions))


# =============================================================================================
# Check 3: stock connectors and filler
# =============================================================================================
CONN_A = re.compile(r'^(?:moreover|furthermore|notably|importantly|interestingly|hence|thus(?!\s+far)|also|'
                    r'besides|what is more|more importantly|most importantly|last but not least|needless to say|'
                    r'on top of that|significantly)\b(?!\s+(?:larger|smaller|more|less|better|worse|higher|lower))',
                    re.I)
CONN_B = re.compile(r'^(?:in addition|additionally|therefore|consequently|as a consequence)\b', re.I)
STOCK_RE = re.compile(
    r'\bit (?:is|should be|must be|can be|has to be|may be|was) (?:worth (?:noting|mentioning|pointing out|'
    r'emphasi[sz]ing|stressing|remembering)|(?:important|interesting|crucial|essential|necessary|useful|'
    r'instructive|noteworthy|worthwhile) to (?:note|mention|point out|stress|emphasi[sz]e|remember|recall|'
    r'keep in mind|notice|highlight)|noted|mentioned|emphasi[sz]ed|stressed|pointed out|recalled|remembered|'
    r'highlighted)\s+(?:here\s+)?that\b|\bit is noteworthy that\b|\bit (?:is|becomes) (?:evident|obvious|apparent) that\b|'
    r'\bneedless to say\b|\bit goes without saying\b', re.I)
IN_ORDER_RE = re.compile(r'\bin order (?:to|for)\b', re.I)
ALT = {'moreover': 'drop it, or say how the point follows', 'furthermore': 'drop it, or say how the point follows',
       'additionally': 'drop it; a new point needs no announcement', 'in addition': 'drop it, or merge with the previous sentence',
       'also': 'move *also* after the subject (We also ...)', 'thus': 'use *so* or a mid-sentence *therefore*',
       'hence': 'use *so* or a mid-sentence *therefore*', 'therefore': 'move it inside the sentence, or use *so*',
       'notably': 'drop it; state the fact', 'importantly': 'drop it; say why it matters',
       'interestingly': 'drop it; let the reader judge', 'consequently': 'use *so*, or join with the previous sentence',
       'in particular': 'keep only if you narrow a general statement', 'besides': 'drop it',
       'significantly': 'drop it, or give the number'}


def sentence_start(plain):
    return re.sub(r'^[\s\x22“‘(\[•\-–—]+', '', plain)


def check_connectors(doc, opts):
    flags = []
    openers = []
    prose = [s for s in doc.sents if s.kind != 'caption']
    words = sum(s.words for s in doc.sents if s.kind == 'prose') or 1
    last_open = {}
    for idx, s in enumerate(prose):
        st = sentence_start(s.plain)
        ma, mb = CONN_A.match(st), CONN_B.match(st)
        if ma or mb:
            m = ma or mb
            w = m.group(0).lower()
            openers.append(w)
            if ma:
                flags.append(flag(3, s, 'Sentence opens with *%s*. %s.' % (m.group(0), ALT.get(w, 'drop it').capitalize())))
            else:
                prev = [p for p in range(max(0, idx - 3), idx) if p in last_open and prose[p].section == s.section]
                if prev:
                    flags.append(flag(3, s, 'Second stock connector in a row: *%s* after *%s* (line %d). '
                                            'Chains of connectors read as padding; %s.'
                                      % (m.group(0), last_open[prev[-1]], prose[prev[-1]].line,
                                         ALT.get(w, 'drop one'))))
            last_open[idx] = m.group(0)
        for m in STOCK_RE.finditer(s.plain):
            flags.append(flag(3, s, 'Filler *%s*: state the point directly.' % m.group(0)))
        for m in IN_ORDER_RE.finditer(s.plain):
            flags.append(flag(3, s, '*%s*: write *%s*.' % (m.group(0), 'to' if m.group(0).lower().endswith('to') else 'for')))
    return dict(flags=flags, openers=Counter(openers), rate=round(1000 * len(openers) / words, 2))


# =============================================================================================
# Check 4: inflated vocabulary
# =============================================================================================
INFLATED = [
    (r'utili[sz](?:e|es|ed|ing|ation|ations)', 'use'),
    (r'leverag(?:e|es|ed|ing)', 'use, exploit'),
    (r'facilitat(?:e|es|ed|ing)', 'allow, help, make easier'),
    (r'elucidat(?:e|es|ed|ing)', 'explain, clarify'),
    (r'delv(?:e|es|ed|ing)', 'study, examine'),
    (r'endeavou?r(?:s|ed|ing)?', 'try, attempt, effort'),
    (r'plethora', 'many'),
    (r'myriad', 'many'),
    (r'paradigms?', 'approach, framework, model'),
    (r'aforementioned', 'this, these, the ... above'),
    (r'commenc(?:e|es|ed|ing)', 'begin, start'),
    (r'ascertain(?:s|ed|ing)?', 'determine, check'),
    (r'showcas(?:e|es|ed|ing)', 'show'),
    (r'underscor(?:e|es|ed|ing)', 'show, stress'),
    (r'harness(?:es|ed|ing)?', 'use'),
    (r'unveil(?:s|ed|ing)?', 'show, report'),
    (r'realms?', 'area, field, regime'),
    (r'intricate(?:ly)?|intricacies', 'complex, detailed'),
    (r'meticulous(?:ly)?', 'careful, carefully'),
    (r'whilst', 'while'),
    (r'amongst', 'among'),
    (r'henceforth', 'from now on, below'),
    (r'heretofore', 'so far, until now'),
    (r'thereof', 'of it, of them'),
    (r'wherein', 'where, in which'),
    (r'multitudes?(?: of)?', 'many'),
    (r'prior to', 'before'),
    (r'subsequent to', 'after'),
    (r'in the vicinity of', 'near, about'),
    (r'in close proximity to', 'near'),
    (r'due to the fact that', 'because'),
    (r'owing to the fact that', 'because'),
    (r'(?:in spite of|despite) the fact that', 'although'),
    (r'a (?:large|great|significant|substantial) number of', 'many'),
    (r'the (?:vast )?majority of', 'most'),
    (r'(?:has|have|had) the (?:ability|capability|capacity) to', 'can'),
    (r'(?:is|are) capable of', 'can'),
    (r'with the help of', 'with, using'),
    (r'for the purpose of', 'for, to'),
    (r'at this point in time|at the present time', 'now'),
    (r'in light of', 'given, because of'),
    (r'with regards? to', 'about, for, on'),
    (r'a wide (?:array|variety|range) of', 'many, several (or name them)'),
    (r'play(?:s|ed|ing)? (?:a|an) (?:key|crucial|vital|pivotal|important|central|essential) role in', 'matter for, set, control (say how)'),
]
INFLATED_RE = [(re.compile(r'\b(?:%s)\b' % p, re.I), alt) for p, alt in INFLATED]


def check_vocab(doc, opts):
    flags = []
    hits = Counter()
    for s in doc.sents:
        for rx, alt in INFLATED_RE:
            for m in rx.finditer(s.plain):
                hits[m.group(0).lower()] += 1
                flags.append(flag(4, s, '*%s*: write *%s*.' % (m.group(0), alt)))
    return dict(flags=flags, hits=hits)


# =============================================================================================
# Check 5: hype and intensifiers
# =============================================================================================
HYPE = [
    (r'novel(?:ty)?', 'always', 'new, or say what is new'),
    (r'remarkabl[ey]', 'always', 'drop it, or give the number'),
    (r'promising', 'always', 'say what it achieves'),
    (r'crucial(?:ly)?', 'always', 'important, or say why it matters'),
    (r'unprecedented', 'always', 'give the comparison'),
    (r'groundbreaking|ground-breaking|revolutionary|game-?chang(?:ing|er)', 'always', 'drop it'),
    (r'state[- ]of[- ]the[- ]art', 'always', 'name the method and give the comparison'),
    (r'cutting[- ]edge', 'always', 'drop it'),
    (r'paramount|pivotal|invaluable', 'always', 'important, or say why'),
    (r'excellent|outstanding|impressive|superb|exceptional(?:ly)?|extraordinary|tremendous(?:ly)?|spectacular',
     'always', 'give the number'),
    (r'powerful', 'comparative', 'give the comparison (more powerful than ...)'),
    (r'dramatic(?:ally)?', 'number', 'give the number'),
    (r'very', 'number', 'drop it, or give the number'),
    (r'extremely|incredibly|vastly|hugely|enormously|immensely|greatly', 'number', 'drop it, or give the number'),
    (r'highly', 'number', 'drop it, or give the number'),
    (r'significant(?:ly)?', 'stat', 'give the number, or use *substantial* or *large*'),
]
HYPE_RE = [(re.compile(r'\b(?:%s)\b' % p, re.I), kind, alt) for p, kind, alt in HYPE]


def check_hype(doc, opts, vague_lines):
    flags = []
    for s in doc.sents:
        num = has_number(s.plain)
        stat = bool(STAT_RE.search(s.plain) or STAT_CS_RE.search(s.plain))
        for rx, kind, alt in HYPE_RE:
            for m in rx.finditer(s.plain):
                w = m.group(0)
                lw = w.lower()
                before = s.plain[:m.start()].lower().split()[-1:] or ['']
                after = s.plain[m.end():].lower().split()[:1] or ['']
                if kind == 'number' and (num or s.i in vague_lines):
                    continue
                if lw == 'very' and after[0].strip(PUNCT) in ('first', 'same', 'end', 'beginning', 'last', 'least', 'top', 'bottom'):
                    continue
                if lw == 'highly' and after[0].strip(PUNCT) in ('boosted', 'collimated', 'energetic', 'ionizing', 'ionising', 'excited', 'relativistic', 'correlated'):
                    continue
                if kind == 'comparative' and before[0] in ('more', 'less', 'as'):
                    continue
                if kind == 'stat' and (num or stat or s.i in vague_lines):
                    continue
                if re.search(r'\bplay(?:s|ed|ing)? (?:a|an) (?:key|crucial|vital|pivotal|important|central|essential) '
                             r'role\b', s.plain[max(0, m.start() - 12):m.end() + 6], re.I):
                    continue          # already flagged by check 4
                flags.append(flag(5, s, '*%s*: %s.' % (w, alt)))
    return dict(flags=flags)


# =============================================================================================
# Check 6: vague result claims
# =============================================================================================
VAGUE_RE = re.compile(r'\b(?:improv(?:e|es|ed|ing|ement|ements)|better|enhanc(?:e|es|ed|ing|ement|ements)|'
                      r'outperform(?:s|ed|ing)?|gain(?:s|ed|ing)|superior|boost(?:s|ing)?|'
                      r'(?:significant|substantial|large|considerable|major|notable|clear|dramatic) gain)\b', re.I)
BASELINE_RE = re.compile(r'\b(?:than|compared (?:to|with)|in comparison (?:to|with)|relative to|with respect to|'
                         r'versus|vs\.?|against|over(?= (?:the|a|an|our|their|this|that|those|existing|previous|'
                         r'standard|traditional|current|conventional|untagged|inclusive)\b)|instead of|baseline|'
                         r'benchmark|reference (?:method|search|analysis|selection|model|tagger)|without)\b', re.I)
GENERIC = set('''existing previous traditional conventional standard current other classical prior earlier
state-of-the-art methods method approaches approach techniques technique algorithms algorithm models model
analyses analysis searches search works work studies study results ones those before alternatives
alternative baselines the a an all most many some any common usual typical'''.split())
MODALS = {'could', 'would', 'may', 'might', 'can', 'will', 'should', 'must', 'shall'}
RESEARCH_VERBS = {'estimate', 'estimates', 'study', 'studies', 'explore', 'explores', 'quantify', 'quantifies',
                  'evaluate', 'evaluates', 'measure', 'measures', 'assess', 'assesses', 'investigate',
                  'investigates', 'examine', 'examines', 'compute', 'computes', 'calculate', 'calculates',
                  'test', 'tests', 'determine', 'determines', 'probe', 'probes', 'characterize', 'characterizes'}


def named_baseline(plain):
    for m in BASELINE_RE.finditer(plain):
        w = m.group(0).lower()
        if w in ('baseline', 'benchmark') or w.startswith('reference') or w == 'without':
            return True
        nxt = [t.strip(PUNCT).lower() for t in plain[m.end():].split()[:4]]
        content = [t for t in nxt if t and t not in GENERIC and t not in FW]
        if content:
            return True
    return False


def check_vague(doc, opts):
    flags = []
    vague = set()
    sents = doc.sents
    for k, s in enumerate(sents):
        if s.plain.rstrip().endswith('?'):
            continue
        if PH_O in s.raw and any(doc.store[x.group(1)]['kind'] == 'C' for x in PH_RE.finditer(s.raw)):
            continue                      # a claim about cited work
        if re.search(r'\b(?:could|would|may|might)\b', s.plain, re.I):
            continue                      # a hypothetical or an outlook, not a result
        hit = None
        for m in VAGUE_RE.finditer(s.plain):
            before = [t.strip(PUNCT).lower() for t in s.plain[:m.start()].split()[-4:]]
            after = s.plain[m.end():].lower().split()[:1]
            w = m.group(0).lower()
            if before and before[-1] in ('to', 'not', 'no', 'n\'t', 'without', 'with', 'such', 'further', 'possible',
                                          'potential', 'any', 'for'):
                continue
            if any(b in RESEARCH_VERBS for b in before[-3:]):
                continue
            if any(b in MODALS for b in before[-2:]) or 'not' in before[-2:]:
                continue
            if w == 'better' and after and re.match(r'(understand|understood|known|suited|than|able|described)', after[0]):
                continue
            if re.search(r'\bwhether\b|\bif\b', s.plain[:m.start()], re.I) and w not in ('outperforms', 'outperformed'):
                continue
            hit = m
            break
        if not hit:
            continue
        pre = [t.strip(PUNCT).lower() for t in s.plain[:hit.start()].split()[-2:]]
        back = 3 if pre and pre[-1] in ('the', 'these', 'this', 'that', 'those') else 1
        window = [x for x in sents[max(0, k - back):k + 2] if x.block == s.block]
        if any(has_number(x.plain, strict=True) for x in window):
            continue
        if any(named_baseline(x.plain) for x in window):
            continue
        vague.add(s.i)
        flags.append(flag(6, s, '*%s* with no number and no named baseline nearby. Give the size of the change and '
                                'what it is compared with (for example *a factor of 2 over the untagged search*).'
                          % hit.group(0)))
    return dict(flags=flags, vague=vague)


# =============================================================================================
# Check 7: acronyms
# =============================================================================================
ACR_TOKEN_RE = re.compile(r'(?<![A-Za-z0-9\u0370-\u03ff\\])([A-Z][A-Za-z0-9@&]*(?:-[A-Z0-9][A-Za-z0-9@&]*)*)'
                          r'(?![A-Za-z0-9\u0370-\u03ff])')
DEF_PAREN_RE = re.compile(r'((?:[A-Za-z][\w\'’-]*\s+){0,8}[A-Za-z][\w\'’-]*)\s*\(\s*([A-Z][A-Za-z0-9@&-]*[A-Z0-9][a-z0-9]?s?)'
                          r'\s*-?\s*(?:[;,][^)]*)?\)')
DEF_REV_RE = re.compile(r'\b([A-Z][A-Za-z0-9@&-]*[A-Z0-9])s?\s*\(\s*([A-Za-z][^()]{4,80})\)')
DEF_PHRASE_RE = re.compile(r'(?:[Rr]eferred to as|[Hh]ereafter|[Hh]enceforth|called|denoted(?: as| by)?|'
                           r'abbreviated(?: as)?|or simply)\s+(?:the\s+)?[“\x22]?([A-Z][A-Za-z0-9-]*[A-Z0-9])|'
                           r'\b([A-Z][A-Za-z0-9-]*[A-Z0-9])s?\s+(?:stands for|is short for)\b')


def acr_norm(tok):
    t = tok
    if len(t) >= 3 and t.endswith('s') and t[:-1].upper() == t[:-1]:
        t = t[:-1]
    return t


def is_acronym(t):
    if len(t) < 2 or sum(c.isupper() for c in t) < 2:
        return False
    if re.search(r'[a-z]', t) and not re.fullmatch(r'[A-Z0-9@&-]*[0-9][a-z]', t):
        return False
    if re.fullmatch(r'[IVX]+', t) or re.fullmatch(r'[WZH]{2,4}', t) or re.fullmatch(r'[XYZ]{2,3}', t):
        return False
    if re.search(r'\d[A-Z]', t) or re.fullmatch(r'[A-Z]{2}\d+', t):
        return False          # identifiers and versions (CTEQ6L1, MSTW2008LO, KS0, IM12)
    if re.fullmatch(r'[A-Z]{7,}', t):
        return False
    return True


def initials_ok(acr, words):
    letters = [c for c in acr if c.isalpha()]
    if not letters:
        return False
    first = letters[0].lower()
    for w in words[-(len(letters) + 3):]:
        for part in re.split(r'[-/]', w):
            if part[:1].lower() == first:
                return True
    return False


def find_definitions(plain):
    defs = []
    for m in DEF_PAREN_RE.finditer(plain):
        acr = acr_norm(m.group(2).rstrip('-'))
        words = m.group(1).split()
        if is_acronym(acr) and words and initials_ok(acr, words) and words[-1] != acr:
            defs.append(acr)
    for m in DEF_REV_RE.finditer(plain):
        acr = acr_norm(m.group(1))
        inner = m.group(2).split()
        if is_acronym(acr) and len(inner) >= 2 and any(w[:1].lower() == acr[0].lower() for w in inner[:3]):
            defs.append(acr)
    for m in DEF_PHRASE_RE.finditer(plain):
        acr = acr_norm(m.group(1) or m.group(2))
        if is_acronym(acr):
            defs.append(acr)
    return defs


MATHY_RE = re.compile('[\u0370-\u03ff±→←↔≈∼≤≥⟨⟩′∗×√=<>+−µ]|^[A-Za-z]$')


def find_acronyms(plain, known, pdf_like=False):
    out = []
    for m in ACR_TOKEN_RE.finditer(plain):
        tok = m.group(1)
        if re.match(r'\s*\(\s*\d', plain[m.end():m.end() + 4]):
            continue                                  # SU(3), U(1) and the like
        if pdf_like:
            before = plain[:m.start()].split()[-1:] or ['']
            after = plain[m.end():].split()[:1] or ['']
            touch = plain[max(0, m.start() - 1):m.start()] + plain[m.end():m.end() + 1]
            if MATHY_RE.search(before[0]) or MATHY_RE.search(after[0]) or MATHY_RE.search(touch):
                continue                              # flattened math from PDF extraction (Gµν, K0S, ⟨EN⟩)
        whole = acr_norm(tok)
        if whole.upper() in known:
            out.append(whole)
            continue
        parts = tok.split('-') if '-' in tok else [tok]
        for p in parts:
            p = acr_norm(p)
            if is_acronym(p):
                out.append(p)
    return out


def cited_name(s, acr, store):
    '''True when the first use of a name is followed within a few words by a citation, the usual way the
    papers introduce a tool or a tagger (Pythia 8.3 [25], CATHODE [16]).'''
    m = re.search(r'(?<![A-Za-z0-9])%s(?![A-Za-z0-9])' % re.escape(acr), s.raw)
    if not m:
        return False
    tail = s.raw[m.end():m.end() + 60]
    for x in PH_RE.finditer(tail):
        if store[x.group(1)]['kind'] == 'C' and len(tail[:x.start()].split()) <= 4:
            return True
    return False


def check_acronyms(doc, opts):
    known = KNOWN_ACR | {k.upper() for k in opts.known}
    flags, info = [], []
    ordered = sorted(doc.sents, key=lambda s: (s.line, s.i))
    defs = defaultdict(lambda: {'abstract': [], 'body': []})
    uses = defaultdict(list)
    cited = set()
    for s in ordered:
        scope = 'abstract' if s.part == 'abstract' else 'body'
        for a in set(find_definitions(s.plain)):
            defs[a][scope].append((s.line, s.i))
        for a in find_acronyms(s.plain, known, doc.pdf_like):
            uses[a].append(s)
            if a not in cited and not uses[a][:-1] and cited_name(s, a, doc.store):
                cited.add(a)
    for a, us in sorted(uses.items(), key=lambda kv: (kv[1][0].line, kv[0])):
        d = defs.get(a, {'abstract': [], 'body': []})
        isknown = a.upper() in known
        if isknown and not d['body'] and not d['abstract']:
            continue
        abs_uses = [s for s in us if s.part == 'abstract']
        body_uses = [s for s in us if s.part != 'abstract']
        main_uses = [s for s in body_uses if s.kind != 'caption']
        if body_uses:
            if d['body']:
                first_def = min(d['body'])
                early = [s for s in main_uses if (s.line, s.i) < first_def]
                if early:
                    flags.append(flag(7, early[0], '*%s* is used here, before its definition on line %d. Define it at '
                                                   'first use (corpus: no acronym appears before its definition).'
                                      % (a, first_def[0])))
                if len(d['body']) > 1:
                    info.append(flag(7, None, '*%s* is defined %d times (lines %s); once is enough.'
                                     % (a, len(d['body']), ', '.join(str(x[0]) for x in d['body'][:4])),
                                     line=d['body'][1][0], part='', text='', info=True))
                n_other = sum(1 for s in body_uses if (s.line, s.i) not in d['body'])
                if n_other == 0 and not isknown:
                    info.append(flag(7, None, '*%s* is defined (line %d) but never used again; spell it out instead.'
                                     % (a, first_def[0]), line=first_def[0], part='', text='', info=True))
            elif not isknown and a not in cited:
                first = (main_uses or body_uses)[0]
                if d['abstract']:
                    flags.append(flag(7, first, '*%s* is defined only in the abstract (line %d). Define it again at '
                                                'its first use in the main text.' % (a, d['abstract'][0][0])))
                else:
                    flags.append(flag(7, first, '*%s* is never defined (%d use%s). Spell it out at first use, '
                                                'as *Long Form (%s)*, or add it to --known if it is standard.'
                                      % (a, len(us), '' if len(us) == 1 else 's', a)))
        if abs_uses and not isknown and not d['abstract']:
            flags.append(flag(7, abs_uses[0], '*%s* is used in the abstract without a definition there. The abstract '
                                              'is read alone: spell it out, or drop the acronym.' % a))
    return dict(flags=flags, info=info, n_acr=len(uses))


# =============================================================================================
# Check 8: terminology variants
# =============================================================================================
WORDTOK_RE = re.compile('[A-Za-z][A-Za-z\'’]*(?:-[A-Za-z][A-Za-z\'’]*)*')
PARTICLES = {'up', 'off', 'on', 'out', 'down', 'in', 'over', 'back', 'away', 'through', 'about'}
SPELL_FAMILIES = [
    ('-or/-our', re.compile(r'\b(flavo|colo|behavio|favo|hono|labo|neighbo|humo|vapo|rigo|vigo|odo|tumo|armo|'
                            r'endeavo|harbo|rumo|savio|valo|splendo|parlo)(u?)r(s|ed|ing|ful|less|al|ally|ite|ites|'
                            r'able|ably|ings)?\b', re.I), lambda m: 'UK' if m.group(2) else 'US'),
    ('-ize/-ise', re.compile(r'\b(real|normal|renormal|optim|minim|maxim|character|util|organ|recogn|emphas|summar|'
                             r'general|local|regular|parametr|parameter|standard|visual|final|initial|special|'
                             r'categor|author|central|neutral|polar|random|symmetr|quant|linear|discret|digit|'
                             r'synchron|stabil|ideal|hypothes|memor|critic|theor|trivial|vector|token|mobil|homogen|'
                             r'harmon|magnet|crystall|marginal|factor|diagonal|orthogonal|unitar|legal|item|priorit|'
                             r'capital|conceptual|formal|individual|modular|sanit|apolog|familiar|immun|material|'
                             r'modern|natural|minimal|maximal|optimal|global|personal|summar|tensor|matrix)'
                             r'i([sz])(e|es|ed|ing|ation|ations|er|ers|able)\b', re.I),
     lambda m: 'UK' if m.group(2).lower() == 's' else 'US'),
    ('-yze/-yse', re.compile(r'\b(?!analyses\b)(anal|paral|catal|hydrol|electrol|dial)y([sz])(e|es|ed|ing|er|ers)\b', re.I),
     lambda m: 'UK' if m.group(2).lower() == 's' else 'US'),
    ('-l/-ll', re.compile(r'\b(model|label|travel|cancel|signal|tunnel|channel|level|fuel|total|equal|dial|counsel|'
                          r'marshal|jewel)(l?)(ed|ing|er|ers)\b', re.I), lambda m: 'UK' if m.group(2) else 'US'),
    ('-er/-re', re.compile(r'\b(cent|fib|lit|theat|calib|sab|somb|spect)(er|re|r)(s|d|ed|ing)?\b(?!-?[a-z])', re.I),
     lambda m: 'UK' if m.group(2).lower() in ('re', 'r') else 'US'),
    ('other', re.compile(r'\b(catalog|analog|artifact|aluminum|defense|offense|skeptic|sulfur|judgment|'
                         r'acknowledgment|aging|fulfill|enroll|focused|focusing|percent)(s|al|ally)?\b|'
                         r'\b(catalogue|analogue|artefact|aluminium|defence|offence|sceptic|sulphur|judgement|'
                         r'acknowledgement|ageing|fulfil|enrol|focussed|focussing|per cent)(s|al|ally)?\b', re.I),
     lambda m: 'US' if m.group(1) else 'UK'),
]
PARAM_RE = re.compile(r'\bparamet(e?)ri[sz](?:e|es|ed|ing|ation|ations)\b', re.I)


def term_tokens(doc):
    '''Word tokens with case, position flags and line, from all sentences.'''
    out = []
    for s in doc.sents:
        p = s.plain
        toks = list(WORDTOK_RE.finditer(p))
        for k, m in enumerate(toks):
            pre = p[:m.start()].rstrip()
            initial = (k == 0) or pre.endswith((':', '•', '.', '?', '!', '(', '“', '\x22'))
            nxt = p[m.end():m.end() + 2]
            out.append(dict(w=m.group(0), lw=m.group(0).lower(), s=s, k=k, initial=initial,
                            punct_after=bool(re.match(r'\s*[.,;:)]', nxt)) or m.end() == len(p),
                            next=(toks[k + 1].group(0).lower() if k + 1 < len(toks)
                                  and not re.search(r'[.,;:()]', p[m.end():toks[k + 1].start()]) else None)))
    return out


def check_terms(doc, opts):
    flags, notes = [], []
    toks = term_tokens(doc)
    by_sent = defaultdict(list)
    for t in toks:
        by_sent[t['s'].i].append(t)
    # (a) hyphen / space / closed forms
    hyph = defaultdict(list)
    for t in toks:
        if '-' in t['lw'] and re.fullmatch(r'[a-z]+(?:-[a-z]+)+', t['lw']) and len(t['lw']) >= 5:
            hyph[t['lw']].append(t)
    words = defaultdict(list)
    for t in toks:
        words[t['lw']].append(t)
    for h, hs in hyph.items():
        parts = h.split('-')
        if any(len(p) < 2 for p in parts[1:]) or (len(parts[0]) < 2 and parts[0] not in ('b', 'c', 't', 'x', 'e')):
            continue
        closed = ''.join(parts)
        opens = []
        for sid, ts in by_sent.items():
            for k in range(len(ts) - len(parts) + 1):
                if all(ts[k + q]['lw'] == parts[q] for q in range(len(parts))) and all(
                        ts[k + q]['next'] == parts[q + 1] for q in range(len(parts) - 1)):
                    nx = ts[k + len(parts) - 1]
                    opens.append(dict(t=ts[k], next=nx['next'], punct_after=nx['punct_after'],
                                      form=' '.join(ts[k + q]['w'] for q in range(len(parts)))))
        cl = words.get(closed, [])
        variants = []
        if cl and len(closed) >= 5:
            variants.append(('closed', cl[0]['w'], cl))
        pdf_closed = doc.pdf_like and bool(cl)
        if opens and parts[-1] not in PARTICLES and parts[0] not in FW:
            def attributive(nxt, punct):
                return bool(nxt) and not punct and nounish(nxt)
            h_attr = any(attributive(t['next'], t['punct_after']) for t in hs)
            o_attr = any(attributive(o['next'], o['punct_after']) for o in opens)
            noun_pos = [t for t in hs if t['punct_after'] or (t['next'] in FW and t['next'] not in ('and', 'or', 'nor', 'to'))]
            if (h_attr and o_attr) or noun_pos:
                variants.append(('open', opens[0]['form'], [o['t'] for o in opens]))
        if pdf_closed and any(k == 'open' for k, _, _ in variants):
            variants = [v for v in variants if v[0] != 'closed']     # the closed form may be an extraction artifact
        if not variants:
            continue
        forms = [(hs[0]['w'], hs)] + [(name, ts) for _, name, ts in variants]
        forms.sort(key=lambda f: -len(f[1]))
        major = forms[0]
        minors = forms[1:]
        desc = '; '.join('*%s* %d×' % (name, len(ts)) for name, ts in forms)
        first_minor = min((t for _, ts in minors for t in ts), key=lambda t: (t['s'].line, t['s'].i))
        lines = sorted({t['s'].line for _, ts in minors for t in ts})
        keep = ('Keep *%s*' % major[0]) if len(major[1]) > len(minors[0][1]) else 'Pick one'
        closed_only = all(kind == 'closed' for kind, _, _ in variants)
        f = flag(8, first_minor['s'], 'One term, %d spellings: %s. %s (minority on lines %s).'
                 % (len(forms), desc, keep, ', '.join(map(str, lines[:6])) + (' …' if len(lines) > 6 else '')),
                 sub='hyphen')
        if closed_only and doc.pdf_like:
            f['msg'] += ' The closed form may be a hyphen lost in PDF extraction.'
            f['info'] = True
            notes.append(f)
        else:
            flags.append(f)
    # closed vs open, without a hyphenated form (data set / dataset)
    seen = set(h.replace('-', '') for h in hyph)
    for sid, ts in by_sent.items():
        for k in range(len(ts) - 1):
            a, b = ts[k], ts[k + 1]
            if a['next'] != b['lw']:
                continue
            w1, w2 = a['lw'], b['lw']
            closed = w1 + w2
            if (closed in seen or len(w1) < 3 or len(w2) < 3 or w1 in FW or w2 in FW or w2 in PARTICLES
                    or closed not in words or w1 in ('out', 'over', 'under', 'every', 'any', 'some', 'no', 'can')):
                continue
            seen.add(closed)
            opens = [(x, y) for q in by_sent.values() for x, y in zip(q, q[1:])
                     if x['lw'] == w1 and y['lw'] == w2 and x['next'] == w2]
            cl = words[closed]
            forms = sorted([('%s %s' % (a['w'], b['w']), [o[0] for o in opens]), (cl[0]['w'], cl)],
                           key=lambda f: -len(f[1]))
            minor = forms[1]
            lines = sorted({t['s'].line for t in minor[1]})
            keep = ('Keep *%s*' % forms[0][0]) if len(forms[0][1]) > len(minor[1]) else 'Pick one'
            f = flag(8, minor[1][0]['s'], 'One term, 2 spellings: %s. %s (minority on lines %s).'
                     % ('; '.join('*%s* %d×' % (n, len(t)) for n, t in forms), keep,
                        ', '.join(map(str, lines[:6]))), sub='closed')
            if doc.pdf_like:
                f['msg'] += ' The closed form may be a hyphen lost in PDF extraction.'
                f['info'] = True
                notes.append(f)
            else:
                flags.append(f)
    # (b) capitalization
    def shape(w):
        if w.isupper():
            return 'upper'
        if w[0].isupper() and w[1:].islower():
            return 'title'
        if w.islower():
            return 'lower'
        return 'mixed'
    caps = defaultdict(lambda: defaultdict(list))
    for sid, ts in by_sent.items():
        for k, t in enumerate(ts):
            if t['initial'] or len(t['w']) < 4 or '-' in t['w']:
                continue
            sh = shape(t['w'])
            if sh == 'mixed':
                continue
            if sh == 'title':
                prev_cap = k > 0 and not ts[k - 1]['initial'] and ts[k - 1]['w'][0].isupper()
                next_cap = k + 1 < len(ts) and ts[k + 1]['w'][0].isupper() and t['next'] == ts[k + 1]['lw']
                after = t['s'].plain[t['s'].plain.find(t['w']):][len(t['w']):len(t['w']) + 4]
                if prev_cap or next_cap or re.match(r'\s*(?:\d|[IVX]+\b|[A-H]\b|N\b|x\b|\()', after):
                    continue
            if sh == 'upper' and (len(t['w']) <= 4 or t['w'] in KNOWN_ACR):
                continue
            caps[t['lw']][sh].append(t)
    for lw, shapes in caps.items():
        if len(shapes) < 2 or lw in ('figure', 'table', 'section', 'appendix', 'equation'):
            continue
        n_low = len(shapes.get('lower', []))
        n_cap = len(shapes.get('title', [])) + len(shapes.get('upper', []))
        if 'lower' in shapes and n_cap <= n_low:
            continue        # a usually-lower-case word: the capitals are sentence starts or titles
        forms = sorted(shapes.items(), key=lambda kv: -len(kv[1]))
        minor = [t for _, ts in forms[1:] for t in ts]
        lines = sorted({t['s'].line for t in minor})
        desc = '; '.join('*%s* %d×' % (ts[0]['w'], len(ts)) for _, ts in forms)
        flags.append(flag(8, minor[0]['s'], 'Capitalization varies mid-sentence: %s (minority on lines %s).'
                          % (desc, ', '.join(map(str, lines[:6]))), sub='case'))
    # multi-word Title Case phrases against lower case
    phrases = defaultdict(list)
    for sid, ts in by_sent.items():
        k = 0
        while k < len(ts):
            if not ts[k]['initial'] and ts[k]['w'][0].isupper() and ts[k]['w'][1:].islower() and len(ts[k]['w']) >= 3:
                e = k
                while (e + 1 < len(ts) and ts[e]['next'] == ts[e + 1]['lw'] and ts[e + 1]['w'][0].isupper()
                       and ts[e + 1]['w'][1:].islower() and len(ts[e + 1]['w']) >= 3):
                    e += 1
                if e > k:
                    phrases[' '.join(x['lw'] for x in ts[k:e + 1])].append(ts[k])
                k = e + 1
            else:
                k += 1
    for ph, occ in phrases.items():
        ws = ph.split()
        low = []
        for sid, ts in by_sent.items():
            for k in range(len(ts) - len(ws) + 1):
                if all(ts[k + q]['w'] == ws[q] for q in range(len(ws))) and not ts[k]['initial'] and all(
                        ts[k + q]['next'] == ws[q + 1] for q in range(len(ws) - 1)):
                    low.append(ts[k])
        if low:
            forms = sorted([(' '.join(w.capitalize() for w in ws), occ), (ph, low)], key=lambda f: -len(f[1]))
            lines = sorted({t['s'].line for t in forms[1][1]})
            flags.append(flag(8, forms[1][1][0]['s'], 'Capitalization varies: %s (minority on lines %s).'
                              % ('; '.join('*%s* %d×' % (n, len(t)) for n, t in forms), ', '.join(map(str, lines[:6]))),
                              sub='case'))
    # (c) US/UK spelling, and parametrization/parameterization
    fam_hits = defaultdict(lambda: {'US': [], 'UK': []})
    for s in doc.sents:
        for fam, rx, side in SPELL_FAMILIES:
            for m in rx.finditer(s.plain):
                fam_hits[fam][side(m)].append((m.group(0), s))
    us = sum(len(v['US']) for f, v in fam_hits.items() if f != '-ize/-ise')
    uk = sum(len(v['UK']) for v in fam_hits.values())
    dialect = 'US' if us >= uk else 'UK'
    other = 'UK' if dialect == 'US' else 'US'
    if us + uk:
        for fam, v in fam_hits.items():
            minority = v[other]
            if dialect == 'UK' and fam == '-ize/-ise':
                if v['US'] and v['UK']:
                    minority = v['US'] if len(v['US']) < len(v['UK']) else v['UK']
                else:
                    continue
            majority_total = sum(len(x[dialect]) for x in fam_hits.values())
            if not minority or (not v[dialect] and majority_total == 0):
                continue
            words_m = Counter(w.lower() for w, _ in minority)
            lines = sorted({s.line for _, s in minority})
            examples = ', '.join(sorted({w.lower() for w, _ in v[dialect]})[:3]) or ', '.join(
                sorted({w.lower() for f2, x in fam_hits.items() for w, _ in x[dialect]})[:3])
            flags.append(flag(8, minority[0][1], '%s spelling %s in a text that otherwise uses %s spelling (%s). '
                                                 'Pick one (lines %s).'
                              % ('British' if other == 'UK' else 'American',
                                 ', '.join('*%s* %d×' % (w, c) for w, c in words_m.most_common(4)),
                                 'American' if dialect == 'US' else 'British', examples,
                                 ', '.join(map(str, lines[:6]))), sub='spelling'))
    pv = defaultdict(list)
    for s in doc.sents:
        for m in PARAM_RE.finditer(s.plain):
            pv['parameter-' if m.group(1) else 'parametr-'].append((m.group(0), s))
    if len(pv) == 2:
        forms = sorted(pv.items(), key=lambda kv: -len(kv[1]))
        minor = forms[1][1]
        flags.append(flag(8, minor[0][1], 'Both *%s* (%d×) and *%s* (%d×). Pick one (lines %s).'
                          % (forms[0][1][0][0], len(forms[0][1]), minor[0][0], len(minor),
                             ', '.join(str(s.line) for _, s in minor[:6])), sub='spelling'))
    flags.sort(key=lambda f: f['line'])
    return dict(flags=flags, info=notes)


# =============================================================================================
# Check 9: figure and table references
# =============================================================================================
FIGWORD_RE = re.compile(r'\b(Figs?\.?|Figures?|FIGS?\.)\s*(?=\d|N\b)')
TABWORD_RE = re.compile(r'\b(Tabs?\.?|Tables?|TABLES?)\s*(?=\d|[IVX]+\b|N\b)')
APPWORD_RE = re.compile(r'\b(Apps?\.|Appendix|Appendices)\s*(?=[A-H]\b)')
NUMLIST_TOK = re.compile(r'\s*(?:(\d+)|([IVX]+|[A-H])\b|(,|and\b|&|–|-|—|to\b|or\b)|\(([a-z])\)|([a-z])\b)')
EXTERNAL_RE = re.compile(r'^\s*(?:of|in|from)\s+(?:Ref|Refs|\[|the\s+(?:ATLAS|CMS|LHCb|original)|ATLAS|CMS|'
                         r'LHCb|their|that|this paper|the paper|the original|previous)', re.I)
FORM_FIG = r'(?:Figs?\.?|Figures?)\s*(?:N|\d+)[a-z]?(?:\s*\([a-z]\))?'


def parse_numlist(s, pos, letters=False, roman=False):
    nums, i, last, rng = [], pos, None, False
    while True:
        m = NUMLIST_TOK.match(s, i)
        if not m:
            break
        if m.group(1) or (m.group(2) and (letters or roman)):
            if m.group(1):
                v = int(m.group(1))
            elif letters and re.fullmatch(r'[A-H]', m.group(2)):
                v = ord(m.group(2)) - 64
            elif roman and re.fullmatch(r'[IVX]+', m.group(2)):
                v = roman_or_int(m.group(2))
            else:
                break
            if rng and last is not None and v > last:
                nums.extend(range(last + 1, v + 1))
            else:
                nums.append(v)
            last, rng = v, False
        elif m.group(3):
            if not nums:
                break
            rng = m.group(3) in ('–', '-', '—', 'to')
        elif m.group(4) or m.group(5):
            if not nums or letters:
                break
        i = m.end()
    return nums, i


def text_refs(sents):
    '''References written out in text: Fig. 3, Figs. 2 and 4, Table II, App. B.'''
    refs = []
    for s in sents:
        p = s.plain
        for rx, kind in ((FIGWORD_RE, 'fig'), (TABWORD_RE, 'tab'), (APPWORD_RE, 'app')):
            for m in rx.finditer(p):
                nums, end = parse_numlist(p, m.end(), letters=(kind == 'app'), roman=(kind == 'tab'))
                if not nums or EXTERNAL_RE.match(p[end:end + 40]):
                    continue
                if re.search(r'(?:\bof|\bin)\s+(?:Ref\.?|Refs\.?)\s*$', p[max(0, m.start() - 12):m.start()]):
                    continue
                for v in nums:
                    refs.append(dict(kind=kind, num=v, line=s.line, seq=s.i, ctx=s.kind, sent=s))
    return refs


def fig_form(plain):
    p = plain.strip()
    if re.match(r'^(?:The\s+)?(?:(?:left|right|top|bottom|upper|lower|middle|center)\s+(?:left\s+|right\s+)?panels?\s+of\s+)?'
                + FORM_FIG + r'\s+(?:shows?|compares?|displays?|presents?|illustrates?|plots?|gives?|summari[sz]es?|'
                r'depicts?|demonstrates?|contains?|reports?|lists?)\b', p, re.I):
        return 'subject'
    if re.match(r'^In\s+(?:the\s+[\w-]+\s+(?:[\w-]+\s+)?panels?\s+of\s+)?' + FORM_FIG + r'[^,]{0,40},\s*we\b', p):
        return 'in_we'
    if re.search(r'(?:[;,(]\s*|^)see\s+(?:also\s+)?(?:the\s+[\w\s-]{0,40}?)?' + FORM_FIG, p, re.I):
        return 'see'
    if re.search(r'\bas\s+(?:can\s+be\s+|is\s+)?(?:seen|shown|illustrated|visible|displayed)\s+in\s+'
                 r'(?:the\s+[\w\s-]{0,30}?of\s+)?' + FORM_FIG, p, re.I):
        return 'as_seen'
    if re.search(r'\b(?:is|are|was|were|be|been)\s+(?:\w+ly\s+)?(?:shown|plotted|presented|displayed|given|'
                 r'illustrated|compared|summari[sz]ed|depicted|drawn|listed|reported|collected|provided|found)\s+'
                 r'(?:in|on)\s+(?:the\s+[\w\s-]{0,40}?of\s+)?' + FORM_FIG, p, re.I):
        return 'passive'
    if re.search(r'\(\s*' + FORM_FIG + r'\s*\)', p):
        return 'paren'
    return 'other'


EMPTY_HANDOFF_RE = re.compile(r'^(?:' + FORM_FIG + r')\s+(?:shows|presents|displays|depicts|illustrates|gives|'
                              r'contains|summari[sz]es)\s+(?:the\s+|our\s+)?(?:main\s+|final\s+|obtained\s+)?'
                              r'(?:results?|distributions?|plots?|comparisons?|performance|outcomes?|histograms?|'
                              r'output|numbers)\s*\.?$', re.I)


def check_figures(doc, opts):
    flags, info = [], []
    conv = doc.conv
    body = [s for s in doc.sents if s.kind != 'caption']
    kname = {'fig': 'Fig.', 'tab': 'Table', 'app': 'Appendix'}

    def numstr(kind, n):
        if kind == 'app':
            return 'Appendix %s' % chr(64 + n)
        if kind == 'tab' and doc.roman_tables:
            return 'Table %s' % int_to_roman(n)
        return '%s %d' % (kname[kind], n)
    # all references as (kind, num, line, seq, ctx)
    refs = []
    lab = {l['key']: l for l in conv.labels}
    for r in conv.refs:
        for key in r['keys']:
            l = lab.get(key)
            if l is None:
                if r['cmd'] != 'pageref':
                    flags.append(flag(9, None, '\\%s{%s} has no matching \\label, so it prints ?? .'
                                      % (r['cmd'], key) if r['cmd'] != 'crossref' else '@%s has no matching label.' % key,
                                      line=r['line'], part='', text=''))
                continue
            if l['kind'] in ('fig', 'tab', 'app') and l['num']:
                refs.append(dict(kind=l['kind'], num=l['num'], line=r['line'], seq=r['seq'],
                                 ctx='caption' if r['ctx'] == 'fcaption' else r['ctx'], key=key))
    if doc.fmt != 'tex' or not conv.refs:
        for r in text_refs(doc.sents):
            refs.append(r)
    for line, msg in conv.bugs:
        flags.append(flag(9, None, msg, line=line, part='', text=''))
    floats = conv.floats
    defined = defaultdict(dict)
    for f in floats:
        for n in f['nums']:
            defined[f['kind']][n] = f
    if doc.fmt == 'tex':
        used_keys = {k for r in conv.refs for k in r['keys']}
        any_labels = any(f['keys'] for f in floats)
        for f in floats:
            for n in f['nums']:
                if not f['keys']:
                    if any_labels:
                        flags.append(flag(9, None, '%s (line %d) has no \\label, so the text cannot refer to it.'
                                          % (numstr(f['kind'], n), f['line']), line=f['line'], part='', text=''))
                    continue
                if not any(k in used_keys for k in f['keys']) and not any(
                        r['kind'] == f['kind'] and r['num'] == n for r in refs):
                    flags.append(flag(9, None, '%s (\\label{%s}, line %d) is never referenced in the text.'
                                      % (numstr(f['kind'], n), f['keys'][0], f['line']), line=f['line'], part='', text=''))
        for l in conv.labels:
            if l['kind'] == 'app' and l['key'] not in used_keys:
                flags.append(flag(9, None, 'Appendix label \\label{%s} (line %d) is never referenced; cite each appendix '
                                           'where the main text needs it.' % (l['key'], l['line']),
                                  line=l['line'], part='', text=''))
        n_eq = [l for l in conv.labels if l['kind'] == 'eq']
        n_eq_un = [l for l in n_eq if l['key'] not in used_keys]
        if n_eq_un:
            info.append(flag(9, None, '%d of %d equation labels are never referenced (%s). Fine if intended; '
                                      'otherwise drop the number.' % (len(n_eq_un), len(n_eq),
                                                                       ', '.join(l['key'] for l in n_eq_un[:5])),
                             line=n_eq_un[0]['line'], part='', text='', info=True))
    else:
        rawrefs = getattr(doc, 'rawrefs', set())
        for kind in ('fig', 'tab'):
            un = [(n, f) for n, f in sorted(defined[kind].items())
                  if not any(r['kind'] == kind and r['num'] == n for r in refs) and (kind, n) not in rawrefs]
            runs = []
            for n, f in un:
                if runs and n == runs[-1][-1][0] + 1:
                    runs[-1].append((n, f))
                else:
                    runs.append([(n, f)])
            for run in runs:
                if len(run) == 1:
                    n, f = run[0]
                    msg = '%s (caption on line %d) is never referenced in the text.' % (numstr(kind, n), f['line'])
                else:
                    msg = '%s %d-%d (captions on lines %d-%d) are never referenced in the text.' % (
                        'Figs.' if kind == 'fig' else 'Tables', run[0][0], run[-1][0], run[0][1]['line'],
                        run[-1][1]['line'])
                flags.append(flag(9, None, msg, line=run[0][1]['line'], part='', text=''))
        heads = getattr(doc, 'heads', []) or []
        apps = []
        for line, title in heads:
            m = re.match(r'^(?:Appendix|APPENDIX)\s+([A-H])\b', title)
            if m:
                apps.append((ord(m.group(1)) - 64, line, title))
        orphans = [(n, line, title) for n, line, title in apps
                   if not any(r['kind'] == 'app' and r['num'] == n for r in refs) and ('app', n) not in rawrefs]
        if orphans:
            names = ', '.join('%s (line %d)' % (numstr('app', n), line) for n, line, _ in orphans)
            flags.append(flag(9, None, '%s %s never cited in the text; cite each appendix where the main text needs '
                                       'it, with its verdict (corpus: CHARM App. E and TRACK App. C-E are the slips).'
                              % (names, 'is' if len(orphans) == 1 else 'are'), line=orphans[0][1], part='', text=''))
        for kind in ('fig', 'tab'):
            if defined[kind]:
                for r in refs:
                    if r['kind'] == kind and r['num'] not in defined[kind] and r['ctx'] != 'caption':
                        flags.append(flag(9, r['sent'], '%s is referenced but no caption defines it.'
                                          % numstr(kind, r['num'])))
                        defined[kind][r['num']] = None
    # order of first citation in the body
    for kind in ('fig', 'tab'):
        first = {}
        for r in sorted((r for r in refs if r['kind'] == kind and r['ctx'] not in ('caption',)),
                        key=lambda r: (r['line'], r['seq'])):
            first.setdefault(r['num'], r)
        order = sorted(first.items(), key=lambda kv: (kv[1]['line'], kv[1]['seq']))
        for idx, (n, r) in enumerate(order):
            later_lower = [(m, rr) for m, rr in order[idx + 1:] if m < n]
            if later_lower:
                m, rr = min(later_lower)
                flags.append(flag(9, r.get('sent'), '%s is first cited here, before %s (first cited on line %d). '
                                                    'Number %s in the order the text first cites them.'
                                  % (numstr(kind, n), numstr(kind, m), rr['line'],
                                     'figures' if kind == 'fig' else 'tables'),
                                  line=r['line'], part=r['sent'].part if r.get('sent') else '',
                                  text=r['sent'].excerpt() if r.get('sent') else ''))
    # empty hand-offs, forms, Fig./Figure usage
    forms = Counter()
    usage = Counter()
    for s in body:
        p = s.plain
        if re.search(FORM_FIG, p):
            forms[fig_form(p)] += 1
        for m in re.finditer(r'\b(Figures?|Figs?\.?)(?=\s*(?:N\b|\d))', p):
            form = 'Figure' if m.group(1).startswith('Figure') else ('Fig.' if m.group(1).endswith('.') else 'Fig')
            pos = 'start' if not p[:m.start()].strip(' \x22“(') else 'mid'
            usage[pos + ':' + form] += 1
        if EMPTY_HANDOFF_RE.match(p.strip()):
            flags.append(flag(9, s, 'This hand-off names the figure but not what to see. Say what the figure shows '
                                    'about the result (corpus rule: quantity first, then the panel, then the reading).'))
    flags.sort(key=lambda f: f['line'])
    return dict(flags=flags, info=info, forms=forms, usage=usage)


def int_to_roman(n):
    vals = [(10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    out = ''
    for v, r in vals:
        while n >= v:
            out += r
            n -= v
    return out


# =============================================================================================
# Check 10: passive voice
# =============================================================================================
BE = {'is', 'are', 'was', 'were', 'be', 'been', 'being'}
PASS_ADV = {'not', 'also', 'then', 'only', 'still', 'often', 'further', 'thus', 'therefore', 'well', 'now',
            'already', 'always', 'never', 'first', 'again', 'here', 'instead', 'all', 'both', 'each',
            'subsequently', 'thereby', 'usually', 'typically', 'generally', 'currently'}
PARTICIPLE_IRREG = set('''shown given known done made seen taken found chosen driven drawn written set put built
held left kept brought thought sought bound broken spent sent lost met paid said told understood undertaken
overcome begun grown thrown proven hidden laid led fed split spread struck worn born borne frozen
forgotten fallen risen withheld upheld dealt meant won cut run read'''.split())
IT_PASSIVE_RE = re.compile(r'\bit (?:is|was|has been|had been|can be|could be|will be|may be) (?:found|shown|'
                           r'observed|seen|demonstrated|concluded|determined|verified|confirmed|expected|believed|'
                           r'assumed|argued|known|estimated|suggested|proposed) that\b', re.I)


def passive_count(low):
    n = 0
    for k, t in enumerate(low):
        if t not in BE:
            continue
        j, skipped = k + 1, 0
        while j < len(low) and skipped < 2 and (low[j] in PASS_ADV or (low[j].endswith('ly') and len(low[j]) > 3)):
            j += 1
            skipped += 1
        if j < len(low):
            w = low[j]
            if (w.endswith('ed') and len(w) >= 4 and w not in NOT_PART and WORD_RE.match(w)) or w in PARTICIPLE_IRREG:
                n += 1
    return n


def check_passive(doc, opts):
    flags = []
    rows = []
    groups = [('abstract', lambda s: s.part == 'abstract'), ('intro', lambda s: s.part == 'intro'),
              ('body', lambda s: s.part == 'body'), ('concl', lambda s: s.part == 'concl'),
              ('app', lambda s: s.part == 'app'), ('prose', lambda s: s.kind == 'prose'),
              ('caption', lambda s: s.kind == 'caption')]
    for name, pred in groups:
        ss = [s for s in doc.sents if pred(s)]
        if not ss:
            continue
        p = [s for s in ss if passive_count(s.low)]
        rows.append(dict(part=name, n=len(ss), passive=len(p), pct=round(100 * len(p) / len(ss), 1)))
        if name == 'abstract' and len(ss) >= 3 and len(p) / len(ss) > 0.30:
            flags.append(flag(10, p[0], 'The abstract has a passive in %d of %d sentences (%.0f%%; corpus 18%%, flag above '
                                        '30%%). Give the choices and results to *we*: *We find ...*, *We show ...*.'
                              % (len(p), len(ss), 100 * len(p) / len(ss)),
                              text='; '.join('L%d: %s' % (s.line, shorten(s.show, 70)) for s in p[:3])))
    for s in doc.sents:
        for m in IT_PASSIVE_RE.finditer(s.plain):
            flags.append(flag(10, s, '*%s*: state it with *we* (*We find that ...*) or state the fact directly.'
                              % m.group(0)))
    prose_words = sum(s.words for s in doc.sents if s.kind == 'prose') or 1
    we = sum(1 for s in doc.sents if s.kind == 'prose' for w in s.low if w in ('we', 'our', 'us', 'ours'))
    return dict(flags=flags, rows=rows, we_per_1k=round(1000 * we / prose_words, 1))


# =============================================================================================
# Driver and report
# =============================================================================================
class Doc:
    pass


def sniff(text):
    if re.search(r'\\(?:documentclass|begin\s*\{document\}|section\*?\s*\{|subsection\*?\s*\{|cite[pt]?\s*\{|'
                 r'begin\s*\{(?:equation|figure|abstract|align))', text):
        return 'tex'
    if (re.search(r'^#{1,6}\s+\S', text, re.M) or re.search(r'!\[[^\]]*\]\(', text)
            or re.search(r'^\s*\*\*[^*]+\*\*', text, re.M) or re.search(r'\[@\w', text)):
        return 'md'
    return 'txt'


def load(path, fmt):
    if path == '-':
        data = sys.stdin.buffer.read()
        name = 'stdin'
    else:
        with open(path, 'rb') as f:
            data = f.read()
        name = os.path.basename(path)
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        text = data.decode('latin-1')
    text = text.lstrip('\ufeff')
    if fmt == 'auto':
        ext = os.path.splitext(path)[1].lower() if path != '-' else ''
        fmt = {'.tex': 'tex', '.ltx': 'tex', '.latex': 'tex', '.md': 'md', '.markdown': 'md', '.rmd': 'md',
               '.qmd': 'md', '.txt': 'txt', '.text': 'txt'}.get(ext) or sniff(text)
    return name, fmt, text


def analyse(text, fmt, name='draft'):
    store = Store()
    if fmt == 'tex':
        res = parse_tex(text, store)
    elif fmt == 'md':
        res = parse_md(text, store)
    else:
        res = parse_txt(text, store)
    doc = Doc()
    doc.name, doc.fmt, doc.store = name, fmt, store
    doc.conv = res['conv']
    doc.includes = res.get('includes', [])
    doc.heads = res.get('heads', [])
    doc.sents = make_sentences(res['blocks'], store, res.get('vocab'))
    doc.words = sum(s.words for s in doc.sents)
    doc.roman_tables = bool(re.search(r'\b(?:TABLE|Table|Tab\.?)\s+[IVX]+\b', text))
    doc.rawrefs = res.get('rawrefs', set())
    doc.pdf_like = fmt == 'txt' and looks_extracted(text)
    if fmt != 'tex' and fmt != 'md':
        doc.conv.floats = res.get('text_floats', [])
    return doc


def run_checks(doc, opts):
    res = {}
    want = opts.only
    if 1 in want:
        res[1] = check_long(doc, opts)
    if 2 in want:
        res[2] = check_verb(doc, opts)
    if 3 in want:
        res[3] = check_connectors(doc, opts)
    if 4 in want:
        res[4] = check_vocab(doc, opts)
    vague = check_vague(doc, opts)
    if 6 in want:
        res[6] = vague
    if 5 in want:
        res[5] = check_hype(doc, opts, vague['vague'] if 6 in want else set())
    if 7 in want:
        res[7] = check_acronyms(doc, opts)
    if 8 in want:
        res[8] = check_terms(doc, opts)
    if 9 in want:
        res[9] = check_figures(doc, opts)
    if 10 in want:
        res[10] = check_passive(doc, opts)
    return res


def fmt_num(x):
    if isinstance(x, float):
        return ('%.1f' % x).rstrip('0').rstrip('.') if x != int(x) else str(int(x))
    return str(x)


def report_md(doc, res, opts):
    L = []
    nflags = sum(len(r['flags']) for r in res.values())
    W = doc.words or 1
    n_prose = sum(1 for s in doc.sents if s.kind == 'prose')
    n_cap = sum(1 for s in doc.sents if s.kind == 'caption')
    n_fn = sum(1 for s in doc.sents if s.kind == 'footnote')
    fmt_name = {'tex': 'LaTeX', 'md': 'Markdown', 'txt': 'plain text'}[doc.fmt]
    L.append('# Style check: %s' % doc.name)
    L.append('')
    L.append('%s words in %d sentences (%d prose, %d caption%s) · %s input'
             % ('{:,}'.format(doc.words), len(doc.sents), n_prose, n_cap,
                (', %d footnote' % n_fn) if n_fn else '', fmt_name))
    L.append('')
    if not doc.sents:
        L.append('No sentences found. Check the input format (--format tex|md|txt).')
        return '\n'.join(L) + '\n'
    rate = 1000.0 * nflags / W
    full = len(opts.only) == len(CHECKS)
    if full:
        L.append('**%d flags, %.1f per 1,000 words.** The five reference papers, run through the same checks as plain '
                 'text, give about %.1f per 1,000 words. A flag asks you to reread a sentence; it is not always an '
                 'error, and the reference papers break most rules now and then.' % (nflags, rate, CORPUS_RATE_TOTAL))
    else:
        L.append('**%d flags, %.1f per 1,000 words** (checks %s only).'
                 % (nflags, rate, ', '.join(str(k) for k in sorted(opts.only))))
    L.append('')
    if doc.includes:
        L.append('Note: this file pulls in other files (%s). The checker does not follow \\input or \\include; '
                 'run it on those files too.' % ', '.join(doc.includes[:6]))
        L.append('')
    L.append('| check | flags | per 1,000 words | reference papers |')
    L.append('|---|---|---|---|')
    for k, key, name in CHECKS:
        if k not in res:
            continue
        nf = len(res[k]['flags'])
        L.append('| %d. %s | %d | %.1f | %.1f |' % (k, name, nf, 1000.0 * nf / W, CORPUS_RATE.get(k, 0)))
    L.append('')
    # ---- 1
    if 1 in res:
        r = res[1]
        L.append('## 1. Long sentences (> %d words)' % opts.max_words)
        L.append('')
        L.append('Corpus: a median of 23 words per prose sentence, with about 1 sentence in 10 above 40 words; '
                 'caption sentences have a median of 18. A long sentence is fine when it has visible structure.')
        L.append('')
        L.append('| part | sentences | median | mean | p90 | % ≤ 12 | % > 30 | % > 40 | corpus median | corpus % > 40 |')
        L.append('|---|---|---|---|---|---|---|---|---|---|')
        for row in r['rows']:
            c = CORPUS_LEN.get(row['part'])
            L.append('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s |'
                     % (PART_LABEL[row['part']], row['n'], fmt_num(row['median']), fmt_num(row['mean']), row['p90'],
                        fmt_num(row['le12']), fmt_num(row['gt30']), fmt_num(row['gt40']),
                        c[1] if c else '', fmt_num(c[6]) if c else ''))
        L.append('')
        add_flags(L, r['flags'])
        add_flags(L, r['info'], heading='Long but structured (not counted as flags; the corpus accepts these)')
    if 2 in res:
        r = res[2]
        L.append('## 2. Late main verb')
        L.append('')
        L.append('Corpus: the first finite verb sits at a median of word 5, and only 14%% of sentences reach it after '
                 'word 10. This draft: median word %s over %d sentences of 15 or more words. Flagged: the main verb '
                 'comes after word %d and follows an opening phrase of %d or more words, or a subject of %d or more. '
                 'The verb finder is a heuristic and skips sentences where it is unsure.'
                 % (fmt_num(r['median']) if r['median'] is not None else 'n/a', r['n'], LATE_VERB, LATE_OPENER,
                    LATE_SUBJECT))
        L.append('')
        add_flags(L, r['flags'])
    if 3 in res:
        r = res[3]
        L.append('## 3. Stock connectors, filler openers, *in order to*')
        L.append('')
        top = ', '.join('%s %d' % (w, c) for w, c in r['openers'].most_common(6)) or 'none'
        L.append('Corpus: *Moreover, Furthermore, Thus* and *Hence* open 5 of 985 prose sentences, and *Also, Besides, '
                 'Notably, Importantly, Interestingly* open none; consequence sits inside the sentence (*so*, a '
                 'mid-sentence *therefore*). *In addition* and *Additionally* (19 openers) and *Therefore* are flagged '
                 'only when they follow another connector. *In order to* appears 3 times in 25,000 words. This draft: '
                 '%.1f stock openers per 1,000 words (%s).' % (r['rate'], top))
        L.append('')
        add_flags(L, r['flags'])
    if 4 in res:
        L.append('## 4. Inflated words and phrases')
        L.append('')
        L.append('Corpus: 462 forms of *use, show, find, estimate, predict, measure, compare, test, study* against 5 of '
                 '*utilize* or *leverage*, and none of *elucidate, delve, facilitate, endeavor*. Filler is rare (1 *the '
                 'fact that* in 25,000 words). Inflated words often come from translation tools or automatic polishing.')
        L.append('')
        add_flags(L, res[4]['flags'])
    if 5 in res:
        L.append('## 5. Hype and intensifiers')
        L.append('')
        L.append('Corpus: 2.1 intensifiers per 1,000 words, mostly comparatives with a baseline; promotional words '
                 'cluster in abstracts. Words such as *very* and *significantly* are skipped when the sentence gives '
                 'a number, and *significant* when it has a statistical meaning.')
        L.append('')
        add_flags(L, res[5]['flags'])
    if 6 in res:
        L.append('## 6. Vague result claims')
        L.append('')
        L.append('Corpus: a result is a number with a unit, a baseline and a condition (13 *factor of N*, 34 *N% CL*). '
                 'A claim passes when it, or its neighbour in the same paragraph, has a number or a named baseline. '
                 'Purpose clauses (*to improve*), modals and negations are skipped.')
        L.append('')
        add_flags(L, res[6]['flags'])
    if 7 in res:
        r = res[7]
        L.append('## 7. Acronyms')
        L.append('')
        L.append('Corpus: no acronym is used before its definition, and the abstract and the main text each define '
                 'their own. Standard HEP acronyms (LHC, ATLAS, SM, QCD, CL, GeV, ...) are skipped unless you '
                 'define them; add your own with --known.')
        L.append('')
        add_flags(L, r['flags'])
        add_flags(L, r['info'], heading='Notes (not counted as flags)')
    if 8 in res:
        L.append('## 8. Terminology variants')
        L.append('')
        L.append('Corpus: the term a paper is about never varies (*HNL* 167 to 2); drift appears in secondary terms '
                 'and spelling (*flavor* 63, *flavour* 2). A hyphen before a noun (*low-mass resonance*) next to an '
                 'open noun phrase (*at low mass*) is grammar, not a variant, and is not flagged.')
        L.append('')
        add_flags(L, res[8]['flags'])
        add_flags(L, res[8]['info'], heading='Notes (not counted as flags)')
    if 9 in res:
        r = res[9]
        L.append('## 9. Figure and table references')
        L.append('')
        L.append('Corpus: figures are cited in the text about 3.7 times per 1,000 words, usually as *X is shown in '
                 'Fig. N* or *claim; see Fig. N*; the slips were out-of-order first citations and uncited figures '
                 'or appendices.')
        L.append('')
        add_flags(L, r['flags'])
        total = sum(r['forms'].values())
        if total:
            L.append('How this draft hands off to figures (report only):')
            L.append('')
            L.append('| form | this draft | corpus (64 references) |')
            L.append('|---|---|---|')
            for key, desc, n in CORPUS_FIG_FORMS:
                L.append('| %s | %d (%.0f%%) | %d (%.0f%%) |' % (desc, r['forms'].get(key, 0),
                                                                100.0 * r['forms'].get(key, 0) / total, n, 100.0 * n / 64))
            L.append('')
        if r['usage']:
            mid = {k.split(':')[1]: v for k, v in r['usage'].items() if k.startswith('mid')}
            start = {k.split(':')[1]: v for k, v in r['usage'].items() if k.startswith('start')}
            L.append('Abbreviation: mid-sentence %s; sentence-initial %s. APS style, which CHARM and TRACK follow, writes '
                     '*Fig.* inside a sentence and *Figure* at its start.'
                     % (', '.join('%s %d' % kv for kv in sorted(mid.items())) or 'none',
                        ', '.join('%s %d' % kv for kv in sorted(start.items())) or 'none'))
            L.append('')
        add_flags(L, r['info'], heading='Notes (not counted as flags)')
    if 10 in res:
        r = res[10]
        L.append('## 10. Passive voice (report only)')
        L.append('')
        L.append('Corpus: a passive in 40% of body sentences and 18% of abstract sentences; *we* with an active verb '
                 'for choices and results (13.6 *we/our/us* per 1,000 words). Only an abstract above 30% and '
                 '*It is found that ...* are flagged.')
        L.append('')
        L.append('| part | sentences | with a passive | % | corpus % |')
        L.append('|---|---|---|---|---|')
        for row in r['rows']:
            L.append('| %s | %d | %d | %s | %s |' % (PART_LABEL[row['part']], row['n'], row['passive'],
                                                    fmt_num(row['pct']), fmt_num(CORPUS_PASSIVE.get(row['part'], 0))))
        L.append('')
        L.append('*We/our/us* per 1,000 prose words: %s (corpus %s).' % (fmt_num(r['we_per_1k']), CORPUS_WE_PER_1K))
        L.append('')
        add_flags(L, r['flags'])
    return '\n'.join(L).rstrip() + '\n'


def add_flags(L, flags, heading=None):
    if not flags:
        if heading is None:
            L.append('No flags.')
            L.append('')
        return
    if heading:
        L.append('%s:' % heading)
        L.append('')
    for f in flags:
        loc = 'L%d' % f['line'] if f['line'] else '-'
        part = (' · %s' % PART_LABEL.get(f['part'], f['part'])) if f['part'] else ''
        L.append('- **%s**%s · %s' % (loc, part, f['msg']))
        if f.get('text'):
            L.append('  > %s' % f['text'].replace('\n', ' '))
    L.append('')


def report_json(doc, res, opts):
    W = doc.words or 1
    out = dict(file=doc.name, format=doc.fmt, words=doc.words, sentences=len(doc.sents),
               flags_total=sum(len(r['flags']) for r in res.values()),
               flags_per_1000_words=round(1000.0 * sum(len(r['flags']) for r in res.values()) / W, 2),
               reference_flags_per_1000_words=CORPUS_RATE_TOTAL, includes=doc.includes, checks={})
    for k, key, name in CHECKS:
        if k not in res:
            continue
        r = res[k]
        d = dict(name=name, key=key, flags=[{kk: vv for kk, vv in f.items() if kk != 'info'} for f in r['flags']],
                 per_1000_words=round(1000.0 * len(r['flags']) / W, 2), reference_per_1000_words=CORPUS_RATE.get(k))
        if r.get('info'):
            d['notes'] = [{kk: vv for kk, vv in f.items() if kk != 'info'} for f in r['info']]
        if k == 1:
            d['length_distribution'] = r['rows']
            d['corpus'] = {p: dict(zip(['sentences', 'median', 'mean', 'p90', 'le12', 'gt30', 'gt40'], v))
                           for p, v in CORPUS_LEN.items()}
        if k == 2:
            d['median_verb_position'] = r['median']
        if k == 3:
            d['openers'] = dict(r['openers'])
            d['openers_per_1000_words'] = r['rate']
        if k == 9:
            d['reference_forms'] = dict(r['forms'])
            d['abbreviation_usage'] = dict(r['usage'])
        if k == 10:
            d['passive_by_part'] = r['rows']
            d['corpus_passive_pct'] = CORPUS_PASSIVE
            d['we_per_1000_words'] = r['we_per_1k']
        out['checks'][str(k)] = d
    return json.dumps(out, ensure_ascii=False, indent=1)


def parse_only(s):
    if not s:
        return {k for k, _, _ in CHECKS}
    ids = set()
    for part in re.split(r'[,\s]+', s.strip()):
        if not part:
            continue
        if part.isdigit() and 1 <= int(part) <= len(CHECKS):
            ids.add(int(part))
            continue
        hits = [k for k, key, _ in CHECKS if key.startswith(part.lower())]
        if len(hits) != 1:
            raise SystemExit('style_check.py: unknown check %r (use 1-10 or %s)'
                             % (part, ', '.join(key for _, key, _ in CHECKS)))
        ids.add(hits[0])
    return ids


def main(argv=None):
    ap = argparse.ArgumentParser(description='Flag places where a physics-paper draft drifts from the style of '
                                             'five papers from the Whiteson group.')
    ap.add_argument('file', help='a .tex, .md or .txt file, or - for stdin')
    ap.add_argument('--max-words', type=int, default=40, help='long-sentence threshold (default 40)')
    ap.add_argument('--only', default='', help='comma-separated checks, by number or name (long, verb, '
                                               'connectors, vocab, hype, vague, acronyms, terms, figures, passive)')
    ap.add_argument('--json', action='store_true', help='print JSON instead of Markdown')
    ap.add_argument('--format', default='auto', choices=['auto', 'tex', 'md', 'txt'], help='input format')
    ap.add_argument('--known', default='', help='comma-separated acronyms to treat as standard (no definition needed)')
    ap.add_argument('--dump', action='store_true', help='print the sentences the checker extracted, then stop')
    args = ap.parse_args(argv)
    args.only = parse_only(args.only)
    args.known = {k.strip() for k in args.known.split(',') if k.strip()}
    if args.max_words < 5:
        raise SystemExit('style_check.py: --max-words must be at least 5')
    try:
        name, fmt, text = load(args.file, args.format)
    except OSError as e:
        raise SystemExit('style_check.py: cannot read %s: %s' % (args.file, e))
    doc = analyse(text, fmt, name)
    if args.dump:
        for s in doc.sents:
            print('L%-5d %-9s %-8s %3dw  %s' % (s.line, PART_LABEL.get(s.part, s.part)[:9], s.kind[:8], s.words, s.show))
        return 0
    res = run_checks(doc, args)
    out = report_json(doc, res, args) if args.json else report_md(doc, res, args)
    sys.stdout.write(out if out.endswith('\n') else out + '\n')
    return 0


def _main():
    try:
        return main()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        return 0


if __name__ == '__main__':
    sys.exit(_main())
