from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4292"
CLAIM_ID = "L-133"
BRANCH = "MTS_R2FR_Y5_TRANSITION_MEMBERSHIP_AND_NONEH_MONOPOLE_ZERO_OR_SHARED_RESIDUAL_VECTOR_4292"
DECISION = "TRANSITION_MEMBERSHIP_CONDITIONAL_SELECTOR_NONEH_MONOPOLE_REDUCED_TO_SHARED_RESIDUAL_VECTOR_NONCLAIM"
MARKER = "PPC4161_TRANSITION_MEMBERSHIP_AND_NONEH_MONOPOLE_ZERO_OR_SHARED_RESIDUAL_VECTOR_4292"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_MEMBERSHIP_AND_NONEH_MONOPOLE_ZERO_OR_SHARED_RESIDUAL_VECTOR_4292"
NEXT_TARGET = "4293-Y5-R2FR-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md"

FORMAL_PATH = FORMAL / "308-PPC4161-transition-membership-and-nonEH-monopole-zero-or-shared-residual-vector.md"
DOC_PATH = POST / "4292-Y5-R2FR-transition-membership-and-nonEH-monopole-zero-or-shared-residual-vector.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4292_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PI_B_COEFFICIENT = 0.167893843691
TRANSITION_PIB = 0.5000000000287336
EPSILON_UNIT_BOUND = PI_B_COEFFICIENT * TRANSITION_PIB

