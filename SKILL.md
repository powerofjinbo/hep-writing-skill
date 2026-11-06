---
name: hep-paper-writing
description: Draft, restructure and polish experimental or phenomenological high-energy-physics papers (hep-ph, hep-ex, ML for HEP) in the clear, story-driven style of five papers by Daniel Whiteson's group, with one central question, ideas layered from familiar to new, plain sentences with the verb up front, results as numbers against a baseline, and figures and captions that carry the evidence. Use it whenever the user drafts or revises any part of a physics paper, thesis chapter or proceedings (title, abstract, introduction, methods, results, conclusions, captions, figure plans, outlines), asks to make physics writing clearer or better organized, says a draft has no story, wants notes (including notes written in Chinese) turned into English paper text, or asks for feedback on a draft or a figure, even without naming this skill.
---

# Writing HEP papers with a clear story

This skill captures how five experimental and phenomenological HEP papers from Daniel Whiteson's group (UC Irvine) make complex work easy to follow. Use it to plan, draft, restructure or edit any part of a paper. The numbers below were measured on these papers, and every quote is verbatim.

| Tag | Paper |
|---|---|
| TOP | Tong, Corcoran, Fieg, Fenton, Whiteson, *New Physics in Single Resonant Top Quarks*, arXiv:2311.00121 |
| CHARM | Whiteson, *The era of charmed resonance searches at the LHC*, arXiv:2609.32054 |
| TIME | Fieg, Fox, Zhang, Ghosh, Varada, Whiteson, *Time-dependent signals of new physics at the LHC*, arXiv:2605.11071 |
| HNL | Feng, Hewitt, La Rocco, Whiteson, *Characterizing Heavy Neutral Leptons: ...*, arXiv:2510.16107 |
| TRACK | Miller et al., *Fast and Precise Track Fitting with Machine Learning*, arXiv:2505.02937 |

## The style in one paragraph

Each paper tells one story and repeats its key terms and numbers from the abstract to the conclusions. It leads the reader from the familiar to the new: the field, how the current approach works, what is missing, why the gap can be closed now, and then "In this paper, we". Inside the paper, the reader sees the whole plan before its parts and the easy case before the hard one. Every section, paragraph and sentence starts by saying what it is about. Sentences are of medium length, but the subject and verb come first, and each sentence makes one claim. Results are numbers set against a baseline, with their conditions attached. Figures carry the evidence: the text states the claim and points to the figure, and the caption explains every line, color and panel.

## Seven principles

### 1. One story, told early and echoed everywhere

*Why:* readers decide from the abstract whether to read on, and they remember one sentence afterwards. When the title, abstract, introduction and conclusions repeat the same key phrase and the same numbers, readers can check that the paper delivered what it promised.

- Write the story in one sentence before drafting anything: *We show that [idea or method] [does what] for [object], by [number] compared with [baseline], [condition].*
- Before any formalism, name in plain words the one assumption or trade-off of the standard approach that your paper changes. Then repeat that contrast, with the same key word, in the abstract, method, key result and conclusions. TRACK's method lets one "optimize directly for the true targets" [TRACK abstract s7], while traditional fitting "optimizes a proxy based on the distance between the track and the hits" [TRACK abstract s8]; the word *proxy* returns in Sec. V and the conclusions. TIME's contrast is the assumption that signals are constant in time. CHARM's is the trade-off between background reduction and tagging efficiency, which becomes its figure of merit.
- Plant the title's key phrase in the introduction's question or contribution (3/5 papers).
- Keep names, numbers and conditions identical in the abstract, body and conclusions. The corpus slips here: TOP's conclusions change the mass range given in its abstract.

### 2. A funnel that turns on a gap, an enabler and "In this paper, we"

*Why:* a reader accepts a new study only after seeing what is missing and why it can be done now. A bare gap invites the reply *perhaps for a good reason*.

