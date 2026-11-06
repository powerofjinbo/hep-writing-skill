# Story and structure

Read this file when you plan a paper, or draft or revise its title, abstract, introduction, section layout or conclusions. Reread it before submission to check that they tell one story.

Paper tags: TOP = Tong, Corcoran, Fieg, Fenton, Whiteson, "New Physics in Single Resonant Top Quarks", arXiv:2311.00121 (6 pp); CHARM = Whiteson, "The era of charmed resonance searches at the LHC", arXiv:2609.32054 (12 pp); TIME = Fieg, Fox, Zhang, Ghosh, Varada, Whiteson, "Time-dependent signals of new physics at the LHC", arXiv:2605.11071 (12 pp); HNL = Feng, Hewitt, La Rocco, Whiteson, "Characterizing Heavy Neutral Leptons: Measuring Parameters, Discriminating Majorana versus Dirac, and Using FASER2 as a Trigger for ATLAS", arXiv:2510.16107 (15 pp); TRACK = Miller et al. (incl. Baldi, Whiteson), "Fast and Precise Track Fitting with Machine Learning", arXiv:2505.02937 (19 pp).

**Conventions.** Quotes are verbatim; tags give paper, section and paragraph (¶), and s is an abstract sentence. Invented examples (italics, after *Before:* and *After:*) follow one made-up study, a muon-spectrometer trigger for long-lived particles, with made-up numbers. k/5 counts papers. Related files: layering-and-flow.md, sentences-and-words.md, figures-and-evidence.md. The *After* sentences show the target form and assume the author supplied every fact in them; their numbers are made up. When you edit a real draft, take every fact and number from the author's material, and mark anything missing with a placeholder such as [baseline?] instead of inventing it.

## Contents

- STORY-1. One story, told four times
- STORY-2. Carry one central contrast to the end
- STORY-3. A funnel introduction, linked by pick-ups
- STORY-4. A narrow, fair gap, and why now
- STORY-5. Contribution, roadmap and headings line up
- STORY-6. The body as a ladder of cases
- STORY-7. An abstract in fixed moves
- STORY-8. The headline number keeps its conditions
- STORY-9. The model as a vehicle
- STORY-10. Conclusions that stand alone, then end one step wider
- STORY-11. A short title that earns its claims
- Templates; Corpus slips to avoid

### STORY-1. One story, told four times

**Rule.** Before drafting, write the question and its answer as one sentence: object, method, number, baseline, condition. The title, the abstract's result, the contribution and the conclusions' recap restate it with the same nouns, and the number never changes.

**Why it works.** A reader of any one part gets the same story, and each part confirms the last.

**Prevalence.** Tight in HNL, TRACK and CHARM; partial in TIME; loose in TOP. HNL's contribution and conclusions share one frame; TRACK's abstract s6–s10 nearly copy intro ¶4; CHARM carries *competitive* from abstract s3 to §V ¶1. TIME's resonance gain never reaches its abstract, and TOP's names and numbers drift (slips 2, 6).

**Exemplars.**
- "we explore the potential of FASER2 to constrain its mass and couplings and determine its spinor nature" [HNL §I ¶5] returns as "we have investigated the potential of FASER2 to measure the mass and coupling of an HNL" [HNL §VIII ¶1].
- "This work demonstrates that, with 'cradle to grave' observations ... one can precisely determine the HNL's properties" [HNL §I ¶10]: the story sentence, inside the introduction.

**Draft violation and fix.**
- Before: *Abstract: our framework improves LLP sensitivity. Conclusions: the strategy looks promising in many scenarios.*
- After: *Abstract and conclusions: the muon-spectrometer trigger keeps 31% of decays at 1–5 m, against 12% for the standard trigger.*

**Boundaries.** The title never carries the number, and the introduction may hold it back (TOP, CHARM, TIME). Near-verbatim reuse between abstract and introduction is accepted (TRACK).

### STORY-2. Carry one central contrast to the end

**Rule.** Before any formalism, state in plain words the one assumption or trade-off of the standard approach that your paper changes, and why changing it helps. Repeat that contrast, with the same key word, in the abstract, method, key result and conclusions.

