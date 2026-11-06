# Sentences and words

Read this file when you draft or revise sentences: their shape and length, names and definitions, voice and tense, and the wording of results and hedges. Check a finished draft against the norms and the revision pass (T6).

Paper tags: TOP = Tong, Corcoran, Fieg, Fenton, Whiteson, "New Physics in Single Resonant Top Quarks", arXiv:2311.00121 (6 pp); CHARM = Whiteson, "The era of charmed resonance searches at the LHC", arXiv:2609.32054 (12 pp); TIME = Fieg, Fox, Zhang, Ghosh, Varada, Whiteson, "Time-dependent signals of new physics at the LHC", arXiv:2605.11071 (12 pp); HNL = Feng, Hewitt, La Rocco, Whiteson, "Characterizing Heavy Neutral Leptons: Measuring Parameters, Discriminating Majorana versus Dirac, and Using FASER2 as a Trigger for ATLAS", arXiv:2510.16107 (15 pp); TRACK = Miller et al. (incl. Baldi, Whiteson), "Fast and Precise Track Fitting with Machine Learning", arXiv:2505.02937 (19 pp).

**Conventions.** Quotes are verbatim; tags give paper, section and paragraph (¶), and s is an abstract sentence. Invented examples (italics, after *Before:* and *After:*) follow one made-up study, a muon-spectrometer trigger for long-lived particles. k/5 counts papers. Counts cover the prose (985 sentences, 25,027 words), not the captions, unless stated. Related files: story-and-structure.md, layering-and-flow.md, figures-and-evidence.md. The *After* sentences show the target form and assume the author supplied every fact in them; their numbers are made up. When you edit a real draft, take every fact and number from the author's material, and mark anything missing with a placeholder such as [baseline?] instead of inventing it.

**Corpus norms.** Targets, not limits. Per-paper values are in the order TOP, CHARM, TIME, HNL, TRACK.

| Measure | Corpus | Per paper |
|---|---|---|
| Median sentence | 23 words | 22, 23, 25, 26, 22 |
| Sentences over 40 words | 11% | 5, 12, 10, 18, 6% |
| Sentences of 12 words or fewer | 11% | 13, 14, 7, 10, 12% |
| Main verb, median position | word 4 after a subject, 7 after a fronted phrase | 3–4 and 6–7.5 |
| *we/our/us* per 1,000 words | 13.6 (captions 2.4) | 12, 13, 12, 18, 12 |
| Sentences with a passive | 35% (bodies 40%, abstracts 18%) | 46, 30, 43, 35, 26% |
| Hedges per 1,000 words | 3.8 (intensifiers 2.1) | 2.5, 2.1, 3.9, 6.5, 2.7 |

## Contents

- SENTENCES-1. Known subject, early verb, new point last
- SENTENCES-2. One claim per sentence, and marked order when long
- SENTENCES-3. Logic in plain words
- SENTENCES-4. One name per object
- SENTENCES-5. Plain verbs, everyday words, no filler
- SENTENCES-6. Terms, symbols and tools defined at first use
- SENTENCES-7. Results with number, unit, baseline and condition
- SENTENCES-8. Calibration by scope, not by hedges or praise
- SENTENCES-9. *We* for choices, the passive for settings
- SENTENCES-10. A tense for each status
- Templates; Corpus slips to avoid

### SENTENCES-1. Known subject, early verb, new point last

**Rule.** Open with a short subject the reader already has: the object just named, a summary noun (*These shortcomings*) or the case in hand. Reach the main verb by about word 5, and end on the new point. Put a needed frame (a case, a purpose, a condition) first, in about five words.

**Why it works.** Each sentence attaches to the last before anything new arrives.

**Prevalence.** 5/5, measured (norms). *This*, *These* or *Such* opens 74 sentences. Locations: TOP tγ mode ¶2, CHARM §IV ¶1, TIME §III.A ¶8, HNL §I ¶1, TRACK §I ¶2.

**Exemplars.**
- "These shortcomings point toward the need for physics beyond the SM (BSM)." [HNL §I ¶1]: a summary noun picks up the list; the new idea comes last.
- "With a model of the jet flavor and momenta in each bin, predictions of the tagged spectrum require a description of the tagging performance." [CHARM §IV ¶1]: what is in hand, then what is missing.

