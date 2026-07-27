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
DOC_PATH = ROOT / "4132-Y5-R2FR-source-denominator-ellJ-MH-equality.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_DENOMINATOR_ELLJ_MH_EQUALITY_4132"
CHECKPOINT_ID = "4132"
DECISION = "DENOMINATOR_EQUALITY_REDUCED_TO_RANK_ONE_AMPLITUDE_VECTOR_PARENT_ZERO_UNSIGNED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4132_00_4131_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4131_NEXT_TARGET.csv",
        "4132-Y5-R2FR-source-denominator-ellJ-MH-equality.md",
        "4131 selected source denominator ell_J/M_H equality.",
    ),
    "SRC4132_01_4131_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4131_STATUS.csv",
        "SOURCE_SLOT_TAIL_SPLIT_COMMON_G_CALIBRATION_BOUND_VECTOR_FILLED",
        "Current-chain source-slot/common-G calibration status.",
    ),
    "SRC4132_02_4131_common": (
        SOURCE_DIR / "P8_Y5_R2FR_4131_COMMON_G_PRODUCT_GATE.csv",
        "z_ellJ",
        "Current-chain effective coupling product identifies z_ellJ as source denominator throat.",
    ),
    "SRC4132_03_4108_ellj": (
        SOURCE_DIR / "P8_Y5_R2FR_4108_ELLJ_DECOMPOSITION.csv",
        "ELJ4108_0_exact_decomposition",
        "Current-chain ell_J owner decomposition.",
    ),
    "SRC4132_04_4108_subdenom": (
        SOURCE_DIR / "P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR.csv",
        "PHT4108_2_qbasic_zero",
        "PiM/Htau subdenominator q-basic zero route.",
    ),
    "SRC4132_05_4098_mass": (
        SOURCE_DIR / "P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM.csv",
        "TARGET_IDENTITY_NOT_PARENT_DERIVED",
        "Source mass/Hamiltonian equality target.",
    ),
    "SRC4132_06_4098_newton": (
        SOURCE_DIR / "P8_Y5_R2FR_4098_GAUSS_NEWTON_CONSEQUENCE.csv",
        "RADIAL_HAIR_BOUND_ROUTE",
        "Newton consequence and radial-hair failure route.",
    ),
    "SRC4132_07_4012_charge": (
        SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv",
        "CONDITIONAL_SAME_CHARGE_THEOREM_UNSIGNED",
        "PiM/Htau/Hilbert same-charge theorem.",
    ),
    "SRC4132_08_3998_denominator": (
        SOURCE_DIR / "P8_Y5_R2FR_3998_HILBERT_MASS_DENOMINATOR_THEOREM.csv",
        "DENOMINATOR_ROUTE_REDUCED_NO_NEWTON_CLAIM",
        "Hilbert mass denominator theorem.",
    ),
    "SRC4132_09_3986_rank_one": (
        SOURCE_DIR / "P8_Y5_R2FR_3986_PIM_HILBERT_EQUALITY_REDUCTION_THEOREM.csv",
        "RANK_ONE_CHARGE_DIRECTION_DERIVED",
        "Rank-one EH exterior reduction of PiM/Hilbert equality.",
    ),
    "SRC4132_10_3986_cert": (
        SOURCE_DIR / "P8_Y5_R2FR_3986_PIM_HILBERT_CERTIFICATE_UPDATE.csv",
        "Z_closed_total_source_monopole",
        "Reduced certificate for closed source monopole residual.",
    ),
    "SRC4132_11_3601_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3601_ELLJ_BOUND_ROWS.csv",
        "ELJB3601_11_ellJ_total",
        "Older ell_J bound rows.",
    ),
    "SRC4132_12_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4132_source_denominator_ellJ_MH_equality.py",
        "Reproducible generator for this 4132 checkpoint.",
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


