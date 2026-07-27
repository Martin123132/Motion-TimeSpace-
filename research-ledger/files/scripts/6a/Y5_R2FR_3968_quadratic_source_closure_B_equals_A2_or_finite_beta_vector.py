from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3968"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3968-Y5-R2FR-quadratic-source-closure-B-equals-A2-or-finite-beta-vector.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3968_SOURCE_REGISTER.csv",
    "square_law": SRC / "P8_Y5_R2FR_3968_SINGLE_MASS_SQUARE_LAW_THEOREM.csv",
    "premises": SRC / "P8_Y5_R2FR_3968_PARENT_PREMISE_TESTS.csv",
    "obstructions": SRC / "P8_Y5_R2FR_3968_BETA_SQUARE_LAW_OBSTRUCTION_VECTOR.csv",
    "feed": SRC / "P8_Y5_R2FR_3968_BETA_VECTOR_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3968_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3968_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3968_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3968_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3968_VALIDATION.csv",
}

NEXT_DOC = "3969-Y5-R2FR-single-exterior-mass-uniqueness-or-beta-obstruction-bounds.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3969_single_exterior_mass_uniqueness_or_beta_obstruction_bounds.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3968_00_3967_next", SRC / "P8_Y5_R2FR_3967_NEXT_TARGET.csv", "NEXT3967_0", "3967 handoff"),
        ("SRC3968_01_beta_law", SRC / "P8_Y5_R2FR_3967_BETA_AB_LAW_ROLLED_FORWARD.csv", "BLAW3967_2_beta_exact", "beta_eff exact law"),
        ("SRC3968_02_ppn_theorem", SRC / "P8_Y5_R2FR_3967_PPN_STABILITY_THEOREM_OR_BOUND.csv", "PPN3967_2_beta_AB_law", "PPN beta square condition"),
        ("SRC3968_03_ppn_vector", SRC / "P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv", "DPPN3967_1_beta_source", "delta_beta_source row"),
        ("SRC3968_04_feed", SRC / "P8_Y5_R2FR_3967_LOCAL_GR_GATE_FEED_UPDATE.csv", "LGF3967_1_beta_total_update", "delta_beta_total feed"),
        ("SRC3968_05_claim", SRC / "P8_Y5_R2FR_3967_CLAIM_GATE.csv", "CLG3967_4_local_GR_claim", "local GR claim block"),
        ("SRC3968_06_eh_attempt", SRC / "P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv", "T506_EH_plus_silent_reduction", "EH plus silence reduction"),
        ("SRC3968_07_eh_requirements", SRC / "P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv", "EH505_4_source_measure_calibration", "source-measure calibration requirement"),
        ("SRC3968_08_min_parent_chain", SRC / "P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv", "DC511_5", "weak-field PPN vector compute step"),
        ("SRC3968_09_min_parent_residual", SRC / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv", "AR511_7_metric_PPN_tail", "metric PPN tail blocker"),
        ("SRC3968_10_einstein_lhs", SRC / "P8_Y5_GR_LEFT_HAND_GATE_2619_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv", "ELH2619_1_EH_variation_template", "EH variation template"),
        ("SRC3968_11_newton_ppn", SRC / "P8_Y5_GR_LEFT_HAND_GATE_2619_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv", "NWF2619_3_ppn_gamma_beta", "PPN bridge template"),
        ("SRC3968_12_operator_pack", SRC / "P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv", "ORP2619_7_source_normalization", "source normalization residual"),
        ("SRC3968_13_beta_vector", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_6_total_abs", "finite beta source vector"),
        ("SRC3968_14_r11_beta", SRC / "P8_Y5_NO_SHADOW_2515_R11_BETA_RESIDUAL_VECTOR.csv", "R11_2515_08", "source-normalization operator beta channel"),
        ("SRC3968_15_kappa", SRC / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "LAW2576_5_kappa_v", "second-order coupling ledger"),
        ("SRC3968_16_pg9", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG9_second_order_source_stability", "second-order source stability contract"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def square_law_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SQL3968_0_problem",
            "claim_piece": "beta square law target",
            "mathematical_form": "delta_beta_source = B_source/A_source^2 - 1",
            "derivation": "3967 showed beta=1 requires B_source=A_source^2 after fixed observed GM",
            "status": "TARGET_EXACT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SQL3968_1_single_mass_exterior_proposition",
            "claim_piece": "single exterior mass implies square law",
            "mathematical_form": "g_00= -1 + 2 mu/r c^-2 - 2 mu^2/r^2 c^-4 + O(c^-6), with mu=A_source mu_0",
            "derivation": "write W=mu_0/r, then g_00=-1+2 A_source W/c^2-2 A_source^2 W^2/c^4+O(c^-6), so B_source=A_source^2",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SQL3968_2_why_this_is_not_smuggling",
            "claim_piece": "parent route contract",
            "mathematical_form": "single mass exterior = EH-dominant local metric + one parent-owned monopole + same observed readout",
            "derivation": "the square follows from single-parameter exterior geometry, but MTS must still derive the premises from its parent action",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SQL3968_3_multi_charge_obstruction",
            "claim_piece": "why beta catches hidden source sectors",
            "mathematical_form": "U=sum_i A_i W_i but U^2 terms contain B_ij W_i W_j; beta=1 requires B_ij=A_i A_j for all i,j",
            "derivation": "any independent source charge, boundary mass, projector stress, or readout tail creates a separate quadratic coefficient unless locked to the same monopole",
            "status": "OBSTRUCTION_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SQL3968_4_square_law_residual",
            "claim_piece": "finite fallback",
            "mathematical_form": "Delta_B_square := B_source - A_source^2; delta_beta_source=Delta_B_square/A_source^2",
            "derivation": "if the parent single-mass theorem is not signed, Delta_B_square becomes the finite beta source residual",
            "status": "RESIDUAL_BRANCH_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def premise_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PREM3968_0_EH_dominance", "local exterior operator is EH plus silent/bounded residual", "DeltaE_munu=0 or below PPN locks", "open_conditional"),
        ("PREM3968_1_single_monopole", "all exterior 1/r charge is one parent-owned mass parameter", "mu_ext = G_eff M_eff with no mu_extra, boundary, projector, or memory monopole", "open_conditional"),
        ("PREM3968_2_same_metric_readout", "g00 used for clocks/orbits/PPN is the same metric sourced by the parent equation", "no post-variation coframe/readout/gauge mass redefinition", "open_conditional"),
        ("PREM3968_3_source_measure_glue", "worldtube Hilbert source equals exterior charge", "B_xi/G_eff=M_eff[Pi_M J_H] and Delta_cal=0 or bounded", "open_conditional"),
        ("PREM3968_4_no_second_source_prefactor", "no independent source-only quadratic prefactor", "matter/source weights cannot generate B_source != A_source^2", "not_signed"),
        ("PREM3968_5_no_hidden_quadratic_stress", "q_loc, boundary/domain/projector, and R11 sectors have no O(U^2) stress", "all beta obstruction rows theorem-zero or finite-bounded", "not_signed"),
        ("PREM3968_6_fixed_coupling", "kappa_MTS, ell_J, and source scale are fixed before readout", "no kappa_coupling or ell_J second-order drift in kappa_v", "not_signed"),
    ]
    return [
        {
            "premise_id": premise_id,
            "premise": premise,
            "required_identity": identity,
            "current_status": status,
            "effect_if_true": "supports B_source=A_source^2 and beta=1 under fixed observed GM",
            "effect_if_false": "feeds Delta_B_square and delta_beta_source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for premise_id, premise, identity, status in specs
    ]


def obstruction_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("OBS3968_0_single_mass", "Delta_B_single_mass", "exterior has more than one parent-owned monopole", "mu_ext != one constant mass parameter", "prove single-exterior-mass uniqueness or bound extra monopoles"),
        ("OBS3968_1_EH_operator", "Delta_B_operator", "non-EH/R11 operator changes nonlinear g00 coefficient", "DeltaE_munu contributes at O(U^2)", "EH operator selection or R11 beta coefficient vector"),
        ("OBS3968_2_source_prefactor", "Delta_B_source_prefactor", "source-only matter prefactor has independent quadratic response", "B_source != A_source^2 from source weights", "no-source-only theorem or finite source-weight kernel"),
        ("OBS3968_3_q_loc", "Delta_B_q_loc", "q_loc contributes to second-order source equation", "q_loc^{nu}_{O(U^2)} != 0", "second-order Ward zero or q_loc beta projection"),
        ("OBS3968_4_PiM", "Delta_B_PiM", "Pi_M/source measure varies at second order", "delta^2(Pi_M J_H) not locked to mass square", "Pi_M chain-map/variation theorem or finite coefficient"),
        ("OBS3968_5_boundary_domain", "Delta_B_boundary_domain", "boundary/domain/projector stress carries beta tail", "B gains boundary/domain U^2 term", "topological no-flux or boundary beta bound"),
        ("OBS3968_6_readout", "Delta_B_readout", "readout/gauge/coframe transforms beta after variation", "U fixed after readout differs from source U through O(U^2)", "fixed-before-readout theorem through second order"),
        ("OBS3968_7_coupling", "Delta_B_coupling", "kappa_MTS or ell_J drifts at second order", "kappa_coupling in kappa_v is nonzero", "constant coupling/source-current scale theorem or bound"),
        ("OBS3968_8_total", "Delta_B_square_abs", "absolute square-law obstruction envelope", "B_source-A_source^2=sum obstruction terms", "all terms theorem-zero or finite-sourced under no cancellation"),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "failure_mode": failure,
            "failure_form": form,
            "zero_or_bound_requirement": requirement,
            "feeds": "delta_beta_source; delta_beta_total; Delta_PPN_source_abs",
            "score_term": f"|{symbol}|",
            "status": "RETAINED_SYMBOLIC_RESIDUAL",
            "score_ready": True,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, symbol, failure, form, requirement in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BFEED3968_0_Delta_B_square",
            "target": "Delta_B_square",
            "update_formula": "Delta_B_square := B_source-A_source^2 = Delta_B_single_mass+Delta_B_operator+Delta_B_source_prefactor+Delta_B_q_loc+Delta_B_PiM+Delta_B_boundary_domain+Delta_B_readout+Delta_B_coupling",
            "meaning": "the beta source gap is now decomposed by physical cause instead of left as an unfilled coefficient",
            "status": "SYMBOLIC_DECOMPOSITION_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BFEED3968_1_delta_beta_source",
            "target": "delta_beta_source",
            "update_formula": "delta_beta_source = Delta_B_square/A_source^2",
            "meaning": "if single-mass square law fails, the finite obstruction becomes the beta source residual",
            "status": "EXACT_FORMULA_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BFEED3968_2_no_cancellation_bound",
            "target": "delta_beta_source_abs",
            "update_formula": "|delta_beta_source| <= (sum_i |Delta_B_i|)/|A_source|^2",
            "meaning": "no cancellation credit between independent source/operator/readout obstructions",
            "status": "BOUND_BRANCH_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BFEED3968_3_local_GR",
            "target": "local_GR_source_branch",
            "update_formula": "local_GR beta pass requires Delta_B_square=0 or |Delta_B_square|/A_source^2 below beta lock, plus non-beta PPN vector closure",
            "meaning": "this is the narrowest next proof target for local GR after Newton",
            "status": "NEXT_GATE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3968_0_conditional_proof_found",
            "status": "SINGLE_MASS_IMPLIES_B_EQUALS_A2",
            "meaning": "if MTS derives a single parent-owned exterior mass parameter in an EH-dominant observed metric, the beta square law follows directly",
            "claim_status": "conditional_not_parent_signed",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3968_1_parent_gap_identified",
            "status": "NEED_SINGLE_EXTERIOR_MASS_UNIQUENESS",
            "meaning": "the remaining proof is not beta algebra; it is uniqueness of the exterior mass/source parameter and silence of hidden quadratic sectors",
            "claim_status": "blocks_local_GR_until_closed_or_bounded",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "D3968_2_finite_fallback",
            "status": "DELTA_B_SQUARE_VECTOR_READY",
            "meaning": "if the uniqueness theorem fails, beta becomes a finite obstruction vector that can be compared to the beta lock",
            "claim_status": "nonclaim_score_branch",
            "next_action": "fill obstruction coefficients or prove zeros",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3968_0_sources",
            "gate": "source register",
            "requirement": "all cited source paths and needles found",
            "status": "PASS_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3968_1_square_law",
            "gate": "B_source=A_source^2",
            "requirement": "single exterior mass parameter plus EH observed metric and no hidden U^2 source sectors",
            "status": "CONDITIONAL_PROOF_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3968_2_obstruction_vector",
            "gate": "Delta_B_square vector",
            "requirement": "all square-law failure modes mapped to explicit residual components",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3968_3_beta_claim",
            "gate": "PPN beta",
            "requirement": "Delta_B_square=0 or finite value below beta lock, plus operator/readout/source pieces closed",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3968_4_next",
            "gate": "next theorem",
            "requirement": "prove single-exterior-mass uniqueness or fill obstruction bounds",
            "status": "NEXT_TARGET_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3968_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive single-exterior-mass uniqueness for the local compact branch, or assign finite source/operator/readout obstruction bounds feeding Delta_B_square",
            "success_condition": "B_source=A_source^2 becomes parent-signed through single monopole exterior geometry, or Delta_B_square gets finite nonclaim rows under the beta comparator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "SINGLE_MASS_SQUARE_LAW_CONDITIONAL_PROOF_AND_OBSTRUCTION_VECTOR_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "proved B=A^2 conditionally from one parent-owned exterior mass parameter; retained Delta_B_square obstruction vector for unsatisfied parent premises",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3968 - Quadratic Source Closure B Equals A2 Or Finite Beta Vector

Timestamp: `{timestamp}`

## Result

3968 takes the direct derivation route.

The square law is conditionally proven from a single exterior mass parameter:

```text
g_00 = -1 + 2 mu/(r c^2) - 2 mu^2/(r^2 c^4) + O(c^-6)
mu = A_source mu_0
W = mu_0/r

therefore

g_00 = -1 + 2 A_source W/c^2 - 2 A_source^2 W^2/c^4 + O(c^-6)
B_source = A_source^2
beta_eff = B_source/A_source^2 = 1
```

That is the clean route. It does **not** yet prove MTS local GR, because MTS still has to derive the premises:

- EH-dominant observed exterior metric;
- one parent-owned exterior monopole;
- source/worldtube/Gauss charge equality;
- same metric/coframe readout through second order;
- no hidden `q_loc`, boundary/domain/projector, R11, or coupling `U^2` stress.

## Finite Fallback

If those premises do not close:

```text
Delta_B_square := B_source - A_source^2
delta_beta_source = Delta_B_square/A_source^2
|delta_beta_source| <= (sum_i |Delta_B_i|)/|A_source|^2
```

So the beta problem is no longer vague. It is either the single-mass exterior theorem, or a finite obstruction vector.

## Source Intake

Source needles found: `{found}/{len(sources)}`.

## Decision

Next target: prove single-exterior-mass uniqueness for the compact local branch, or fill finite obstruction rows.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3968 - Quadratic Source Square Law

- Timestamp: `{timestamp}`
- Status: `SINGLE_MASS_SQUARE_LAW_CONDITIONAL_PROOF_AND_OBSTRUCTION_VECTOR_READY`
- Conditional derivation:
  `g_00=-1+2mu/(rc^2)-2mu^2/(r^2c^4)+...`, `mu=A_source mu_0` implies `B_source=A_source^2` and `beta_eff=1`.
- Remaining parent proof: derive one parent-owned exterior mass parameter in an EH-dominant observed metric with no hidden `U^2` source/readout/operator sectors.
- Fallback:
  `Delta_B_square=B_source-A_source^2`,
  `delta_beta_source=Delta_B_square/A_source^2`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3968 - Quadratic Source Square Law"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    sources = source_register_rows(timestamp)
    return {
        "sources": sources,
        "square_law": square_law_rows(timestamp),
        "premises": premise_rows(timestamp),
        "obstructions": obstruction_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    square_law = rows["square_law"]
    premises = rows["premises"]
    obstructions = rows["obstructions"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    obstruction_symbols = {row["symbol"] for row in obstructions}
    needed_obstructions = {
        "Delta_B_single_mass",
        "Delta_B_operator",
        "Delta_B_source_prefactor",
        "Delta_B_q_loc",
        "Delta_B_PiM",
        "Delta_B_boundary_domain",
        "Delta_B_readout",
        "Delta_B_coupling",
        "Delta_B_square_abs",
    }

    return [
        val("VAL3968_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3968_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3968_02_square_law", any(row["row_id"] == "SQL3968_1_single_mass_exterior_proposition" and "B_source=A_source^2" in row["derivation"] for row in square_law), "single-mass square-law proposition written"),
        val("VAL3968_03_not_smuggled", any(row["status"] == "CONDITIONAL_NOT_PARENT_SIGNED" for row in square_law), "conditional status prevents GR smuggling"),
        val("VAL3968_04_premises", len(premises) >= 7 and any(row["premise_id"] == "PREM3968_1_single_monopole" for row in premises), "parent premise tests written"),
        val("VAL3968_05_obstruction_vector", needed_obstructions <= obstruction_symbols, "Delta_B_square obstruction vector complete"),
        val("VAL3968_06_feed", {"Delta_B_square", "delta_beta_source", "delta_beta_source_abs", "local_GR_source_branch"} <= {row["target"] for row in feed}, "beta/local-GR feed rows present"),
        val("VAL3968_07_decision", any(row["status"] == "NEED_SINGLE_EXTERIOR_MASS_UNIQUENESS" for row in decisions), "decision selects single-exterior-mass uniqueness next"),
        val("VAL3968_08_claim_gate", any(row["status"] == "BLOCKED_NONCLAIM" for row in claims), "claim gate blocks beta/local-GR promotion"),
        val("VAL3968_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to single exterior mass uniqueness or bounds"),
        val("VAL3968_10_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3968_11_score_ready", all(row["score_ready"] for row in obstructions), "obstruction rows are score-ready symbolics"),
        val("VAL3968_12_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3968_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3968_14_spine_updated", SPINE_PATH.exists() and "3968 - Quadratic Source Square Law" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3968_15_csv_parse", parsed, parse_detail),
        val("VAL3968_16_script_compile", True, "script compiled before validation write"),
        val("VAL3968_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["square_law"], rows["square_law"])
    write_csv(OUTPUTS["premises"], rows["premises"])
    write_csv(OUTPUTS["obstructions"], rows["obstructions"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3968 validation failed: {failed}")

    print(f"3968 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Single-mass square-law theorem and Delta_B_square obstruction vector assembled")


if __name__ == "__main__":
    run()