**Draft violation and fix.**
- Before: *Because of the high Run 3 pileup and a trigger designed for prompt muons, the real-time selection of decays far from the beam line is difficult.*
- After: *Decays far from the beam line are hard to select in real time. Run 3 pileup is high, and the trigger was designed for prompt muons.*

**Boundaries.** HNL and TIME front phrases most (42% and 37% of sentences) to walk through cases, but keep them short. HNL's 84-word sentence reaches its verb at word 21 (§I ¶5). Never put a display between subject and verb (CHARM §II ¶2); for pick-ups between sentences, see layering-and-flow.md.

### SENTENCES-2. One claim per sentence, and marked order when long

**Rule.** Make one claim per sentence, with at most one qualifier: a reason, a condition or a consequence. Aim for a median of 20–25 words, let one sentence in ten pass 40, and give a single fact a sentence of 12 words or fewer. When a sentence must be long, order it frame, claim, number, condition, and mark its parts: (i), (ii) for a list, *respectively* for pairs, one semicolon between clauses of the same shape. Split anything over 50 words that is not a marked list or a display.

**Why it works.** A reader holds one claim and one qualifier at a time; markers show where the parts of a long sentence end.

**Prevalence.** 5/5, measured (norms). Just 41 sentences pass 50 words, 11 of them with a display. Semicolons occur in all five (54; CHARM 24), *respectively* 11 times (HNL 9), numbered lists only in CHARM (weaker evidence: 1/5). Locations: TOP Discussion ¶1, CHARM §I ¶5, TIME §IV.C ¶2, HNL §III ¶7, TRACK abstract s2.

**Exemplars.**
- "The T mass resolution is similar to that in the hadronic mode, as the lepton is well measured but the neutrino is unmeasured." [TOP Discussion ¶1]: a claim and one reason.
- "Sidebands in mass require selection of the signal region in advance, or scanning several regions; sidebands in time similarly require advance knowledge of the time dependence, or scanning." [TIME §IV.C ¶2]: two mirrored clauses around one semicolon.

**Draft violation and fix.**
- Before: *The trigger keeps 31% of decays at 1–5 m and the rate increases by 4 kHz and it needs a new calibration, and the results are in Fig. 4.*
- After: *The trigger keeps 31% of decays at 1–5 m but adds 4 kHz to the rate (Fig. 4). It also needs a new calibration.*

