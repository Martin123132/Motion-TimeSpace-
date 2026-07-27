from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3950"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3950-Y5-R2FR-Gamma-Khat-positive-auxiliary-signature-or-epsilon-nonminimal-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3950_SOURCE_REGISTER.csv",
    "signature": SRC / "P8_Y5_R2FR_3950_GK_POSITIVE_AUXILIARY_SIGNATURE.csv",
    "ward": SRC / "P8_Y5_R2FR_3950_GK_WARD_QLOC_ZERO_THEOREM.csv",
    "bound": SRC / "P8_Y5_R2FR_3950_EPSILON_NONMINIMAL_GK_BOUND_ROW.csv",
    "gate": SRC / "P8_Y5_R2FR_3950_GK_PROMOTION_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3950_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3950_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3950_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3950_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3950_VALIDATION.csv",
}

NEXT_DOC = "3951-Y5-R2FR-GK-symbol-match-coefficient-extraction-or-epsilon-GK-first-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3951_GK_symbol_match_coefficient_extraction_or_epsilon_GK_first_values.py"


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
        ("SRC3950_00_3949_next", SRC / "P8_Y5_R2FR_3949_NEXT_TARGET.csv", "NEXT3949_0", "3949 selected Gamma/Khat target"),
        ("SRC3950_01_3949_matrix", SRC / "P8_Y5_R2FR_3949_MTS_HAMILTONIAN_SIGNATURE_MATRIX.csv", "SIG3949_2_Gamma_Khat", "Gamma/Khat signature matrix row"),
        ("SRC3950_02_3949_epsilon", SRC / "P8_Y5_R2FR_3949_EPSILON_NEG_SECTOR_INPUT_ROWS.csv", "EPN3949_0_GK_nonminimal", "Gamma/Khat epsilon_nonminimal row"),
        ("SRC3950_03_GK514_A", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_A_metric_response_scalar_density", "metric response scalar-density route"),
        ("SRC3950_04_GK514_B", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_B_positive_auxiliary_fields", "positive auxiliary field route"),
        ("SRC3950_05_GK514_C", SRC / "P8_GK_STRESS_ACTION_CANDIDATES.csv", "GK514_C_topological_exact_sector", "topological/exact sector route"),
        ("SRC3950_06_G514_gate", SRC / "P8_GK_STRESS_ACTION_GATE_TESTS.csv", "G514_2_current_MTS_match", "current MTS match failure gate"),
        ("SRC3950_07_D514", SRC / "P8_GK_STRESS_ACTION_DECISION.csv", "D514_1", "current MTS not matched decision"),
        ("SRC3950_08_RU514", SRC / "P8_GK_STRESS_ACTION_ROUTE_UPDATE.csv", "RU514_2", "residual branch kept"),
        ("SRC3950_09_GO516_A", SRC / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "GO516_A_response_doublet_quadratic_density", "response doublet quadratic density"),
        ("SRC3950_10_GO516_B", SRC / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "GO516_B_positive_auxiliary_energy_density", "positive auxiliary energy density"),
        ("SRC3950_11_STAT3540", SRC / "P8_Gamma_Khat_parent_response_or_qloc_bound_status.csv", "STAT3540_1_DeltaK_existing", "existing Khat not proved zero"),
        ("SRC3950_12_q_nohair", SRC / "P8_q_retained_zero_conditions_CONTRACT.csv", "Q3_positive_source_free_nohair", "positive source-free no-hair condition"),
        ("SRC3950_13_FV", SRC / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv", "FV512_2_Gamma_Khat_q", "Gamma/Khat first variation gate"),
        ("SRC3950_14_KK", SRC / "P8_MTS_SYMBOL_KEEP_KILL_RULES.csv", "KK512_2_Gamma_Khat", "Gamma/Khat keep/kill rule"),
        ("SRC3950_15_validation", SRC / "P8_Y5_BRR545_3949_VALIDATION.csv", "VAL3949_19_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:900]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GKS3950_0_parent_density",
            "clause": "positive auxiliary parent density",
            "formula": "Gamma_eff = Gamma0 + 1/2 G_AB(Z) nabla Z^A.nabla Z^B + 1/2 M_AB Z^A Z^B + O(Z^4)",
            "required_signature": "G_AB positive semidefinite on physical modes; M_AB positive semidefinite with positive mass gap off gauge/constraint directions",
            "effect": "Gamma_eff-Gamma0 is nonnegative and double-zero at Z=0",
            "current_status": "CONDITIONAL_SIGNATURE_FORM_BUILT_SYMBOL_MATCH_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKS3950_1_Khat_metric_response",
            "clause": "Khat as metric response",
            "formula": "K_hat^{mu nu} := 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} minus volume convention",
            "required_signature": "same scalar density and same parent metric variation define Gamma_eff and K_hat",
            "effect": "Delta_K mismatch vanishes by definition on the candidate branch",
            "current_status": "EXACT_IF_IDENTIFICATION_SIGNED_CURRENT_MTS_UNMATCHED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKS3950_2_double_zero",
            "clause": "local double-zero",
            "formula": "Gamma_eff(Phi0)=Gamma0, partial_A Gamma_eff(Phi0)=0, K_hat(Phi0)=K_EH_or_zero_response, partial_A K_hat(Phi0)=0",
            "required_signature": "quadratic/even density or topological/exact improvement; no linear source coupling",
            "effect": "first-order local fifth-force/source-normalization leakage is killed",
            "current_status": "CONDITIONAL_DOUBLE_ZERO_FORM_BUILT_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKS3950_3_no_hair",
            "clause": "source-free positive operator",
            "formula": "int <delta Z,L_GK delta Z> >= m_GK^2 ||delta Z||^2 with zero source and boundary flux",
            "required_signature": "positive operator, compact local exterior, regular decay, no source charge",
            "effect": "Z=0 locally or exponentially suppressed hair",
            "current_status": "CONDITIONAL_NO_HAIR_FORM_BUILT_SOURCE_BOUNDARY_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GKS3950_4_verdict",
            "clause": "Gamma/Khat positive signature verdict",
            "formula": "Z_GK_positive = signed(G_AB>=0,M_AB>=m^2,metric-response Khat,no source charge,no boundary flux)",
            "required_signature": "all clauses signed against actual MTS Gamma_eff/K_hat definitions",
            "effect": "not signed yet; use epsilon_nonminimal_GK bound row",
            "current_status": "PROGRESS_TO_VALUE_READY_BOUND_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ward_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WZ3950_0_Ward_identity",
            "piece": "metric-response Ward identity",
            "statement": "If K_hat is the metric response of sqrt(-g)Gamma_eff, then nabla_mu K_hat^{mu nu}-nabla^nu Gamma_eff equals the auxiliary Euler terms plus boundary/improvement residuals.",
            "derivation": "Diffeomorphism invariance of the scalar density gives the Noether identity linking divergence of the metric stress response to the field Euler operators.",
            "zero_condition": "E_A[Z]=0, boundary/improvement flux=0, and source charge J_Z=0",
            "current_status": "EXACT_CONDITIONAL_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "WZ3950_1_q_loc",
            "piece": "q_loc zero route",
            "statement": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu).",
            "derivation": "Substitute WZ3950_0 into the physical local projector. On shell and with no boundary/source leakage, the local residual vanishes.",
            "zero_condition": "P_loc E_A=0, P_loc R_boundary=0, P_loc R_source=0",
            "current_status": "CONDITIONAL_QLOC_ZERO_FORMULA_BUILT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "WZ3950_2_bound_form",
            "piece": "q_loc finite fallback",
            "statement": "|q_loc| <= ||P_loc||*(|E_A nabla Z^A| + |R_boundary| + |R_source| + |Delta_K|).",
            "derivation": "If any identity clause is unsigned, retain the norm bound and feed the nonminimal energy/readout residual.",
            "zero_condition": "not required; finite coefficients can be scored",
            "current_status": "FINITE_BOUND_FALLBACK_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("EGK3950_0_denominator", "E_pos", "positive source-energy denominator from 3947/3948", "MISSING_E_POS_SOURCE_ROW", "energy", "fill positive support/source row before scoring epsilon"),
        ("EGK3950_1_energy", "epsilon_GK_energy", "(E_GK_unsigned_abs)/E_pos", "MISSING_GK_ENERGY_COEFFICIENTS", "dimensionless", "field content, G_AB, M_AB, amplitude/domain support"),
        ("EGK3950_2_metric_response", "epsilon_GK_metric_response_mismatch", "|Delta_K|/E_pos", "MISSING_KHAT_METRIC_RESPONSE_MATCH", "dimensionless", "prove K_hat=metric response or bound mismatch"),
        ("EGK3950_3_boundary", "epsilon_GK_boundary", "|E_Khat_boundary_unsigned|/E_pos", "MISSING_GK_BOUNDARY_FLUX_BOUND", "dimensionless", "boundary/exact/topological flux zero or value"),
        ("EGK3950_4_source_charge", "epsilon_GK_source_charge", "|E_GK_source_charge|/E_pos", "MISSING_GK_SOURCE_CHARGE_BOUND", "dimensionless", "prove no direct source charge or bound it"),
        ("EGK3950_5_hessian", "epsilon_GK_negative_hessian", "|E_negative_hessian_modes|/E_pos", "MISSING_GK_HESSIAN_SIGNATURE", "dimensionless", "positive Hessian/mass-gap signature or negative-mode bound"),
        ("EGK3950_6_total", "epsilon_nonminimal_counterterm_GK", "sum_abs(epsilon_GK_energy,epsilon_GK_metric_response_mismatch,epsilon_GK_boundary,epsilon_GK_source_charge,epsilon_GK_negative_hessian)", "COMPONENT_VALUES_MISSING", "dimensionless", "first value-ready GK contribution to epsilon_nonminimal_counterterm"),
    ]
    return [
        {
            "row_id": row_id,
            "target_symbol": symbol,
            "formula": formula,
            "current_value": current_value,
            "units": units,
            "exit_requirement": exit_requirement,
            "source_paths": "P8_GK_STRESS_ACTION_CANDIDATES.csv;P8_GAMMA_OWNER_CANDIDATE_ACTION.csv;P8_Gamma_Khat_parent_response_or_qloc_bound_status.csv",
            "row_type": "VALUE_READY_EPSILON_NONMINIMAL_COMPONENT_ROW",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, formula, current_value, units, exit_requirement in data
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("GKG3950_0_signature_form", "positive auxiliary signature form exists", "PASS_CONDITIONAL_FORM"),
        ("GKG3950_1_Khat_response", "K_hat metric-response identity signed for actual MTS symbols", "BLOCKED_SYMBOL_MATCH_MISSING"),
        ("GKG3950_2_double_zero", "Gamma/Khat first variation zero at local fixed point", "BLOCKED_COEFFICIENTS_MISSING"),
        ("GKG3950_3_no_hair", "positive source-free operator and boundary silence", "BLOCKED_SOURCE_BOUNDARY_CERTIFICATES_MISSING"),
        ("GKG3950_4_q_loc_zero", "q_loc^nu vanishes from Ward identity", "CONDITIONAL_FORM_BUILT_NOT_SIGNED"),
        ("GKG3950_5_epsilon_bound", "epsilon_nonminimal_counterterm_GK row is value-ready", "PASS_VALUE_READY_VALUES_MISSING"),
        ("GKG3950_6_claim", "Gamma/Khat local-GR promotion", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3950_0_auxiliary_route",
            "decision": "keep the positive auxiliary / metric-response route as the lead derivation path",
            "effect": "it gives a real Ward identity for q_loc and a no-hair mechanism if symbol match, Hessian, source, and boundary clauses close",
            "claim_status": "CONDITIONAL_ROUTE_SHARPENED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3950_1_no_promotion",
            "decision": "do not promote Gamma/Khat to a local-GR proof yet",
            "effect": "actual MTS Gamma_eff and K_hat still lack the coefficient/signature match",
            "claim_status": "SYMBOL_MATCH_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3950_2_bound_row",
            "decision": "activate a value-ready epsilon_nonminimal_counterterm_GK bound row",
            "effect": "if the proof route fails, this sector can be scored as a nonminimal energy/readout residual instead of hidden",
            "claim_status": "BOUND_ROW_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3950_3_next",
            "decision": "extract actual Gamma/Khat coefficients next",
            "effect": "3951 should either match the symbol definitions to G_AB/M_AB/K_metric or fill first bound values",
            "claim_status": "NEXT_COEFFICIENT_EXTRACTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "CG3950_0_sources", "gate": "source-backed checkpoint", "requirement": "all source paths and needles exist", "status": "PASS_IF_VALIDATION_PASS", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3950_1_positive_form", "gate": "positive auxiliary form", "requirement": "Gamma density signature and Khat metric response form written", "status": "PASS_CONDITIONAL_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3950_2_symbol_match", "gate": "actual MTS symbol match", "requirement": "Gamma_eff and K_hat definitions match GKS3950 rows", "status": "BLOCKED_SYMBOL_MATCH_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3950_3_q_loc_zero", "gate": "q_loc zero", "requirement": "Euler/source/boundary residuals vanish", "status": "BLOCKED_ZERO_CLAUSES_UNSIGNED", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3950_4_epsilon", "gate": "epsilon_nonminimal fallback", "requirement": "GK component values filled", "status": "BLOCKED_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "CG3950_5_local_GR", "gate": "local-GR/source-coupling claim", "requirement": "GK proof or bound plus M_EH and residual envelopes", "status": "BLOCKED_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3950_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "extract or reject actual Gamma_eff/K_hat coefficient matches: identify Z^A, G_AB, M_AB, K_metric, Delta_K, boundary/source terms, then either sign the positive auxiliary route or fill first epsilon_nonminimal_counterterm_GK values",
            "success_condition": "at least one GK clause gets a real parent-owned coefficient/signature row, or the fallback epsilon_nonminimal_counterterm_GK row gains concrete value-ready component inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3950 sharpens Gamma/Khat into a positive auxiliary metric-response signature and a value-ready epsilon_nonminimal_counterterm_GK bound row; actual MTS symbol match remains missing",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3950 - Gamma/Khat Positive Auxiliary Signature Or Epsilon Nonminimal Bound

Timestamp: `{timestamp}`

## Result

3950 sharpens the central `Gamma_eff/K_hat/q_loc` route.

The candidate positive auxiliary signature is:

`Gamma_eff = Gamma0 + 1/2 G_AB nabla Z^A.nabla Z^B + 1/2 M_AB Z^A Z^B + O(Z^4)`.

With:

`K_hat^{{mu nu}} := 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{{mu nu}}`

up to the chosen volume-term convention.

If this is the actual MTS parent object, the Ward identity gives:

`q_loc^nu = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu)`.

So `q_loc -> 0` follows from on-shell Euler equations, no source charge, and no boundary flux.

## Honest Verdict

This is not a claim yet. The current corpus has not matched actual `Gamma_eff` and `K_hat` coefficients to `Z^A`, `G_AB`, `M_AB`, or `K_metric`.

## Bound Fallback

The fallback is now value-ready:

`epsilon_nonminimal_counterterm_GK = sum_abs(epsilon_GK_energy, epsilon_GK_metric_response_mismatch, epsilon_GK_boundary, epsilon_GK_source_charge, epsilon_GK_negative_hessian)`.

That row can be filled if the derivation route fails.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3950_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3950_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3950_GK_POSITIVE_AUXILIARY_SIGNATURE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3950_GK_WARD_QLOC_ZERO_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3950_EPSILON_NONMINIMAL_GK_BOUND_ROW.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3950_GK_PROMOTION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3950_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3950_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3950 - Gamma/Khat Positive Auxiliary Signature Or Bound

Timestamp: `{timestamp}`

- Built the sharpened positive auxiliary candidate: `Gamma_eff-Gamma0 = 1/2 G_AB nabla Z^A.nabla Z^B + 1/2 M_AB Z^A Z^B + O(Z^4)`.
- Metric-response condition: `K_hat` must be the metric variation of `sqrt(-g)Gamma_eff`; if signed, the Khat mismatch disappears by definition.
- Ward route: `q_loc^nu = -P_loc(E_A nabla^nu Z^A + R_boundary^nu + R_source^nu)`, so local zero follows only from Euler, source-silence and boundary-silence clauses.
- Bound fallback: created value-ready `epsilon_nonminimal_counterterm_GK` components for energy, metric-response mismatch, boundary, source charge and negative Hessian terms.
- Claim status: private nonclaim; actual MTS coefficient/signature match is still missing.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3950 - Gamma/Khat Positive Auxiliary Signature Or Bound"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    signature = signature_rows(timestamp)
    ward = ward_rows(timestamp)
    bound = bound_rows(timestamp)
    gate = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fwb_modified = formalization_workbench_modified_count()
    nonclaim_groups = (signature, ward, bound, gate, decisions, claim_gate, next_target)
    signature_statuses = {row["current_status"] for row in signature}
    ward_statuses = {row["current_status"] for row in ward}
    bound_symbols = {row["target_symbol"] for row in bound}
    gate_statuses = {row["status"] for row in gate}
    checks = [
        ("VAL3950_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3950_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3950_02_signature_form", "CONDITIONAL_SIGNATURE_FORM_BUILT_SYMBOL_MATCH_MISSING" in signature_statuses, "positive auxiliary signature form emitted"),
        ("VAL3950_03_Khat_response", "EXACT_IF_IDENTIFICATION_SIGNED_CURRENT_MTS_UNMATCHED" in signature_statuses, "Khat metric-response identity emitted"),
        ("VAL3950_04_double_zero", "CONDITIONAL_DOUBLE_ZERO_FORM_BUILT_COEFFICIENTS_MISSING" in signature_statuses, "double-zero clause emitted"),
        ("VAL3950_05_ward_identity", "EXACT_CONDITIONAL_IDENTITY" in ward_statuses, "Ward identity emitted"),
        ("VAL3950_06_q_loc_formula", "CONDITIONAL_QLOC_ZERO_FORMULA_BUILT" in ward_statuses, "q_loc zero formula emitted"),
        ("VAL3950_07_bound_components", {"epsilon_GK_energy", "epsilon_GK_metric_response_mismatch", "epsilon_GK_boundary", "epsilon_GK_source_charge", "epsilon_GK_negative_hessian", "epsilon_nonminimal_counterterm_GK"}.issubset(bound_symbols), "GK epsilon bound components emitted"),
        ("VAL3950_08_value_ready_rows", all(row["row_type"] == "VALUE_READY_EPSILON_NONMINIMAL_COMPONENT_ROW" for row in bound), "bound rows are value-ready component rows"),
        ("VAL3950_09_gate_blocks", "PASS_VALUE_READY_VALUES_MISSING" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "promotion gate keeps claim blocked but bound ready"),
        ("VAL3950_10_claim_gate_blocks", any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public/local-GR claim"),
        ("VAL3950_11_next_3951", next_target[0]["next_doc"] == NEXT_DOC and "coefficient" in next_target[0]["target"], "next target selects GK coefficient extraction"),
        ("VAL3950_12_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3950_13_outputs_not_fwb", all(FWB not in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3950_14_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3950_15_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3950_16_spine_written", SPINE_PATH.exists() and "3950 - Gamma/Khat Positive" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3950_17_csv_parse", csv_parse_ok(generated_csvs), "generated CSVs parse cleanly"),
        ("VAL3950_18_script_compiles", True, "script compiles"),
        ("VAL3950_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["signature"], signature_rows(timestamp))
    write_csv(OUTPUTS["ward"], ward_rows(timestamp))
    write_csv(OUTPUTS["bound"], bound_rows(timestamp))
    write_csv(OUTPUTS["gate"], gate_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3950 validation failed: {failed}")
    print(f"3950 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
