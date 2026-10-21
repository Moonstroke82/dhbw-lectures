---
course: Data Analytics
session: 9
title: Experiments and A/B Testing
subtitle: Practice tasks on causal claims, test plans, sample size, analysing results, pitfalls and difference-in-differences — plus a portfolio-style experiment report
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the content of session 9 on your own or in the lab. Tasks 1, 2 and 6 need only paper and pencil (and a calculator). Tasks 3–5 use Python with SciPy and statsmodels (Seabold & Perktold, 2010); the numbers in tasks 3–6 describe made-up companies and are invented for practice. Task 7 is a portfolio-style task on the public e-mail experiment from the lab (Hillstrom, 2008), which you can download without login:

```python
import pandas as pd
URL = "https://hillstorm1.s3.us-east-2.amazonaws.com/hillstorm_no_indices.csv.gz"
df = pd.read_csv(URL)          # copy of Hillstrom (2008); 64,000 rows, 12 columns
```

If this copy is not reachable, the original CSV is linked in the blog post (Hillstrom, 2008). The terms follow the slides: confounder, randomisation unit, primary metric (overall evaluation criterion), guardrail and diagnostic metrics, minimum effect δ, n ≈ 16σ²/δ², sample ratio mismatch (SRM), peeking, Holm correction, novelty effect and difference-in-differences (Kohavi et al., 2020). Use α = 0.05 (two-sided) and power 80 % unless a task says otherwise.

## Causal Claim or Not?

For each statement, decide whether the **causal conclusion** is justified. If not, name the most likely **alternative explanation** (confounder, reverse causality, selection, seasonality or chance) and describe a **better test** in one or two sentences.

1. "Customers who use our mobile app spend 40 % more than web-only customers. We should push every customer to the app."
2. "Stores with more staff on the shop floor sell more. Hiring more staff will raise sales."
3. "After we launched the new search on 1 December, revenue rose by 25 % compared with November."
4. "Employees who attended the voluntary sales training closed more deals in the following year."
5. "In a randomised test, half of the new users got the new onboarding. 7-day retention was 41.2 % vs. 39.8 % (p = 0.003, no sample ratio mismatch)."
6. "Our 20 most profitable customers all use the premium support line. Premium support makes customers profitable."

::: answer lines=10
:::

::: hint
Ask: who decided which unit got the "treatment"? If the units chose themselves, or the business chose them for a reason, that reason may also drive the outcome.
:::

::: solution
1. **Not justified — selection (and a confounder).** Engaged, high-spending customers are the ones who install the app. Test: randomly offer an app incentive (e.g. a voucher for the first app order) to half of the web-only customers and compare their spend over the following months (an "encouragement" design; the randomised offer is the treatment).
2. **Not justified — reverse causality.** Busy stores get more staff because they sell more. Test: randomly assign extra staff hours to some stores for some weeks (cluster randomisation by store and week), or at least compare changes over time with comparable stores.
3. **Not justified — seasonality and a before/after comparison.** December has Christmas sales; other changes (campaigns) also happened. Test: an A/B test of the new search (users randomised), or compare December with the previous December and with a comparison group that kept the old search.
4. **Not justified — self-selection.** Motivated or already successful sales people volunteer for training. Test: randomly assign training places (e.g. a waiting-list design: half trained now, half next quarter) and compare deals in the meantime.
5. **Justified** — random assignment, no SRM, a pre-defined metric. Remaining questions: is +1.4 pp practically relevant, is the effect stable over time (novelty), and was 7-day retention the planned primary metric (not picked after looking at many metrics)?
6. **Not justified — selection on the outcome and reverse causality.** Only the top 20 are looked at; profitable customers are offered (or can afford) premium support. There is no comparison group at all. Test: offer premium support at random to some eligible customers and compare profit and churn.

Marking: 1 point per statement (verdict with a fitting explanation and test), 6 points.
:::

## A Test Plan for a Delivery Platform

A food delivery platform wants to lower the **minimum order value** from EUR 15 to EUR 10, hoping for more orders. Restaurants and riders are shared by all customers in a city. Write a test plan with these elements: hypothesis (H₀ and H₁), variants, **randomisation unit**, primary metric, at least two guardrail metrics and one diagnostic metric, and the decision rule. Then answer:

1. Why could randomising **customers** give a misleading result here?
2. Propose a randomisation unit that avoids this problem and name its main drawback.