**Boundaries.** Summaries run longer (HNL's conclusions: median 32 words); keep them in linear order. Markers cannot rescue an overloaded sentence (CHARM §IV ¶4: 57 words, three semicolons). Avoid dashes, and keep paired parentheses (*X (Y) for A (B)*) to line styles in captions. A short sentence must say something: TRACK ends App. B with *See Tab IV.*

### SENTENCES-3. Logic in plain words

**Rule.** Mark each cause-and-effect link with one plain word (*because*, *due to*, *so*, *therefore*, *implies*, *requiring*). For a result, give the claim first and the cause after. Write a contrast as two clauses of the same shape, joined by *but*, *while* or a semicolon, so only the contrasted words differ.

**Why it works.** The reader follows the physics one link at a time, and the grammar does the comparing.

**Prevalence.** 5/5: *due to* 23, *because* 13, *therefore* 13, *so* 9; *but* 51, *while* 24, *rather than* 13. Locations: TOP tγ mode ¶2, CHARM §IV ¶14, TIME §I ¶4, HNL §III ¶7, TRACK §V ¶4.

**Exemplars.**
- "A larger Uµ implies a shorter HNL lifetime, requiring the HNLs to have higher energies to reach FASER2 before decaying." [HNL §III ¶7]: three links, two plain words.
- "Here, the LS method fails to provide an unbiased estimate, because its assumed Gaussian noise model does not accurately describe the data." [TRACK §V ¶4]: the result, then its cause.
- "The two non-tagged jets correspond to the W boson, and the three jets together correspond to the top quark." [TOP tγ mode ¶2]: one verb twice, so the reader can draw the decay.

**Draft violation and fix.**
- Before: *At high pileup the occupancy is higher and the efficiency is lower, and at low pileup it is better.*
- After: *At high pileup, more hits overlap, so the trigger keeps 25% of decays; at low pileup, it keeps 31%.*

**Boundaries.** Use the word that the logic needs (slip 7). Keep twin statements in one form and one unit: "Events with mT less than 200 are rejected." [TOP tγ mode ¶2] has no GeV, but its twin in the tj section does.

### SENTENCES-4. One name per object

**Rule.** Give each object, quantity, method and benchmark one name, with one spelling, one hyphenation and one symbol. Repeat it exactly, in captions and axis labels too. An acronym may replace its long form after the definition.

**Why it works.** A reader, above all a non-native one, takes a new word for a new object.

**Prevalence.** The central term is fixed in 4/5: *untagged* (CHARM), *time-dependent* (TIME), *HNL* (HNL), *track fitting* (TRACK); TOP's T has 8 names. Secondary terms drift in 5/5: CHARM's gain (*Sensitivity ratio G* in a caption), TIME's *time*, *timing* and *temporal information*, HNL's Dirac *model* and *hypothesis*, TRACK's four names for its targets.

**Exemplars.**
- "The underlying data is assumed to be Model 1, a Majorana HNL with mN = 1.84 GeV and Uµ = 0.0036." [HNL Fig. 6 caption]: a fixed label and its appositive, repeated wherever the case returns.
- "a search that uses timing information at the LHC can be up to a factor of two stronger compared to one that does not use time information" [TIME abstract s5]: two names for one input in one sentence.

**Draft violation and fix.**
- Before: *The muon-spectrometer trigger keeps 31% of decays. The MS-only algorithm runs in 2 µs, and our standalone selection rejects 99% of the background.*
- After: *The muon-spectrometer trigger keeps 31% of decays. It runs in 2 µs and rejects 99% of the background.*

**Boundaries.** Synonyms belong only where a paper maps the field's names onto its own (CHARM's *flavor-blind*). Hyphenate the modifier (*time-dependent signal*), not the noun phrase (*the time dependence*). Give a number one form (HNL writes 2, 2.0 and 2.00 GeV). For names in the front matter, see STORY-1 in story-and-structure.md.

### SENTENCES-5. Plain verbs, everyday words, no filler

**Rule.** Make a concrete object the subject and put the action in a plain verb (*use*, *show*, *find*, *measure*), not in *utilize*, *leverage* or a noun (*requires application of*). Say the core idea in everyday words, with at most one image, glossed at once; keep technical terms for the method. Delete phrases that announce (*it is worth noting that*, *in order to*), and write *allows*, not *allows for*.

**Why it works.** Plain words are read fastest and survive translation.

**Prevalence.** 5/5, measured. Plain verb forms outnumber inflated ones 462 to 5, and *facilitate* and *delve* never occur. *In order to* appears 3 times; the tic is *allow(s) for*, about 20 times. Everyday framing words: TOP *discovery window*, CHARM *break-even*, TIME *handle*, HNL *cradle to grave*, TRACK *follow the hits*.

**Exemplars.**
- "To predict the tagged dijet mass spectrum from the untagged spectrum requires application of the tagging efficiency to the jets." [CHARM §III ¶1]: the action hidden in a noun; a later section writes *we apply the efficiencies*.
- "However, new physics with a time variation would provide an additional handle to separate signal from background." [TIME abstract s3]: the method in one everyday noun.

**Draft violation and fix.**
- Before: *In order to facilitate the identification of displaced decays, we leverage the exploitation of the absence of inner-detector tracks.*
- After: *A long-lived particle leaves no inner-detector track, so we select muons that appear only in the spectrometer.*

**Boundaries.** Technical nouns are not filler (*production*, *sensitivity*). *Of course* is a concession when its answer follows (HNL §I ¶6), and filler when none does (CHARM App. B ¶4). In the method, the technical term is the plain word: "using a profile likelihood ratio [31] with the CLs technique [32, 33]" [TOP Stat. Analysis].

### SENTENCES-6. Terms, symbols and tools defined at first use