def denominator_identity_rows() -> List[dict]:
    data = [
        (
            "DEN4132_0_target_equality",
            "ell_J / M_H equality",
            "ell_J(Pi_M J_H_total) = M_H^dress = H_tau[S]-H_ref = B_tau/G_ref",
            "one source denominator must feed common-G calibration, Newton/Gauss, and fixed-source PPN",
            "TARGET_IDENTITY",
        ),
        (
            "DEN4132_1_ellJ_decomposition",
            "z_ellJ",
            "z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units",
            "ell_J is an owner decomposition, not an arbitrary source-current scale",
            "EXACT_DECOMPOSITION_IMPORTED",
        ),
        (
            "DEN4132_2_hilbert_mass_definition",
            "M_H^dress",
            "M_H[S] := N_G int_S Pi_M^H J_H_total[tau,e_obs]",
            "source mass is defined before orbital GM readout and includes dressed matter plus EM/Poynting once",
            "SOURCE_DENOMINATOR_DEFINITION_LOCK",
        ),
        (
            "DEN4132_3_hamiltonian_equality",
            "B_tau/G_ref = M_H",
            "Delta_Gauss := B_tau/G_ref - M_H[Pi_M^H J_H_total]",
            "if nonzero, failure is physical amplitude/radial/source hair, not a unit convention",
            "FAILURE_IDENTITY",
        ),
        (
            "DEN4132_4_newton_consequence",
            "Newton source",
            "Delta_Gauss=0 and d(Pi_M J_H)=0 imply Phi_N=-G_ref M_H/r and a_r=-G_ref M_H/r^2",
            "first-order Newton source denominator closes only after source equality and surface independence",
            "CONDITIONAL_NEWTON_CONSEQUENCE",
        ),
    ]
    rows: List[dict] = []
    for identity_id, symbol, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "identity_id": identity_id,
                "symbol": symbol,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def rank_one_reduction_rows() -> List[dict]:
    data = [
        (
            "R1R4132_0_rank_one",
            "controlled EH exterior charge space",
            "Q_proj = lambda_PiM_EH Q_EH + Q_extra",
            "controlled stationary EH monopole exterior has one scalar charge direction after fixed reference subtraction",
            "RANK_ONE_DIRECTION_IMPORTED",
        ),
        (
            "R1R4132_1_not_arbitrary_projector",
            "Pi_M freedom",
            "Pi_M/Hilbert equality reduces to lambda_PiM_EH, Q_extra, parent_JH_origin, and boundary leakage",
            "source denominator is no longer an arbitrary projector problem in the controlled branch",
            "PROJECTOR_FREEDOM_REDUCED",
        ),
        (
            "R1R4132_2_equality_conditions",
            "Pi_M J_H = J_EH^M",
            "lambda_PiM_EH=1 and Q_extra=0 and parent_JH_origin=true and exact_boundary_leakage=0",
            "these are still not parent-signed",
            "AMPLITUDE_EQUALITY_UNSIGNED",
        ),
        (
            "R1R4132_3_reduced_residual",
            "epsilon_denominator_4132",
            "|lambda_PiM_EH-1| + |Q_extra|/|Q_ref| + epsilon_parent_JH_origin + epsilon_boundary_leakage + epsilon_universal_G + epsilon_PPN_source_stability",
            "this is the current denominator residual vector for Newton/PPN/common-G",
            "REDUCED_RESIDUAL_VECTOR",
        ),
    ]
    rows: List[dict] = []
    for reduction_id, target, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "reduction_id": reduction_id,
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


