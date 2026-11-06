# Figures and evidence

Read this file when you plan, make or caption figures and tables, write the sentences that point to them, or report a result with its baseline, bound, assumptions and limitations. Run template T3 on every figure before submission.

Paper tags: TOP = Tong, Corcoran, Fieg, Fenton, Whiteson, "New Physics in Single Resonant Top Quarks", arXiv:2311.00121 (6 pp); CHARM = Whiteson, "The era of charmed resonance searches at the LHC", arXiv:2609.32054 (12 pp); TIME = Fieg, Fox, Zhang, Ghosh, Varada, Whiteson, "Time-dependent signals of new physics at the LHC", arXiv:2605.11071 (12 pp); HNL = Feng, Hewitt, La Rocco, Whiteson, "Characterizing Heavy Neutral Leptons: Measuring Parameters, Discriminating Majorana versus Dirac, and Using FASER2 as a Trigger for ATLAS", arXiv:2510.16107 (15 pp); TRACK = Miller et al. (incl. Baldi, Whiteson), "Fast and Precise Track Fitting with Machine Learning", arXiv:2505.02937 (19 pp).

**Conventions.** Quotes are verbatim; text printed inside a figure is in `code font`. Invented examples (italics, after *Before:* and *After:*) use the muon-spectrometer trigger study of story-and-structure.md. k/5 counts papers. Related: FLOW-9 to FLOW-12, STORY-8, STORY-10. The *After* sentences show the target form and assume the author supplied every fact in them; their numbers are made up. When you edit a real draft, take every fact and number from the author's material, and mark anything missing with a placeholder such as [baseline?] instead of inventing it.

**Contents.** EVIDENCE-1 Storyline; 2 Point; 3 Captions; 4 Mechanism; 5 Key number; 6 Baseline; 7 Bound; 8 Verbs; 9 Assumptions; 10 Pairs; 11 Vocabulary; 12 Uncertainty and tables; Templates; Corpus slips.

### EVIDENCE-1. Plan the figures as the storyline, and open with a picture of the idea

**Rule.** Before drafting, list the figures in reading order, each with the question it answers: the idea as a schematic, the inputs, one worked distribution, the result against its baseline, the plot that explains it, the checks.

**Why it works.** A reader who only looks at the figures still follows the argument.

**Prevalence.** The arc 5/5; a schematic first 4/5 (CHARM lets Eq. (1) carry the idea). TIME climbs from a known to a learned oscillation.

**Exemplars.**
- "The analytic helix function h(p̄) maps the parameters to the hits, while the unknown function f(x̄) maps the hits to the parameters." [TRACK Fig. 1 caption] The whole problem.
- "For Dirac HNLs, only the top process is allowed." [HNL Fig. 1 caption] The schematic carries the payoff.

**Draft violation and fix.**
- Before: *Figure 1 shows the trigger efficiency for five decay lengths.*
- After: *Figure 1 sketches one event: a scalar decays 3 m from the beam line, and its muons leave spectrometer hits but no inner-detector track.*

**Boundaries.** A letter can stop at the result (TOP); longer papers move checks to appendices (CHARM keeps 4 of 13 figures in the main text). Spend the schematic's color on the property the story turns on (the muon charge, HNL Fig. 1).

### EVIDENCE-2. Give every figure its point, at the pointer or in the caption

**Rule.** Cite a figure in a sentence that gives the claim first and the figure last, then say what to see (FLOW-11). If the text does not give the point, the caption must.

**Why it works.** The reader knows what the figure proves before looking.

**Prevalence.** Claim-first pointers 5/5; the figure is the subject in only 10 of 88 references. Caption takeaways: HNL 7 of 11; CHARM, TIME and TRACK a few. TOP fails both ways: "Limits as a function of the T mass are shown in Figure 5." [TOP Statistical Analysis]

**Exemplars.**
- "Our limits agree with the published results to within 10%, despite our simplified treatment of systematic uncertainties; see Fig. 5." [CHARM App. A] Finding, number, evidence.
- "The Dirac best-fit point recreates the signal shape well, but at the expense of a significantly larger event rate." [HNL Fig. 4 caption] The point, in the caption.