**Rule.** Define a term where it first appears, in apposition (*X, the Y of Z*) or as *Long Form (ACR)*, plain description first. Bring each symbol and tool with a noun that says what it is (*the gain G*, *the GN2 tagger*). Gloss a display's symbols with *where ...* or *Here, X is ...*. Say what a large or small value means. Never open a sentence with a symbol.

**Why it works.** The reader never meets a word they cannot interpret.

**Prevalence.** 5/5. *Long Form (ACR)*: HNL 21, TIME 4, TRACK 3, TOP 1, CHARM 1; *we define* occurs twice, so apposition does the work. *where* follows 14 of 34 displays. Tools carry a type noun in all five: TOP's *CLs technique*, CHARM's *GN2 tagger*, TIME's *CATHODE method*, HNL's *FASER2 experiment*, TRACK's *L-BFGS-B algorithm*. No sentence opens with a symbol.

**Exemplars.**
- "A fairly minimal way to extend the SM is to add sterile neutrinos, fermionic gauge eigenstates with no SM gauge quantum numbers." [HNL §I ¶2]: a new object, glossed in apposition.
- "A value of G > 1 indicates a gain, where the improved (smaller) limit ... overcomes the cost of the tagging efficiency." [CHARM §IV]: what a value means, and which direction is better.

**Draft violation and fix.**
- Before: *We apply the MS-BDT to all events with a good PV, and R is defined in Section 5.*
- After: *We classify each candidate with a boosted decision tree (BDT). Its score R runs from 0 to 1, and R > 0.8 selects signal.*

**Boundaries.** Most papers leave field names (LHC, ATLAS, QCD) undefined; expand anything a neighboring field might not know. Define in the body even if the abstract used the term. Never give a symbol two meanings (slip 3). For limits, write *stronger* or *weaker*, not *higher*.

### SENTENCES-7. Results with number, unit, baseline and condition

**Rule.** State a result in one sentence: the claim, the number with its unit and CL or uncertainty, the baseline, and the condition. Give a comparison as a factor (*a factor of N*, *N times as ... as*) or a pair of values, never as *much better*. Give each number one form: one word or symbol for an approximation, ± for an uncertainty.

**Why it works.** A reader who quotes the sentence alone quotes it correctly.

**Prevalence.** 5/5, measured: 108 percentages, 34 *N% CL*, 18 values with ±, 13 *a factor of N* and 5 *N times*. Projections say *expected* in all four phenomenology papers. Locations: TOP Discussion ¶1, CHARM §IV ¶15, TIME §III.A ¶8, HNL §V ¶3, TRACK §V ¶2.

**Exemplars.**
- "The NN is able to predict track parameters at a speed of 2.08 × 10−4 s/track using a batch size of 100,000, while the LS method predicts tracks at a speed of 0.268 s/track, a relative factor of over 1,000." [TRACK §V ¶2]: number, unit, condition, baseline, factor.
- "We find that FASER2 has the ability to measure mN to about 2 MeV (a fractional uncertainty of 0.1%)" [HNL §V ¶3]: the absolute and the relative value.

**Draft violation and fix.**
- Before: *Our trigger shows a significant improvement in sensitivity compared to previous approaches, as can be seen in Fig. 6.*
- After: *For decay lengths of 1–5 m, the new trigger strengthens the expected limit by 40% over the standard muon trigger (Fig. 6).*

**Boundaries.** The condition may come first or last, but must survive into the abstract (slip 4; STORY-8 in story-and-structure.md). *Up to* needs the condition for the maximum. Pick one style for approximations (HNL *approximately*, TIME ≈).

### SENTENCES-8. Calibration by scope, not by hedges or praise

**Rule.** Put *may*, *could* and *likely* on physics, extrapolations and future work. State a computed number flatly; for a projection, use *can* or *would* with *expected*. Hedge the reading of a number (*suggests*), not the number. Bound a result with a scope clause, and label each simplification with its direction (*conservatively*). State a weak result flatly, then explain it. Praise only by comparison with a baseline.

**Why it works.** The reader can tell what was shown from what is expected, and can check a comparison.

