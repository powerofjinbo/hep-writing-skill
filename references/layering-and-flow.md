# Layering and flow

Read this file when you plan, draft or revise the body of a paper (the sections between introduction and conclusions, and the appendices): the order of cases, how sections and paragraphs open and close, how sentences link, and how the text points to figures and equations.

Paper tags: TOP = Tong, Corcoran, Fieg, Fenton, Whiteson, "New Physics in Single Resonant Top Quarks", arXiv:2311.00121 (6 pp); CHARM = Whiteson, "The era of charmed resonance searches at the LHC", arXiv:2609.32054 (12 pp); TIME = Fieg, Fox, Zhang, Ghosh, Varada, Whiteson, "Time-dependent signals of new physics at the LHC", arXiv:2605.11071 (12 pp); HNL = Feng, Hewitt, La Rocco, Whiteson, "Characterizing Heavy Neutral Leptons: Measuring Parameters, Discriminating Majorana versus Dirac, and Using FASER2 as a Trigger for ATLAS", arXiv:2510.16107 (15 pp); TRACK = Miller et al. (incl. Baldi, Whiteson), "Fast and Precise Track Fitting with Machine Learning", arXiv:2505.02937 (19 pp).

**Conventions.** Quotes are verbatim, tagged by paper, section and paragraph (¶). Invented examples (italics, after *Before:* and *After:*) use the made-up study of story-and-structure.md, a muon-spectrometer trigger for long-lived particles. k/5 counts papers; *body* counts cover the 672 sentences between introduction and conclusions, plus appendices. STORY-6 in story-and-structure.md orders the whole body. The *After* sentences show the target form and assume the author supplied every fact in them; their numbers are made up. When you edit a real draft, take every fact and number from the author's material, and mark anything missing with a placeholder such as [baseline?] instead of inventing it.

**Contents.** FLOW-1 Map first; FLOW-2 Simple to hard; FLOW-3 Words first; FLOW-4 Section openers and closers; FLOW-5 Paragraphs; FLOW-6 Sentence links; FLOW-7 Cases first; FLOW-8 Usual way, cost, choice; FLOW-9 Expectation and diagnosis; FLOW-10 Justification; FLOW-11 References; FLOW-12 Known answer and benchmark; Templates; Corpus slips.

### FLOW-1. Give the map and the shared setup before the parts

**Rule.** Before the first step, show the whole: a count, a list, a master formula or a flowchart. State once what all branches share, then deliver the parts in the announced order.

**Why it works.** Each detail lands in a slot the reader already holds.

**Prevalence.** 5/5: CHARM §II (Eq. 1 and ingredients (i)–(iii), delivered in Secs. III–IV); HNL §III ¶4–¶6 (Fig. 2, then its boxes); TIME §IV ¶2–¶5 (three cases, then one shared simulation); TRACK §III–§IV (data once, then both fitters); TOP Exp. Sens. (shared selection, then the two modes).

**Exemplars.**
- "Predicting the charm-tagged fraction κ requires (i) a model of the flavor fractions of the QCD background" [CHARM §II ¶3]
- "For the first two considered cases of known and learned signal oscillation – Section IV A and Section IV B respectively – we generate" [TIME §IV ¶4]

**Draft violation and fix.**
- Before: *Vertices are built from spectrometer hits, the trigger is emulated, and later events are split by radius.*
- After: *The analysis has three steps: select events with a displaced vertex, predict the background from a control region, and fit the vertex radius.*