**Why it works.** The reader knows what *better* means before the first number, so every result supports one idea.

**Prevalence.** End to end in 3/5: TRACK, *proxy* versus *true target* (abstract s8, §II, §V ¶7, §VII ¶2); TIME, time invariance (abstract s2, §I ¶4, §VI ¶1); CHARM, background reduction versus tagging efficiency (abstract s1, §II ¶8, the definition of G). HNL uses a physical handle, the companion muon's charge (§I ¶8). TOP has none.

**Exemplars.**
- "traditional fitting, which optimizes a proxy based on the distance between the track and the hits" [TRACK abstract s8]; after the hardest test, "χ2hit is no longer a proxy for the true target" [TRACK §V ¶7].
- "When the signal is time-dependent and the background is not, their differing behavior provides additional discriminating information" [TIME §I ¶4]: the mechanism, before any likelihood.

**Draft violation and fix.**
- Before: *Current triggers have several limitations, so we propose a novel graph-neural-network approach.*
- After: *Current triggers need a track that points back to the beam line, so they miss distant decays. Ours uses muon-spectrometer hits alone.*

**Boundaries.** The contrast may come late when an easy case comes first (HNL ¶8). Do not inflate it: TIME's *highly motivated* (§I ¶2) needs ¶3's *It is possible that*.

### STORY-3. A funnel introduction, linked by pick-ups

**Rule.** Write five or six paragraphs that narrow from the field to your work: territory, status quo and how it works, gap, why now, contribution, roadmap. Open each paragraph by naming its role and picking up the end of the one before: its key noun, a summary noun, or a *However* that answers it.

**Why it works.** The reader always knows the step, and the words carry the link without *Moreover*.

**Prevalence.** The moves: 5/5. Four introductions have 5–6 paragraphs (328–590 words, 56–74% of them before *In this paper*); HNL has 11. All 13 breaks before the contribution open with a pick-up (TOP, CHARM, TIME ¶1–¶4; HNL, TRACK ¶1–¶3); *In this paper* (HNL: *In this work*) marks the turn itself. No introduction opens a sentence with *Moreover* or *Furthermore*.

**Exemplars.**
- "Searches for new physics in interactions involving top quarks benefit from both motivations." [TOP Intro ¶2]: two words fold ¶1 into ¶2.
- "However, the fitting problem has received significantly less attention." [TRACK §I ¶2] The next paragraph: "Traditional approaches to track fitting use maximum likelihood estimation" [TRACK §I ¶3].

**Draft violation and fix.**
- Before: *(¶3 ends on trigger rates.) Moreover, machine learning is becoming popular in high energy physics.*
- After: *These rate limits leave room for a classifier that rejects prompt background at the first trigger level.*

**Boundaries.** A paragraph may hold several sub-steps of its role (TIME ¶1). The gap may come before the status quo's mechanism (TRACK ¶2–¶3).

### STORY-4. A narrow, fair gap, and why now

**Rule.** Credit the closest work, then name the one thing it did not do, as a measured fact in the present perfect. Give the gap's reason if you know it, then say in one sentence what has changed or why this place is right. Save *no dedicated search* and *the first to* for checkable facts.

**Why it works.** A narrow gap can be checked, and the enabler answers the silent question: why has nobody done this?

**Prevalence.** A measured gap: 4/5 (TOP ¶3, CHARM ¶2, TIME ¶1, TRACK ¶2); HNL's is a future need (¶3). Credit first: 5/5 (TOP ¶4, CHARM ¶3, TIME ¶1, HNL ¶9, TRACK ¶3). Why now or here: 5/5 (TOP ¶4, CHARM ¶3, TIME ¶3, HNL ¶4, TRACK ¶3). A literal question: CHARM only (weaker evidence: 1/5).

**Exemplars.**
- "ATLAS studied the tγ final state [14], but did not examine the invariant mass of the system." [TOP Intro ¶4]: credit, then one missing piece.
- "Historically, charm identification was too inefficient" [CHARM §I ¶2], then "However, dedicated charm taggers have since improved substantially" [CHARM §I ¶3]: the reason, then the change.