def equality_audit_rows() -> List[dict]:
    data = [
        (
            "AUD4132_0_matter_descent",
            "R_md",
            "S_matter descends through q with no source-only weight or hidden vertex",
            "not jointly parent-signed",
            "BOUND_OR_THEOREM_REQUIRED",
        ),
        (
            "AUD4132_1_Ward_projection",
            "R_Ward",
            "Hilbert/Ward conservation survives Pi_M projection, exterior support, and boundary/non-Hilbert tails",
            "not jointly parent-signed",
            "BOUND_OR_THEOREM_REQUIRED",
        ),
        (
            "AUD4132_2_PiM_chainmap",
            "R_PiM",
            "Pi_M is fixed parent chain map on the Hilbert mass-current complex",
            "identity/inclusion branch adopted privately, but full physical domain remains unsigned",
            "PARTIAL_REDUCTION_NOT_PUBLIC_CLAIM",
        ),
        (
            "AUD4132_3_Htau_integrability",
            "R_Htau",
            "H_tau is integrable and boundary symplectic curl is exact, zero, or bounded",
            "curl/integrability gate still open",
            "BOUND_OR_THEOREM_REQUIRED",
        ),
        (
            "AUD4132_4_reference_support_frame_units",
            "R_ref+R_W+R_frame+R_units",
            "reference, worldtube support, observed frame/tau/surface, and units are fixed before measured GM",
            "anti-laundering clauses not all parent-signed",
            "BOUND_OR_THEOREM_REQUIRED",
        ),
        (
            "AUD4132_5_rank_one_amplitude",
            "lambda_PiM_EH and Q_extra",
            "rank-one geometry reduces amplitude problem but does not force lambda=1 or Q_extra=0",
            "needs parent normalization/extra-monopole theorem or source-backed bound",
            "REDUCED_BUT_UNSIGNED",
        ),
        (
            "AUD4132_6_verdict",
            "ell_J/M_H equality",
            "current corpus reduces denominator equality to a smaller vector but does not prove it",
            "no Newton/local-GR/source-normalization pass",
            "ZERO_NOT_CLAIMED",
        ),
    ]
    rows: List[dict] = []
    for audit_id, target, condition, current_status, status in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "target": target,
                "condition": condition,
                "current_status": current_status,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def bound_schema_rows() -> List[dict]:
    data = [
        (
            "BS4132_0_denominator_master",
            "epsilon_denominator_4132",
            "|lambda_PiM_EH-1| + |Q_extra|/|Q_ref| + epsilon_parent_JH_origin + epsilon_boundary_leakage + epsilon_universal_G + epsilon_PPN_source_stability",
            "dimensionless",
            "master source denominator residual",
            "all terms parent-zero or numeric source-backed bounds",
        ),
        (
            "BS4132_1_Gdot",
            "Gdot_denominator",
            "d ln(G_ref*M_H*ell_J*readout)/dt = z_den dot(A_N)+explicit_t",
            "yr^-1",
            "LLR Gdot/G envelope",
            "|...| <= 1.3e-12 yr^-1 with source path and A_N profile",
        ),
        (
            "BS4132_2_PPN",
            "PPN_fixed_U_source",
            "U=G_ref M_H/r; denominator residual feeds gamma,beta,alpha_i,xi,zeta source-stability rows",
            "dimensionless",
            "PPN source-stability",
            "each PPN component passes independently; no orbital-GM laundering",
        ),
        (
            "BS4132_3_R10",
            "R10_denominator_channel",
            "alpha_R10(lambda)=K_den(lambda)*epsilon_denominator_S*epsilon_denominator_T/M_den^2",
            "dimensionless alpha(lambda)",
            "short-range source normalization",
            "requires K_den, M_den^2, tau(lambda), source/test denominator residuals, alpha_bound(lambda)",
        ),
        (
            "BS4132_4_Newton_Gauss",
            "Delta_Gauss_radial_hair",
            "Delta_Gauss:=B_tau/G_ref-M_H; partial_r ln M_H ~ N_G int_A d(Pi_M J_H)/M_H",
            "dimensionless or length^-1",
            "Newton/Gauss inverse-square source",
            "requires surface-independence or radial/range bound rows",
        ),
        (
            "BS4132_5_common_G",
            "z_ellJ_in_G_eff_product",
            "D_A ln(G_ref*w_common*ell_J*R_frame*C_extra) contains z_ellJ",
            "dimensionless per normalized A_N",
            "common-G/source calibration",
            "z_ellJ must be zero or included in common-G bound vector",
        ),
    ]
    rows: List[dict] = []
    for bound_id, target, formula, units, arena, pass_rule in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "target": target,
                "formula": formula,
                "units": units,
                "arena": arena,
                "pass_rule": pass_rule,
                "status": "NONCLAIM_BOUND_SCHEMA_FILLED",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4132_0_reduction",
            "The source denominator equality is reduced to a rank-one amplitude/source vector, not left as arbitrary ell_J freedom.",
            "DENOMINATOR_REDUCED",
            "score lambda_PiM_EH, Q_extra, parent_JH_origin, boundary leakage, universal G, and PPN stability",
        ),
        (
            "DEC4132_1_no_claim",
            "ell_J/M_H/Hamiltonian/Gauss equality is not parent-signed from the current corpus.",
            "PARENT_ZERO_UNSIGNED",
            "no Newton/local-GR/source-normalization pass",
        ),
        (
            "DEC4132_2_anti_laundering",
            "Orbital GM remains output-only; it cannot define M_H or ell_J.",
            "ANTI_ORBITAL_GM_LAUNDERING_LOCKED",
            "keep source denominator independent of orbital fit",
        ),
        (
            "DEC4132_3_next",
            "Next target is parent_JH_origin plus extra-monopole charge Q_extra, because rank-one geometry already did its part.",
            "NEXT_PARENT_JH_QEXTRA_SELECTED",
            "try to prove parent Hilbert-current origin and Q_extra=0, or fill source-backed bounds",
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
            "status_id": "STATUS4132_0",
            "result": DECISION,
            "summary": (
                "4132 attacks ell_J/M_H equality and reduces it to a controlled rank-one amplitude/source vector. "
                "The denominator is no longer arbitrary: in the controlled EH exterior Q_proj=lambda_PiM_EH Q_EH+Q_extra, "
                "so equality requires lambda_PiM_EH=1, Q_extra=0, parent Hilbert-current origin, boundary leakage zero, "
                "universal G normalization, and PPN source stability. These are not parent-signed, so denominator bound "
                "schemas are filled for Gdot, PPN, R10, Newton/Gauss, and common-G calibration."
            ),
            "rank_one_reduction": "True",
            "denominator_equality_signed": "False",
            "bound_schemas_filled": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM prediction, Maxwell derivation, alpha derivation, or source-normalization pass",
            "next_target": "4133 parent Hilbert-current origin and extra-monopole charge",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4132_0",
            "target_doc": "4133-Y5-R2FR-parent-JH-origin-and-extra-monopole-charge.md",
            "target_script": "scripts/Y5_R2FR_4133_parent_JH_origin_and_extra_monopole_charge.py",
            "objective": (
                "try to prove the projected Hilbert source current has parent origin and no extra monopole charge in the controlled EH local branch; "
                "if unsigned, fill lambda_PiM_EH, Q_extra/Q_ref, parent_JH_origin, and boundary-leakage bound rows"
            ),
            "success_gate": "parent_JH_origin=true and Q_extra=0 are signed, or every live amplitude term has nonclaim bound schema with units/source links",
            "reason": "4132 reduced source denominator equality to rank-one amplitude/source terms; those are now the shortest denominator blockers.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4132_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4132_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4132_DENOMINATOR_IDENTITY": SOURCE_DIR / "P8_Y5_R2FR_4132_DENOMINATOR_IDENTITY.csv",
        "P8_Y5_R2FR_4132_RANK_ONE_REDUCTION": SOURCE_DIR / "P8_Y5_R2FR_4132_RANK_ONE_REDUCTION.csv",
        "P8_Y5_R2FR_4132_EQUALITY_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4132_EQUALITY_AUDIT.csv",
        "P8_Y5_R2FR_4132_BOUND_SCHEMAS": SOURCE_DIR / "P8_Y5_R2FR_4132_BOUND_SCHEMAS.csv",
        "P8_Y5_R2FR_4132_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4132_DECISION_GATES.csv",
        "P8_Y5_R2FR_4132_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4132_STATUS.csv",
        "P8_Y5_R2FR_4132_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4132_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4132 - Source Denominator ell_J / M_H Equality",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The source denominator is no longer arbitrary: controlled EH exterior gives a rank-one amplitude form.",
        "- Equality still needs `lambda_PiM_EH=1`, `Q_extra=0`, parent Hilbert-current origin, boundary silence, universal `G`, and PPN source stability.",
        "- No Newton/local-GR pass is claimed; denominator bound schemas are filled.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Denominator Identity", "", "| symbol | status | meaning |", "|---|---|---|"])
    for row in denominator_identity_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['meaning']} |")
    sections.extend(["", "## Rank-One Reduction", "", "| target | status | meaning |", "|---|---|---|"])
    for row in rank_one_reduction_rows():
        sections.append(f"| {row['target']} | {row['status']} | {row['meaning']} |")
    sections.extend(["", "## Bound Schemas", "", "| target | units | arena |", "|---|---|---|"])
    for row in bound_schema_rows():
        sections.append(f"| {row['target']} | {row['units']} | {row['arena']} |")
    sections.extend(["", "## Claim Ceiling", "", f"- {status['claim_state']}.", "- This checkpoint reduces the denominator problem; it does not close it.", "", "## Next Target", "", "- `4133-Y5-R2FR-parent-JH-origin-and-extra-monopole-charge.md`", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4132_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4132_DENOMINATOR_IDENTITY": denominator_identity_rows,
        "P8_Y5_R2FR_4132_RANK_ONE_REDUCTION": rank_one_reduction_rows,
        "P8_Y5_R2FR_4132_EQUALITY_AUDIT": equality_audit_rows,
        "P8_Y5_R2FR_4132_BOUND_SCHEMAS": bound_schema_rows,
        "P8_Y5_R2FR_4132_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4132_STATUS": status_rows,
        "P8_Y5_R2FR_4132_NEXT_TARGET": next_target_rows,
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
        "VAL4132_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4132_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

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
    add("VAL4132_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    identity_text = flatten_rows([outputs["P8_Y5_R2FR_4132_DENOMINATOR_IDENTITY"]])
    identity_ok = all(token in identity_text for token in ["ell_J(Pi_M J_H_total)", "z_ellJ", "M_H[S]", "Delta_Gauss", "Phi_N=-G_ref M_H/r"])
    add("VAL4132_3_identity", "denominator identity rows contain ell_J, M_H, Delta_Gauss and Newton consequence", identity_ok, "identity tokens checked")

    rank_text = flatten_rows([outputs["P8_Y5_R2FR_4132_RANK_ONE_REDUCTION"]])
    rank_ok = all(token in rank_text for token in ["Q_proj = lambda_PiM_EH Q_EH + Q_extra", "lambda_PiM_EH=1", "REDUCED_RESIDUAL_VECTOR"])
    add("VAL4132_4_rank_one", "rank-one reduction and reduced residual vector are present", rank_ok, "rank-one tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4132_EQUALITY_AUDIT"]])
    audit_ok = all(token in audit_text for token in ["BOUND_OR_THEOREM_REQUIRED", "PARTIAL_REDUCTION_NOT_PUBLIC_CLAIM", "REDUCED_BUT_UNSIGNED", "ZERO_NOT_CLAIMED"])
    add("VAL4132_5_audit", "equality audit blocks overclaim and lists live terms", audit_ok, "audit tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4132_BOUND_SCHEMAS"]])
    bound_ok = all(token in bound_text for token in ["epsilon_denominator_4132", "Gdot_denominator", "PPN_fixed_U_source", "R10_denominator_channel", "Delta_Gauss_radial_hair", "z_ellJ_in_G_eff_product"])
    add("VAL4132_6_bounds", "bound schemas cover denominator, Gdot, PPN, R10, Newton/Gauss and common-G", bound_ok, "bound tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4132_DECISION_GATES"]])
    decision_ok = all(token in decision_text for token in ["DENOMINATOR_REDUCED", "PARENT_ZERO_UNSIGNED", "ANTI_ORBITAL_GM_LAUNDERING_LOCKED", "NEXT_PARENT_JH_QEXTRA_SELECTED"])
    add("VAL4132_7_decisions", "decision gates record reduction, no-claim, anti-laundering and next target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4132_STATUS"])
    status_ok = bool(status) and status[0].get("result") == DECISION and status[0].get("rank_one_reduction") == "True" and status[0].get("denominator_equality_signed") == "False"
    add("VAL4132_8_status", "status records rank-one reduction and unsigned denominator equality", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4132_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4133-Y5-R2FR-parent-JH-origin-and-extra-monopole-charge.md"
    add("VAL4132_9_next_target", "next target is parent JH origin and extra-monopole charge", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4132_10_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4132*")) or any(FORMALIZATION.rglob("4132-Y5-R2FR*"))
    add("VAL4132_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4132_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4132_VALIDATION.csv"
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