::: answer lines=12
:::

::: hint
If treated customers order more, what happens to the delivery times of control customers in the same city?
:::

::: solution
Example plan:

- **Hypothesis:** H₀: orders per customer per week are the same with a minimum of EUR 10 and EUR 15; H₁: they differ (two-sided — small orders could also crowd out larger ones).
- **Variants:** A: minimum EUR 15 (control) · B: minimum EUR 10.
- **Randomisation unit:** see 2.
- **Primary metric:** contribution margin (or gross order value) per customer per week — not just the number of orders, because small orders may be unprofitable. Accept "orders per customer" if the student names margin as a guardrail.
- **Guardrails:** delivery time (mean and 90th percentile), share of late deliveries, cancellation rate, contribution margin per order, rider utilisation, customer complaints; trust guardrail: sample ratio.
- **Diagnostic:** share of orders between EUR 10 and 15, average basket value, orders per active customer.
- **Decision rule:** roll out B if the primary metric improves significantly (95 % interval above zero) and no guardrail gets significantly worse beyond a tolerance set in advance (e.g. +2 minutes delivery time).

1. **Interference (spill-over):** treated customers order more small orders, riders and kitchens are busier, and control customers in the same city wait longer — so the control group is affected by the treatment. The difference between the groups is then biased (it can look larger, because control gets worse, or hide costs). Randomising customers also lets a customer see a different minimum than their flatmate.
2. **Cluster randomisation by city** (or by city and time slot, a "switchback" design that alternates the variant per city and time block). Drawback: far fewer randomisation units (e.g. 30 cities), so much **less power** and a high risk of chance imbalance between cities; switchback designs need the effect to "reset" between time blocks. The analysis must use the city (or city × time block) as the unit (Kohavi et al., 2020, Chapters 14 and 22).

Marking (8 points): hypothesis 1; variants and decision rule 1; primary metric with reason 1; guardrails and diagnostic 2; interference explained 2; cluster unit with drawback 1.
:::

## Sample Size and Duration

A meal-kit company tests a new landing page. Today **4.0 %** of visitors start a free trial. The product owner wants to detect an increase of **0.5 percentage points**. About **6,000 visitors per day** reach the page; they are split 50/50.

1. Compute *n* per variant with the rule of thumb n ≈ 16σ²/δ². How many days does the test need? How long would you run it, and why?
2. Compute *n* with statsmodels (`proportion_effectsize`, `NormalIndPower`). Why does it differ slightly from the rule?
3. The team would rather detect **0.25 pp**. What happens to *n* and the duration?
4. To limit risk, the team wants to show the new page to only **10 %** of the visitors (90/10 split, δ = 0.5 pp). How many visitors are needed in total, and how long does the test run?
5. A colleague proposes to stop after **10,000 visitors per variant**. What is the power for δ = 0.5 pp? Explain what this means in one sentence.

::: answer lines=12
:::

::: hint
`NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.8, ratio=r)` returns `nobs1`; the second group has `ratio · nobs1` units. Leave out `power` and pass `nobs1` to get the power instead — or use `.power(...)`.
:::

::: solution
Code (tested with statsmodels 0.15.0):

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

