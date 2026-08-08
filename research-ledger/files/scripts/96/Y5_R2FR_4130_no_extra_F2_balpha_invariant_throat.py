from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4130-Y5-R2FR-no-extra-F2-balpha-invariant-throat.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_NO_EXTRA_F2_BALPHA_INVARIANT_THROAT_4130"
CHECKPOINT_ID = "4130"
DECISION = "BALPHA_INVARIANT_THROAT_DERIVED_NO_EXTRA_F2_PARENT_ZERO_UNSIGNED_BOUND_SCHEMAS_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4130_00_4129_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4129_NEXT_TARGET.csv",
        "4130-Y5-R2FR-no-extra-F2-balpha-invariant-throat.md",
        "4129 selected no-extra-F2 / b_alpha invariant throat.",
    ),
    "SRC4130_01_4129_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4129_STATUS.csv",
        "STANDARD_VISIBLE_EM_BASELINE_LOCKED_PARENT_OWNER_UNSIGNED_DEVIATION_BOUNDS_FILLED",
        "Current-chain baseline EM lock and deviation-bound route.",
    ),
    "SRC4130_02_4129_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4129_FINITE_BOUND_SCHEMAS.csv",
        "FBR4129_3_b_alpha",
        "4129 b_alpha bound schema.",
    ),
    "SRC4130_03_3994_no_extra_f2": (
        SOURCE_DIR / "P8_Y5_R2FR_3994_NO_EXTRA_F2_OPERATOR_DOMAIN_THEOREM.csv",
        "EXACT_LINEAR_IDENTITY_FOR_BOUND_BRANCH",
        "No-extra-F2 theorem, countermodel, and b_alpha identity.",
    ),
    "SRC4130_04_3995_joint_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3995_JOINT_ALPHA_F2_CURRENT_BOUND_ROWS.csv",
        "EXACT_INVARIANT_IDENTITY",
        "Joint alpha/F2/current invariant rows.",
    ),
    "SRC4130_05_3996_product": (
        SOURCE_DIR / "P8_Y5_R2FR_3996_BALPHA_SOURCE_PRODUCT_VECTOR.csv",
        "EXECUTABLE_PRODUCT_VECTOR_READY",
        "b_alpha source product vector and source-slot tail.",
    ),
    "SRC4130_06_3865_joint": (
        SOURCE_DIR / "P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv",
        "EXACT_NONCLAIM_LINEAR_CONSTRAINT",
        "s_XF2/z_g/b_alpha joint constraint and arena schema.",
    ),
    "SRC4130_07_4019_no_extra_op": (
        SOURCE_DIR / "P8_Y5_R2FR_4019_NO_EXTRA_OPERATOR_THEOREM.csv",
        "FINITE_SCORER_INTERFACE",
        "No-extra-operator finite scorer interface.",
    ),
    "SRC4130_08_4043_alpha_xi": (
        SOURCE_DIR / "P8_Y5_R2FR_4043_ALPHA_XI_BOUND_VECTOR.csv",
        "PROJECTOR_STRESS_ZERO_IN_PRIVATE_BRANCH_ELSE_ACTIVE_BOUND_VECTOR",
        "PPN alpha/xi fallback vector.",
    ),
    "SRC4130_09_4090_alpha3": (
        SOURCE_DIR / "P8_Y5_R2FR_4090_ALPHA3_FALLBACK_PRODUCT_CONTRACT.csv",
        "NO_CANCELLATION_GUARD",
        "Alpha3 fallback product no-cancellation guard.",
    ),
    "SRC4130_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4130_no_extra_F2_balpha_invariant_throat.py",
        "Reproducible generator for this 4130 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def invariant_rows() -> List[dict]:
    data = [
        (
            "INV4130_0_action_coefficients",
            "z_g and s_XF2",
            "S_EM,J=-1/4 int lambda_A F_Q^2 + int g_J A_Q J_Q; z_g:=D_A ln g_J; s_XF2:=D_A ln lambda_A",
            "defines current/source normalization drift and direct F2 drift in the same vertical direction A_N",
            "DEFINITION_LOCK",
        ),
        (
            "INV4130_1_rescaling_law",
            "field/current rescaling",
            "A_Q -> exp(sigma) A_Q gives z_g -> z_g - D_A sigma and s_XF2 -> s_XF2 - 2 D_A sigma",
            "z_g and s_XF2 separately are partly convention-dependent",
            "EXACT_RESCALING_LAW",
        ),
        (
            "INV4130_2_balpha_invariant",
            "b_alpha",
            "b_alpha := 2 z_g - s_XF2",
            "b_alpha is invariant under the A_Q normalization gauge and is the physical alpha/source-coupling throat",
            "EXACT_GAUGE_INVARIANT_IDENTITY",
        ),
        (
            "INV4130_3_current_gauge_reduction",
            "same-current gauge",
            "choose D_A sigma=z_g => z_g'=0 and s_XF2'=-b_alpha",
            "when same-current owner permits this gauge, scoring can use b_alpha alone instead of separate z_g and s_XF2",
            "EXACT_CONDITIONAL_GAUGE_REDUCTION",
        ),
        (
            "INV4130_4_no_alpha_only_shortcut",
            "arena product",
            "arena_signal = P_alpha b_alpha + P_z z_g_tail + P_s s_XF2_tail + source_slot_tail",
            "alpha-only bounds are invalid unless the current/source-slot tails are zero or separately bounded",
            "NO_ALPHA_ONLY_SHORTCUT",
        ),
    ]
    rows: List[dict] = []
    for invariant_id, symbol, equation, meaning, status in data:
        row = row_base()
        row.update(
            {
                "invariant_id": invariant_id,
                "symbol": symbol,
                "equation": equation,
                "meaning": meaning,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def no_extra_f2_audit_rows() -> List[dict]:
    data = [
        (
            "F2A4130_0_countermodel",
            "ordinary symmetry countermodel",
            "DeltaS_F2=-1/4 int sqrt(-g_obs) lambda(Phi,readout,hidden) F_Q^2 is diffeomorphism and U(1) gauge invariant",
            "ordinary covariance plus U(1) gauge symmetry does not ban extra F2",
            "COUNTERMODEL_RETAINED_NO_SHORTCUT",
        ),
        (
            "F2A4130_1_image_theorem",
            "parent image/no-extra-F2 theorem",
            "Allowed[S_vis]=Image(ParentGenerate) contains Q-subblock only as C_P N_Q F_Q^2 with no separate Coeff(F_Q^2) and no hidden/readout Hom into it",
            "if parent-signed, D_A lambda_F2=D_A f_X=D_A delta_lambda_rad=0",
            "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED",
        ),
        (
            "F2A4130_2_baseline_branch",
            "standard visible EM baseline",
            "lambda_A is the calibrated constant Maxwell coefficient and no MTS hidden/readout F2 operator is included",
            "C_XF2=s_XF2=0 by baseline matter-sector import, not an MTS prediction",
            "BASELINE_ZERO_NOT_PARENT_PREDICTION",
        ),
        (
            "F2A4130_3_parent_prediction",
            "MTS parent-owned no-extra-F2",
            "requires typed parent object language, image theorem, same-current owner, radiative/readout closure, and no hidden-to-F2 morphism",
            "not signed by current corpus",
            "PARENT_ZERO_UNSIGNED",
        ),
        (
            "F2A4130_4_fallback",
            "finite b_alpha branch",
            "if no-extra-F2 is unsigned, retain b_alpha and source-slot tails with no-cancellation absolute products",
            "turns F2/current ambiguity into a test vector",
            "BOUND_BRANCH_ACTIVE",
        ),
    ]
    rows: List[dict] = []
    for audit_id, clause, formula, implication, status in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "clause": clause,
                "formula": formula,
                "implication": implication,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def balpha_bound_rows() -> List[dict]:
    data = [
        (
            "BND4130_0_balpha_master",
            "b_alpha",
            "b_alpha=2 z_g-s_XF2",
            "dimensionless per normalized A_N",
            "primary invariant to score MTS EM/alpha/source deviations",
            "clock;spectroscopy;R10;WEP;source-normalization",
            "source-backed b_alpha projection or theorem zero",
        ),
        (
            "BND4130_1_clock",
            "clock_alpha_product",
            "|S_alpha b_alpha dot(A_N)| <= |clock_drift_limit| - residual_budget",
            "time^-1",
            "clock tests constrain alpha drift only after A_N profile and sensitivity S_alpha are specified",
            "clock;fine-structure drift",
            "S_alpha;dot(A_N);clock bound;non-alpha residuals",
        ),
        (
            "BND4130_2_spectroscopy",
            "spectroscopy_alpha_product",
            "|K_alpha b_alpha DeltaA_N| <= |Delta_nu/nu|_limit - residual_budget",
            "dimensionless frequency ratio",
            "spectroscopy constrains b_alpha through transition sensitivity coefficients",
            "spectroscopy;alpha variation",
            "K_alpha;DeltaA_N;transition data;calibration residuals",
        ),
        (
            "BND4130_3_R10",
            "R10_alpha_source_product",
            "alpha_R10(lambda)=K_alpha(lambda) b_alpha_S b_alpha_T tau_alpha(lambda)/M_alpha^2 + source_tail",
            "dimensionless alpha(lambda)",
            "short-range tests score b_alpha only with source/test projection and no-cancellation tails",
            "R10;fifth-force;source coupling",
            "K_alpha;tau_alpha;M_alpha^2;source/test b_alpha;alpha_bound(lambda)",
        ),
        (
            "BND4130_4_WEP",
            "WEP_alpha_product",
            "eta_EM_source <= readout_floor*|Qe_Earth DeltaQe|*(|b_alpha|+source_slot_tail)",
            "dimensionless eta",
            "WEP constrains differential EM source response but not universal common mode alone",
            "WEP;composition;EM binding",
            "Qe maps;readout_floor;eta bound;source-slot tail",
        ),
        (
            "BND4130_5_PPN_alpha_xi",
            "PPN_alpha_xi_projection",
            "Delta_alpha_xi <= |W_alpha b_alpha| + |W_domain epsilon_domain| + source_tail",
            "dimensionless PPN residual",
            "PPN alpha_i/xi rows require product-level bounds and no cancellation between channels",
            "PPN alpha1 alpha2 alpha3 xi zeta",
            "W_alpha;epsilon_domain;PPN bounds;coframe/source denominator",
        ),
    ]
    rows: List[dict] = []
    for bound_id, target, formula, units, meaning, observable_links, required_inputs in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "target": target,
                "formula": formula,
                "units": units,
                "meaning": meaning,
                "observable_links": observable_links,
                "required_inputs": required_inputs,
                "status": "NONCLAIM_BOUND_SCHEMA_FILLED",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def product_gate_rows() -> List[dict]:
    data = [
        (
            "PG4130_0_source_product",
            "B_EM_source",
            "|b_alpha|+|Dln c_pre|+|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|z_rad|",
            "source-slot tail is the next real obstruction after invariant reduction",
            "SOURCE_PRODUCT_VECTOR_READY_INPUTS_MISSING",
        ),
        (
            "PG4130_1_no_cancellation",
            "absolute product guard",
            "each b_alpha/source-slot/PPN channel must pass individually unless a parent identity sets it exactly zero",
            "prevents hiding alpha/source residuals through fitted cancellations",
            "NO_CANCELLATION_GUARD",
        ),
        (
            "PG4130_2_common_scalar",
            "Dln w_common",
            "common scalar source/G calibration shifts universal source strength and must be owned by G_ref/action-scale or bounded by Gdot/PPN/source calibration",
            "connects alpha throat back to the main common coupling problem",
            "COMMON_G_CALIBRATION_NEXT_PRESSURE",
        ),
    ]
    rows: List[dict] = []
    for gate_id, target, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "target": target,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4130_0_invariant_reduction",
            "The EM alpha/source branch is reduced to the gauge-invariant throat b_alpha=2 z_g-s_XF2; z_g and s_XF2 alone are convention-sensitive.",
            "INVARIANT_THROAT_DERIVED",
            "score b_alpha plus explicit source-slot tails, not alpha-only shortcuts",
        ),
        (
            "DEC4130_1_no_extra_F2_unsigned",
            "Ordinary diffeo plus U(1) symmetry does not ban extra F2 operators; the parent image/no-extra-F2 theorem is exact but unsigned.",
            "PARENT_NO_EXTRA_F2_UNSIGNED",
            "keep b_alpha bound branch active",
        ),
        (
            "DEC4130_2_baseline_zero",
            "Standard visible EM baseline has C_XF2=s_XF2=b_alpha=0 by imported matter-sector definition, not by MTS prediction.",
            "BASELINE_ZERO_NOT_PREDICTION",
            "safe for local-GR baseline tests, not for public alpha derivation claims",
        ),
        (
            "DEC4130_3_bounds",
            "b_alpha now has nonclaim bound schemas for clock, spectroscopy, R10, WEP, and PPN alpha/xi arenas.",
            "BOUND_SCHEMAS_FILLED",
            "next target should attack source-slot tail and common-G calibration",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4130_0",
            "result": DECISION,
            "summary": (
                "4130 derives the gauge-invariant alpha/source throat b_alpha=2 z_g-s_XF2 and blocks alpha-only shortcuts. "
                "The no-extra-F2 parent image theorem remains unsigned because ordinary diffeomorphism and U(1) symmetry allow "
                "countermodel F_Q^2 coefficients. The standard visible EM baseline sets C_XF2/s_XF2/b_alpha to zero by imported "
                "matter-sector definition, while MTS-specific deviations now have nonclaim bound schemas for clocks, spectroscopy, "
                "R10, WEP, and PPN alpha/xi arenas."
            ),
            "balpha_invariant_derived": "True",
            "parent_no_extra_F2_signed": "False",
            "bound_schemas_filled": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4131 source-slot tail and common-G calibration",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4130_0",
            "target_doc": "4131-Y5-R2FR-source-slot-tail-and-common-G-calibration.md",
            "target_script": "scripts/Y5_R2FR_4131_source_slot_tail_and_common_G_calibration.py",
            "objective": (
                "attack the source-slot tail |Dln c_pre|+|Dln w_rel|+|Dln kappa_A|+|Dln R_A|+|z_rad| and the common scalar "
                "Dln w_common; try to prove they are fixed calibration/representation data, or fill Gdot/PPN/WEP/R10 bound rows"
            ),
            "success_gate": "source-slot tail and common-G calibration are parent-zero, or each live term has a nonclaim bound schema with units and arena links",
            "reason": "4130 compresses EM alpha/F2/current ambiguity into b_alpha plus source-slot/common-G tails.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4130_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4130_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4130_INVARIANT_IDENTITY": SOURCE_DIR / "P8_Y5_R2FR_4130_INVARIANT_IDENTITY.csv",
        "P8_Y5_R2FR_4130_NO_EXTRA_F2_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4130_NO_EXTRA_F2_AUDIT.csv",
        "P8_Y5_R2FR_4130_BALPHA_BOUND_SCHEMAS": SOURCE_DIR / "P8_Y5_R2FR_4130_BALPHA_BOUND_SCHEMAS.csv",
        "P8_Y5_R2FR_4130_PRODUCT_GATES": SOURCE_DIR / "P8_Y5_R2FR_4130_PRODUCT_GATES.csv",
        "P8_Y5_R2FR_4130_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4130_DECISION_GATES.csv",
        "P8_Y5_R2FR_4130_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4130_STATUS.csv",
        "P8_Y5_R2FR_4130_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4130_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4130 - No-Extra-F2 / b_alpha Invariant Throat",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The physical EM alpha/source throat is the gauge-invariant `b_alpha=2 z_g-s_XF2`.",
        "- Ordinary diffeomorphism plus U(1) gauge symmetry does not ban extra `F_Q^2`; the parent image theorem is still unsigned.",
        "- Standard visible EM baseline has `b_alpha=0` by imported matter-sector definition, not by MTS prediction.",
        "- MTS-specific deviations now have clock, spectroscopy, R10, WEP, and PPN bound schemas.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Invariant Identity", "", "| invariant_id | symbol | status |", "|---|---|---|"])
    for row in invariant_rows():
        sections.append(f"| {row['invariant_id']} | {row['symbol']} | {row['status']} |")
    sections.extend(["", "## No-Extra-F2 Audit", "", "| clause | status | implication |", "|---|---|---|"])
    for row in no_extra_f2_audit_rows():
        sections.append(f"| {row['clause']} | {row['status']} | {row['implication']} |")
    sections.extend(["", "## Bound Schemas", "", "| target | units | observable_links |", "|---|---|---|"])
    for row in balpha_bound_rows():
        sections.append(f"| {row['target']} | {row['units']} | {row['observable_links']} |")
    sections.extend(["", "## Claim Ceiling", "", f"- {status['claim_state']}.", "- This checkpoint improves the scoring variable; it does not derive `alpha` or local GR.", "", "## Next Target", "", "- `4131-Y5-R2FR-source-slot-tail-and-common-G-calibration.md`", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4130_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4130_INVARIANT_IDENTITY": invariant_rows,
        "P8_Y5_R2FR_4130_NO_EXTRA_F2_AUDIT": no_extra_f2_audit_rows,
        "P8_Y5_R2FR_4130_BALPHA_BOUND_SCHEMAS": balpha_bound_rows,
        "P8_Y5_R2FR_4130_PRODUCT_GATES": product_gate_rows,
        "P8_Y5_R2FR_4130_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4130_STATUS": status_rows,
        "P8_Y5_R2FR_4130_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4130_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4130_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4130_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    invariant_text = flatten_rows([outputs["P8_Y5_R2FR_4130_INVARIANT_IDENTITY"]])
    invariant_ok = all(token in invariant_text for token in ["b_alpha := 2 z_g - s_XF2", "EXACT_GAUGE_INVARIANT_IDENTITY", "NO_ALPHA_ONLY_SHORTCUT"])
    add("VAL4130_3_invariant", "invariant identity and no alpha-only shortcut are present", invariant_ok, "invariant tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4130_NO_EXTRA_F2_AUDIT"]])
    audit_ok = all(token in audit_text for token in ["COUNTERMODEL_RETAINED_NO_SHORTCUT", "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_PARENT_SIGNED", "BASELINE_ZERO_NOT_PARENT_PREDICTION", "BOUND_BRANCH_ACTIVE"])
    add("VAL4130_4_f2_audit", "no-extra-F2 audit keeps countermodel, conditional theorem, baseline zero, and bound branch", audit_ok, "audit tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4130_BALPHA_BOUND_SCHEMAS"]])
    bound_ok = all(token in bound_text for token in ["clock_alpha_product", "spectroscopy_alpha_product", "R10_alpha_source_product", "WEP_alpha_product", "PPN_alpha_xi_projection"])
    add("VAL4130_5_bounds", "b_alpha bound schemas cover clock, spectroscopy, R10, WEP, and PPN", bound_ok, "bound tokens checked")

    product_text = flatten_rows([outputs["P8_Y5_R2FR_4130_PRODUCT_GATES"]])
    product_ok = all(token in product_text for token in ["B_EM_source", "NO_CANCELLATION_GUARD", "COMMON_G_CALIBRATION_NEXT_PRESSURE"])
    add("VAL4130_6_product_gates", "product gates include source tail, no-cancellation, and common-G pressure", product_ok, "product tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4130_DECISION_GATES"]])
    decision_ok = all(token in decision_text for token in ["INVARIANT_THROAT_DERIVED", "PARENT_NO_EXTRA_F2_UNSIGNED", "BASELINE_ZERO_NOT_PREDICTION", "BOUND_SCHEMAS_FILLED"])
    add("VAL4130_7_decisions", "decision gates record invariant, unsigned parent zero, baseline zero, and bounds", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4130_STATUS"])
    status_ok = bool(status) and status[0].get("result") == DECISION and status[0].get("balpha_invariant_derived") == "True" and status[0].get("parent_no_extra_F2_signed") == "False"
    add("VAL4130_8_status", "status records b_alpha invariant and unsigned parent no-extra-F2", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4130_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4131-Y5-R2FR-source-slot-tail-and-common-G-calibration.md"
    add("VAL4130_9_next_target", "next target is source-slot tail and common-G calibration", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4130_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4130*")) or any(FORMALIZATION.rglob("4130-Y5-R2FR*"))
    add("VAL4130_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4130_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4130_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