**Draft violation and fix.**
- Before: *Figure 9: Distributions of the test statistic under both hypotheses.*
- After: *Figure 9: Test statistic under the signal-plus-background (red) and background-only (black) hypotheses for a 1 TeV scalar with cτ = 1 m. The median signal experiment lies beyond 99% of background experiments.*

**Boundaries.** A neutral *X is shown in Fig. N* works if the reading follows at once (TRACK, Figs. 6–7). A caption takeaway carries its condition, as in HNL.

### EVIDENCE-3. Write each caption in a fixed order of jobs

**Rule.** Open with a noun phrase naming the quantity and its variable. Then give the conditions that set the plot apart (sample, benchmark, luminosity, working point), decode each mark right after its noun, and map the panels. End with the point and, if needed, one sentence on what could be misread.

**Why it works.** A reader who jumps to the figure needs no text.

**Prevalence.** Noun-phrase openings 5/5 (64 of 67 captions). Conditions restated: HNL 8 of 11, TOP 4 of 5, CHARM 6 of 13, TIME 3 of 7, TRACK 1 of 18. Keys after the noun: mainly CHARM and TIME. Panel maps 5/5. A guard against misreading 4/5 (not TOP).

**Exemplars.**
- "Top: Mass distribution of the signal (red) and background (black) before (solid) and after (dashed) weighting by the LR." [TIME Fig. 4 caption] Two factors, four parentheses.
- "The background is time-independent, wiggles are statistical." [TIME Fig. 3 caption] A false signal, stopped.

**Draft violation and fix.**
- Before: *Figure 5: Comparison of the results for the different configurations.*
- After: *Figure 5: Trigger efficiency versus decay radius for a 1 TeV scalar with Run 3 pileup, for the new trigger (red) and the standard trigger (black). Top: barrel; bottom: endcaps. The dip at 7 m is the gap between two muon stations.*

**Boundaries.** Repeat conditions across twin captions, not explanations. A caption is neither a section (TIME Fig. 2: about 340 words) nor a bare label (TRACK: 8 words for 25 panels). Mark what is published: "Open markers are the published anchor values." [CHARM Fig. 11 caption] (weaker evidence: 2/5).

### EVIDENCE-4. Show the distribution before the number, and the mechanism after it

**Rule.** Before a limit or an accuracy, show the distribution it comes from and name the feature that drives it. After the number, give its cause in its own sentence. Call a surprise a surprise, and show the plot that explains it.

**Why it works.** The number reads as a consequence of something seen.

**Prevalence.** 5/5: TOP Figs. 3–4 before Fig. 5; CHARM Fig. 2 before Fig. 3; TIME Fig. 4; HNL Figs. 3–4 before its tests, and Fig. 4 (right) for *this surprising result*; TRACK Fig. 10 before Fig. 11. The mechanism above the payoff in one figure: TIME, CHARM (weaker evidence: 2/5).

**Exemplars.**
- "the gluon jet from the T has a broader radiation pattern, with more energy falling outside of the cone, which translates into a longer low-mass tail and weaker sensitivity." [CHARM §IV ¶15] Cause, effect, observable.
- "Here, the LS method fails to provide an unbiased estimate, because its assumed Gaussian noise model does not accurately describe the data." [TRACK §V ¶4] A failure and its cause, in one sentence.

**Draft violation and fix.**
- Before: *The expected limit is 2.0 fb at 1 TeV (Fig. 8).*
- After: *Signal vertices cluster at radii of 4–7 m, where the punch-through background has fallen a hundredfold (Fig. 7). A fit to this distribution gives an expected limit of 2.0 fb (Fig. 8).*

**Boundaries.** One representative distribution is enough before a scan (TIME shows one period). The figure must show what it is cited for (slip 9).

### EVIDENCE-5. Read the key number into the text as a factor with a direction, per regime, with its condition

**Rule.** For each result figure, write in the text the number to remember, with its unit and condition. Give the comparison as a factor with a direction word (*a factor of 2 stronger*). When the gain changes along the axis, give one number per regime and say where and why it vanishes.