- All five introductions make the same moves, in nearly the same order: territory, then how the status quo works, then the gap, then the enabler (why now or why here), then "In this paper, we ...", then a roadmap. (TRACK states its gap before the status quo's mechanism.) Optional moves are an explicit question (CHARM) and a preview of the results (HNL, TRACK).
- About two-thirds of the intro's words come before "In this paper" (56–74% in four papers). Typical length: 5–6 paragraphs of about 3–5 sentences each, 330–600 words in all. A broad first sentence is fine, but narrow to the paper's territory within one or two sentences.
- Open each intro paragraph by picking up the end of the one before: its key noun, a summary noun, or a *However* that answers it. All 13 paragraph breaks before the contribution do this, so no intro needs *Moreover* or *Furthermore*. For example: "Searches for new physics in interactions involving top quarks benefit from both motivations." [TOP Intro ¶2] *In this paper, we* marks the turn.
- Credit the closest work first (5/5), then name the one thing it did not do: "ATLAS studied the tγ final state [14], but did not examine the invariant mass of the system." [TOP Intro ¶4]
- State the gap as a measured fact, often in the present perfect and turning on *However*: "However, the fitting problem has received significantly less attention." [TRACK §I ¶2] Keep absolute claims for facts a reader can check: "However, no dedicated search for dijet resonances containing charm-tagged jets has been performed." [CHARM abstract s2]
- Give the reason for the gap, then the enabler: "Historically, charm identification was too inefficient" [CHARM §I ¶2], then "However, dedicated charm taggers have since improved substantially" [CHARM §I ¶3].
- Optionally turn the gap into a question that the conclusions answer: "This raises the questions: what level of performance is necessary to open the era of charmed dijet resonance searches?" [CHARM §I ¶4]
- Announce the contribution with *In this paper, we* + one verb, built from the gap's nouns. Enumerate when there are several items: "In this paper, we (i) model current charm-tagging performance in a dijet resonance search to predict the charm-tagged background, (ii) explore the sensitivity of LHC datasets to resonances decaying to charm pairs ... and (iii) explore the performance required to allow for dedicated charm-tagged dijet searches." [CHARM §I ¶5]
- End with a roadmap that gives each section one clause with an action verb. The best clauses state the finding: "In Sec. VI, we show that these same measurements may be used to determine if an HNL is a Majorana or Dirac fermion." [HNL §I ¶11]

### 3. Overview before detail, easy case before hard case

*Why:* a reader can place a step only after seeing the whole plan, and can trust a hard case only after seeing the method work on an easy one.

- Show the whole pipeline once, early: one master equation with its ingredients listed, or a flowchart. CHARM writes the tagged spectrum as one equation, then lists what it needs: "Predicting the charm-tagged fraction κ requires (i) a model of the flavor fractions of the QCD background as a function of jet pT" [CHARM §II ¶3]. Later sections fill in each ingredient.
- Say how many things are coming, then name them: "The tracking task has two distinct steps, finding and fitting." [TRACK §I ¶2]
- Climb a ladder of cases and say so aloud. Examples: known oscillation, then learned oscillation, then sidebands in time [TIME §IV]; Gaussian noise, then skewed noise [TRACK]; a benchmark with about 8600 events, then one with only 80 [HNL]. HNL turns to the hard case with "Of course, HNLs may be discovered with significantly fewer events." [HNL §I ¶6]
- Open each harder case with the limit of the one before, and name what carries over: "The above analysis requires knowing the time dependence in advance" [TIME §IV B ¶1]. TOP is the exception: it runs two parallel channels with one shared template, not a ladder.
- Work one benchmark point fully, then scan.
- In a phenomenology paper, treat the model as a vehicle. Say once which of its features the results use and how far the results reach, and cut model detail that no result uses: "Whatever the origin of this interaction, we use the time-modulation that it predicts" [TIME §II ¶3].
- Validate on a known answer before making the new claim, in one main-text sentence: "For a signal of a narrow Gaussian, our machinery recovers the ATLAS limits on the same signal shape [23] to within 10%; see Appendix A." [CHARM §II ¶6]
- The main text holds the claim and the verdict of each check. Appendices hold the variations, and each appendix is cited where it is needed, together with its verdict: "several variations on these assumptions are also explored in Appendix D, and do not qualitatively impact the conclusions." [CHARM §IV ¶4]

### 4. Every unit opens with its job

*Why:* readers skim first sentences. If each section and paragraph states its job up front, the skim alone gives the argument.

- **Sections** open with a purpose or a bridge from what we now have to what we need next: "With a model of the jet flavor and momenta in each bin, predictions of the tagged spectrum require a description of the tagging performance." [CHARM §IV ¶1] A results section can open as a small abstract (what the baseline assumed, what we do here, what we find, and why): "Their analysis assumes no intrinsic time variation in the signal. In this section, we reinterpret their search and apply it to a time-varying signal. We find tighter limits than those placed on models in which the signal is uniform in time." [TIME §III ¶1]
- **Paragraphs** do one job, stated in the first sentence. They end on the payoff (a mechanism or a number) or a hand-off. None of 40 sampled paragraphs ends on a summary sentence. A results section likewise ends on its headline number or its reason; state caveats where they bite, before that last payoff.
- A section that opens with its headline number must still define the metric at first use, in the same sentence or the one before (*the PU rejection, the inverse of the fraction of pileup jets that pass, rises from 12 to 45*).
- **Sentences** name their case first when several cases are in play: "In the skewed noise model, the difference in the approaches becomes apparent." [TRACK §V ¶4] This is how readers keep their place: about one sentence in eight opens this way.
- Put the reason in the same sentence as the choice: "This definition is used to allow direct comparison with ATLAS results." [CHARM §III ¶3]
- Put the justification where the doubt arises, not in a pile of caveats at the end. Fence the scope where a simplification is made ("for simplicity", "As a simplifying assumption"). Answer the obvious objection where the reader will raise it ("Of course, ...", "In practice, this is not a limitation").
- Before your choice, give the usual way (or the ideal case) and its concrete cost here, then *Instead*, your choice. When a result is weak or surprising, diagnose it before the fix, and let the diagnosis motivate the next step.
- Give each mechanism in words or a picture before its equation. Then present the equation as a sandwich: what it computes, the display, the symbols (*where ...* or *Here, X is ...*), then what it means. For example: "A value of G > 1 indicates a gain" [CHARM §IV ¶8]. Define the figure of merit by name: "The figure of merit is G, the relative gain in limits on the product of the cross section and branching ratio" [CHARM §IV ¶7].

### 5. Plain sentences: subject and verb first, one claim each

*Why:* readers hold the subject in memory until the verb arrives. An early verb and one claim per sentence keep that load small, which matters for the many readers who are not native English speakers.

Measured on 985 prose sentences from the five papers:

| Measure | Corpus value |
|---|---|
| Median sentence length | 23 words (papers 22–26) |
| Sentences over 40 words | about 11% |
| Position of the first finite verb | median word 5 |
| *we/our/us* | 13.6 per 1,000 words |
| Sentences with a passive | 40% in body text, 18% in abstracts |
| Plain verbs (*use, show, find, estimate, ...*) vs. *utilize/leverage* | 462 vs. 5 |
| Semicolons; dashes | 2.2; 0.3 per 1,000 words |

So the target is medium-length sentences with a fast start, not choppy ones. When simplifying, split a sentence where it holds two claims rather than chopping everything short.

- Open with a short subject the reader already has: the object just named, a summary noun (*These shortcomings*) or the case in hand. Reach the main verb by about word 5, and end on the new point. Keep an opening phrase to about five words ("In this section,", "For long oscillation periods,").
- Make one claim per sentence, and join a trade-off with *but*. When a sentence must be long, give it visible structure: (i)/(ii)/(iii), *respectively*, or a semicolon between parallel clauses. Split anything over 50 words that is not a marked list or a display.
- Mark each cause with one plain word (*because, due to, so, therefore*), and write a contrast as two clauses of the same shape (*but, while, rather than*), so only the contrasted words differ.
- Use short sentences (12 words or fewer) for setup, status and takeaways: "These questions are unanswered in the literature." [CHARM §I ¶4]
- Use *To [purpose], we [verb]* for choices and *we* + an active verb for results (*we consider, we find, we estimate, we show*). Use the passive to record a tool and its settings ("Jets are required to have ..."). Never write *It was found that*. Use the present tense for what the paper does and finds, and the simple past for a named earlier study (*ATLAS studied ...*).
- Use plain verbs: *use, study, find, show, estimate, predict, compare, measure, test*. Avoid *utilize, leverage, facilitate, elucidate, delve, showcase, underscore, pivotal, paves the way*.
- Use few connectors, and plain ones. *However* is almost the only contrast word. Use *so* or *therefore* inside the sentence, *To* + verb for purpose ("To predict the charm-tagged spectra, we apply ..."), and *First/Then/Finally* only for real sequences. *Moreover, Furthermore, Thus, Hence* and *Also* together open 4 of 672 sentences. Cut *It is worth noting that*, *In order to* and *the fact that*.
- When *This* points back to more than the last clause, add a noun ("This approach", "These sensitivities").
- Define a term where it first appears, in apposition or as *Long Form (ACR)*: "sterile neutrinos, fermionic gauge eigenstates with no SM gauge quantum numbers" [HNL §I ¶2]. Then never rename it. In the corpus, the term a paper is about never varies. Where secondary terms drift (TOP has eight names for its heavy quark), readers wonder whether they are different objects. Introduce each tool with a noun that says what it is (*the pyhf package*, *the GN2 tagger*), and never open a sentence with a symbol or a numeral.
- Prefer a period. Avoid em-dash asides, nested parentheses and semicolons used as commas.

### 6. A result is a number with a baseline and a condition

*Why:* a number without a baseline cannot be judged, and a condition placed far from its number gets lost when the result is quoted.

- Let one sentence carry the number, its unit or CL, the baseline and the condition: the sensitivity "can be up to a factor of two stronger compared to one that does not use time information" [TIME abstract s5].
- Build the baseline with your own machinery, switching off only the new ingredient, so that shared biases cancel (4/5): "Limits from the untagged and tagged spectra are computed with the identical machinery" [CHARM §II ¶8]. Choose the comparison that isolates the claim, not the one that gives the largest factor. When a headline gain combines several new ingredients, split it by ingredient with the controls the author has (how much comes from the new network, and how much from the added information).
- Compare with *a factor of N*, *N times* or *N% versus M%*, and say which direction is a gain: "The NN has classification accuracy of 96.2% versus 85.6% for the LS pipeline." [TRACK §VI ¶6] Do not describe one number both ways: TIME calls the same limit ratio *a factor of two* in one section and *50% stronger* in another.
- Give the mechanism right after the number: "The improved limits are primarily due to concentration of the signal in time, allowing for higher signal-to-background ratios." [TIME §III ¶1]
- Give the realistic number first and the bound second. If the result needs a future improvement, give today's value and the improved one, each with its assumption.
- Match the verb to the strength of the evidence (*exclude, reject, favor, disfavor*), and use one verb per number in the text, caption and abstract. State computed numbers flatly, use *can* or *would* with *expected* for projections, and hedge with *may* or *could* only for physics possibilities and future work. Only 6 of 68 modal hedges in the corpus touch a paper's own result. Calibrate with conditions instead: "in the simulated setting described here" [TRACK abstract s10].
- State a weak or negative result plainly, then explain it ("modestly better sensitivity than the untagged search" [CHARM §V ¶3]).
- Name the principal limitation in a plain sentence, then say whether the result survives it: "The principal limitation to our study is the lack of published pT-dependent charm efficiency" [CHARM §V ¶7]; "Our conclusions are quantitatively sensitive to these assumptions, but survive under the variations we explore." [CHARM §V ¶7]

### 7. Figures carry the evidence

*Why:* many readers look at the figures before the text. A figure must say what it shows on its own, and the text must say what to see in it. Otherwise each reader draws a different conclusion.

**Design**
- Make the first figure a schematic of the idea, before any data plot (4 of 5 papers).
- Plot the figure of merit as a ratio to the baseline, with a break-even line at 1. Put the baseline, the new method and a bound (an idealized method or "approximate ceiling") on the same axes, so the gain has a scale.
- Give each factor one visual channel, and state the mapping once: "color denotes the flavor and line style the scenario" [CHARM Fig. 11 caption]. Keep each method's color fixed across the whole paper.
- Paired panels change one condition and share the scale. Stacked panels put the mechanism on top and the payoff below. Print the condition on the panel itself, such as *Z′→cc̄, 2.0 TeV, 1+2 tag fit*.
- Draw the uncertainty that drives the conclusion. Use tables for numbers readers will quote and figures for trends.

**Captions** (64 of 67 open with a noun phrase; median caption sentence 18 words; almost never *we*). Give the jobs in this order:
1. The quantity and its variable, as a noun phrase: *X versus Y*.
2. The conditions that set this plot apart (sample, benchmark, luminosity, working point, and any log axis or object definition the author gives), so the caption stands alone.
3. An encoding key right after each noun it decodes: "CATHODE learned time score (solid blue) compared to the true temporal modulation (dashed orange)." [TIME Fig. 5 caption]
4. A panel map that matches the artwork: *Top: ... Bottom: ...* or *Left, ...; right, ...*.
5. The point or a reading rule: "A ratio greater than one indicates the tagged search is more powerful (smaller σ)" [CHARM Fig. 3 caption]. For a main-result figure, also give the headline number in the caption, so the figure stands alone (6 of 11 HNL captions do). A diagnostic figure can carry a reading rule instead. Never let neither the caption nor the text carry the takeaway.
6. If needed, one guard against a likely misreading: "The background is time-independent, wiggles are statistical." [TIME Fig. 3 caption]

Name curves by line style or label rather than by colors nobody has chosen yet, and avoid cosmetic placeholders such as *[color?]*; one note to the author about styling is enough.

**Text–figure coupling**
- Lead with the claim and point last (*...; see Fig. N*, *as shown in Fig. N*, *X is shown in Fig. N*). The figure is the grammatical subject in only 10 of 88 references.
- To introduce a main-result figure, say what it plots, then say at once what to notice, regime by regime and in panel order: "Figure 3 shows the relative gain G versus mass for several working points, for Z′ and T signals. For the Z′, the ϵc = 0.6 working point has a gain greater than 1 across the full mass range; for the T, there is gain for lower masses." [CHARM §IV ¶9]
- Cite every figure, table and appendix, in number order, on or before its page. In LaTeX, place each figure environment right after the paragraph that first cites it.

## How to work

### Step 0: find the story before touching sentences

Before drafting or editing, write down these five items. Show them to the user when you restructure or plan.
1. The one-sentence story.
2. The gap and the enabler.
3. The ladder of cases, easy to hard.
4. The figure that carries each claim.
5. The headline number with its baseline and condition.

If the user's material lacks a piece, such as a baseline for the headline number, ask for it or leave a visible placeholder like *[baseline?]*. Never invent it.

### Drafting from notes or results
1. Build the skeleton: sections, each answering one question, and a figure list in story order (schematic, then inputs and validation, then main result versus baseline, then robustness).
2. Draft the abstract and introduction from the templates below.
3. Draft each body section: opener, overview, cases in ladder order, results with numbers and mechanisms, scope fences and caveats where they apply.
4. Write the captions with the caption anatomy above.
5. Revise with the checklist. For a long LaTeX or Markdown draft, run `python3 scripts/style_check.py draft.tex` and judge each flag yourself: the script is a smoke detector, not a style authority.

### Editing a draft
Work top-down: story, then structure, then paragraphs, then sentences, then words, then figures. Polishing sentences in a paragraph that should move is wasted work.
1. Diagnose. Is there a one-sentence story? Are the gap, enabler and contribution present, in that order? Are the cases in ladder order? Does every paragraph open with its job? Are sentence length, verb position and connectors in the corpus range? Are terms consistent? Does every result have a number, a baseline and a condition? Are the captions complete?
2. Rewrite. Keep every physics statement, number, citation and LaTeX command. Fitting a draft to the templates must not change what it claims (see *Rewrite without changing the claims* below).
3. Reread each rewritten sentence against its source for meaning drift: who did what, the scope, the direction of an effect, the condition. Merging or splitting sentences is where drift creeps in.
4. Return what the user asked for, in the order and format they asked for. By default: the revised text first, ready to paste, in the input's format; then the main changes in 3–5 bullets of one line each (about 15–20 words); then at most 3–4 short questions (see *Read it as a referee*).

### Rewrite without changing the claims
The templates (gap, enabler, a result with a baseline) tempt you to sharpen what the author wrote, whether you are editing a draft or drafting from notes. Resist that:
- Keep the scope of every claim. If the draft says *these searches [9, 10] did not use the vertex time*, do not write that *searches* in general have not. Do not generalize from one example to a class: one autoencoder that failed does not make *unsupervised methods* prone to failure.
- Never drop a claim because it lacks a number. Keep it, and mark the missing number (*improves the limit by [factor?] over cτ = [range?]*) or ask. Give each placeholder its own descriptive name; never use one letter for two quantities.
- Do not write your own reading of an unstated baseline or condition into the text. Put it to the user as a question, or use a placeholder such as *[baseline: without the timing cut?]*.
- Keep each statement at the author's level of certainty. An explanation the author offers as their interpretation becomes *We attribute this to ...* or *This is consistent with ...*, not *This is because ...*.
- When the material gives no mechanism for a result, leave a placeholder in the text and offer your best candidate explanation in the notes, marked as a suggestion to confirm.
- Define standard variables and tools at first use even when the notes do not (for example a pileup discriminant like R_pT), using the standard definition, and ask the author to check it.
- Keep an author's claim that you doubt, and flag it in the notes; do not silently correct it.

### Read it as a referee
Style is half the job; the other half is what a referee will ask first. After the text, add at most 3–4 short questions, the most important first. Typical ones: a confound in the comparison (different luminosity, samples or training), an undefined reference point (what is *t* = 0?), the selection a quoted efficiency refers to, whether a difference is significant given its spread, and a missing baseline that would isolate the claim. When a quick estimate settles a point (a velocity, a scaling with luminosity), do it and give the result in the notes, not in the paper text.

### Restructuring a project into a paper
A paper *has no story* most often because it follows lab-notebook order: first we tried X, then Y. Reorder it around the question.
- Lead with the claim that the evidence supports, and order the results as a ladder.
- A dead end becomes one or two sentences of motivation or an appendix (*A natural first approach, X, sculpts the background because Y*).
- Side studies (hyperparameter scans, other masses) become robustness checks: the verdict goes in the main text, the details in an appendix.
- Null and closure tests become validation, placed before the main result.
- Keep the evidence for the central claim, including the diagnosis behind it, in the main text; move only variations to appendices.
- Give every figure a job in the storyline, and mark which figures exist and which need new runs. Drop or demote any figure without a job.

### Captions and figure feedback
Check each figure against the design rules and each caption against the caption anatomy. Name concrete fixes: which panel lacks a unit, which two colors encode the same thing, where a ratio panel or break-even line would make the claim visible.

## Templates

**Abstract** (5–8 sentences, about 100–240 words; when revising, stay near the draft's length). Keep the gap and aim sentences short, let the aim arrive within the first third, and let the result be the long sentence.
1. Context (1–2 sentences): why this class of search or measurement matters.
2. Status quo, described by how it works or what it assumes.
3. Gap: *However, [X] has not been [studied / used / generalized].*
4. Aim: *We [study / propose / characterize] [X] [for Y].*
5. Method in one line: *Using [data, simulation or model], we [estimate / predict] [quantity].*
6. Result: *[Quantity] [improves / reaches] [number and unit or CL] compared with [baseline], [condition].*
7. Implication: *These results [provide targets for X / motivate Y].*

**Introduction** (5–6 one-job paragraphs)
1. Territory: what this class of physics or method does and why it matters.
2. Status quo: how it works now, and its main challenge.
3. Gap: *However, ...*, with the reason it has been left open (*Historically, ...*).
4. Enabler: what has changed. Optionally: *This raises the question: ...?*
5. Contribution: *In this paper, we (i) ..., (ii) ..., and (iii) ....* Optionally preview the headline number.
6. Roadmap: *Section II describes ... Section III shows that ...*

**Section opener:** *With [X] in hand, [Y] requires [Z].* or *[Previous work] assumes [A]. In this section, we [do B]. We find [C], because [D].*

**Results paragraph:** *[Claim with number and baseline]; see Fig. N. For [regime 1], ...; for [regime 2], .... This is because [mechanism].* Or: *Figure N shows [quantity] versus [variable] for [cases]. [What to notice, regime by regime.] [Takeaway with number.]*

**Caption:** *[Quantity] versus [variable] for [cases], [conditions]. Top: ...; bottom: .... [Solid/dashed, colors, bands mean ...]. [A value above 1 means ... / takeaway.]*

**Conclusions** (3–7 short paragraphs)
1. Re-establish the problem in one or two sentences, so the conclusions can be read alone.
2. *We have [done X].* Give the headline number with the same baseline and condition as in the abstract.
3. Give further results in ladder order.
4. *The principal limitation is ...*, then whether the result survives it and what would remove it.
5. The implication, one step wider than the results and aimed at a named reader. No paper writes *In summary* or *In conclusion*. A concrete recommendation is welcome: "Tagger development aimed at dijet resonances should therefore target the high-efficiency working points." [CHARM §V ¶5]

## Guardrails

- **Faithfulness first.** Never invent numbers, references, results, or citations. Keep the author's claims at their original strength. Where a template slot is empty, use a placeholder and say so.
- **Reference examples are made up.** The *After* sentences in `references/` follow an invented study (a muon-spectrometer trigger for long-lived particles) with invented numbers. They show the target form only. Never carry their facts or numbers into the user's text, even when the user's topic is similar.
- **Preserve LaTeX.** Keep `\cite`, `\ref`, `\label`, math, macros and symbols exactly. Change words, not notation.
- **Language.** Write paper text in English. Write explanations, change notes and questions in the user's language; if the user writes in Chinese, explain in Chinese.
- **Plain notes.** Explain changes in words the user already knows. Do not use this skill's shorthand (*enabler*, *ladder*, *pivot*, *one step wider*) without saying what it means. The text is the deliverable, so keep notes short. When the user asks for a list of changes, give one line per bullet. When the user sets no format, a few short bullets on the main choices and the open questions help more than either silence or an essay.
- **References.** In paper text, leave *[ref]* placeholders for claims that need a citation. In your notes you may name standard references you are sure of (authors, year, title), marked *please verify*; never guess arXiv numbers or BibTeX keys.
- **Do not copy the corpus's slips.** These include typos, a key object with several names, captions that contradict the artwork, uncited figures or appendices, numbers that drift between abstract and conclusions, a condition dropped from an abstract headline, *allows for* where *allows* will do, and the rare *it is worth noting that*.
- **Style serves content.** These rules describe what made these papers clear. When a rule conflicts with clarity for a specific passage, choose clarity and say why.

## Checklist before you return text

- [ ] The one-sentence story is visible in the title, the abstract result, the intro contribution and the conclusions, with the same key phrase and numbers.
- [ ] The intro runs territory, status quo, gap, enabler, *In this paper, we*, roadmap.
- [ ] The overview comes before the details, cases run from easy to hard, and validation comes before the new claim.
- [ ] Each section and paragraph opens with its job; paragraphs end on a payoff or hand-off.
- [ ] Sentences: median around 20–25 words, the verb early, one claim each, few and plain connectors, no inflated verbs.
- [ ] Every key object has one name, defined at first use; there is no acronym before its definition.
- [ ] Every result has a number, a baseline and a condition; one number is not stated both as a factor and as a percent; verbs match the evidence; limitations are named plainly.
- [ ] Captions: quantity versus variable, conditions, encoding key, panel map, point or reading rule.
- [ ] Every caption matches the rendered figure (panels, colors), and every number in the text is read off the final figure.
- [ ] Every figure, table and appendix is cited in order, and the text says what to see.
- [ ] Nothing was invented, dropped, widened or reinterpreted; every rewritten sentence was reread against its source.
- [ ] LaTeX is intact; the notes are short, plain, in the user's language, and in the format the user asked for.

## Bundled resources

This file is enough for a paragraph-level edit. For bigger tasks, read only the one or two references the task needs; each holds the full evidence, more examples, before-and-after rewrites and templates.

| Task | Read | What it holds |
|---|---|---|
| Title, abstract, introduction, conclusions, paper outline | `references/story-and-structure.md` | The story sentence, funnel, gap and enabler, abstract moves, the model as a vehicle, conclusions, the echo check |
| Organizing a section, flow between paragraphs, equations | `references/layering-and-flow.md` | Overview first, case ladders, section and paragraph openers, connectors, cross-references, appendices |
| Polishing sentences and wording | `references/sentences-and-words.md` | Measured norms, sentence shape, one name per object, definitions, results wording, hedging, voice and tense |
| Figures, captions, results paragraphs, limitations | `references/figures-and-evidence.md` | Figure storyline, design rules, caption order, text–figure coupling, baselines and bounds, tables |

- `scripts/style_check.py`: flags long sentences, late verbs, stock connectors, inflated words, hype, vague claims, undefined acronyms, term variants and figure-order problems in a `.tex`, `.md` or `.txt` draft (`-` reads stdin). It is worth running on drafts longer than about a page. The report explains each flag and its corpus basis, so there is no need to read `scripts/README.md`. Run `python3 scripts/style_check.py --help` for options.