pw = NormalIndPower()
p0, d = 0.04, 0.005
print(16 * p0 * (1 - p0) / d**2)                        # rule of thumb
h = proportion_effectsize(p0 + d, p0)
print(pw.solve_power(effect_size=h, alpha=0.05, power=0.8))
h2 = proportion_effectsize(p0 + 0.0025, p0)
print(pw.solve_power(effect_size=h2, alpha=0.05, power=0.8))
n1 = pw.solve_power(effect_size=h, alpha=0.05, power=0.8, ratio=9)
print(n1, 9 * n1, 10 * n1)                              # treatment, control, total
print(pw.power(effect_size=h, nobs1=10000, alpha=0.05))
```

1. 16 · 0.04 · 0.96 / 0.005² = **24,576** per variant, 49,152 in total → 8.2 days at 6,000 visitors per day. Run **two full weeks** (14 days): whole weeks cover weekday and weekend behaviour, and a little extra protects against lower traffic.
2. statsmodels: **25,530** per variant (8.5 days). It uses Cohen's h, the difference of arcsine-transformed proportions, which accounts for the variance being different at 4.0 % and 4.5 %; the rule uses p₀(1 − p₀) and rounds 2(1.96 + 0.84)² ≈ 15.7 up to 16.
3. Halving δ multiplies *n* by about four: rule **98,304**, statsmodels **99,309** per variant → about 33 days → run **five weeks**. Discuss whether an effect of 0.25 pp is worth that time.
4. With a 90/10 split, the smaller group limits the precision: statsmodels gives **14,184** in the treatment group and 127,652 in the control group, **141,836** in total → 23.6 days → run **four weeks** (instead of two). Unequal splits cost time; they are a risk trade-off (Kohavi et al., 2020, Chapter 15, discusses ramping exposure step by step).
5. Power **0.42**: if the page really raises the trial rate by 0.5 pp, a test with 10,000 visitors per variant finds a significant result only in about 42 % of cases — a non-significant result would say very little. (With the planned 14 days, 42,000 per variant, the power is 0.95.)

Marking (10 points): 1 rule and duration with whole weeks (2); 2 number and reason (2); 3 (2); 4 (2); 5 power and interpretation (2).
:::

## Analyse a Finished Test

A public transport company tested a **one-page checkout** in its ticket app against the current three-step checkout, randomised by user account (50/50). The primary metric is the share of users who buy at least one ticket during the test; the guardrail is the share of users who had at least one app crash.

| Variant | Users | Buyers | Users with a crash |
|---|---|---|---|
| A: three-step checkout (control) | 18,412 | 2,946 | 77 |
| B: one-page checkout | 18,388 | 3,127 | 112 |

1. Check the sample ratio first.
2. Compute the conversion rates, the absolute and relative difference, the standard error, the 95 % confidence interval and the p-value. Do the main steps by hand and check them with statsmodels.
3. Analyse the guardrail in the same way.
4. What do you recommend? Write the recommendation in two or three sentences, answer first.

::: answer lines=14
:::

::: solution
Code (tested with SciPy 1.18.1, statsmodels 0.15.0):

```python
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep

print(stats.chisquare([18388, 18412]))                        # SRM check
for xb, xa in [(3127, 2946), (112, 77)]:                       # buyers, crashes
    print(xb / 18388 - xa / 18412,
          proportions_ztest([xb, xa], [18388, 18412]),
          confint_proportions_2indep(xb, 18388, xa, 18412, method="wald"))
