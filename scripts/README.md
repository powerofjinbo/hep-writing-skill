# style_check.py

`style_check.py` flags places where a draft of an experimental or phenomenological HEP paper drifts from the
writing style of five papers from Daniel Whiteson's group: TOP (arXiv:2311.00121), CHARM (2609.32054),
TIME (2605.11071), HNL (2510.16107) and TRACK (2505.02937). It is one file and uses the Python 3 standard
library only.

A flag asks you to reread a sentence. It is not always an error: the five papers break most of these rules now
and then, and the report gives their rate next to yours. The corpus norms come from the analysis files
`lens-sentences.md` (sentence and word metrics), `lens-layering.md` §4-5 and `connector_counts_output.md`.

## Run it

```
python3 scripts/style_check.py draft.tex                 # Markdown report on stdout
python3 scripts/style_check.py draft.md --max-words 35
python3 scripts/style_check.py - < draft.txt             # stdin; the format is sniffed
python3 scripts/style_check.py draft.tex --only long,verb,acronyms
python3 scripts/style_check.py draft.tex --json > report.json
python3 scripts/style_check.py draft.tex --dump          # the sentences the checker read
```

| option | meaning |
|---|---|
| `--max-words N` | long-sentence threshold (default 40) |
| `--only LIST` | run some checks, by number or name: `1,3` or `long,verb,connectors,vocab,hype,vague,acronyms,terms,figures,passive` |
| `--json` | all flags, notes and statistics as JSON |
| `--format tex\|md\|txt` | override the format taken from the file extension |
| `--known A,B` | acronyms that need no definition in this paper |
| `--dump` | print each extracted sentence with its line, part and word count, then stop |

The report opens with a summary table: flags per check, flags per 1,000 words, and the rate on the five papers.
Then comes one section per check, giving the corpus norm, the flags (line, part of the paper, message, the
sentence cut to about 170 characters) and any notes that are not counted as flags. Line numbers are those of the
input file.

## What it reads

- **LaTeX.** It drops comments, `\iffalse` blocks, the preamble and everything after `\end{document}`. It
  expands `\newcommand` and `\def` macros, including macros with arguments and `\be ... \ee` shortcuts. Inline
  math becomes a placeholder that counts as one word per operand; display math (`equation`, `align`, `\[ \]`,
  `$$`) becomes one word and keeps its closing punctuation. `\cite` counts as zero words. `\ref`, `\eqref`,
  `\cref` and `\autoref` are recorded for check 9, and `\label` is recorded. Formatting commands keep their text,
  `\SI`/`\si` units are written out, and accents, quotes and dashes are converted. Tables, `tikzpicture` and
  verbatim are dropped. Figure and table captions and footnotes are read as separate parts. The abstract,
  introduction, conclusions and appendices are found from the environments and headings; acknowledgments and
  the bibliography are dropped. `\input` and `\include` are not followed; the report says so.
- **Markdown.** It handles headings, lists, emphasis, links, inline code and fenced code, `$...$` math, LaTeX
  commands, pandoc citations `[@key]`, pandoc-crossref `@fig:x` and `{#fig:x}`, images, and caption paragraphs
  that start with *Figure N:* or *Table N:*.
- **Plain text.** Blank lines separate paragraphs. It finds headings (numbered, all capitals, or known names
  such as *Introduction*), captions that start with *FIG. N* or *Figure N:*, and a reference list starting at
  *[1]*. Text before the first heading is read as the abstract. It also reads pdftotext output: figure text is
  dropped, line-end hyphens are repaired, and numbered equations become placeholders. When the text looks
  extracted from a PDF (an arXiv stamp, or many hyphenated line ends), two artifacts are demoted to notes: a
  hyphen lost in extraction (*charmtagging*) and flattened math read as an acronym.

## The checks

**1 `long`: long sentences.**
- *Flags* a sentence above `--max-words` words (default 40) and suggests a split point such as *, which*. A
  sentence of 41-60 words with visible structure (a semicolon, (i)/(ii), *respectively*) is listed as a note,
  not a flag. The report tabulates the draft's length distribution by part next to the corpus.
- *Basis:* the median prose sentence has 23 words, 11% pass 40, and caption sentences have a median of 18
  (lens-sentences §2.1, rules 1 and 4).