SOURCES = {
    "SRC4292_00_4289_split": (
        FORMAL / "305-PPC4161-transition-monopole-absorption-or-residual-profile-gate.md",
        "q_tr = q_tr^Hilbert-monopole + q_tr^residual.",
        "4289 gives the split into absorbable Hilbert monopole and residual vector.",
    ),
    "SRC4292_01_4290_epsilon": (
        FORMAL / "306-PPC4161-transition-Hilbert-monopole-source-lock-or-first-residual-bound-row.md",
        "epsilon_mu_tr = mu_extra_tr/(G_cal M_H^dress).",
        "4290 defines the non-EH transition monopole residual.",
    ),
    "SRC4292_02_4291_membership": (
        FORMAL / "307-PPC4161-PiM-Htau-private-selector-glue-reactivation-or-residual-transfer.md",
        "transition same-worldtube membership,",
        "4291 makes transition membership the live blocker after PiM/Htau is narrowed.",
    ),
    "SRC4292_03_4289_decomposition_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4289_TRANSITION_DECOMPOSITION.csv",
        "CONDITIONAL_ABSORBABLE",
        "4289 machine row says Hilbert monopole is absorbable only conditionally.",
    ),
    "SRC4292_04_4291_reduction_csv": (
        SOURCE_DIR / "P8_Y5_R2FR_4291_TRANSITION_SOURCE_LOCK_REDUCTION.csv",
        "LIVE_BLOCKER_WITH_BOUND_ROW",
        "4291 records epsilon_mu_tr as live blocker with a first bound row.",
    ),
    "SRC4292_05_4176_Jtr": (
        SOURCE_DIR / "P8_Y5_R2FR_4176_TRANSITION_CURRENT_CLOSE_OR_BOUND.csv",
        "J_tr^nu := Pi_loc nabla_mu T_cross^{mu nu}",
        "4176 defines the local transition current and its no-flux closure selector.",
    ),
    "SRC4292_06_4284_direct_fail": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "So the transition shell cannot be treated as a direct local metric source.",
        "4284 forbids treating the raw shell as a direct local metric source.",
    ),
    "SRC4292_07_186_worldtube": (
        FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md",
        "W_H = closure(supp J_H_total)",
        "186 gives the same-worldtube definition.",
    ),
    "SRC4292_08_4155_JHtotal": (
        SOURCE_DIR / "P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv",
        "J_H_total=J_matter+J_EM+J_binding+dB_impr+J_rest_retained",
        "4155 says the source current is assembled once before readout.",
    ),
    "SRC4292_09_194_Gcal": (
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi).",
        "4178/194 gives the calibrated coupling used by epsilon_mu_tr.",
    ),
    "SRC4292_10_4290_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4290_EPSILON_MU_BOUND_ROW.csv",
        "0.08394692185032419",
        "4290 supplies the unit-window transition epsilon bound.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4292 separates the transition shell into three non-confused routes. A same-worldtube Hilbert-membership "
                "selector would absorb the l=0 transition monopole into M_H^dress and sets mu_extra_tr=0 for that component, "
                "but the current corpus does not parent-sign that the raw transition shell belongs to J_H_total before readout. "
                "The no-flux selector from 4176 can close J_tr in compact local collars, but that is a local selector and not a "
                "proof that the Solar transition shell is a direct metric source. Therefore the live nonclaim object is a shared "
                "transition residual vector with epsilon_mu_tr first: epsilon_mu_tr=mu_extra_tr/(G_cal M_H^dress), unit private "
                "AJ capacity 0.08394692185032419 at Pi_B_tr=0.5000000000287336, plus multipoles, time/range/frame/species/beta "
                "hair and cGamma/AJ profile terms."
            ),
            (
                "4292 source register, transition membership theorem/audit, route classifier, epsilon_mu shared residual vector, "
                "control runner, decision, firewall and status rows."
            ),
            "private_transition_membership_conditional_epsilon_mu_shared_residual_vector_nonclaim",
            (
                "Build the shared epsilon_mu_tr bound runner across WEP, R10, PPN, clocks and orbital tests, while separately "
                "attempting parent membership proof for q_tr^Hilbert-monopole in J_H_total."
            ),
            (
                "Treating local no-flux closure as global membership, counting a direct transition shell as safe, hiding "
                "mu_extra_tr inside G_cal, or promoting private AJ capacity to empirical local-GR evidence."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def membership_theorem_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "MT4292_0_same_source_functional",
            "Hilbert-membership selector",
            "S_src -> S_src + S_tr^H[g_obs,psi_tr]; T_tr^H=-(2/sqrt(-g_obs))*delta S_tr^H/delta g_obs",
            "CONDITIONAL_SELECTOR_THEOREM",
            "If the transition term is in the same observed-metric source action before readout, it is Hilbert source, not an extra force.",
        ),
        (
            "MT4292_1_same_worldtube",
            "support membership",
            "supp J_tr^H subset W_H=closure(supp J_H_total) or W_H is enlarged before readout",
            "REQUIRED_NOT_PARENT_SIGNED",
            "This is the live membership gap: current sources do not prove the raw transition shell is in J_H_total.",
        ),
        (
            "MT4292_2_monopole_absorption",
            "l=0 Hilbert shell absorption",
            "M_H^dress -> M_H^dress+M_tr^H; Phi_N=-G_cal(M_H^dress+M_tr^H)/r",
            "DERIVED_IF_MT4292_0_AND_MT4292_1",
            "The monopole is source dressing only after same-worldtube Hilbert membership is established.",
        ),
        (
            "MT4292_3_noneh_zero",
            "non-EH monopole zero inside membership selector",
            "mu_extra_tr := mu_metric_tr - G_cal M_tr^H = 0",
            "ZERO_INSIDE_SELECTOR_ONLY",
            "This is not a numerical claim; it is a definition of the Hilbert-owned component.",
        ),
        (
            "MT4292_4_no_flux_selector",
            "local no-flux alternative",
            "J_tr^nu=Pi_loc nabla_mu T_cross^{mu nu}=0 under signed no-flux local collar clauses",
            "LOCAL_SELECTOR_NOT_GLOBAL_MEMBERSHIP",
            "No-flux local closure can make the current absent locally without proving direct shell metric safety.",
        ),
        (
            "MT4292_5_raw_shell_rejection",
            "direct shell source route",
            "P_metric,loc q_tr direct profile",
            "REJECTED_BY_4284",
            "The raw transition shell cannot be inserted as a direct local metric source.",
        ),
    ]
    return [
        {
            **common(),
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "formula": formula,
            "status": status,
            "derivation_or_reason": reason,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for theorem_id, claim_piece, formula, status, reason in raw
    ]


def membership_audit_rows() -> List[Dict[str, str]]:
    raw = [
        ("MA4292_0_parent_source_action", "same observed-metric source action contains S_tr^H", "UNSIGNED", "required to call q_tr Hilbert-owned"),
        ("MA4292_1_support_lock", "supp J_tr^H subset or pre-readout extension of W_H", "UNSIGNED", "required for same-worldtube membership"),
        ("MA4292_2_once_only_current", "J_tr^H enters J_H_total once with matter/EM/binding", "CONDITIONAL_FROM_4155", "prevents double source accounting"),
        ("MA4292_3_monopole_only", "exterior transition contribution is pure l=0 after selector", "UNSIGNED", "multipoles remain residuals"),
        ("MA4292_4_no_boundary_flux", "transition current or flux absent/routed in local collar", "CONDITIONAL_FROM_4176", "selector local only unless parent-signed"),
        ("MA4292_5_no_nonEH_monopole", "mu_extra_tr=0", "ZERO_IF_MEMBERSHIP_SELECTOR_ELSE_BOUND_ROW", "epsilon_mu_tr is live outside selector"),
        ("MA4292_6_no_direct_metric_shell", "raw q_tr is not a direct local metric source", "SIGNED_REJECTION_FROM_4284", "protects against smuggled closure"),
        ("MA4292_7_verdict", "transition membership proof", "NOT_PARENT_SIGNED", "use shared residual vector until parent source action signs membership"),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "clause": clause,
            "status": status,
            "meaning": meaning,
            "membership_parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, status, meaning in raw
    ]


def route_classifier_rows() -> List[Dict[str, str]]:
    raw = [
        ("ROUTE4292_A", "Hilbert membership", "S_tr^H in J_H_total before readout and same worldtube", "CONDITIONAL_BEST_ROUTE", "absorbs l=0; sets mu_extra_tr=0 for that component"),
        ("ROUTE4292_B", "local no-flux selector", "J_tr=0 in compact collar under no-flux clauses", "PRIVATE_SELECTOR_ONLY", "local current absent; does not prove raw shell safe"),
        ("ROUTE4292_C", "raw direct metric shell", "P_metric,loc q_tr as direct source", "REJECTED", "fails 4284 suppression by huge factor"),
        ("ROUTE4292_D", "shared residual vector", "epsilon_mu_tr plus multipoles/hair scored across arenas", "NEXT_EXECUTABLE_ROUTE", "turns remaining transition residue into empirical/derivation gates"),
    ]
    return [
        {
            **common(),
            "route_id": route_id,
            "route": route,
            "condition": condition,
            "status": status,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for route_id, route, condition, status, effect in raw
    ]


def epsilon_shared_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "ES4292_0_epsilon_mu_tr",
            "epsilon_mu_tr",
            "mu_extra_tr/(G_cal M_H^dress)",
            f"{EPSILON_UNIT_BOUND:.16g}",
            "private_AJ_capacity_seed_from_4290",
            "WEP; PPN gamma/beta; orbital GM; clocks; R10 if range hair couples",
        ),
        (
            "ES4292_1_multipole",
            "Q_l_ge_1_tr",
            "sum_l>=1 Q_lm/r^(l+1)",
            "MISSING_PARENT_ZERO_OR_PROFILE",
            "not_absorbable_into_GM",
            "PPN anisotropy; tidal/orbital precession",
        ),
        (
            "ES4292_2_time_drift",
            "dln_mu_tr_dt",
            "dln mu_obs/dt contribution",
            "MISSING_NUMERIC_OR_PARENT_ZERO",
            "source_drift_row_required",
            "Gdot; clocks; ephemerides",
        ),
        (
            "ES4292_3_range_hair",
            "alpha_tr(lambda)",
            "finite-range transition hair",
            "MISSING_R10_CURVE_OR_ZERO_THEOREM",
            "R10_runner_needed",
            "short-range fifth-force",
        ),
        (
            "ES4292_4_frame_species",
            "delta_frame_source; eta_source_AB",
            "frame/composition source-charge dependence",
            "MISSING_SAME_FRAME_SOURCE_BLINDNESS",
            "WEP_source_row_required",
            "Eotvos; clocks; source universality",
        ),
        (
            "ES4292_5_beta_AJ",
            "delta_beta_source; A_J_residual_tr",
            "PPN beta and cGamma/AJ transition profile residual",
            "MISSING_BETA_AND_PROFILE_ROWS",
            "PPN_and_profile_runner_needed",
            "perihelion; Shapiro; local-GR cGamma/AJ branch",
        ),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "symbol": symbol,
            "formula_or_definition": formula,
            "current_bound_or_status": bound_or_status,
            "row_type": row_type,
            "observable_link": observable,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, symbol, formula, bound_or_status, row_type, observable in raw
    ]