**Why it works.** The reader can quote it, and the direction word removes the doubt of a bare percent.

**Prevalence.** 5/5 (*factor of* 14 times; *N times as* in TOP and TRACK). Gaps in 4/5: CHARM's headline is only "a gain greater than 1" [CHARM §IV ¶13]; TIME's learned oscillation and TRACK's precision gain get no number; TOP never says where its limits cross theory.

**Exemplars.**
- "For 10^-4 ≲ TPeriod/month ≲ 36, ... the resulting improvement on Ns is a factor of about 1.6 over the time-independent analysis." [TIME §III A] Regime, factor, baseline.
- "Doubling the sensitivity of the untagged search requires a light-jet mis-tag rate of 0.016 at ϵc = 0.3, compared to 0.083 for the current tagger, a factor of 5" [CHARM §IV ¶16] Two values, then the factor.

**Draft violation and fix.**
- Before: *The new trigger improves the limit by 60%, as can be seen in Fig. 6.*
- After: *For decay lengths of 1–5 m, the new trigger lowers the expected limit by a factor of 2.5, from 5.0 to 2.0 fb (Fig. 6). Below 0.5 m the limits meet, because both triggers then use the inner tracker.*

**Boundaries.** Never mix factors and percents: TIME writes a factor of two and 50% stronger for the same ratio of about 0.5 (slip 3), and HNL writes "changing the coupling by a factor of 10%" [HNL §III]. The condition travels with the number (STORY-8).

### EVIDENCE-6. Build the baseline with your own machinery, draw it as the reference, and say which side wins

**Rule.** Compute the baseline with your own inputs, statistics and code, switching off only the new ingredient. Plot your result relative to it with a labeled line at 1, or draw it as a labeled reference, and say which side is a gain.

**Why it works.** Shared biases cancel, and the answer reads above or below one line.

**Prevalence.** Own baseline 4/5 (TOP uses theory curves): CHARM computes both limits with one machinery; TIME removes time from its own likelihood. A labeled reference 4/5: `Time-independent` at 1.0 (TIME), a dashed line at 1 (CHARM), λexp with its p-value (HNL), a `Random Guess` diagonal (TRACK). The reading rule in words 3/5 (not TOP or TIME). The ratio as the y quantity: CHARM, TIME (weaker evidence: 2/5).

**Exemplars.**
- "A ratio greater than one indicates the tagged search is more powerful (smaller σ)" [CHARM Fig. 3 caption] The reading rule, in the caption.
- "Residuals with mean close to zero indicate a lack of bias ..., while residuals with small variance indicate small uncertainties." [TRACK §V ¶1] The reading rule, before any result.

**Draft violation and fix.**
- Before: *Our trigger keeps 31% of decays at 1–5 m, compared with the 10% ATLAS reports [n].*
- After: *On the same simulated events, the standard trigger keeps 12% of decays at 1–5 m and ours 31%. Figure 6 divides our limit by the standard one; below the line at 1, ours wins.*