- *Limits:* the corpus itself has one sentence in ten above 40 words, so good prose gets some flags too.

**2 `verb`: late main verb.**
- *Flags* a sentence of 15 or more words whose main verb comes after word 12 when one of two things holds: the
  opening phrase or clause runs 15 or more words, or the subject runs 14 or more words.
- *Basis:* the first finite verb sits at a median of word 5, and 14% of sentences pass word 10 (lens-sentences
  §2.6, rule 2). The corpus's own example of the problem is flagged:
  "By measuring the energy and momentum of the HNL decay products at FASER2 using only this fully-visible decay mode, we show that the HNL mass and coupling can be constrained" [HNL §I s17].
- *Limits:* there is no part-of-speech tagger. The verb finder uses a list of about 450 verbs, morphology and
  context, and says *verb* when unsure, so it misses some late verbs rather than inventing them. Captions and
  subordinate clauses with no comma are skipped. Now and then the message names the verb of a relative clause
  instead of the main verb.

**3 `connectors`: stock connectors and filler.**
- *Flags* sentences that open with *Moreover, Furthermore, Thus, Hence, Also, Besides, Notably, Importantly,
  Interestingly*. It flags *In addition, Additionally, Therefore, Consequently* only when they follow another
  connector within three sentences. It also flags *It is worth noting that*, *It should be noted that* and similar
  phrases, and *in order to*.
- *Basis:* *Moreover, Furthermore, Thus* and *Hence* open 5 of 985 prose sentences, and the other words in the
  first list open none. *In addition* and *Additionally* open 19, so only chains of them are flagged. *In order
  to* appears 3 times in 25,000 words (lens-layering §4, rule 18; lens-sentences rule 19).
- *Limits:* it reads only the opening words of a sentence. A connector in mid-sentence is not flagged, and the
  corpus allows those.

**4 `vocab`: inflated words.**
- *Flags* about 45 words and phrases and gives a plain word for each: *utilize, leverage, facilitate, elucidate,
  delve, endeavor, plethora, myriad, paradigm, aforementioned, prior to, due to the fact that, a large number of,
  has the ability to, plays a crucial role in*, and so on.
- *Basis:* there are 462 forms of *use, show, find, estimate, ...* against 5 of *utilize* or *leverage*
  (lens-sentences §3e, rule 6), for example
  "is the first to utilize a far-forward detector as a trigger for ATLAS" [HNL §I s32].
- *Limits:* a fixed list. A word used correctly in a technical sense (*paradigm* in a philosophy-of-science
  remark) is still flagged.

**5 `hype`: hype and intensifiers.**
- *Flags* *novel, remarkable, promising, crucial, unprecedented, groundbreaking, state-of-the-art, excellent,
  powerful* and similar words. It also flags *very, extremely, highly, greatly, dramatically* unless the sentence
  gives a number, and *significant(ly)* unless the sentence gives a number or has a statistical meaning (σ, CL,
  excess, p-value ...). It skips comparatives (*more powerful*), *the very first* and *highly boosted*.
- *Basis:* there are 2.1 intensifiers per 1,000 words, mostly comparatives with a baseline, and promotional words
  cluster in abstracts (lens-sentences §2.5, §3f, rule 14).
- *Limits:* it does not read context. *Very* before a technical adjective (*very forward*) is flagged even when
  harmless. *Significant* is not flagged in a sentence that check 6 already flags.

**6 `vague`: vague result claims.**
- *Flags* *improve, better, enhance, outperform, gain(s), superior, boost* when neither the sentence nor its
  neighbour in the same paragraph has a number or a named baseline. Phrases such as *the improved limits* look
  three sentences back. Labels (*Fig. 3*, *Model 1*), years, collision energy and luminosity do not count as
  numbers. Generic baselines (*existing methods*, *previous searches*) do not count as named.
- *Basis:* a result is a number with a unit, a baseline and a condition (lens-sentences §3b, rules 7-8).
- *Limits:* it skips purpose clauses (*to improve*), negations, hypotheticals (*could, would, may, might*),
  conditionals, claims about cited work (a citation in the sentence), plans (*we estimate the enhancement*) and
  *better understood*. Any nearby number counts, even one that does not measure the claimed gain.

