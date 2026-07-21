from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4544"
CLAIM_ID = "L-386"
BRANCH_ID = "MTS_R2FR_Y5_DTXI0_LOCAL_STATIONARITY_TPERP_4544"
MARKER = "PPC4161_DTXI0_LOCAL_STATIONARITY_ZERO_AND_TENSOR_PERP_SILENCE_OR_PROFILE_SOURCE_ROW_4544"
PACKET_MARKER = "PPC4161_PACKET_DTXI0_LOCAL_STATIONARITY_ZERO_AND_TENSOR_PERP_SILENCE_OR_PROFILE_SOURCE_ROW_4544"
DECISION = "DTXI_ZERO_THEOREM_DERIVED_CONDITIONAL_TT_GDOT_SILENCE_SPLIT_BOUND_FORM_ACTIVE_NONCLAIM"
NEXT_TARGET = "4545-Y5-R2FR-attractor-stationarity-and-boundary-silence-from-Bianchi-Hamiltonian-local-conservation.md"

FORMAL_PATH = FORMAL / "560-PPC4161-DtXi0-local-stationarity-zero-and-tensor-perp-silence-or-profile-source-row.md"
DOC_PATH = POST / "4544-Y5-R2FR-DtXi0-local-stationarity-zero-and-tensor-perp-silence-or-profile-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4544_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_DTXI_ZERO_THEOREM.csv"
JRES_CLAUSE_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_JRES_ZERO_CLAUSE_MAP.csv"
TENSOR_PERP_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_TENSOR_PERP_GDOT_SPLIT.csv"
FINITE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_DTXI_TPERP_FINITE_BOUND.csv"
PROFILE_SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_PROFILE_SOURCE_ROW_TEMPLATE.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4544_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4544_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4544_00_4543_status",
            "label": "4543 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4543_STATUS.csv",
            "needle": "profile_zero_route_identified",
            "role": "imports the selected D_t Xi_0/tensor-perp zero route",
        },
        {
            "source_id": "SRC4544_01_4543_theorem",
            "label": "4543 product-to-profile theorem",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4543_PRODUCT_TO_COEFFICIENT_THEOREM.csv",
            "needle": "T_perp,Gdot",
            "role": "imports C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot",
        },
        {
            "source_id": "SRC4544_02_4190_stationarity",
            "label": "4190 stationarity contract",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4190_STATIONARITY_CONTRACT.csv",
            "needle": "STC4190_3_stationary_sources",
            "role": "supplies the local stationarity route",
        },
        {
            "source_id": "SRC4544_03_4190_status",
            "label": "4190 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4190_STATUS.csv",
            "needle": "exact_zero_lemma_closed",
            "role": "confirms exact zero lemma was still open before 4544",
        },
        {
            "source_id": "SRC4544_04_4193_projector_zero",
            "label": "4193 projector-zero contract",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4193_PROJECTOR_ZERO_CONTRACT.csv",
            "needle": "P_loc J_res = 0",
            "role": "lists the source, attractor and boundary clauses for exact zero",
        },
        {
            "source_id": "SRC4544_05_4193_Jres",
            "label": "4193 residual-source decomposition",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4193_JRES_DECOMPOSITION.csv",
            "needle": "J_res = U_B S_cg + D_m Delta_h m_L - D_t m_L + boundary_in",
            "role": "defines the residual source whose local projection must vanish",
        },
        {
            "source_id": "SRC4544_06_4193_budget",
            "label": "4193 finite profile budget",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4193_FINITE_PROFILE_BUDGET.csv",
            "needle": "BUD4193_SYMBOLIC_DTXI",
            "role": "provides fallback profile budget form",
        },
        {
            "source_id": "SRC4544_07_4541_tensor",
            "label": "4541 tensor obstruction",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4541_CGAMMA_OBSTRUCTION_LEDGER.csv",
            "needle": "CGO4541_4_tensor",
            "role": "keeps homogeneous tensor residue as a hard obstruction unless projected or bounded",
        },
        {
            "source_id": "SRC4544_08_4542_bound",
            "label": "4542 Gdot bound",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4542_FIRST_SELECTED_BOUND_ROW.csv",
            "needle": "2.42e-14",
            "role": "sets the source-backed Gdot product threshold",
        },
        {
            "source_id": "SRC4544_09_4189_fill",
            "label": "4189 coefficient fill",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4189_FIRST_COEFFICIENT_FILL.csv",
            "needle": "c_Gamma D_t Xi_0",
            "role": "shows D_t Xi_0 is the scalar profile feeding Gdot",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "ZTH4544_0_profile_definition",
            "statement": "Xi_0 := N_0[P_loc Gamma_mem]",
            "proof_step": "This is imported from STC4190_0 and fixes the object whose local time derivative feeds Gdot.",
            "requires": "smooth scalar projection N_0",
            "status": "definition_filled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZTH4544_1_local_green_problem",
            "statement": "L_Xi delta Xi = P_loc J_res with boundary data B_Xi delta Xi = b_Xi",
            "proof_step": "4193 gives J_res; 4544 packages the scalar residual as a local Green/uniqueness problem rather than an assumed plateau.",
            "requires": "parent-owned L_Xi, boundary operator B_Xi and projection P_loc",
            "status": "derived_contract",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZTH4544_2_uniqueness_zero",
            "statement": "If gap(L_Xi|collar) >= mu_Xi > 0, P_loc J_res = 0, b_Xi = 0 and ker(L_Xi) is removed by the boundary condition, then delta Xi = 0 in the local collar.",
            "proof_step": "Coercive uniqueness: multiply by delta Xi, integrate over the collar, use no-flux/Dirichlet boundary routing, and use the positive gap to force ||delta Xi||=0.",
            "requires": "positive/gapped scalar memory operator plus exact projector-zero and boundary silence",
            "status": "conditional_theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZTH4544_3_time_derivative_zero",
            "statement": "If the local invariants and boundary data are stationary along tau, then D_t Xi_0 = 0.",
            "proof_step": "With delta Xi=0 and smooth N_0, D_t Xi_0 = DN_0[P_loc Gamma_mem] D_t(P_loc Gamma_mem); stationary source/readout invariants and stationary boundary data make this derivative vanish.",
            "requires": "STC4190_3 plus PZ4193_3 and PZ4193_4 parent-signed",
            "status": "conditional_theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZTH4544_4_gdot_silence",
            "statement": "If D_t Xi_0 = 0 and T_perp,Gdot = 0, then C_Gamma_Gdot = 0.",
            "proof_step": "Substitute into C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot.",
            "requires": "ZTH4544_3 plus tensor/perp scalar-boundary silence",
            "status": "conditional_silence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def jres_clause_rows() -> list[dict[str, Any]]:
    pz_rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4193_PROJECTOR_ZERO_CONTRACT.csv")
    mapped: list[dict[str, Any]] = []
    for row in pz_rows:
        mapped.append(
            {
                "clause_id": row["contract_id"].replace("PZ4193", "PZ4544"),
                "condition": row["condition"],
                "role": row["role"],
                "required_evidence": row["required_evidence"],
                "old_status": row["status"],
                "4544_result": "required_for_exact_DtXi0_zero" if row["status"] == "open" else "active_hygiene_rule",
                "closed_by_4544": "False",
                "next_action": "try parent-signing from Bianchi/Hamiltonian local conservation" if row["status"] == "open" else "keep as no-cancellation guard",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return mapped


def tensor_perp_rows() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "TPS4544_0_definition",
            "piece": "T_perp,Gdot",
            "projection_statement": "T_perp,Gdot := P_Gdot[Gamma_perp/K_perp]",
            "4544_result": "split_into_TT_trace_boundary_pieces",
            "status": "derived_split",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "split_id": "TPS4544_1_TT",
            "piece": "transverse_tracefree_monopole",
            "projection_statement": "P_Gdot^monopole[Gamma_perp^TT] = 0",
            "4544_result": "first-order scalar Gdot readout does not see pure tracefree/angle-averaged tensor residue",
            "status": "mathematical_projection_zero_if_TT_definition_holds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "split_id": "TPS4544_2_trace_scalar",
            "piece": "trace_or_scalar_boundary_residue",
            "projection_statement": "P_Gdot^monopole[Gamma_perp^tr/scalar] need not vanish",
            "4544_result": "this is the remaining tensor-perp contribution to bound",
            "status": "open_residual",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "split_id": "TPS4544_3_boundary",
            "piece": "incoming_boundary_or_homogeneous_mode",
            "projection_statement": "P_Gdot[Gamma_perp^bdy] = 0 only under parent-selected no-influx/Hamiltonian routing",
            "4544_result": "boundary silence is required before local Gdot silence can be claimed",
            "status": "open_residual",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def finite_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "FB4544_0_DtXi_dynamic",
            "quantity": "|D_t Xi_0|",
            "bound_form": "|D_t Xi_0| <= K_t (||P_loc D_t J_res||/mu_Xi + ||D_t b_Xi||/beta_Xi + ||D_t h_ker||)",
            "derivation": "Differentiate the local Green problem and use the inverse norm of L_Xi plus boundary control.",
            "needed_inputs": "K_t, mu_Xi, beta_Xi, P_loc D_t J_res, D_t b_Xi, kernel/homogeneous drift",
            "status": "finite_bound_formula_derived_not_numeric",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "FB4544_1_Tperp",
            "quantity": "|T_perp,Gdot|",
            "bound_form": "|T_perp,Gdot| <= T_trace + T_boundary after TT monopole projection",
            "derivation": "The scalar Gdot readout kills pure TT monopole response but not scalar trace or boundary residue.",
            "needed_inputs": "trace/scalar residue amplitude and boundary/homogeneous mode amplitude",
            "status": "finite_bound_formula_derived_not_numeric",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "FB4544_2_product_budget",
            "quantity": "|C_Gamma_Gdot|",
            "bound_form": "|c_Gamma| K_t (||P_loc D_t J_res||/mu_Xi + ||D_t b_Xi||/beta_Xi + ||D_t h_ker||) + T_trace + T_boundary <= 2.42e-14 yr^-1",
            "derivation": "Insert FB4544_0 and FB4544_1 into the 4543 channel identity and product bound.",
            "needed_inputs": "same as FB4544_0 plus T_trace and T_boundary",
            "status": "first_explicit_nonzero_profile_source_budget",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def profile_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_row_id": "PSR4544_0_source_silence",
            "missing_or_derived_input": "P_loc D_t[U_B S_cg]",
            "units": "source/time in Xi equation",
            "source_path_or_parent_clause": "PZ4193_1_source_silence",
            "needed_for": "P_loc D_t J_res = 0 or finite D_t Xi_0 bound",
            "status": "needs_parent_signature_or_numeric_source_bound",
            "valid_for_claim": "False",
        },
        {
            "source_row_id": "PSR4544_1_attractor_homogeneity",
            "missing_or_derived_input": "P_loc D_t[D_m Delta_h m_L]",
            "units": "source/time in Xi equation",
            "source_path_or_parent_clause": "PZ4193_2_attractor_homogeneity",
            "needed_for": "no spatial attractor drift feeding Gdot profile",
            "status": "needs_parent_signature_or_numeric_source_bound",
            "valid_for_claim": "False",
        },
        {
            "source_row_id": "PSR4544_2_attractor_stationarity",
            "missing_or_derived_input": "P_loc D_t^2 m_L",
            "units": "source/time in Xi equation",
            "source_path_or_parent_clause": "PZ4193_3_attractor_stationarity",
            "needed_for": "local memory stationarity D_t Xi_0=0",
            "status": "selected_for_4545_derivation",
            "valid_for_claim": "False",
        },
        {
            "source_row_id": "PSR4544_3_boundary_silence",
            "missing_or_derived_input": "D_t b_Xi and T_boundary",
            "units": "yr^-1 equivalent after projection",
            "source_path_or_parent_clause": "PZ4193_4_boundary_silence",
            "needed_for": "tensor-perp and scalar profile silence",
            "status": "selected_for_4545_derivation",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4544_0_DtXi_zero_theorem",
            "gate": "D_t Xi_0 exact zero theorem",
            "status": "PASS_AS_CONDITIONAL_THEOREM",
            "meaning": "the theorem is now explicit, but its projector/source/boundary clauses are not parent-signed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4544_1_TT_projection",
            "gate": "TT tensor-perp Gdot projection",
            "status": "PASS_IF_TT_DEFINITION_HOLDS",
            "meaning": "pure tracefree tensor monopole response is silent, but scalar trace/boundary residue remains",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4544_2_full_Tperp_silence",
            "gate": "full T_perp,Gdot silence",
            "status": "BLOCKED_TRACE_BOUNDARY_RESIDUE",
            "meaning": "trace/scalar and boundary pieces still need proof or bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4544_3_local_Gdot_pass",
            "gate": "local Gdot/channel pass",
            "status": "BLOCKED_PARENT_SIGNATURE_OR_NUMERIC_BUDGET",
            "meaning": "C_Gamma_Gdot can be zero or bounded only after PZ clauses close or finite budget inputs are sourced",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4544_0",
            "decision": DECISION,
            "meaning": "4544 constructs the non-smuggled route from projector-zero to D_t Xi_0=0, and narrows tensor-perp: pure TT monopole response is silent, but scalar trace/boundary residue remains. The fallback is now an explicit finite source budget, not a vague missing-input note.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4544_0",
            "target": NEXT_TARGET,
            "objective": "try to parent-sign the attractor stationarity and boundary silence clauses using local conservation/Hamiltonian boundary routing; if not, fill the first numeric source-budget row",
            "derive_first": "P_loc[D_t m_L]=0 and P_loc[boundary_in]=0 from stationary local invariants plus no-flux/Hamiltonian boundary conditions",
            "fallback": "source K_t, mu_Xi, beta_Xi, D_t J_res and T_boundary values for FB4544_2",
            "avoid": "claiming local Gdot silence from TT projection alone",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "DtXi0_zero_theorem_written": "True",
            "DtXi0_zero_parent_signed": "False",
            "TT_Gdot_projection_zero": "conditional_true",
            "full_Tperp_zero": "False",
            "finite_profile_bound_written": "True",
            "numeric_profile_source_row_available": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    zero_theorem: list[dict[str, Any]],
    jres_clauses: list[dict[str, Any]],
    tensor_split: list[dict[str, Any]],
    finite_bounds: list[dict[str, Any]],
    profile_sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4544_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    green_problem = any(row["theorem_id"] == "ZTH4544_1_local_green_problem" and "P_loc J_res" in row["statement"] for row in zero_theorem)
    checks.append({"validation_id": "VAL4544_01_green_problem", "status": "PASS" if green_problem else "FAIL", "detail": "local Green problem derived for profile zero route"})

    uniqueness = any(row["theorem_id"] == "ZTH4544_2_uniqueness_zero" and "mu_Xi" in row["statement"] for row in zero_theorem)
    checks.append({"validation_id": "VAL4544_02_uniqueness", "status": "PASS" if uniqueness else "FAIL", "detail": "coercive uniqueness route to delta Xi=0 written"})

    open_clauses = [row for row in jres_clauses if row["old_status"] == "open" and row["closed_by_4544"] == "False"]
    checks.append({"validation_id": "VAL4544_03_open_clauses_honest", "status": "PASS" if len(open_clauses) >= 4 else "FAIL", "detail": "projector-zero clauses remain explicit and unclaimed"})

    tt_zero = any(row["split_id"] == "TPS4544_1_TT" and "projection_zero" in row["status"] for row in tensor_split)
    residual_open = any(row["split_id"] == "TPS4544_2_trace_scalar" and row["status"] == "open_residual" for row in tensor_split)
    checks.append({"validation_id": "VAL4544_04_tensor_split", "status": "PASS" if tt_zero and residual_open else "FAIL", "detail": "TT projection is separated from scalar/boundary residuals"})

    finite_budget = any(row["bound_id"] == "FB4544_2_product_budget" and "2.42e-14" in row["bound_form"] for row in finite_bounds)
    checks.append({"validation_id": "VAL4544_05_finite_budget", "status": "PASS" if finite_budget else "FAIL", "detail": "nonzero profile/source budget is explicit"})

    selected_sources = any(row["source_row_id"] == "PSR4544_2_attractor_stationarity" and row["status"] == "selected_for_4545_derivation" for row in profile_sources) and any(row["source_row_id"] == "PSR4544_3_boundary_silence" and row["status"] == "selected_for_4545_derivation" for row in profile_sources)
    checks.append({"validation_id": "VAL4544_06_next_sources", "status": "PASS" if selected_sources else "FAIL", "detail": "4545 targets stationarity and boundary silence, not all clauses at once"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    blocked = any(row["claim_gate_id"] == "CG4544_3_local_Gdot_pass" and row["status"].startswith("BLOCKED") for row in gates)
    checks.append({"validation_id": "VAL4544_07_claim_firewall", "status": "PASS" if gates_ok and blocked else "FAIL", "detail": "local Gdot/GR remains nonclaim until parent signature or numeric budget"})

    csv_paths = [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        JRES_CLAUSE_MAP_CSV,
        TENSOR_PERP_SPLIT_CSV,
        FINITE_BOUND_CSV,
        PROFILE_SOURCE_ROW_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4544_08_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4544_09_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4544_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4544 D_t Xi_0 local stationarity and tensor-perp silence theorem/bound"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    zero_theorem: list[dict[str, Any]],
    jres_clauses: list[dict[str, Any]],
    tensor_split: list[dict[str, Any]],
    finite_bounds: list[dict[str, Any]],
    profile_sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4544 - D_t Xi_0 local stationarity zero and tensor-perp silence or profile source row

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4543 showed that the Gdot channel is:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot.
```

4544 turns the desired local-vacuum/profile silence into an actual theorem contract:

```text
L_Xi delta Xi = P_loc J_res,      B_Xi delta Xi = b_Xi.
```

If the scalar memory operator is gapped, the local projected residual source vanishes, the boundary data are silent, and the homogeneous kernel is removed, coercive uniqueness gives `delta Xi=0`. With stationary local invariants and stationary boundary data, this gives:

```text
D_t Xi_0 = 0.
```

The tensor-perp obstruction is also narrowed. A pure transverse-tracefree monopole contribution is silent to the scalar Gdot readout, but trace/scalar and boundary pieces are not automatically killed:

```text
T_perp,Gdot = T_TT,Gdot + T_trace,Gdot + T_boundary,Gdot,
P_Gdot^monopole[T_TT] = 0,
T_trace,Gdot + T_boundary,Gdot still open.
```

So the branch has moved from "we need a plateau" to a real route: either parent-sign the projector-zero/boundary clauses, or satisfy the finite budget:

```text
|c_Gamma| K_t (||P_loc D_t J_res||/mu_Xi + ||D_t b_Xi||/beta_Xi + ||D_t h_ker||)
  + T_trace + T_boundary <= 2.42e-14 yr^-1.
```

## D_t Xi_0 Zero Theorem

{markdown_table(zero_theorem)}

## J_res Zero Clause Map

{markdown_table(jres_clauses)}

## Tensor-Perp Gdot Split

{markdown_table(tensor_split)}

## Finite Bound Form

{markdown_table(finite_bounds)}

## Profile Source Row Template

{markdown_table(profile_sources)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_memory_bound",
        "claim": "4544 derives the conditional D_t Xi_0 zero theorem from a local Green/uniqueness problem and splits tensor-perp into TT-silent and scalar/boundary residual pieces; local Gdot silence remains nonclaim until projector-zero and boundary clauses are parent-signed or numerically bounded.",
        "current_evidence": "Generated source register, D_t Xi_0 zero theorem, J_res clause map, tensor-perp Gdot split, finite bound form, profile source template, claim gates, status and validation CSVs.",
        "status": "conditional_DtXi_zero_theorem_and_tensor_perp_split_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Claiming local Gdot silence from TT projection alone while scalar trace/boundary residue remains open.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Parent signatures for stationarity/boundary silence are not yet supplied.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    zero_theorem = zero_theorem_rows()
    jres_clauses = jres_clause_rows()
    tensor_split = tensor_perp_rows()
    finite_bounds = finite_bound_rows()
    profile_sources = profile_source_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_THEOREM_CSV, zero_theorem)
    write_csv(JRES_CLAUSE_MAP_CSV, jres_clauses)
    write_csv(TENSOR_PERP_SPLIT_CSV, tensor_split)
    write_csv(FINITE_BOUND_CSV, finite_bounds)
    write_csv(PROFILE_SOURCE_ROW_CSV, profile_sources)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, zero_theorem, jres_clauses, tensor_split, finite_bounds, profile_sources, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, zero_theorem, jres_clauses, tensor_split, finite_bounds, profile_sources, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4544 D_t Xi_0 Local Stationarity And Tensor-Perp Silence

Marker: `{MARKER}`  
4544 replaces a plateau assumption with a conditional Green/uniqueness theorem: if `L_Xi delta Xi = P_loc J_res` has positive gap, zero projected source, silent boundary data and no homogeneous kernel, then `delta Xi=0`; with stationary local invariants, `D_t Xi_0=0`. It also narrows `T_perp,Gdot`: pure TT monopole response is silent, while trace/scalar and boundary pieces remain as finite residuals. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4544 Packet Integration - Profile Zero Theorem And Tensor-Perp Split

Marker: `{PACKET_MARKER}`  
The local packet now carries the exact theorem contract for `D_t Xi_0=0` and the finite fallback budget `|c_Gamma| K_t(...) + T_trace + T_boundary <= 2.42e-14 yr^-1`. This is a forward derivation, not a claim: stationarity and boundary silence still need parent signatures.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