**Prevalence.** 5/5, measured. Only 6 of 68 modal hedges touch a paper's own result, and the CHARM and TIME abstracts have no intensifier. Scope clauses: TOP abstract s3, CHARM abstract s5, TIME §VI ¶2, HNL §I ¶5, TRACK abstract s10. Projections take *can* or *would*: HNL abstract s4, TIME abstract s5, CHARM §V ¶4. Weak results stated plainly: TOP Models ¶4, CHARM §V ¶3, TIME §IV.B ¶5, HNL §VI ¶1, TRACK App. D.

**Exemplars.**
- "we expect that FASER2 would only favor the Majorana model over the Dirac model at 87.8% CL (1.2σ)" [HNL §VI ¶1]: the weak number, flat; the next paragraph opens *To understand this surprising result*.
- "the NN matches the performance of the idealized LS method, which suggests that it is approaching the optimal precision." [TRACK §V ¶3]: the observation flat, its reading hedged.
- "Up to systematic effects, the SM background will be time-invariant." [TIME §VI ¶2]: the premise, with its exception first.

**Draft violation and fix.**
- Before: *Our results may potentially suggest that the new trigger could possibly improve the sensitivity by roughly about 40%, a remarkable result.*
- After: *In our simulation, the new trigger strengthens the expected limit by 40%. With a full detector simulation, the gain would likely be smaller.*

**Boundaries.** Use one hedge, never two. A status opener must be true: *As expected* helps, *Trivially* misfires (slip 6). Keep *significantly* for statistics. Do not soften the abstract: HNL's *somewhat less precise* hides a coupling uncertainty that grows from 3% to 25%. Match the verb to the number (slip 5). For assumptions and limitations, see figures-and-evidence.md.

### SENTENCES-9. *We* for choices, the passive for settings

**Rule.** Write *we* and an active verb for what the authors chose, assumed or found, purpose first: *To [purpose], we [verb]*. Record a tool and its settings in the passive, with the tool in a *with* phrase. A result may take *we find* or the measured quantity as its subject. Never write *It was found that*.

**Why it works.** The reader can tell decisions a referee may question from settings anyone would reproduce.

**Prevalence.** 5/5 (norms). *To [purpose], we [verb]* opens 16 sentences (TOP 2, CHARM 4, TIME 1, HNL 4, TRACK 5). Setup takes both voices in all five: *We use* (TOP), *We fit* (CHARM), *we generate* (TIME, TRACK), *we simulate* (HNL), beside *is simulated with*. No paper writes *it is found* or *it was shown*.

**Exemplars.**
- "To predict the charm-tagged spectra, we apply the efficiencies of the GN2 charm single-jet tagger [6]" [CHARM §IV]: purpose, then the authors' action.
- "The detector response is simulated with Delphes v3.5.0" [TOP Exp. Sens. ¶2]: a setting; the tool matters, not the actor.

**Draft violation and fix.**
- Before: *It was decided to require at least three segments, and it was found that the background is reduced by 90%.*
- After: *To suppress noise, we require at least three segments, which removes 90% of the background.*

**Boundaries.** A choice can carry its rejected option and its reason (CHARM §III ¶3; T3). Own an assumption with its direction: *We conservatively assume* (HNL §VII.B ¶1). Captions take almost no *we* (8 tokens in 3,301 words); 64 of 67 open with a noun phrase naming the plot (figures-and-evidence.md).

### SENTENCES-10. A tense for each status

**Rule.** Use the present for what the paper does and finds, and for what a figure shows. Use the present perfect for the state of the field and for the recap. Use the simple past for one completed study by a named group, and for a test run once. Use *will* for predictions.

**Why it works.** A change of tense then signals a change of status, not noise.

**Prevalence.** 5/5. About 12 of 283 *we* tokens take the past, 8 of them in HNL's conclusions. The field takes the present perfect in all five, from TOP's *has not been explored* to TRACK's *has received comparatively little attention*. A named prior study takes the past in TOP, TIME and CHARM.

**Exemplars.**
- "ATLAS studied the tγ final state [14], but did not examine the invariant mass of the system." [TOP Intro ¶4]: one completed study, in the past.
- "We find tighter limits than those placed on models in which the signal is uniform in time." [TIME §III intro]: the result, in the present.