**7 `acronyms`: acronyms.**
- *Flags* an acronym used before its definition. It flags one that is never defined, once per acronym, with its
  count. It flags one defined only in the abstract, and one used in the abstract without a definition there.
  Notes list acronyms defined twice, or defined and never used again.
  A definition is *Long Form (ACR)*, *ACR (Long Form)*, *referred to as ACR*, or *ACR stands for*. A name
  introduced with a citation (*Pythia 8.3 [25]*, *L-BFGS-B [26]*) counts as introduced. Standard HEP acronyms
  (LHC, HL-LHC, ATLAS, CMS, LHCb, SM, BSM, QCD, CL, NLO, PDF, MC, ML, NN, GeV, ...) and common software names need
  no definition; add more with `--known`.
- *Basis:* no acronym is used before its definition in any of the five papers, and the abstract and the body each
  define their own. The corpus's slip, TRACK's undefined *LS*, is flagged (lens-sentences §3c, rule 10).
- *Limits:* other definition forms (*ACR, the long form,*) are missed. All-capital names of 7 or more letters,
  version identifiers (*CTEQ6L1*) and two letters plus digits (*KS0*) are skipped. In PDF text, flattened math can
  still look like an acronym (*Z_A* printed as *ZA*).

**8 `terms`: terminology variants.**
- *Flags* one term written several ways: hyphenated, open and closed (*time-dependence / time dependence*,
  *data set / dataset*, *pile-up / pileup*), and capitalization (*Gaussian / gaussian*, *Standard Model / standard
  model*). It also flags mixed American and British spelling (*flavor / flavour*, *modeling / modelling*,
  *analyze / analyse*, *-ize / -ise*, *center / centre*), and *parametrization / parameterization*. A hyphen before
  a noun (*low-mass resonance*) next to an open noun phrase (*at low mass*) is grammar and is not flagged; the
  check needs the two forms in the same role.
- *Basis:* the term a paper is about never varies, while drift appears in secondary terms and spelling (*flavor*
  63, *flavour* 2; *committee-of-experts* against *mixture of experts*) (lens-sentences §3d, rule 12).
- *Limits:* it cannot see synonyms. TOP's eight names for its heavy quark need a reader. In PDF text, closed forms
  are demoted to notes, because pdftotext drops line-end hyphens.