**Boundaries.** Give the absolute scale once (TIME: 223 ± 19 expected events, 207 observed). Check the machinery on a known answer (FLOW-12); TIME never says how close its rebuilt limit comes. Draw each ratio one way up (CHARM's Fig. 5 inverts its G) and on one y-range (slip 6).

### EVIDENCE-7. Bracket the result between the baseline and a bound, and give the realistic case first

**Rule.** Show the result between the baseline and a bound: an idealized method, a perfect detector, an improved scenario. Give the realistic number first and the limiting one second, each with its condition, and say why the bound is out of reach.

**Why it works.** The reader sees the gain and the room left.

**Prevalence.** 4/5 (not TOP). TRACK draws an idealized fitter on every result plot; CHARM, a perfect tagger's ceiling; TIME gives about 2 before about 7 for an unconstrained background; HNL gives 87.8% CL with today's flux uncertainty, then 99.8% CL.

**Exemplars.**
- "requires information not usually present during track fitting, so cannot be used in experiments, but gives an upper bound on what might be achieved through extremely effective optimization." [TRACK §IV] The oracle, and why it is out of reach.
- "In the limiting case of a completely unconstrained background, we find that this improvement factor is ≈ 7." [TIME §VI ¶3] The limit, after the realistic factor.

**Draft violation and fix.**
- Before: *With a perfect spectrometer, the trigger keeps 60% of decays.*
- After: *With today's spectrometer, the trigger keeps 31% of decays at 1–5 m. With the planned HL-LHC chambers it would keep 40%, and a perfect spectrometer bounds it at 60%.*

**Boundaries.** Discuss a bound where you draw it; CHARM's ceilings reach the text only in its conclusions. Check the bound against your own numbers (slip 8).

### EVIDENCE-8. Match the verb to the evidence, and fence the claim

**Rule.** Choose the verb by the evidence: *project*, *expect* and *would* for simulated sensitivity, *favor* for a weak preference, *exclude* or *reject* for a decisive test (by convention, 95% CL or more). Use one verb per number in caption, text and abstract, and put the scope inside the claim's sentence.

**Why it works.** The reader can trust every verb.

**Prevalence.** Fences 5/5: TOP never writes *we exclude*; TRACK scopes its headline to the simulated setting; CHARM writes *modestly better*; TIME writes *up to*. Only 6 of 68 modal hedges touch a paper's own result. Verbs are looser: HNL writes *would only favor* at 87.8% CL but "would be rejected at 91.3% CL (1.4σ)" [HNL §VII C].

**Exemplars.**
- "In this paper we derive projected constraints for the production of a vector-like top partner" [TOP Conclusions ¶1] *Projected* marks a simulation.
- "we expect that FASER2 would only favor the Majorana model over the Dirac model at 87.8% CL (1.2σ)" [HNL §VI ¶1] A weak result, a weak verb.

**Draft violation and fix.**
- Before: *We exclude long-lived scalars up to 1.2 TeV and prove that the new trigger is superior.*
- After: *With 300 fb−1, a search using the new trigger would be expected to exclude long-lived scalars up to 1.2 TeV, for the simulated detector of Sec. III.*

**Boundaries.** State your own computed numbers plainly; hedge extrapolations. Verbs inflate in captions and abstracts (slip 5).

### EVIDENCE-9. State each assumption and limitation where it bites, with its size or direction

**Rule.** Write each assumption as one flat sentence, with its number, where it is used, and say whether it makes the result conservative or optimistic. Vary the assumption the result hangs on. Name the main limitation plainly, and repeat it in the conclusions with its remedy (FLOW-10, STORY-10).

**Why it works.** The referee's question is answered where it arises.

**Prevalence.** A number or a direction 5/5 (TOP prices unsimulated backgrounds with a flat 50%). The key assumption varied 4/5: CHARM (six efficiency scenarios), TIME (an unconstrained background), HNL (5% against 60% flux uncertainty), TRACK (two noise models).

**Exemplars.**
- "We conservatively assume the peak instantaneous luminosity, corresponding to roughly 200 pileup events per bunch crossing, which gives the maximal expected background." [HNL §VII B] Assumption, number, direction.
- "Our study applies binary thresholds per jet, which is less powerful than directly using the tagger's continuous output." [CHARM §V ¶6] A simplification, with its bias.

**Draft violation and fix.**
- Before: *Some simplifying assumptions were made for the backgrounds and the detector.*
- After: *We take a 50% uncertainty on the cosmic-muon background, five times the spread of the measured rates, so our limits are conservative.*

**Boundaries.** Keep limits of scope (HNL: muon couplings only) apart from limits of method. Keep each assumption fixed; TOP's mass range drifts from [150 − 1000] GeV to O(100) GeV.

### EVIDENCE-10. Build comparisons as controlled pairs, and print the changed condition on each panel

**Rule.** When panels or figures are compared, change one condition and keep the layout, axes, color scale, colors and caption wording. Print the changed condition on each panel.

**Why it works.** The eye goes straight to the one difference.

**Prevalence.** Controlled pairs 5/5: HNL changes one condition per pair, on one color scale (Figs. 4, 9, 10); TRACK puts Gaussian noise left and skewed right; CHARM stacks Z′ over T, TOP hadronic over leptonic; TIME sets two limit types side by side (Fig. 2). The condition on the panel 5/5 (`T → tγ mode, bjjγ final state`, TOP), but HNL Figs. 6, 7, 11 and TRACK Figs. 4, 8, 12 leave it to the caption.

**Exemplars.**
- "Muons produced in association with Majorana HNLs can be found with OS or SS muons in FASER2 with equal rates, resulting in a symmetric distribution" [HNL Fig. 9 caption] Its twin, Fig. 10, ends on *asymmetric*.
- "Left: Gaussian hit noise, right: skewed hit noise model." [TRACK Fig. 6 caption] One convention for every result.

**Draft violation and fix.**
- Before: *Figure 5 shows the efficiency without pileup, and Fig. 6 with pileup, a new selection and another scale.*
- After: *Figures 5 and 6 share binning, axes and colors and differ only in pileup, which each panel prints in its corner.*

**Boundaries.** Separate ranges are fine when each panel's message lies inside it and its key number is on the plot (HNL Fig. 6). A zoom per panel can hide the comparison: in HNL Fig. 5, mass precisions of 0.1% and 1% look alike.

### EVIDENCE-11. Keep one vocabulary: the same words, numbers, colors and styles everywhere

**Rule.** Label axes, legends and panels in the text's exact terms and notation, and quote the plot's numbers. Give each factor one visual channel (color, then line style or marker fill), state the mapping once, and keep it for the whole paper.

**Why it works.** The reader matches a sentence to a curve without translating.

**Prevalence.** Labels tied to the text, and mappings kept within a family of figures, 5/5: TRACK keeps one color per method (Figs. 6–8, 11), HNL one per hypothesis (Figs. 6, 7, 11). Two channels for two factors 4/5 (TRACK uses panels). But 4/5 reuse a main color for a new meaning (slip 7).

**Exemplars.**
- "refer to this quantity, χ2hit, as the hit residual, a measure of the distance between the fitted track and the hits" [TRACK §II ¶5] The term later labels Fig. 8 (`Hit Residual`).
- "Six charm-tagging efficiency scenarios, drawn as per-jet efficiency versus jet pT: color denotes the flavor and line style the scenario." [CHARM Fig. 11 caption] The mapping, stated once.

**Draft violation and fix.**
- Before: *In Fig. 3 the new trigger is red; in Fig. 6 red is the standard trigger, and the axis reads L1 acceptance.*
- After: *In every figure the new trigger is red and the standard trigger black, and every efficiency axis reads Trigger efficiency, as in the text.*

**Boundaries.** Write labels in the text's notation, not code output (HNL Fig. 5: `U: 3.60e-03`). Give ordered parameters an ordered palette, and prefer a sequential color map to a rainbow (HNL Fig. 8).

### EVIDENCE-12. Make the numbers checkable: draw their uncertainty, and tabulate the ones readers will quote

**Rule.** Draw on the result plot the uncertainty the conclusion depends on, and say in the caption what the band contains. Put exact numbers in tables beside their figures, say in the caption what one entry means, and point the text to the cell that matters.

**Why it works.** The reader can weigh a gain against its uncertainty, and copy exact numbers.

**Prevalence.** Drawn uncertainty 3/5: CHARM (bands in six figures, budgeted in Table I), TIME (interquartile bars over 100 realizations), HNL (√µi bars, 1σ–4σ contours); TOP and TRACK draw none. Tables 4/5 (TIME has none): TOP's yields back the log-scale stacks of Figs. 3–4, and TRACK's Table II backs Figs. 6–7.

**Exemplars.**
- "the vertical bars denote the 25% and 75% quartile ranges ... determined by a combination of the finite statistics and the unknown DM parameters" [TIME Fig. 2 caption] What the bars are, and what drives them.
- "Migration between the cone and IFN labels, per jet, tagged fiducial region; entries are fractions of the cone row." [CHARM Table III caption] How to read a cell.

**Draft violation and fix.**
- Before: *The improvement is clearly visible in Fig. 6. Table 2: Cut flow.*
- After: *The band in Fig. 6 holds the hit-efficiency and pileup uncertainties; the gain stays above it at every decay length. Table 2: Signal and background yields in 300 fb−1 after each selection step; the last row is the signal region.*

**Boundaries.** Draw the band the verdict uses (slip 4). A projection may keep out of the fit what the real analysis will constrain, if it says why (CHARM §IV ¶14).

## Templates

**T1. Captions** (EVIDENCE-3, 6, 12): `quantity versus variable` → `conditions` → `key after each noun` → `panel map` → `point or reading rule` → `guard`.
- `[Figure of merit] relative to [baseline] versus [variable], for [conditions]. A value below one means [gain]. Bands show [sources]. Also shown is [bound]. Top, [case 1]; bottom, [case 2].`
- `Distributions of [statistic] under [H1] and [H2], for [benchmark]. Left: assuming [condition], [result with CL]. Right: assuming [condition], [result with CL].`

**T2. Result sentences** (EVIDENCE-2, 5, 7).
- `[Claim with number] compared to [baseline], [condition]; see the [curve] in the [panel] of Fig. N.`
- `For [regime], [method] [lowers] [quantity] by a factor of [N]. For [other regime], the two meet, because [mechanism].`
- `With [today's condition], [result]. If [improvement], it would reach [number]; [bound], out of reach because [reason], gives [number].`

**T3. Figure check before submission.**
- Every display is cited, in order, with what to see.
- Panel maps match the artwork; named colors are the rendered colors.
- Every number in the text is read off the final figure, with the caption's condition and verb.
- Every axis has a quantity and a unit, legible at column width.
- One color per method, hypothesis and baseline; each ratio one way up, with one y-range.
- Every band and legend entry is defined; every bound is checked against your own numbers.

## Corpus slips to avoid

1. **Panel maps for panels that are not there.** "for hadronic (top) and leptonic (center) decays" [TOP Fig. 3 caption] on two panels; "for the NN-based (left) and LS-based (right) pipelines" [TRACK Fig. 10 caption] on three columns.
2. **Caption colors that are not the rendered colors.** "we also show the improvement for a fixed δ = 0 (δ = π/2) in black dotted (dashed) lines." [TIME Fig. 7 caption] The curves are gray.
3. **Numbers that change.** "it constrains cross sections of 100 fb" [TOP Conclusions ¶3] at 300 GeV, where Fig. 5 shows about 600 and 1100 fb. TIME calls a limit half its baseline a factor of two in §III A, but "approximately 50% stronger than those that do not use temporal information" [TIME §IV A].
4. **Verdicts broader than the figure.** "Those flavor fractions agree with those in our sample of simulated √s = 13 TeV collisions, to within uncertainties." [CHARM App. B] Fig. 7 draws a 5% band, and most bb, bc and bℓ points lie outside it.
5. **Verbs stronger than the number.** "the Dirac hypothesis can be rejected at 69.2% CL (0.5σ)" [HNL Fig. 7 caption].
6. **Results drawn but never read, or drawn two ways.** CHARM's Fig. 3 gain (about 1.7 falling to 1.35) gets no number; TRACK never reads the dz bias of Fig. 7. TIME's relative-limit axis spans 0.1–1.1 in Fig. 4 but 0.65–1.02 in Fig. 5.
7. **Colors that change meaning.** TOP's red is tγ (Fig. 2), a 600 GeV signal (Figs. 3–4), then the hadronic final state (Fig. 5). TIME's time-using curve turns blue in Fig. 7, the baseline's color. CHARM's red is charm in Fig. 1 and the T in Fig. 2. TRACK's blue and red are noise models in Fig. 3, then methods.
8. **A bound the results violate.** TRACK's idealized fitter, its upper bound, has a larger skewed-noise d0 error than the realistic fitter (0.28 against 0.13, Table II); the text never says why.
9. **A figure that does not show what it is cited for.** HNL cites Fig. 8 for the cut 3.5 < η < 4.9, but the figure draws neither the signal nor the cut.