**Draft violation and fix.**
- Before: *In this work we studied a muon-spectrometer trigger. We find that the efficiency was 31%, and we will show that it improved the limits.*
- After: *In this work, we study a muon-spectrometer trigger. It keeps 31% of decays at 1–5 m and strengthens the expected limit by 40%.*

**Boundaries.** HNL's conclusions introduce results with both *we have found* and *we found*; pick one form per section. An option tried and dropped takes the past: "Regularization techniques ... reduced performance, and were not used." [TRACK §IV-NN ¶3]

## Templates

**T1. Result.** `[For/At case], [quantity] [is / improves by] [number unit] [at N% CL | ± unc.] [compared to] [baseline][, a factor of N].`

**T2. Mechanism.** `A larger [X] implies [Y], requiring [Z].` / `[Result], because [cause].`

**T3. Choices and settings.** `To [purpose], we [verb] [object].` / `We [choose X] rather than [Y], as [reason].` / `[Sample] is [simulated] with [tool, version] [ref].`

**T4. Definitions.** `[term], the [plain description]` / `the [noun] [symbol]` / `..., where [symbol] is the [noun].` / `A value of [symbol] > [x] indicates [meaning].`

**T5. Scope and weak results.** `In the [simulated] setting described here, [result].` / `[Result], provided [condition].` / `With [current condition], [method] would only [favor X] at [number].` Then the reason, then the improved case (HNL §VI).

**T6. Revision pass.**
1. Length: median 20–25 words; one in ten over 40; none over 50 but marked lists and displays.
2. Shape: known subject, verb by word 5, new point last; one claim, one qualifier.
3. Logic: a plain word per causal link; mirrored clauses for contrasts.
4. Names: one form per key term, in text, captions and axis labels.
5. Words: no *utilize*, *leverage*, *it is worth noting that*, *in order to*, *allows for*.
6. Definitions: each acronym, symbol and tool at first use; one meaning per symbol.
7. Numbers: unit, CL or ±, baseline, condition; the text matches the figure.
8. Calibration and voice: no hedge on a computed number; *To [purpose], we* for choices; present tense for claims.

## Corpus slips to avoid

1. **Overlong sentences that stack clauses.** TOP Intro ¶3 (67 words, with a vague *this* and *it*), HNL §I ¶5 (84), TIME §III.A ¶8 (69), CHARM §IV ¶5 (63), TRACK §VII (64).
2. **Wrong or drifting names.** "the reconstructed mass of the hypothetical T boson" [TOP Stat. Analysis], for a fermion. TRACK's committee of experts is also a mixture of experts.
3. **Undefined terms and overloaded symbols.** TRACK never expands *LS*, and TOP uses mT before defining it. TIME's α names two things, and its µ three.
4. **Numbers that lose their condition or drift.** "the Dirac fermion hypothesis can be rejected at 99.8% CL" [HNL abstract s4] needs a 5% flux uncertainty; today's 60% gives 87.8% CL. TRACK's speed gain is *1,000*, *more than 1,000* and *over 1,000* times.
5. **Words that do not fit the number.** "the Dirac hypothesis can be rejected at 69.2% CL (0.5σ)" [HNL Fig. 7 caption]; "changing the coupling by a factor of 10%" [HNL §III ¶8]; a *variance* that is a standard deviation (HNL §IV.A ¶3).
6. **Promotional and dismissive words.** TRACK's *novel*, in its abstract; TIME's *Trivially*, on a real effect (§V ¶2).
7. **Grammar slips.** "Our estimation of the flavor fractions and efficiencies as well as their uncertainties are discussed in detail in the next section." [CHARM §II ¶5] (agreement); "This can calculated analytically using the same time-dependence assumed above" [TIME §IV.A ¶1] (a missing *be*); *Alternatively* for *In contrast* (TRACK App. D).
8. **Captions, units and spelling.** "for hadronic (top) and leptonic (center) decays" [TOP Fig. 3 caption] names a *center* panel in a two-panel figure. TOP's mT cut of *200* has no unit. CHARM mixes *flavour* with *flavor*.