```

1. χ² = 0.016, **p = 0.90** — no sample ratio mismatch; the split is consistent with 50/50.
2. p̂_A = 2,946 / 18,412 = **16.00 %**, p̂_B = 3,127 / 18,388 = **17.01 %**. Δ = **+1.01 pp**, relative lift +6.3 %. SE = √(0.1600 · 0.8400 / 18,412 + 0.1701 · 0.8299 / 18,388) = **0.00387**. 95 % CI: 1.01 ± 1.96 · 0.387 = **[0.25, 1.76] pp**. z = 2.60, **p = 0.0094** (pooled test; the pooled and unpooled SE agree to four decimals here).
3. Crash rate A 0.42 %, B **0.61 %**: Δ = +0.19 pp, 95 % CI [0.04, 0.34] pp, z = 2.56, **p = 0.010**. The guardrail is significantly worse — relative to the baseline, crashes rise by about 46 %.
4. Example: "Do not roll out the one-page checkout yet: it raised the share of buyers by 1.0 percentage points [0.25, 1.76], but it also increased the share of users with a crash from 0.42 % to 0.61 % (p = 0.01). Fix the crash, then confirm the effect in a short follow-up test." Good answers also mention that crashes may cost buyers in the long run, and that the follow-up test should again have a planned sample size (no peeking).

Marking (10 points): SRM check (1); rates and difference (2); SE, interval and p-value (3); guardrail (2); recommendation with both results (2).
:::

## Diagnose the Pitfalls

Each case describes an experiment that went wrong — or did it? Name the **pitfall**, explain the consequence for the result and say what the team should do.

1. A newsletter test was planned 50/50. The analysis shows 50,421 users in A and 48,977 in B. Variant B has a 3 % higher click rate (p = 0.01).
2. A product manager looked at the dashboard every morning and stopped the test on day 4, when the p-value was 0.03 — "we have a winner".
3. An online shop tested a new product page in 10 countries. Overall, the effect is not significant, but the country-level p-values are 0.004, 0.012, 0.021, 0.034, 0.048, 0.11, 0.27, 0.39, 0.62 and 0.81. The team wants to roll out in the five "significant" countries.
4. A redesigned home page raised the click-through rate on the recommendations by 8.0 % in week 1, 4.1 % in week 2, 1.6 % in week 3 and 1.3 % in week 4 (relative). For users who first visited during the test, the lift was about 1.2 % in every week.
5. To test a new price display, a shop randomised **each page view** to A or B.
6. Run the A/A simulation below (no real difference between A and B). Reproduce the 22.0 % false positives from the slides, then change it so that the analyst looks only on days 7 and 14, and then only on day 14. What do you find?

```python
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
S, D, n, p = 10000, 14, 1000, 0.10   # A/A tests, days, users per arm and day, rate
a = rng.binomial(n, p, size=(S, D)).cumsum(1)   # cumulative conversions, arm A
b = rng.binomial(n, p, size=(S, D)).cumsum(1)
N = n * np.arange(1, D + 1)                       # cumulative users per arm
pool = (a + b) / (2 * N)
z = (a / N - b / N) / np.sqrt(pool * (1 - pool) * 2 / N)
sig = 2 * stats.norm.sf(np.abs(z)) < 0.05         # significant on day d?
print("stop at first p < 0.05:", sig.any(axis=1).mean())
```

::: answer lines=14
:::

::: hint
For case 3, apply Holm: sort the p-values and compare the smallest with 0.05/10, the next with 0.05/9, and so on, stopping at the first that fails. `multipletests(p, method="holm")` in statsmodels does this for you.
:::

::: solution
1. **Sample ratio mismatch.** χ² = 21.0, **p = 0.000005** for a planned 50/50 split — not chance. Users were lost or added unevenly (e.g. a bot filter, a redirect or tracking that fails in B). The 3 % effect **cannot be trusted**; find the cause first (Fabijan et al., 2019), fix it and rerun the test. Do not "correct" the effect by reweighting.
2. **Peeking / optional stopping.** Stopping at the first p < 0.05 inflates the false positive rate far above 5 % (22 % in the simulation of the slides; Johari et al., 2017). Day 4 is also less than one full week. The team should run the test for the planned sample size and duration and analyse once — or use a sequential method designed for continuous monitoring.
3. **Multiple testing (and fishing in segments).** With ten tests and no real effect, P(at least one p < 0.05) = 1 − 0.95¹⁰ = **40 %**. Holm: only 0.004 < 0.05/10 = 0.005 is significant; the next, 0.012, is above 0.05/9 = 0.0056, so the procedure stops. Holm-adjusted p-values: 0.040, 0.108, 0.168, 0.238, 0.288, 0.55, then 1. Bonferroni gives the same result here. Recommendation: do not roll out by country on this basis; if there is a business reason to expect differences, test the most promising country again with a planned test.
4. **Novelty effect.** The lift fades as returning users get used to the new design; for new users it is stable at about 1.2 %. The long-run effect is about **1.2–1.3 %**, not 8 % (or the 4-week average). Decide on the stable effect: is +1.3 % worth the redesign? Report the effect by week, not one average (Kohavi et al., 2020, Chapter 3).
5. **Wrong randomisation unit.** The same user sees different prices on different pages — confusing, possibly damaging trust (and legally risky for prices). Page views of one user are not independent, so naive standard errors are too small. Randomise by **user** (or cookie for anonymous visitors) and analyse per user (Kohavi et al., 2020, Chapter 14).
6. Results with seed 42: stopping at the first daily p < 0.05: **22.0 %** (0.2201); looking only on days 7 and 14 — `sig[:, [6, 13]].any(axis=1).mean()`: **8.4 %**; only on day 14 — `sig[:, -1].mean()`: **5.1 %** (0.0508). Every extra look adds false positives; a single planned analysis keeps the error rate at the chosen α.

Marking (12 points): 2 points per case (pitfall named 1, consequence and action 1).
:::

## When You Cannot Randomise: Difference-in-Differences {.optional}

A retail chain introduces free **click-and-collect** in all stores of region **North** on 1 July. Region **South** does not get it. Marketing wants to know the effect on orders. Average weekly orders per store:

| Region | Q1 | Q2 | Q3 (after the launch) |
|---|---|---|---|
| North (click-and-collect from 1 July) | 405 | 412 | 455 |
| South (unchanged) | 391 | 398 | 419 |

1. Marketing reports "+43 orders per store and week" (Q2 → Q3 in North). What is wrong with this number?
2. Compute the difference-in-differences estimate and the counterfactual for North in Q3. Express the effect in percent of the counterfactual.
3. What is the key assumption, and what do Q1 and Q2 tell you about it?
4. Name two events that would break the assumption, and explain why the chain could not easily run an A/B test instead.

::: answer lines=10
:::

::: solution
1. It is a **before/after** comparison: it mixes the effect of click-and-collect with seasonality (Q3 vs. Q2), general market trends and any other change in the same period. South grew by 21 orders without click-and-collect.
2. DiD = (455 − 412) − (419 − 398) = 43 − 21 = **+22 orders** per store and week. Counterfactual North in Q3 = 412 + 21 = **433**; effect 22 / 433 = **+5.1 %**.
3. **Parallel trends:** without click-and-collect, North would have changed like South. Q1 → Q2: North +7, South +7 — the trends were parallel before the launch, which supports (but cannot prove) the assumption (Kohavi et al., 2020, Chapter 11).
4. Examples: a competitor closes stores in North (or opens in South); a regional holiday or weather event in Q3; a regional advertising campaign; store openings or closures in one region. A/B test: the offer is visible in the store and in local advertising, so it cannot be randomised per customer without confusion; randomising **stores** would be possible (cluster randomisation), but with few stores the power is low and nearby stores influence each other — that is why a quasi-experiment is often used, with a clearly stated assumption.

Marking (8 points): 1 (2); 2 DiD, counterfactual and percent (3); 3 assumption and check (2); 4 (1).
:::

## Portfolio-Style Task: Should the E-Mail Match the Customer?

Marketing has read your lab result (the men's e-mail raised spend most) and asks a follow-up question: *"Next season we can send only one e-mail per customer. Should we send each customer the e-mail that matches what they bought before — or the men's e-mail to everyone? And is the women's e-mail wasted on customers who only bought men's merchandise?"*

Write a short experiment report as a notebook on the Hillstrom (2008) data:

- **Analysis plan first** (a Markdown cell written before any result): three subgroups by past purchases, defined from the pre-treatment columns `mens` and `womens` (*men's only*, *women's only*, *both*); primary metric spend per customer, secondary metric visit rate; α, correction method and decision rule.
- **Trust checks** per subgroup: counts and SRM.
- **Effects** of both e-mails against no e-mail in each subgroup, with 95 % intervals, p-values and a **Holm** correction within each e-mail and metric.
- An **interaction test**: does the effect of the women's e-mail differ between men's-only and women's-only buyers? (Hint: an OLS regression on the women's e-mail and no-e-mail rows, `spend ~ treat * C(buyer, Treatment("womens only"))` with robust standard errors, `cov_type="HC1"`, in `statsmodels.formula.api`; the same for `visit`.)
- The expected **spend per 1,000 e-mails** under two policies: "men's e-mail to everyone" and "matched e-mail".
- A **recommendation** in the five-part structure from session 8, with limits.

```python
import numpy as np
df["buyer"] = np.select([(df.mens == 1) & (df.womens == 1), df.mens == 1],
                        ["both", "mens only"], "womens only")