def control_rows() -> List[Dict[str, str]]:
    controls = [
        ("CTRL4292_0_membership_clean", True, True, True, True, False, 0.0, True, "PASS_HILBERT_MEMBERSHIP_MONOPOLE_ABSORBED"),
        ("CTRL4292_1_membership_missing", False, True, True, False, False, 0.0, False, "FAIL_MEMBERSHIP_UNSIGNED"),
        ("CTRL4292_2_direct_shell", False, False, False, False, True, 0.0, False, "FAIL_DIRECT_SHELL_REJECTED"),
        ("CTRL4292_3_no_flux_local", False, False, False, True, False, 0.0, True, "PASS_LOCAL_NO_FLUX_SELECTOR_ONLY"),
        ("CTRL4292_4_epsilon_inside_capacity", False, False, False, False, False, 0.01, True, "PASS_RESIDUAL_CAPACITY_PRIVATE"),
        ("CTRL4292_5_epsilon_exceeds_capacity", False, False, False, False, False, 0.1, False, "FAIL_EPSILON_EXCEEDS_PRIVATE_CAPACITY"),
        ("CTRL4292_6_multipole_live", True, True, False, True, False, 0.0, False, "FAIL_MULTIPOLE_NOT_ABSORBABLE"),
    ]
    rows = []
    for control_id, membership, monopole_only, multipoles_zero, no_flux, direct_shell, eps_abs, expected, expected_outcome in controls:
        if direct_shell:
            actual = False
            outcome = "FAIL_DIRECT_SHELL_REJECTED"
        elif membership and monopole_only and multipoles_zero:
            actual = True
            outcome = "PASS_HILBERT_MEMBERSHIP_MONOPOLE_ABSORBED"
        elif no_flux and eps_abs == 0.0 and not membership:
            actual = True
            outcome = "PASS_LOCAL_NO_FLUX_SELECTOR_ONLY"
        elif eps_abs > 0.0:
            actual = eps_abs <= EPSILON_UNIT_BOUND + 1.0e-15
            outcome = "PASS_RESIDUAL_CAPACITY_PRIVATE" if actual else "FAIL_EPSILON_EXCEEDS_PRIVATE_CAPACITY"
        elif membership and not multipoles_zero:
            actual = False
            outcome = "FAIL_MULTIPOLE_NOT_ABSORBABLE"
        elif not membership:
            actual = False
            outcome = "FAIL_MEMBERSHIP_UNSIGNED"
        else:
            actual = False
            outcome = "FAIL_UNCLASSIFIED_RESIDUAL"
        rows.append(
            {
                **common(),
                "control_id": control_id,
                "membership_parent_signed": str(membership),
                "monopole_only": str(monopole_only),
                "multipoles_zero": str(multipoles_zero),
                "local_no_flux_selector": str(no_flux),
                "direct_shell_source_attempt": str(direct_shell),
                "epsilon_mu_tr_abs": f"{eps_abs:.16g}",
                "epsilon_mu_tr_private_capacity": f"{EPSILON_UNIT_BOUND:.16g}",
                "actual_pass": str(actual),
                "expected_pass": str(expected),
                "outcome": outcome,
                "expected_outcome": expected_outcome,
                "expected_matches_actual": str(actual == expected and outcome == expected_outcome),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4292_0",
            "decision": DECISION,
            "what_moved": "PiM/Htau is out of the way inside the private selector; transition membership is now a precise parent-source-action/support clause.",
            "not_claimed": "raw Solar transition shell safety; public local-GR; empirical R10/PPN/WEP pass",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4292_0_no_direct_shell", "Raw transition shell projection is rejected by 4284 and cannot be reused as local-GR evidence."),
        ("FW4292_1_no_no_flux_overreach", "Local no-flux selector is not a global same-worldtube membership proof."),
        ("FW4292_2_no_Gcal_hiding", "mu_extra_tr cannot be absorbed into calibrated G_cal."),
        ("FW4292_3_no_monopole_overreach", "Absorbing l=0 does not absorb multipoles, range hair, frame/species leakage or beta residuals."),
        ("FW4292_4_nonclaim", "All rows are private nonclaim until parent membership or shared empirical bounds exist."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4292_0",
            "result": "MEMBERSHIP_CONDITIONAL_NONEH_MONOPOLE_SHARED_VECTOR_READY",
            "membership_parent_signed": "False",
            "local_no_flux_selector_available": "True",
            "direct_shell_route_rejected": "True",
            "epsilon_mu_tr_private_capacity_seed": f"{EPSILON_UNIT_BOUND:.16g}",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4292_0",
            "next_target": NEXT_TARGET,
            "objective": "Use real/source-backed local bounds to score epsilon_mu_tr across WEP, R10, PPN, clocks and orbital source-normalization channels.",
            "why": "Membership is a conditional selector; the executable route is now the shared residual vector.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 308 transition membership and non-EH monopole zero or shared residual vector

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Result

4292 separates three routes that were getting blurred.

### Route A: Hilbert Membership

If the parent action contains a same-source transition term:

```text
S_src -> S_src + S_tr^H[g_obs, psi_tr],
T_tr^H = -(2/sqrt(-g_obs)) delta S_tr^H/delta g_obs,
supp J_tr^H subset W_H = closure(supp J_H_total),
```

then the monopole part is ordinary source dressing:

```text
M_H^dress -> M_H^dress + M_tr^H,
Phi_N = -G_cal (M_H^dress + M_tr^H)/r.
```

Inside that selector:

```text
mu_extra_tr = 0,
epsilon_mu_tr = 0
```

for the Hilbert-owned l=0 component.

But this membership is **not parent-signed** for the raw transition shell in the current corpus.

### Route B: Local No-Flux Selector

The local boundary/no-flux branch can set:

```text
J_tr^nu = Pi_loc nabla_mu T_cross^{{mu nu}} = 0
```

inside compact local collars when its clauses are signed. That is useful, but it is not the same as proving the Solar transition shell is a direct Hilbert source.

### Route C: Direct Shell Source

The direct local metric shell route is rejected by 4284:

```text
raw P_metric,loc q_tr direct source = not safe.
```

## Live Residual Vector

Therefore the executable route is the shared residual vector:

```text
epsilon_mu_tr = mu_extra_tr/(G_cal M_H^dress),
Q_l>=1_tr,
dln_mu_tr_dt,
alpha_tr(lambda),
delta_frame_source,
eta_source_AB,
delta_beta_source,
A_J_residual_tr.
```

The first seed bound from 4290 remains:

```text
|epsilon_mu_tr| <= {EPSILON_UNIT_BOUND:.16g}
```

at `Pi_B_tr={TRANSITION_PIB:.16g}`, `T_res/tau_L=1`, and `|c_Gamma|=1`.

## Meaning

This is progress because the target is no longer "the coupling" in general.

The next executable job is:

```text
score epsilon_mu_tr across WEP, R10, PPN, clocks and orbital source-normalization bounds.
```

No direct shell claim, no closure smuggling, and no hiding `mu_extra_tr` inside `G_cal`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4292 Y5 R2FR transition membership and non-EH monopole zero or shared residual vector

## Purpose

4292 tests whether the transition shell can be made a same-worldtube Hilbert source, and if not, pushes the residue into a real shared bound vector.

## Outcome

The Hilbert-membership theorem is clean but conditional:

```text
S_tr^H in same source action + same W_H before readout => mu_extra_tr=0 for l=0.
```

The current corpus does not parent-sign that membership for the raw transition shell.

## Next

Run `epsilon_mu_tr` as a shared residual against WEP/R10/PPN/clocks/orbital bounds.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    theorem = csv_rows(paths["membership_theorem"])
    audit = csv_rows(paths["membership_audit"])
    routes = csv_rows(paths["route_classifier"])
    shared = csv_rows(paths["epsilon_shared_vector"])
    controls = csv_rows(paths["control_runner"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4292_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited sources exist"),
        ("VAL4292_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4292_2_membership_conditional_not_signed",
            any(row["theorem_id"] == "MT4292_1_same_worldtube" and row["status"] == "REQUIRED_NOT_PARENT_SIGNED" for row in theorem)
            and any(row["audit_id"] == "MA4292_7_verdict" and row["status"] == "NOT_PARENT_SIGNED" for row in audit),
            "membership is conditional and not parent-signed",
        ),
        (
            "VAL4292_3_direct_shell_rejected",
            any(row["route_id"] == "ROUTE4292_C" and row["status"] == "REJECTED" for row in routes),
            "direct shell route is rejected",
        ),
        (
            "VAL4292_4_shared_epsilon_vector",
            any(row["symbol"] == "epsilon_mu_tr" and row["current_bound_or_status"] == f"{EPSILON_UNIT_BOUND:.16g}" for row in shared)
            and any(row["symbol"] == "Q_l_ge_1_tr" for row in shared),
            "epsilon_mu and multipole residual rows are present",
        ),
        (
            "VAL4292_5_control_expected_matches_actual",
            bool(controls) and all(row["expected_matches_actual"] == "True" for row in controls),
            "strict control runner has no expected/pass mismatch",
        ),
        ("VAL4292_6_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4292_7_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4292_8_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-133 private nonclaim row",
        ),
        ("VAL4292_9_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4292_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4292_SOURCE_REGISTER.csv",
        "membership_theorem": SOURCE_DIR / "P8_Y5_R2FR_4292_TRANSITION_MEMBERSHIP_THEOREM.csv",
        "membership_audit": SOURCE_DIR / "P8_Y5_R2FR_4292_TRANSITION_MEMBERSHIP_AUDIT.csv",
        "route_classifier": SOURCE_DIR / "P8_Y5_R2FR_4292_ROUTE_CLASSIFIER.csv",
        "epsilon_shared_vector": SOURCE_DIR / "P8_Y5_R2FR_4292_EPSILON_MU_SHARED_VECTOR.csv",
        "control_runner": SOURCE_DIR / "P8_Y5_R2FR_4292_CONTROL_RUNNER.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4292_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4292_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4292_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4292_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["membership_theorem"], membership_theorem_rows())
    write_csv(paths["membership_audit"], membership_audit_rows())
    write_csv(paths["route_classifier"], route_classifier_rows())
    write_csv(paths["epsilon_shared_vector"], epsilon_shared_rows())
    write_csv(paths["control_runner"], control_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4292 transition membership and epsilon_mu shared vector",
        (
            "4292 separates transition handling into Hilbert membership, local no-flux selector, rejected direct shell route, "
            "and shared residual vector. Hilbert membership would set `mu_extra_tr=0` for the l=0 component, but current sources "
            "do not parent-sign membership for the raw shell. The executable path is now the shared `epsilon_mu_tr` vector across "
            "WEP/R10/PPN/clocks/orbital tests."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4292 packet transition membership conditional residual vector ready",
        (
            "Packet update: transition shell membership is the live parent-action clause; direct shell projection is rejected, "
            "local no-flux remains selector-only, and `epsilon_mu_tr` is ready for shared empirical/theorem-bound scoring."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(f"{CHECKPOINT}: epsilon_mu_tr private capacity seed={EPSILON_UNIT_BOUND:.12e}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
