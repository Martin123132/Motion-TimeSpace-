from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4320"
CLAIM_ID = "L-161"
BRANCH = "MTS_R2FR_Y5_HPERP_DQ_COMPONENT_CERTIFICATE_OR_FIRST_EPSILON_PROFILE_ROW_4320"
DECISION = "DQ_COMPONENTS_CLASSIFIED_SOURCE_READOUT_AND_GEOMETRY_PRIORITIZED_EPSILON_PROFILE_ROUTE_STAGED_NONCLAIM"
MARKER = "PPC4161_HPERP_DQ_COMPONENT_CERTIFICATE_OR_FIRST_EPSILON_PROFILE_ROW_4320"
PACKET_MARKER = "PPC4161_PACKET_HPERP_DQ_COMPONENT_CERTIFICATE_OR_FIRST_EPSILON_PROFILE_ROW_4320"
NEXT_TARGET = "4321-Y5-R2FR-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md"

FORMAL_PATH = FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md"
DOC_PATH = POST / "4320-Y5-R2FR-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4320_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4320_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4319_NEXT_TARGET.csv",
        "eight Dq_i[Hperp]",
        "4319 handoff selecting the eight Hperp Dq components.",
    ),
    "SRC4320_01_component_list": (
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Dq_source_readout[Hperp]",
        "4245 live component list.",
    ),
    "SRC4320_02_EDq": (
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "E_Dq,Hperp^2 := sum_i w_i epsilon_i^2",
        "4245 combined Hperp Dq defect.",
    ),
    "SRC4320_03_geometry_decomp": (
        FORMAL / "262-PPC4161-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md",
        "epsilon_Oloc",
        "4246 geometry epsilon decomposition.",
    ),
    "SRC4320_04_no_shadow_missing": (
        FORMAL / "263-PPC4161-motion-frame-no-shadow-signature-or-epsilon-geom-numeric-fill.md",
        "A_MF_PARENT_SIGNATURE_NOT_FOUND",
        "4247 blocks geometry zero until parent no-shadow is signed.",
    ),
    "SRC4320_05_geom_sampler": (
        FORMAL / "264-PPC4161-epsilon-geom-profile-sampler-or-coframe-shadow-bound-first-row.md",
        "P8_Y5_R2FR_4248_EPSILON_GEOM_PROFILE_INPUTS_CANDIDATE.csv",
        "4248 geometry profile sampler contract.",
    ),
    "SRC4320_06_component_map": (
        FORMAL / "274-PPC4161-component-zero-closure-or-epsilon-map.md",
        "The other seven components remain blocked",
        "4258 component map: geometry matured, other components still blocked.",
    ),
    "SRC4320_07_source_pairing": (
        FORMAL / "335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md",
        "S_cg_nonHilbert = S_A Hperp^A + R_src_readout",
        "4319 source/readout residual split.",
    ),
    "SRC4320_08_Nsrc_bound": (
        FORMAL / "335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md",
        "N_src_nonHilbert <= ||U_B||_inf (C_S C_perp E_Dq,Hperp + ||R_src_readout||)",
        "4319 finite Nsrc bound.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4320 classifies the eight Dq_i[Hperp] components needed by the 4319 finite Hperp/source-support bound. "
            "The combined defect remains E_Dq,Hperp^2=sum_i w_i epsilon_i^2 with epsilon_i>=||Dq_i[Hperp]||. "
            "The best next attack is not the already-mature geometry row but Dq_source_readout[Hperp], because source/readout "
            "feeds the 4319 result twice: through epsilon_source_readout inside E_Dq,Hperp and through the explicit residual "
            "R_src_readout in N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp+||R_src_readout||). Geometry is kept as "
            "the second target with the imported 4246-4248 envelope epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+"
            "epsilon_wall+epsilon_Hodge_geom. No component zero, local GR/Newton, R10, PPN, clock or orbital claim fires."
        ),
        (
            "4320 source register, Dq component status, geometry epsilon import, source-readout schema, EDq aggregation "
            "formulas, runner, firewall, decision, status, next-target and validation CSV."
        ),
        "private_Hperp_Dq_component_priority_and_source_readout_next_nonclaim",
        (
            "Parent-sign source/readout factorization through q or source epsilon_source_readout, R_src_readout, weights w_i, "
            "component epsilons, C_S, C_perp and U_B before feeding local tests."
        ),
        (
            "Treating generic Dq zeros as Hperp-specific zeros, deleting R_src_readout, claiming geometry no-shadow without "
            "A_MF parent signature, or using the EDq bound as a local-GR proof while drift/history/boundary/nonlinear gates remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def component_rows() -> List[Dict[str, str]]:
    specs = [
        (
            1,
            "Dq_source_readout[Hperp]",
            "PRIMARY_NEXT_TARGET",
            "source/readout factors through q, no Hperp source-label leg, readout projector commutes with quotient",
            "epsilon_source_readout >= ||Dq_source_readout[Hperp]|| and R_src_readout finite or zero",
            "E_Dq,Hperp and explicit R_src_readout",
            "highest leverage because it appears twice in 4319",
        ),
        (
            2,
            "Dq_geom[Hperp]",
            "MATURE_EPSILON_PROFILE_ROUTE",
            "A_MF/no-shadow for Hperp plus descended coframe/metric/Hodge/readout and no active wall",
            "epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+epsilon_wall+epsilon_Hodge_geom",
            "E_Dq,Hperp",
            "already decomposed in 4246-4248; keep second, not first",
        ),
        (
            3,
            "Dq_EM[Hperp]",
            "EM_HODGE_ROUTE_AVAILABLE",
            "same-Hodge visible EM branch with no independent constitutive/readout Hperp leg",
            "epsilon_EM >= ||Dq_EM[Hperp]|| with EM/Hodge residual envelope",
            "E_Dq,Hperp",
            "connect after source/readout and geometry because EM route is partly mature",
        ),
        (
            4,
            "Dq_tau[Hperp]",
            "REFERENCE_TIME_ROUTE_OPEN",
            "clock/reference tau descends through q with no Hperp clock-label leg",
            "epsilon_tau >= ||Dq_tau[Hperp]||",
            "E_Dq,Hperp and clock arena",
            "time/clock sensitivity likely important but not first in 4319 source bound",
        ),
        (
            5,
            "Dq_matter[Hperp]",
            "MATTER_DESCENT_ROUTE_OPEN",
            "matter labels and source mass function descend through q",
            "epsilon_matter >= ||Dq_matter[Hperp]||",
            "E_Dq,Hperp and source equality",
            "needed before claim, but harder than source/readout factorization row",
        ),
        (
            6,
            "Dq_boundary_projector[Hperp]",
            "BOUNDARY_DOMAIN_ROUTE_OPEN",
            "local projector/domain boundary is q-owned and has no Hperp wall leg",
            "epsilon_boundary_projector >= ||Dq_boundary_projector[Hperp]||",
            "E_Dq,Hperp and N_boundary_domain",
            "couples to remaining boundary/domain budget",
        ),
        (
            7,
            "Dq_theta_marker[Hperp]",
            "MARKER_SELECTOR_ROUTE_OPEN",
            "theta marker/selector is quotient-owned and has no active representative marker leg",
            "epsilon_theta_marker >= ||Dq_theta_marker[Hperp]||",
            "E_Dq,Hperp and selector drift",
            "selector problem remains real but is less direct than source/readout",
        ),
        (
            8,
            "Dq_coeff[Hperp]",
            "COEFFICIENT_DESCENT_ROUTE_OPEN",
            "local coefficients are parent-owned quotient functions, not fitted representative knobs",
            "epsilon_coeff >= ||Dq_coeff[Hperp]||",
            "E_Dq,Hperp and coefficient naturalness",
            "leave last unless parent coefficient map appears",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for rank, component, status, zero_route, fallback, feeds, note in specs:
        row = base_row()
        row.update(
            {
                "rank": str(rank),
                "component": component,
                "status": status,
                "zero_certificate_required": zero_route,
                "fallback_epsilon_row": fallback,
                "feeds": feeds,
                "source_basis": "4245 component list plus 4319 Nsrc bound",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def geometry_import_rows() -> List[Dict[str, str]]:
    specs = [
        ("epsilon_Oloc", "observed local metric/readout variation from Hperp", "ZERO_IF_OBSERVED_GEOMETRY_DESCENDS_THROUGH_Q", "MISSING_PARENT_SIGNATURE"),
        ("epsilon_coframe", "same-frame/coframe variation from Hperp", "ZERO_IF_COFRAME_DESCENDS_THROUGH_Q", "PROFILE_ROW_AVAILABLE"),
        ("epsilon_projector", "projector/domain/denominator geometry leakage", "ZERO_IF_PROJECTOR_DOMAIN_Q_OWNED", "PROFILE_ROW_REQUIRED"),
        ("epsilon_wall", "active selector-wall or boundary-projector leakage", "ZERO_IF_NO_ACTIVE_SELECTOR_WALL", "PROFILE_ROW_REQUIRED"),
        ("epsilon_Hodge_geom", "Hodge/readout geometry deformation not counted as EM stress", "ZERO_IF_HODGE_DESCENDS_FROM_OBSERVED_GEOMETRY", "PROFILE_ROW_REQUIRED"),
    ]
    rows: List[Dict[str, str]] = []
    for symbol, meaning, zero_route, status in specs:
        row = base_row()
        row.update(
            {
                "symbol": symbol,
                "meaning": meaning,
                "zero_route": zero_route,
                "status": status,
                "imported_formula": "epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+epsilon_wall+epsilon_Hodge_geom",
                "source_path": str(FORMAL / "262-PPC4161-Hperp-geometry-zero-certificate-or-epsilon-geom-profile-fill.md"),
            }
        )
        rows.append(row)
    return rows


def source_readout_schema_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "source_factor_q_certificate",
            "boolean theorem certificate",
            "source/readout functional factors as S_bar[q(Phi),Psi,theta]",
            "MISSING_PARENT_SIGNATURE",
        ),
        (
            "source_label_Hperp_leg",
            "boolean absence certificate",
            "no Hperp representative source-label leg survives quotient stripping",
            "MISSING_PARENT_SIGNATURE",
        ),
        (
            "readout_projector_commutator",
            "operator norm",
            "||[P_readout,Dq]Hperp|| or theorem-zero equivalent",
            "MISSING_BOUND_OR_ZERO",
        ),
        (
            "epsilon_source_readout",
            "Dq component norm",
            "epsilon_source_readout >= ||Dq_source_readout[Hperp]||",
            "MISSING_VALUE",
        ),
        (
            "R_src_readout",
            "source dual norm",
            "explicit residual in S_cg_nonHilbert = S_A Hperp^A + R_src_readout",
            "MISSING_VALUE",
        ),
        (
            "U_B_scope",
            "branch scope certificate",
            "U_B belongs to the local branch being scored and is not a transition-shell shortcut",
            "MISSING_SCOPE_CERTIFICATE",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for symbol, units, requirement, status in specs:
        row = base_row()
        row.update(
            {
                "symbol": symbol,
                "units_or_type": units,
                "requirement": requirement,
                "status": status,
                "source_needed": "parent action/readout definition or local bound row",
                "claim_firewall": "valid_for_claim remains false until sourced numeric/theorem row exists",
            }
        )
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4320_0_EDq",
            "combined Hperp Dq defect",
            "E_Dq,Hperp^2 := sum_i w_i epsilon_i^2, epsilon_i >= ||Dq_i[Hperp]||",
            "4245/4319",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "F4320_1_Nsrc",
            "source-support finite row",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)",
            "4319",
            "BOUND_READY_SOURCE_READOUT_INPUTS_MISSING",
        ),
        (
            "F4320_2_source_readout_zero",
            "source/readout deletion condition",
            "if Dq_source_readout[Hperp]=0 and R_src_readout=0, remove epsilon_source_readout and R_src_readout from the 4319 source row",
            "4320 prioritization",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "F4320_3_geometry_import",
            "geometry profile import",
            "epsilon_geom <= epsilon_Oloc+epsilon_coframe+epsilon_projector+epsilon_wall+epsilon_Hodge_geom",
            "4246-4248",
            "PROFILE_READY_VALUES_MISSING",
        ),
        (
            "F4320_4_Nrest_handoff",
            "canonical residual handoff",
            "N_rest_nonEM^canon = N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N",
            "4318/4319",
            "HANDOFF_READY_NO_CLAIM",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, basis, status in specs:
        row = base_row()
        row.update({"formula_id": formula_id, "name": name, "formula": formula, "basis": basis, "status": status})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUN4320_0_current", "current corpus", "BLOCK_CLAIM", "component priority map produced; no component zero adopted", "no local claim"),
        ("RUN4320_1_source_readout_zero", "source/readout factors through q", "ALLOW_SOURCE_READOUT_DELETION", "R_src_readout=0 and epsilon_source_readout=0", "then attack geometry or residual source constants"),
        ("RUN4320_2_source_readout_bound", "finite source/readout bound", "ALLOW_NONCLAIM_BOUND", "epsilon_source_readout and R_src_readout feed E_Dq/Nsrc", "claim still blocked"),
        ("RUN4320_3_geometry_zero", "A_MF/no-shadow parent signed", "ALLOW_GEOMETRY_ZERO", "epsilon_geom=0", "only after 4246-4248 clauses close"),
        ("RUN4320_4_invalid_generic_zero", "generic Dq zero imported without Hperp argument", "REJECT", "does not certify Dq_i[Hperp]=0", "firewall"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4320_0", "No component can be marked zero unless the Hperp-specific Dq_i argument is certified.", "BLOCK_GENERIC_ZERO_IMPORT"),
        ("FW4320_1", "R_src_readout cannot be deleted by absorbing it into S_A Hperp^A.", "BLOCK_RESIDUAL_ERASURE"),
        ("FW4320_2", "Geometry no-shadow remains blocked until the A_MF parent signature exists.", "BLOCK_GEOMETRY_OVERCLAIM"),
        ("FW4320_3", "Finite epsilon rows are nonclaim until numeric/theorem sources and units are present.", "BLOCK_NUMERIC_CLAIM"),
        ("FW4320_4", "Local GR/Newton/R10/PPN/clock/orbital claims remain blocked by remaining residual gates.", "BLOCK_LOCAL_TEST_CLAIM"),
    ]
    rows: List[Dict[str, str]] = []
    for rule_id, rule, action in specs:
        row = base_row()
        row.update({"rule_id": rule_id, "rule": rule, "action": action})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "decision_id": "DEC4320_0",
            "result": DECISION,
            "reason": "Dq_source_readout[Hperp] is the highest-leverage component because it feeds both E_Dq,Hperp and explicit R_src_readout; geometry is mature but still blocked by A_MF/no-shadow.",
            "next_action": NEXT_TARGET,
        }
    )
    return [row]


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4320_0", "eight_component_map", "COMPLETE_NONCLAIM", "all eight Hperp Dq rows classified"),
        ("STAT4320_1", "source_readout", "PRIMARY_NEXT_TARGET", "prove factorization through q or fill epsilon/Rsrc rows"),
        ("STAT4320_2", "geometry", "SECOND_TARGET", "use imported 4246-4248 epsilon profile"),
        ("STAT4320_3", "local_claim", "BLOCKED", "no local GR/Newton/R10/PPN/clock/orbital claim fires"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, obj, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "object": obj, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4320_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can Dq_source_readout[Hperp] and R_src_readout be theorem-zeroed by quotient factorization, or must a source-readout epsilon/residual row be filled?",
            "preferred_route": "prove source/readout factors through q and has no Hperp source-label leg",
            "fallback_route": "write nonclaim epsilon_source_readout and R_src_readout bound rows with parent/source paths",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 336 - PPC4161 Hperp Dq component certificate or first epsilon profile row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove any `Dq_i[Hperp]=0`, local GR, Newton, R10, PPN, clock safety, orbital safety, or a derived EH parent action.

## Result

The eight `Dq_i[Hperp]` rows are now ranked for attack. The sharp move is `Dq_source_readout[Hperp]` first, because it appears both inside `E_Dq,Hperp` and as the explicit `R_src_readout` term in the 4319 `N_src_nonHilbert` bound. Geometry is not ignored; it is imported as the already-mature 4246-4248 epsilon profile and kept as the second target.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Dq Component Status
{md_table(tables["components"], ["rank", "component", "status", "zero_certificate_required", "fallback_epsilon_row", "feeds", "note"])}

## Geometry Import
{md_table(tables["geometry"], ["symbol", "meaning", "zero_route", "status", "imported_formula"])}

## Source Readout Schema
{md_table(tables["source_readout"], ["symbol", "units_or_type", "requirement", "status", "claim_firewall"])}

## Aggregation Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "basis", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4320 - Hperp Dq component certificate or first epsilon profile row

## Verdict

- Ranked the eight `Dq_i[Hperp]` component gates.
- Picked `Dq_source_readout[Hperp]` as the next target because it controls both `E_Dq,Hperp` and `R_src_readout`.
- Kept geometry second, using the existing `epsilon_geom` five-piece profile rather than re-circling it.
- No local-GR/Newton claim fires.

## Dq Component Status
{md_table(tables["components"], ["rank", "component", "status", "fallback_epsilon_row", "feeds"])}

## Source Readout Schema
{md_table(tables["source_readout"], ["symbol", "requirement", "status"])}

## Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, f"csv parse failed: {exc}"
    if not rows:
        return False, "csv has no data rows"
    return True, f"csv parsed rows={len(rows)}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4320_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4320_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4320_components_8", "eight Dq components listed", len(tables["components"]) == 8, "components")
    add("VAL4320_source_rank_1", "source/readout is rank 1", tables["components"][0]["component"] == "Dq_source_readout[Hperp]" and tables["components"][0]["rank"] == "1", "components")
    add("VAL4320_geometry_rank_2", "geometry is rank 2", tables["components"][1]["component"] == "Dq_geom[Hperp]" and tables["components"][1]["rank"] == "2", "components")
    add("VAL4320_source_feeds_twice", "source/readout feeds EDq and Rsrc", "E_Dq,Hperp" in tables["components"][0]["feeds"] and "R_src_readout" in tables["components"][0]["feeds"], "components")
    add("VAL4320_geometry_subpieces", "five geometry epsilon subpieces imported", len(tables["geometry"]) == 5, "geometry")
    add("VAL4320_source_schema", "source/readout schema contains epsilon and Rsrc", {"epsilon_source_readout", "R_src_readout"}.issubset({r["symbol"] for r in tables["source_readout"]}), "source_readout")
    add("VAL4320_EDq_formula", "EDq aggregation formula present", any("sum_i w_i epsilon_i^2" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4320_Nsrc_formula", "Nsrc formula retains Rsrc", any("N_src_nonHilbert" in r["formula"] and "R_src_readout" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4320_invalid_generic_zero_rejected", "generic component zero shortcut rejected", any(r["runner_id"] == "RUN4320_4_invalid_generic_zero" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4320_firewall_claim", "local claims blocked", any(r["action"] == "BLOCK_LOCAL_TEST_CLAIM" for r in tables["firewall"]), "firewall")
    add("VAL4320_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    add("VAL4320_next_target", "next target is 4321", any("4321" in r["next_target"] for r in tables["next"]), "next")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4320_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4320_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4320_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4320_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4320_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4320_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4320_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4320_SOURCE_REGISTER.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4320_DQ_COMPONENT_STATUS.csv",
        "geometry": SOURCE_DIR / "P8_Y5_R2FR_4320_GEOMETRY_EPSILON_IMPORT.csv",
        "source_readout": SOURCE_DIR / "P8_Y5_R2FR_4320_SOURCE_READOUT_ROW_SCHEMA.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4320_EDQ_AGGREGATION_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4320_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4320_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4320_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4320_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4320_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "components": component_rows(),
        "geometry": geometry_import_rows(),
        "source_readout": source_readout_schema_rows(),
        "formulas": formula_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4320 Hperp Dq component certificate or first epsilon profile row

Marker: `{MARKER}`

4320 ranks the eight `Dq_i[Hperp]` gates. The next derivation target is `Dq_source_readout[Hperp]`, because it controls both `epsilon_source_readout` inside `E_Dq,Hperp` and the explicit `R_src_readout` in the 4319 source-support bound. Geometry remains second via the imported five-piece `epsilon_geom` profile.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4320 packet Hperp Dq component priority

Marker: `{PACKET_MARKER}`

Packet update: attack `Dq_source_readout[Hperp]` before reworking geometry. If source/readout factors through `q`, both the explicit `R_src_readout` and its `E_Dq,Hperp` component can be removed; otherwise write the finite nonclaim source-readout epsilon row.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