```

::: answer lines=8
:::

::: solution
Results (tested with pandas 3.0.6, SciPy 1.18.1, statsmodels 0.15.0; differences to No E-Mail; spend in USD with Welch intervals, visits with Wald intervals):

| Subgroup (share) | Women's e-mail: spend | Women's e-mail: visit | Men's e-mail: spend | Men's e-mail: visit |
|---|---|---|---|---|
| Men's only (45.0 %) | +0.28 [−0.12, 0.68], p = 0.17 | **+1.1 pp** [0.2, 2.0], p = 0.012 | +0.68 [0.25, 1.12], p = 0.002 | +6.9 pp [6.0, 7.9] |
| Women's only (44.9 %) | +0.63 [0.30, 0.97], p = 0.0002 | +7.4 pp [6.4, 8.4] | +0.62 [0.27, 0.96], p = 0.0005 | +7.1 pp [6.1, 8.0] |
| Both (10.1 %) | +0.16 [−0.81, 1.14], p = 0.74 | +7.1 pp [4.6, 9.6] | +1.82 [0.49, 3.16], p = 0.007 | +13.4 pp [10.9, 16.0] |

- **Trust:** subgroup sizes 28,818 / 28,734 / 6,448; SRM p-values 0.83, 0.65 and 0.63 — the split is balanced within each subgroup (as expected, because the subgroups are defined by pre-treatment data).
- **Holm (three subgroups):** women's e-mail, spend: adjusted p 0.35 (men's only), 0.0007 (women's only), 0.74 (both); visit: 0.012 for men's only, < 0.001 for the others. Men's e-mail, spend: 0.004, 0.0015, 0.0074 — all significant.
- **Interaction (women's e-mail, men's only vs. women's only):** visit −6.3 pp [−7.6, −5.0], p < 0.001 — the women's e-mail clearly brings far fewer men's-only buyers to the website. Spend −0.35 [−0.88, 0.17], p = 0.19 — **not significant**: the spend data are too noisy to show a difference, although the point estimates differ.
- **Policies** (subgroup effects weighted by subgroup shares): men's e-mail to everyone 0.450 · 0.68 + 0.449 · 0.62 + 0.101 · 1.82 ≈ **USD 0.768** per customer → about USD 768 per 1,000 e-mails; matched (men's only → men's, women's only → women's, both → men's) ≈ **USD 0.775** → about USD 775. The difference (about USD 7 per 1,000) is far smaller than the uncertainty of the subgroup effects.
- **Recommendation (example):** "Send the men's e-mail to everyone. It raised spend in every subgroup (by USD 0.62 to 1.82 per customer); matching the e-mail to past purchases would add only about USD 7 per 1,000 e-mails, which is well within the noise. The women's e-mail is nearly wasted on men's-only buyers: it brings 1 extra visit per 100 customers instead of 7. Limits: one campaign from 2008, two-week window, revenue instead of profit, unsubscribes not measured, and the spend interaction is not significant. Next step: test the matched policy against the men's e-mail for everyone in a planned experiment with spend as the primary metric."

Marking guide (30 points; training only — the portfolio brief and rubric are published separately):

- **Analysis plan before results** (5 points): subgroups from pre-treatment data only (3 groups, correctly defined); primary and secondary metric; α, Holm correction and decision rule stated before the results. Subgroups chosen after looking at the effects score 0 here.
- **Trust checks** (3 points): counts per subgroup and arm, SRM test, short interpretation.
- **Effects with uncertainty** (8 points): correct differences, intervals and p-values for both e-mails, both metrics and three subgroups (4); Holm correction applied correctly and interpreted (2); absolute effects in business units (USD per customer, visits per 100) (2).
- **Interaction** (5 points): regression set up correctly with robust standard errors (2); correct reading: strong interaction for visits, no significant interaction for spend — "different p-values in two subgroups" is **not** a test of a difference (3).
- **Decision and communication** (7 points): policy comparison with weighted effects (3); five-part summary, answer first, with correct numbers (2); limits and a next step (2).
- **Reproducibility** (2 points): notebook runs top to bottom from the URL, prints library versions, no manual steps.

A strong submission notices that the matched policy and the men's e-mail for everyone are practically equal and recommends the simpler policy — or a new test — instead of over-interpreting the subgroup point estimates.
:::

## References {.references}

- Fabijan, A., Gupchup, J., Gupta, S., Omhover, J., Qin, W., Vermeer, L., & Dmitriev, P. (2019). Diagnosing sample ratio mismatch in online controlled experiments: A taxonomy and rules of thumb for practitioners. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining* (pp. 2156–2164). ACM. https://doi.org/10.1145/3292500.3330722
- Hillstrom, K. (2008, March 20). *The MineThatData e-mail analytics and data mining challenge* [Blog post and dataset]. MineThatData. https://blog.minethatdata.com/2008/03/minethatdata-e-mail-analytics-and-data.html
- Johari, R., Koomen, P., Pekelis, L., & Walsh, D. (2017). Peeking at A/B tests: Why it matters, and what to do about it. In *Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 1517–1525). ACM. https://doi.org/10.1145/3097983.3097992
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy online controlled experiments: A practical guide to A/B testing*. Cambridge University Press. https://doi.org/10.1017/9781108653985
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 92–96). https://doi.org/10.25080/Majora-92bf1922-011