**Draft violation and fix.**
- Before: *To the best of our knowledge, no one has ever studied long-lived particles with timing.*
- After: *Timing has been used to reject beam background [n], but not to select displaced decays. The new readout of every bunch crossing makes this possible.*

**Boundaries.** Enablers vary: a tool, a background now understood, a theory scenario, a facility, a cost-need tension. Say where the rival wins: "a dijet search will be the more sensitive channel" [TOP Models ¶4].

### STORY-5. Contribution, roadmap and headings line up

**Rule.** Announce the contribution with *In this paper, we* and plain verbs, reusing the gap's nouns; number the items if there are several. End with a roadmap that gives each section one clause and a verb saying what it shows. Make each item one results section, in the same order and words.

**Why it works.** The reader ticks off the gap item by item, and the roadmap maps the argument.

**Prevalence.** *In this paper* opens the contribution in 5/5 (TOP ¶5, CHARM ¶5, TIME ¶5, HNL ¶5, TRACK ¶4), and all five reuse the gap's nouns. A roadmap ends 5/5 introductions; TIME's sits inside the contribution. Items, roadmap and headings line up one to one only in TIME (§II to §IV C) and HNL (§V–§VII) (weaker evidence: 2/5).

**Exemplars.**
- "In this paper, we (i) model current charm-tagging performance ... (ii) explore the sensitivity" [CHARM §I ¶5]: numbered items that answer the questions of ¶4.
- "In Sec. VI, we show that these same measurements may be used to determine if an HNL is a Majorana or Dirac fermion." [HNL §I ¶11]: the clause states the finding.

**Draft violation and fix.**
- Before: *Several studies are performed. Section 2 covers the detector and Section 4 the results.*
- After: *In this paper, we (i) design the trigger, (ii) measure its efficiency and (iii) test it under pileup. Section V shows that the gain survives pileup.*

**Boundaries.** One contribution sentence suits a letter (TOP) if its main reason gets its own clause (slip 5). A results preview is optional (HNL, TRACK) and carries the abstract's conditions. The roadmap must match the paper (slip 7).

### STORY-6. The body as a ladder of cases

**Rule.** Order the body as model, setup, method, results, conclusions. Show the whole method once before its parts. Run the results from the standard case to the hardest, name each results heading for its case, and open each rung with the last one's limit. Move validations to appendices or a discussion section, and state each verdict at its pointer.

**Why it works.** The reader learns the method on clean ground, and each harder case answers an objection to the last.

**Prevalence.** The skeleton: 5/5; a validity section in TOP and TIME, appendices in CHARM and TRACK. A ladder: 4/5 (HNL by event count, TIME by prior knowledge, TRACK by noise, CHARM from b-tagging to charm); TOP runs parallel channels. A map first: 5/5 (CHARM Eq. 1, HNL Fig. 2, TIME §IV lead, TRACK Fig. 1, TOP Exp. Sens. ¶4). Results headings name the case in 4/5.

**Exemplars.**
- "The above analysis requires knowing the time dependence in advance" [TIME §IV B ¶1]: the new rung opens on the old one's limit.
- "our machinery recovers the ATLAS limits on the same signal shape [23] to within 10%; see Appendix A" [CHARM §II ¶7]: the verdict travels with its pointer.

**Draft violation and fix.**
- Before: *Section 4 shows the full Run 3 scenario; the simpler case without pileup is in the appendix.*
- After: *Section IV treats events without pileup, where the efficiency depends only on the decay position. Section V adds pileup.*

**Boundaries.** In HNL and TIME, the headings alone tell the story. Setup sections may take generic headings (MODEL, DATA). Split long results sections, and cite every appendix (slip 9).

### STORY-7. An abstract in fixed moves

**Rule.** Write, in order: context; the status quo by its mechanism; a short gap on *However*; the aim with one plain verb; the method in one line; the result with its number and baseline; an optional implication. Keep the pivots to 10–20 words, and split the result past about 40. Leave out citations, software, the roadmap and future work.

**Why it works.** Readers find the aim and the result where they expect them, and short pivots show the turns.

