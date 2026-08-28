# 5409: representative external-4/first production-stability gate

## Decision

**PASS FOR CONTINUED V41 PRODUCTION ONLY.**

Checkpoint 5408 proved the representative `[14]` square-edge identity on the first depth-18 leaf. This gate tests whether that repair survives ordinary production rather than merely passing its construction box.

## Production regression

- accepted boxes advance `7 -> 37`;
- net new certified boxes: `30`;
- pending stack changes `15 -> 13`;
- maximum pending depth recedes `16 -> 14`;
- exact accepted-plus-pending area: `0.039327536205488567`;
- current accepted-area fraction: `0.00036621093750002065`;
- minimum denominator among all accepted rows: `5.865205839369e-07`.

Every depth-17 descendant reached during the regression is certified. The split ledger contains only pre-existing outer-enclosure categories; no new representative external-4/first square class appears. The correct next step is ordinary subdivision, not another analytic replacement.

## Claim boundary

This is a local production-stability result for one active contour path. It does not close that path, the regular-away W3 sum, event-local W3, UV finiteness, local GR, or the full MTS framework.
