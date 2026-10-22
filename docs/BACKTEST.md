# A toy backtest — follow the timeline before reading the percentage

[Home](../README.md) · [한국어 시작](START_HERE.ko.md) · [Source](../src/demo_backtest.py)

## What this example computes

At observation t, compare a short trailing average with a long trailing average using only closes through t. Before the long window is available, signal is WAIT. Afterwards, a higher short average gives BUY; otherwise the state target is FLAT. FLAT means this simulation targets cash; it is not a recommendation. The separate snapshot script retains HOLD for a descriptive non-BUY label and does not simulate positions.

The decision at t can change the simulated holding only at **the next observation's close**. This is a declared classroom convention, not a market-open model or a guaranteed execution price. Dates are observation labels, and no exchange calendar is inferred.

## Default fixture timeline

| Observation | What is known | Decision now | Action now |
| --- | --- | --- | --- |
| January 2–7 | Fewer than five observations | WAIT | NONE |
| January 8, close 101.80 | First complete 3/5 windows | BUY | NONE; decision waits |
| January 9, close 101.20 | Previous BUY is available | BUY again | ENTER using the previous decision |
| Later rows | Prior decisions and current close | New decision | Change only if the prior target requires it |
| Final row | No later observation exists | Pending final signal | Mark holdings at the final close; no invented extra fill |

The default input ends with **10187.75** fictitious equity units from **10000**, a rounded **1.88%** change. The first-observation buy-and-hold illustration ends at **10310.00**, or **3.10%**. These exposure start times differ because the toy rule warms up; the two numbers are a calculation example, not a fair strategy-selection experiment or market result.

## Arithmetic and fields

On entry, `shares = cash / next_close`; cash becomes zero. On exit, `cash = shares * next_close`; shares become zero. Equity is `cash + shares * current_close`. The summary percentage is `(final_equity / initial_cash - 1) * 100`; displayed event values are rounded separately from internal state.

Each event includes current `signal`, previous `executed_signal`, the previous `decision_date`, actual toy `action`, cash, shares and equity. The result also records `execution_assumption` and `pending_final_signal`. No-trade behavior is valid when a decision never has a later observation.

## A tiny example students can check by hand

With closes `[100,100,100,100,200,50]`, short/long windows 3/5 and cash 10000, the fifth observation produces BUY. The sixth observation processes it at 50, so the toy holds **200** units, not 50 units bought at the earlier 200 close. This distinguishes when a value becomes known from when a state change uses it.

Appending later rows should not change earlier events. The [prefix-causality regression](../tests/test_classroom.py) checks that property. A later FLAT decision similarly waits for the next observation before EXIT.

## Assumptions and limits

All prices are invented. The example permits fractional units, has no transaction costs, spread, slippage, taxes, borrowing, liquidity limit or execution failure, and does not force a final liquidation. It does not tune parameters, estimate statistical significance, measure predictive accuracy or validate an investment claim. The deliberately simple public rule is a software lesson and contains no private strategy.

Changing the time convention changes the arithmetic. The 2026-10-21 maintenance update intentionally replaces the earlier same-close simulation; older output is not the expected output for this version. [Repair log](REPAIRS.md) · [Exercise answers](SOLUTIONS.ko.md).