**Prevalence.** Aim and result: 5/5. A gap on *However* or *yet*: 4/5 (TOP s1, CHARM s2, TIME s3, TRACK s4). Status quo by mechanism: 3/5 (CHARM s1, TIME s2, TRACK s8). A number: 4/5 (not CHARM). In 4/5 the pivots are the shortest sentences (11–17 words) and the result the longest (41–54); TOP is flat.

**Exemplars.**
- "However, no dedicated search for dijet resonances containing charm-tagged jets has been performed." [CHARM abstract s2] "We study the charm-tagging performance required to make such searches competitive with the inclusive dijet search." [CHARM abstract s3]: gap and aim in 13 and 16 words.
- "We then consider a second, more difficult, case" [HNL abstract s5]: the abstract climbs the ladder.

**Draft violation and fix.**
- Before: *LLPs are very important [1–3]; after reviewing our MadGraph and Delphes setup, we describe our trigger, show results and discuss future work.*
- After: *However, no trigger selects displaced decays from muon-spectrometer hits alone. We design one and measure its efficiency.*

**Boundaries.** HNL opens with its aim, because its premise is a future discovery, and keeps *However* for the rescue (s7). TIME fuses aim and result in a 50-word last sentence; split that.

### STORY-8. The headline number keeps its conditions

**Rule.** Give the headline number, its baseline and its conditions in one sentence. Keep the number, the baseline's name and the conditions the same in the abstract, body and conclusions, and read them off the final figure. If the result needs a future improvement, give today's value and the improved one, each with its assumption.

**Why it works.** A number without a baseline cannot be judged, and the abstract's version is the one that gets quoted.

**Prevalence.** A baseline in or beside the abstract's result: 4/5 (CHARM s3, TIME s5, TRACK s8, HNL s4); TOP's is only in the body. An explicit condition: 3/5 (TOP s4, CHARM s5, TRACK s10). Numbers stay fixed in HNL and TIME and drift in TOP and TRACK; HNL's lose conditions (slips 1–2). Today-and-tomorrow pairs: HNL §VI, §VIII.

**Exemplars.**
- "can be up to a factor of two stronger compared to one that does not use time information" [TIME abstract s5]: number, bound and baseline in one clause.
- "FASER2 would only be able to favor the Majorana model over the Dirac model at 87.8% CL (1.2σ)" [HNL §VIII ¶2]; the next sentence gives 99.8% CL with the flux uncertainty it assumes.

**Draft violation and fix.**
- Before: *Abstract: a 40% gain. Conclusions: a gain of about 1.5.*
- After: *Abstract and conclusions: for decay lengths of 1–5 m and Run 3 pileup, the new trigger improves the expected limit by 40% over the standard muon trigger.*

**Boundaries.** TIME's abstract gives the realistic gain (about 2); the limiting case (about 7, background unconstrained) comes later, with its condition. Give every claim in the title a number (slip 3).

### STORY-9. The model as a vehicle

**Rule.** Present the model as a benchmark that produces the signature. Say once, early, which of its features the results use and how far the results reach. Pick benchmarks that stand for a class of cases, name the class, and cut model detail that no result uses.

**Why it works.** Readers with other models can use the result, and the story does not stall in unused theory.

**Prevalence.** 4/5, every phenomenology paper: TOP (abstract s3, Discussion ¶2), CHARM (§IV ¶8), TIME (§II ¶3), HNL (§II, Table I caption). TRACK, a method paper, fences its scope instead. Counterexample: TIME's fine-tuning discussion in §II (slip 10).

**Exemplars.**
- "though the limits apply to a range of theoretical models" [TOP abstract s3]: the reach, claimed in the abstract.
- "Whatever the origin of this interaction, we use the time-modulation that it predicts" [TIME §II ¶3]: what the results take from the model.
- "Model 1 represents models with a large number of decays in FASER2" [HNL Table I caption]: a benchmark that stands for a class.

**Draft violation and fix.**
- Before: *We consider the hidden-valley model of Ref. [n].* Three unused paragraphs on its dark sector follow.
- After: *We use a hidden-valley scalar only as a benchmark: the efficiency depends on the decay position, not the model, so the results hold for any neutral particle that decays in the muon spectrometer.*