**9 `figures`: figure and table references.**
- *Flags* five things. A figure or table first cited before a lower-numbered one. A float that is never
  referenced, with runs grouped. A `\ref` with no `\label`. A `\label` placed before `\caption` (it then prints the
  section number). A hand-off such as *Figure 1 shows the results.* that says nothing about what to see. It also
  flags appendices never cited in the text. For a report only, it gives the mix of reference forms (*X is shown
  in Fig. N*, *claim; see Fig. N*, *Figure N shows X*, ...) against the corpus, and the *Fig.*/*Figure* usage.
- *Basis:* the slips found in the corpus are all flagged.
  "Increased coupling to heavy flavor can result in decays predominantly to tg and tγ; see Fig 2." [TOP §Models s14]
  comes before the first citation of Fig. 1.
  TIME cites Fig. 6 before Fig. 5, and TRACK cites Tab. VI before Tab. II and Fig. 12 before Fig. 9. TRACK Table I,
  TRACK Fig. 11 and CHARM App. E are never cited (lens-layering §5).
- *Limits:* in LaTeX, numbering follows the order of the float environments, and written-out *Fig. 3* text is used
  only when the file has no `\ref` at all. A reference to another paper's figure (*Fig. 3 of Ref. [5]*) is skipped
  only when it is phrased that way.

**10 `passive`: passive voice (report only).**
- *Reports* the share of sentences with a passive, by part, next to the corpus, and the *we/our/us* rate.
- *Flags* an abstract with a passive in more than 30% of its sentences (3 or more sentences), and *It is found
  that*, *It was shown that* and similar openings.
- *Basis:* there is a passive in 40% of body sentences and 18% of abstract sentences, and *we* appears 13.6 times
  per 1,000 words (lens-sentences §2.2, rule 5).
- *Limits:* the detector looks for a form of *be* followed by a participle; 24 of 25 hits were true passives in
  the corpus spot check. Passives without *be* are missed.

## Validation

**The five papers, as plain pdftotext output.** There are 235 flags in 28,112 words, 8.4 per 1,000.

| paper | words | flags | per 1,000 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TOP | 2,685 | 12 | 4.5 | 4 | 0 | 1 | 1 | 3 | 0 | 0 | 2 | 1 | 0 |
| CHARM | 5,867 | 44 | 7.5 | 21 | 5 | 1 | 0 | 4 | 1 | 1 | 10 | 1 | 0 |
| TIME | 7,089 | 54 | 7.6 | 20 | 6 | 5 | 4 | 10 | 0 | 1 | 7 | 1 | 0 |
| HNL | 6,988 | 70 | 10.0 | 36 | 11 | 0 | 6 | 12 | 0 | 2 | 3 | 0 | 0 |
| TRACK | 5,483 | 55 | 10.0 | 12 | 4 | 3 | 1 | 17 | 1 | 2 | 9 | 6 | 0 |

Long sentences are 3.3 of the 8.4 flags per 1,000 words; they are sentences above 40 words, which the papers
write at the measured rate. A random sample of 10 corpus flags (seed 20261105) gave 10 true positives by the
rule's definition. Four of them are weak: correct, but a careful editor might keep the sentence. I also reviewed
every flag from checks 2-4 and 6-9 (114 flags) and found 5 false positives and 1 borderline case:
- a sentence merged with figure text by pdftotext (TIME, late verb);
- an abstract clause describing earlier searches (CHARM, vague claim);
- flattened math and flowchart text read as acronyms (TIME *ZA*, HNL *ECOM*);
- the standard ML term *GELU* (borderline).

Most of the 31 terminology flags are real but minor hyphenation choices (*heavy-flavor / heavy flavor*).

**Weak drafts.** `tests/weak_draft.md` (813 words) has 63 planted problems across all ten checks; the checker
finds 63 of 63, with no flag on the three control sentences and no extra flag (77.5 flags per 1,000 words).
`tests/weak_draft2.tex` (392 words, LaTeX) was written afterwards with different wording. Its first run missed
three problems: *the improvement is substantial*, *b-jet / b jet*, and *Monte Carlo / Monte-Carlo*. Fixing them
gave the current rules; it now gives 29 flags (74.0 per 1,000 words). Weak drafts thus get about nine times the
corpus rate.

**LaTeX stripping.** `tests/latex_test.tex` and `tests/latex_hard.tex` cover the preamble, macros, comments,
`\cite`, inline and display math, `align` with `\nonumber`, figure and table floats, subfigures, `\captionof`,
`\cref`, siunitx, `\verb`, a multi-line footnote, lists, accents, acknowledgments and the bibliography. `--dump`
shows every sentence correctly joined and placed in the right part. The flags they get (a `\ref` with no label,
an uncited appendix label, an undefined *HNL*) are all correct.

Run the regression test with
`python3 -I tests/verify_expected.py tests/weak_draft.md tests/expected_weak_draft.tsv 24,51,52`.

## Known limitations

- Every check is a heuristic on words and punctuation. There is no parser, tagger or dictionary, so the checks
  are tuned to flag less when unsure.
- PDF-extracted text carries artifacts: a footnote or figure label merged into a sentence, dropped hyphens, and
  flattened math. These cause most of the remaining false positives on the corpus. Run the checker on the LaTeX
  or Markdown source when you can.
- LaTeX: `\input`/`\include` are not followed. Macros defined in an external `.sty` are not expanded (an unknown
  lower-case macro is dropped). Math, tables and TikZ text are not checked.
- Plain text: the abstract is taken to be the prose before the first heading, and headings are guessed. Use
  `--dump` to check the split.
- Sentence splitting protects common abbreviations (*Fig., Eq., Ref., e.g., et al.*). A sentence that ends in
  *etc.* or starts in lower case may merge with its neighbour.
- Check 8 compares spellings, not meanings. Check 6 accepts any nearby number. Check 9 understands numbering
  only from `\label`/`\ref` or from written-out *Fig. N* with *FIG. N* captions.
- The corpus rates in the report come from five papers (about 28,000 words). They show what a careful paper from
  this group looks like, not a target to hit exactly.