**Boundaries.** In a paragraph, the map is a count before a list (TRACK's five helix parameters). Give every multi-part section a lead sentence; HNL §IV has none.

### FLOW-2. Climb from the simple case to the hard one, and say what carries over

**Rule.** Order cases from best understood to hardest. Say why each new case is needed, name what it reuses, describe only what changes, and compare the result back.

**Why it works.** Each harder case answers a doubt the reader already has.

**Prevalence.** 5/5 order cases this way; 4/5 say why (not TOP), TIME §IV B and HNL §VII by naming the last case's limit. HNL Model 1 → Model 2 → FASER2 + ATLAS; TIME known → learned oscillation → sidebands in time; TRACK Gaussian → skewed noise; CHARM two-charm Z′ → one-charm T; TOP hadronic → leptonic. All five name the carry-over (HNL §VII ¶3; TIME §III B; CHARM §IV; TOP §tj ¶3; TRACK §VI).

**Exemplars.**
- "As noted in Sec. I, however, it is also possible to discover HNLs with far fewer events, and it is interesting to explore what can be done in this case." [HNL §VII ¶2]
- "Applying the same method and statistical analysis as done for Model 1, we find that for Model 2" [HNL §VII ¶3]

**Draft violation and fix.**
- Before: *Figure 5 shows the efficiency with 200 pileup events; the case without pileup is also shown.*
- After: *We first consider events without pileup. We then add the 200 pileup interactions of the HL-LHC and repeat the same selection; only the isolation cut changes.*

**Boundaries.** Give each case a heading that names it (TIME's *Known oscillation*, *Learned oscillation*).

### FLOW-3. Say it in words or a picture, then in symbols, then read the symbols back

**Rule.** Give each mechanism in a plain sentence or a schematic before its equation and its full test. Around each key display, say what it computes, define the symbols right after it, then say what values mean.

**Why it works.** The reader knows what the math is for, and a skimmer still gets its meaning.

**Prevalence.** 5/5, weakest in TOP. TRACK draws Fig. 1 before χ2hit; TIME states the mechanism in words (§I ¶4, §III lead) before Eq. (4); CHARM names *the crucial metric* in §II and reads G > 1 in §IV; HNL reads its Fig. 3 histograms before any fit, and the sign of λ after Eq. (13).

**Exemplars.**
- "While there is a simple analytical expression to map helical parameters to hits h(p̄) → x̄, the inverse function f (x̄) → p̄ has no simple closed-form expression; see Fig. 1." [TRACK §II ¶2]
- "A value of G > 1 indicates a gain" [CHARM §IV]

**Draft violation and fix.**
- Before: *We define q0 = −2 ln λ(0) and compute its distribution with pseudo-experiments.*
- After: *Signal vertices lie far from the beam line and background vertices do not, so the vertex radius separates them. We test this with q0 = −2 ln λ(0); a large q0 disfavors the background-only hypothesis.*

**Boundaries.** A standard formula needs only its *where* clause. Number every equation later text uses (CHARM's G has no number).

### FLOW-4. Enter each section with its job or a bridge; leave it on its payoff

**Rule.** Make the first sentence say what the section does (*In this section, we ...*; *To X, we Y*) or bridge from what the reader holds (*With X, Y requires Z*; *So far, ...*). After any context, mark the turn (*However, if*). End a results section on its number or its reason; a setup section may end on a specification, a pointer or a hand-off. Never end on a recap.

**Why it works.** The reader knows why the section exists and remembers its last sentence.

**Prevalence.** 5/5. First sentences of the 46 body units: purpose 14, context then turn 14, direct 10, bridge 8. Last sentences: verdict 8, number 7, pointer 6, caveat 5, reason 4, other 16, recap 0; 9 of the 12 main-text results units end on a number or its reason.

**Exemplars.**
- "With a model of the jet flavor and momenta in each bin, predictions of the tagged spectrum require a description of the tagging performance." [CHARM §IV ¶1]
- "Here, the improvement gained by using time information is larger for σα = 0.05 than σα = 0 because the sidebands in time allow for the background in the resonance region to be directly constrained." [TIME §IV.C] — its section's last sentence.

**Draft violation and fix.**
- Before: *Muons must have pT > 20 GeV [34]. ... In summary, this section described the selection.*
- After: *To keep only events the trigger records with full efficiency, we require a muon with pT > 20 GeV. ... The selection keeps 31% of decays between 1 and 5 m and 0.2% of the background.*

**Boundaries.** A setup section can end on the quantity its results will report (CHARM §II, *the crucial metric is their ratio*). Answer-first results leads are rarer (TIME §III, HNL §VI; weaker evidence: 2/5).

### FLOW-5. Give each paragraph one job: point first, payoff last

**Rule.** Open with the point or the link to the last paragraph, keep to one job, and end on the mechanism, the number, or a one-clause verdict on what the number shows. Never end on a summary.

**Why it works.** A reader who skims first sentences still follows the argument.

**Prevalence.** 5/5. Of 40 sampled paragraphs, 28 open on a claim or a transition, 19 end on a mechanism or a number, and 1 on a recap; most run 50–130 words. The verdict after a number recurs in four papers: TIME §IV C (*This demonstrates*), TRACK §V (*which suggests*), HNL §III (*suggesting that*), CHARM §IV (*even for the resonance with only a single charm leg*).

**Exemplars.**
- "The Z ′ resonance benefits from the additional charm, where the fraction of leading jets that are genuinely charm is roughly twice as high." [CHARM §IV]
- "This demonstrates the power of the low-signal-to-background regions to constrain uncertainty in the background model." [TIME §IV.C]

**Draft violation and fix.**
- Before: *In this paragraph we discuss the backgrounds. There are several. In summary, the background is important.*
- After: *Punch-through jets dominate the background, because hadrons that leak out of the calorimeter leave spectrometer hits. Cosmic muons add 10%, so even a 50% error on them moves the limit by under 5%.*

**Boundaries.** A method paragraph may end on its last specification (TOP's selections), and a signpost can stand alone (TOP Exp. Sens. ¶4). Split paragraphs with several jobs (slip 5).

### FLOW-6. Link sentences through their content; use few, plain connectors

**Rule.** Start a sentence with what the last one ended on: its key noun, or *This/These* plus a noun that names it. When the relation needs a word, use a plain one (table below). Add a point by stating it; open with *In addition* rarely, with *Moreover* or *Furthermore* almost never.

**Why it works.** The link sits in the words, so the rare connector carries real logic.

**Prevalence.** 5/5, in 672 body sentences: *This/These* + noun opens 22, a bare *This/These* + verb 16; *However* 19 (none in TRACK, which writes *by contrast* or *Here, instead*); *To* + verb 21; additive openers 15 (*In addition* 8, *Additionally* 5, *Moreover* 1, *Furthermore* 1); *Thus*, *Hence*, *Therefore*, *As a result* and *Consequently* 6, each closing a chain.

**Exemplars.**
- "These interaction terms allow for production of T via quark-gluon fusion" [TOP §Models ¶3]
- "The contours run diagonally across the plane, so the gain is set by the pairing of efficiency and mis-tag rate rather than by either alone." [CHARM §IV]

**Draft violation and fix.**
- Before: *Firstly, the timing resolution is 30 ps. Moreover, the efficiency is high. Furthermore, the fake rate is low. Thus, the detector is suitable.*
- After: *With a timing resolution of 30 ps, the spectrometer keeps 95% of signal hits and admits under 1% fakes, so it resolves the 2 ns delay of a slow particle.*

**Boundaries.** A bare *This* + verb suits the sentence just before; name the antecedent when it is a paragraph or a method. Pick up the exact term (slip 3).

### FLOW-7. Name the case first, and write sibling cases in one frame

**Rule.** When the argument runs over cases, regimes or models, open each sentence with its case. Write sibling units, from subsections to clauses, in one frame and one order.

**Why it works.** The reader knows the branch before the claim and compares siblings line by line.

**Prevalence.** 5/5; about one body sentence in eight opens with its case. TIME opens 17 body sentences with *For*, mostly a regime, walking Fig. 2 along its x-axis (§III A). TRACK §V *In the Gaussian*, *In the skewed*; HNL §II *In Model 1*, *In contrast, in Model 2*; CHARM §IV *For the Z′ ...; for the T ...*; TOP's four *In the [state] final state* paragraphs.

**Exemplars.**
- "In the Gaussian noise model, both methods show no bias, as expected" [TRACK §V ¶3] and "In the skewed noise model, the difference in the approaches becomes apparent." [TRACK §V ¶4]
- "Sidebands in mass require selection of the signal region in advance, or scanning several regions; sidebands in time similarly require advance knowledge of the time dependence, or scanning." [TIME §IV.C]

**Draft violation and fix.**
- Before: *The efficiency drops to 40%, which happens when the decay radius is above 3 m and pileup is high.*
- After: *For decay radii above 3 m at high pileup, the efficiency drops to 40%.*

**Boundaries.** Use one short label each time (*Model 1*, not also *the first benchmark*). Put text that twins share in the shared setup; TOP repeats one *pythia* sentence in both.

### FLOW-8. Give the usual way or the ideal case, its cost here, then your choice

**Rule.** Before your choice, state the usual practice, the ideal case or the default, fairly and with a citation; then its cost here in one concrete clause; then your choice (*Instead, we ...*; *Here, instead, ...*; *However, if ...*).

**Why it works.** The choice reads as the answer to a problem the reader has just seen.

**Prevalence.** 5/5, in four forms: practice, cost, alternative (TIME §IV A ¶2 and §IV C; TRACK §II ¶5–¶7); ideal case, complication, method (HNL §VII C); default, then the twist that opens the channel (TOP §Models ¶3–¶4); convention, flaw, kept for a stated reason (CHARM App. E).

**Exemplars.**
- "However, this sacrifices information, as removed signal events cannot contribute and removed background events cannot be used to profile nuisance parameters in the background model. Instead, we weight events by the LR" [TIME §IV.A ¶2]
- "The study above retains the cone-labeling scheme despite its lack of IRC safety, as the tagger efficiencies are only reported for this labeling." [CHARM App. E ¶2]

**Draft violation and fix.**
- Before: *We use vertex weights. Some analyses use cuts instead.*
- After: *A common approach is to cut on the vertex-quality score. However, a cut discards signal vertices that fail it and background vertices that constrain the nuisance parameters. Instead, we weight every vertex by its likelihood ratio.*

**Boundaries.** Credit the practice before its cost (TRACK lists the advantages of least squares first), and avoid straw men.

### FLOW-9. Read each result against the expectation; diagnose a weak one before the fix

**Rule.** Say whether each result matches what the mechanism predicts (*as expected*, with the reason). When a result is weak or surprising, say so, explain it at once, and let the diagnosis motivate the next step.

**Why it works.** Each number tests a mechanism, and a weak result becomes the reason for the fix.

**Prevalence.** Expectation 5/5: *as expected* 8 times in CHARM, TIME, HNL and TRACK; TOP explains its channel ranking by cause. Weak result, diagnosis, fix 4/5: HNL §VI (flux uncertainty, then better flux data); TIME §IV C (mass sidebands, then sidebands in time); TRACK §V ¶4 (a wrong noise model, then a learned one); CHARM §IV (today's tagger, then future taggers).

**Exemplars.**
- "To understand this surprising result, in the right panel of Fig. 4, we show that the Dirac model best-fit recreates the shape ... but overestimates the total event rate by a factor of 2." [HNL §VI]
- "This highlights the importance of constraining the background model uncertainty in the signal region." [TIME §IV.C]

**Draft violation and fix.**
- Before: *The efficiency is 85% in the barrel and 60% in the endcaps. We now add the timing layer.*
- After: *The efficiency is 85% in the barrel but 60% in the endcaps, where coarser segmentation merges nearby hits. A timing layer separates them and raises the endcap efficiency to 80%.*

**Boundaries.** *As expected* needs a stated expectation and a figure that shows it (slip 6); once per paragraph is enough (TRACK §V ¶3 has four).

### FLOW-10. Put the justification where the doubt arises

**Rule.** Give every cut, setting and simplification its reason in the same sentence (*To* + verb, *as*, *because*, *rather than*, *to be conservative*). Label each simplification and say which way it moves the result. Raise an obvious objection yourself (*Of course, ...*; *In practice, ...*) and answer it at once.

**Why it works.** No number looks arbitrary, and the referee's question is answered where it forms.

**Prevalence.** 5/5. *To* + verb opens 21 body sentences (four are TOP's *To satisfy typical trigger requirements*); *for simplicity* appears 5 times in four papers; every paper fences its scope (TOP *Though we do not study it here*; TRACK *For this proof-of-concept study*); objections meet *Of course* (TOP, CHARM, TRACK) or *In practice* (TIME, TRACK).

**Exemplars.**
- "We measure the joint dijet composition rather than the single-jet, as a tag may be applied to either jet." [CHARM §III]
- "In practice, this is not a limitation: a coherence length smaller than the vertex resolution implies TPeriod ≲ 10−14 s" [TIME §II]

**Draft violation and fix.**
- Before: *We require ΔR > 0.4 between the muon and the nearest jet. We assume the cosmic-muon rate is flat in time.*
- After: *We require ΔR > 0.4 between the muon and the nearest jet, so that punch-through does not fake an isolated muon. For simplicity, we take the cosmic-muon rate as flat in time; a daily variation would shift the background by under 2%.*

**Boundaries.** A standard setting needs only its citation. Skip concessions nobody doubted (CHARM App. B's *Of course, a mismodeled flavor composition has an impact*).

### FLOW-11. Make every reference findable, readable and kept

**Rule.** Point to a figure with the claim first and the panel last, then say what to see in it. Give back-references a noun and an address (*the test statistic λ defined in Eq. (13)*). Name each quantity or borrowed tool once, with a gloss of its job, and never rename it. Deliver every forward reference.

**Why it works.** The reader knows what to look for and finds earlier objects without searching.

**Prevalence.** 5/5. Of 64 body figure references, 39 put the quantity or the claim before the pointer and 1 is a bare parenthetical; all but TOP read their figures. TIME and HNL cite sections and equations by number; TOP, CHARM and TRACK name the object. Four papers gloss a borrowed tool (CATHODE, autoencoders, the Asimov dataset, IFN). TIME parks a caveat in §IV B and returns to it in §V.

**Exemplars.**
- "But when the background uncertainty is increased, the sensitivity remains robust, only weakening slightly to Ns < 120 events; see the blue curve in the upper panel of Fig. 7." [TIME §IV.C]
- "The resulting background-muon distribution in (η, pT ) is shown in Fig. 8, peaking at lower η values." [HNL §VII.B]

**Draft violation and fix.**
- Before: *As mentioned before, the results are shown in Figure 6 (see also Figure 7).*
- After: *The new trigger keeps three times more decays beyond 3 m than the standard one; see the red curve in the lower panel of Fig. 6. Below 1 m the curves meet, because both triggers then rely on the inner tracker.*

**Boundaries.** A bare *as above* is fine one paragraph back. Cite every figure in number order, in one form (*Fig.* inside a sentence, *Figure* at its start).

### FLOW-12. Check a known answer, work one benchmark, then generalize; keep details in appendices

**Rule.** Before the new result, show in one main-text sentence, with a number, that the machinery reproduces a known answer. Work one benchmark in full before the scan or a second benchmark. Move validations and variations to appendices, each with its verdict beside the pointer.

**Why it works.** Trust is earned on a known case, and one point is understood before a hundred.

**Prevalence.** Known answer 4/5 (not TOP): CHARM's three checks; TRACK's Gaussian case, where least squares is optimal; HNL's Asimov goodness of fit; TIME's rebuilt ATLAS baseline, without a closeness number. Benchmark first 4/5: TOP (Table I, then Fig. 5); TIME (one period, then the scan); HNL (Model 1, then Model 2); CHARM (mass at today's tagger, taggers at 2 TeV); TRACK does not. Clean main line 5/5; verdict at the pointer 2/5 (CHARM Apps. A, B, D; TRACK App. B).

**Exemplars.**
- "In the Gaussian noise model, both methods show no bias, as expected, and the NN matches the performance of the idealized LS method, which suggests that it is approaching the optimal precision." [TRACK §V ¶3]
- "several variations on these assumptions are also explored in Appendix D, and do not qualitatively impact the conclusions." [CHARM §IV]

**Draft violation and fix.**
- Before: *Figure 6 shows the limits for masses from 200 GeV to 3 TeV and decay lengths from 1 mm to 10 m.*
- After: *Our emulation reproduces the published 2018 trigger efficiency to within 4%; see Appendix A. For a 1 TeV particle with a 1 m decay length, Table II gives the yields; Figure 6 then scans the mass at that decay length.*

**Boundaries.** Say what a check does not validate (CHARM App. B: *validates only our simulation against ATLAS, not against the data*). Flag a lucky benchmark: "but this would require a lucky coincidence in the actual experiment" [TIME §IV.B].

## Templates

- **Carry-over.** `Applying the same [method] as for [case 1], we find [result], [degraded / improved] relative to [case 1].`
- **Section entrance.** `With [what is built], [next step] requires [what is missing].` or `So far, we have [done X]. In the rest of this section, we [Y].`
- **Section exit.** `In the following, we investigate whether [claim] holds up under [stronger test].`
- **Usual way.** `A common approach to [task] is [X]. However, [X] [cost]. Instead, we [Y].`
- **Weak result.** `To understand this [weak / surprising] result, [panel] shows that [cause]. This highlights [need]. With [fix], [better result].`
- **Figure.** `[Claim with number]; see the [curve] in the [panel] of Fig. N. [Feature] indicates [meaning].`

| Job | Use | Avoid |
|---|---|---|
| Turn | *However,* first; *but*, *while*, *rather than*, *instead* inside | *On the other hand* with no first hand |
| Consequence | *so*, mid-sentence *therefore*, *, which ...* | *Thus,* or *Hence,* sentence after sentence |
| Purpose | *To* + verb | *In order to* |
| Addition | a new subject; *In addition* rarely | *Moreover*, *Furthermore*, *Additionally* chains |
| Sequence | *First / Then / Finally*, all present | *Firstly*; a *First* with no second |

## Corpus slips to avoid

1. **Promises and orphans.** TOP's roadmap promises "results in terms of the theoretical parameters" [TOP Intro ¶6] that never appear. CHARM App. E, TRACK Apps. C–E and TRACK Figs. 11 and 13–18 are never cited.
2. **A wrong pointer.** "see Tab. VI for details" [TRACK §III] should point to Table I.
3. **A back-reference to nothing.** "In light of these constraints" [TOP §Models ¶2] follows a sentence about mixing; CHARM App. D's *the pessimistic one* names no scenario.
4. **Sections that end on an aside.** TIME §III A and §V end on side remarks (*Moreover ...*, *Note that ...*).
5. **Units with several jobs.** One 358-word TIME §III A paragraph covers curves, phase, two regimes and the background uncertainty; HNL §VII C fits a model, two equations, three figures and two results in one paragraph; CHARM §IV has no subsections, so its main result arrives late.
6. **An expectation broader than the figure.** "The charm categories have larger fmulti than bottom ones, as expected" [CHARM App. B], yet in Fig. 8 the cc charm jets lie below the bℓ and cb bottom jets in every shared bin.
7. **Wrong or weak connectors.** "Alternatively, the LS model experiences decreases" [TRACK App. D] means *In contrast*; "Trivially, the bunch spacing of ≈ 25 ns produce events" [TIME §V] is dismissive and ungrammatical.
8. **Names that drift or double.** TRACK's *committee-of-experts* becomes *mixture-of-experts* in one subsection; TIME's learned score reuses LR(t), the symbol of the analytic ratio.
9. **Small slips.** TOP heads its twin subsections *tγ mode* and *tj final state*, so the frame breaks at the headings; it writes *Fig 2*, *Fig. 3* and *Figure 5*, cites Fig. 2 before Fig. 1, and never says what to see in Figs. 3–4. HNL §VII ¶1 recaps twice in two sentences. CHARM §II ¶2 splits a subject from its verb with Eq. (1).