**Boundaries.** Back the reach with a reason: TOP's limits "depend only on the level of background and the kinematics" [TOP Discussion ¶2]. A model can be declined outright: "We do not attempt to motivate a particular flavor model" [CHARM §IV ¶8].

### STORY-10. Conclusions that stand alone, then end one step wider

**Rule.** Restate the problem in one or two sentences. Recap the work in one sentence with *we have*, then repeat the abstract's numbers with their conditions, in the present tense; add no new headline. State the principal limitation plainly, with whether the result survives it. End on one sentence wider than the results, for a named reader, and let the close return to the opening's stakes.

**Why it works.** Readers who jump here from the abstract get a close that confirms it, admits its limit and leaves one idea.

**Prevalence.** Problem first: 3/5 (CHARM, TIME, TRACK). A present-perfect recap: 3/5 (CHARM, HNL, TRACK). The abstract's numbers with conditions: 3/5 (HNL, TIME, TRACK). A plain limitation: 4/5 (CHARM §V ¶7, TRACK §VII ¶3, TIME §VI ¶6, HNL §VIII ¶4; none in TOP). A wider last sentence: 4/5 (CHARM ends on robustness). A return to the opening's stakes: strong only in HNL. No paper writes *In summary* or *In conclusion*.

**Exemplars.**
- "The task of track fitting is to most accurately, and without bias, recover the parameters of the helical trajectory" [TRACK §VII ¶1]: the problem restated.
- "The principal limitation to our study is the lack of published pT -dependent charm efficiency" [CHARM §V ¶7], then "Our conclusions are quantitatively sensitive to these assumptions, but survive under the variations we explore." [CHARM §V ¶7]
- "Tagger development aimed at dijet resonances should therefore target the high-efficiency working points." [CHARM §V ¶5]: advice to a named community.

**Draft violation and fix.**
- Before: *In conclusion, we studied many aspects of LLP triggers, and our method works better in most cases. In the future, we plan to apply it to other analyses.*
- After: *We have developed a trigger that uses muon-spectrometer hits alone. It keeps 31% of decays at 1–5 m, against 12%. Our main limitation, the simplified geometry, should not change this gain. Needing no beam-line track, the trigger can select any neutral particle that decays in the spectrometer.*

**Boundaries.** Keep one tense per paragraph; HNL mixes *we have found* and *We performed*. Name the limitation's remedy when you can (HNL: flux data from FASERν). Wider must not mean stronger: TRACK's abstract promises *directly* what its conclusions call *Potential applications*. A conditional close keeps a promise honest (TIME).

### STORY-11. A short title that earns its claims

**Rule.** Write a noun phrase of about seven to nine words that names one searchable object and its setting or means, with no verb, number or software. Plant its key phrase in the introduction's question or contribution. Back every claim it implies with a number.

**Why it works.** Readers find the object in a listing, and the title states what the paper must deliver.

**Prevalence.** 7–9 words in 4/5; HNL has 18, a goal plus three tasks that become Secs. V–VII. All five are noun phrases, without numbers or software. The key phrase returns in the introduction in 3/5 (CHARM ¶4, TRACK ¶4, TIME ¶1 and ¶5) and in the last sentence only in TIME.

**Exemplars.**
- "Fast and Precise Track Fitting with Machine Learning" [TRACK title] becomes "a fast and precise machine-learning-based track fitter" [TRACK §I ¶4] in the contribution.
- "what level of performance is necessary to open the era of charmed dijet resonance searches?" [CHARM §I ¶4]: the title becomes the paper's question.

**Draft violation and fix.**
- Before: *A Study of Long-Lived Particle Triggering Using Graph Neural Networks and XGBoost with the Phase-2 Readout*
- After: *Triggering on displaced decays in the muon spectrometer*

**Boundaries.** A task-list title needs each task as a section in the same words; HNL's *Discriminating* became *Differentiating*. Avoid ambiguity (TOP's *Single Resonant Top Quarks* reads as if the top quark resonates) and breadth beyond the paper (CHARM names all charmed resonance searches but studies dijets).

## Templates

**T1. Story sentence.** `[Method] [verb]s [object] by [number] compared to [baseline], [condition].`

**T2. Abstract.**
1. `[Program] [does X] through [standard approach].`
2. `In most [searches], [assumption].` or `..., where [benefit] outweighs [cost].`
3. `However, [specific thing] has not been [done].`
4. `We study [X] required to [Y].` or `Here, we propose [Z] for [task].`
5. `Using [data or simulation], we [verb] [what].`
6. `[Condition], [object] [verb] [number] compared to [baseline].`
7. Optional: `These results provide [targets for X] and motivate [Y].`

Ladder variant (HNL): `We first consider [case 1] ... We then consider a second, more difficult, case ... However, by [new idea], [result].`

**T3. Introduction.**
1. `A central goal of [field] is [X].`
2. `One fruitful approach is [X], where [mechanism].`
3. `[Group] studied [X] [ref], but did not [Y].`
4. `Historically, [reason]. However, [tool] has since improved [ref].` Optional: `This raises the question: [question]?`
5. `In this paper, we (i) [verb] ..., (ii) [verb] ..., and (iii) [verb] ....`
6. `Section II describes .... Section IV shows that ....`

**T4. Conclusions.**
1. `[The task] is [X]. [Standard approach] assumes [Y].`
2. `We have [developed] [object].` Then: `[Condition], we find [number] compared to [baseline].`
3. `The principal limitation of this study is [X]. Our conclusions are sensitive to [X], but survive [Y].`
4. `[Named community] should therefore [action].` or `This work shows that [lesson].`

**T5. Echo check before submission.**
- One name each for the object, the baseline and the figure of merit, from title to conclusions.
- The same number, baseline and conditions in the abstract, body, conclusions and final figure.
- A number for every claim in the title.
- Contribution items, roadmap clauses and results headings in one order; every appendix cited with its verdict.
- The opening stakes back at the end.

## Corpus slips to avoid

1. **A headline that loses its conditions.** "the Dirac fermion hypothesis can be rejected at 99.8% CL" [HNL abstract s4] needs the flux uncertainty cut from 60% to 5% (today: 87.8% CL). The abstract's 99.7% also needs muon coverage up to |η| < 4.9, which the conclusions drop.
2. **Drifting numbers.** TOP's abstract covers 300–1000 GeV; its conclusions say "mT ∼ O(100) GeV" [TOP Conclusions ¶1] and quote 100 fb at 300 GeV, where Fig. 5 shows about 600–1,100 fb. TRACK's speed-up is *1,000*, *more than 1,000* and *over 1,000* times.
3. **Claims without numbers.** CHARM never states the size of the gain that its Fig. 3 shows. TRACK never puts a number on *Precise*.
4. **Abstracts that outrun the body.** TRACK's abstract says its gains lead *directly* to four downstream improvements; it tests only anomaly detection, in a toy. HNL's abstract credits ATLAS with precise property measurements; the body uses ATLAS only for the Majorana–Dirac test.
5. **Hype and overload.** *Novel* twice in TRACK's abstract; *highly motivated* in TIME §I ¶2; a 50-word TIME abstract sentence with the number last; a 48-word TOP contribution sentence.
6. **One object, several names.** TOP's T is a *top partner*, a *vector-like quark* and once a *T boson*. CHARM's baseline is *inclusive*, *untagged* and *flavor-blind*.
7. **Roadmaps that miss.** TOP promises results "in terms of the theoretical parameters" [TOP Intro ¶6] that never come. CHARM's roadmap stops at Sec. IV. TIME's says *Finally*, then *Then*.
8. **Late results and empty recaps.** CHARM first discusses its perfect-tagger ceilings in the conclusions. TIME recaps its resonance results without a number, in the passive (§VI ¶4).
9. **Hidden answers.** CHARM's Sec. IV runs 15 paragraphs without subsections, with the answer in ¶12. CHARM App. E and TRACK Apps. A, C, D and E are never cited.
10. **Detours.** TIME's mechanism paragraph ends on a tangent that never returns (§I ¶4). HNL's inventory of ATLAS upgrades (§VII A) and TIME's fine-tuning discussion (§II) feed no result.
