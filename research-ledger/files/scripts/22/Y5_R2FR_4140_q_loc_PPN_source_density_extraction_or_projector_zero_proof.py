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
DOC_PATH = ROOT / "4140-Y5-R2FR-q-loc-PPN-source-density-extraction-or-projector-zero-proof.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_QLOC_PPN_SOURCE_DENSITY_OR_PROJECTOR_ZERO_4140"
CHECKPOINT_ID = "4140"
DECISION = "QLOC_PPN_SOURCE_DENSITY_REDUCED_TO_DIVERGENCE_PROJECTOR_ZERO_OR_CURRENT_OVERLAP_BOUND"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4140_00_4139_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4139_NEXT_TARGET.csv",
        "4140-Y5-R2FR-q-loc-PPN-source-density-extraction-or-projector-zero-proof.md",
        "4139 selected q_loc PPN source-density extraction or projector-zero proof.",
    ),
    "SRC4140_01_4139_projector": (
        SOURCE_DIR / "P8_Y5_R2FR_4139_CBETA_QLOC_PROJECTOR_DERIVATION.csv",
        "S_q00^{(4)}",
        "4139 projector derivation naming the missing source density.",
    ),
    "SRC4140_02_4139_acquisition": (
        SOURCE_DIR / "P8_Y5_R2FR_4139_SOURCE_ACQUISITION_PACK.csv",
        "S_q00^{(4)}(x)",
        "4139 source acquisition pack.",
    ),
    "SRC4140_03_4137_action": (
        SOURCE_DIR / "P8_Y5_R2FR_4137_ACTION_FORK.csv",
        "q_loc^nu=P_loc nabla_mu T_GK",
        "4137 exact q_loc stress-divergence identity.",
    ),
    "SRC4140_04_4137_profile": (
        SOURCE_DIR / "P8_Y5_R2FR_4137_QLOC_PROFILE_BOUND_ROWS.csv",
        "D_A_grad",
        "4137 D_A_grad profile component.",
    ),
    "SRC4140_05_4138_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND.csv",
        "D_A_grad <=",
        "4138 D_A_grad insertion and trace-free bound law.",
    ),
    "SRC4140_06_4138_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv",
        "live Khat adoption",
        "4138 live adoption blocker for converting constructed stress into current stress.",
    ),
    "SRC4140_07_3969_q_loc": (
        SOURCE_DIR / "P8_Y5_R2FR_3969_BETA_OBSTRUCTION_BOUND_ROWS.csv",
        "q_loc_U2",
        "Prior q_loc second-order beta obstruction row.",
    ),
    "SRC4140_08_3991_schema": (
        SOURCE_DIR / "P8_Y5_R2FR_3991_PPN_BETA_SOURCE_EVALUATOR_SCHEMA.csv",
        "delta_beta_source_abs",
        "PPN beta source evaluator convention.",
    ),
    "SRC4140_09_3919_inputs": (
        SOURCE_DIR / "P8_Y5_R2FR_3919_BETA_BOUND_INPUTS.csv",
        "A_source",
        "Same-normalized A_source/B_source input ledger.",
    ),
    "SRC4140_10_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4140_q_loc_PPN_source_density_extraction_or_projector_zero_proof.py",
        "Reproducible generator for this 4140 checkpoint.",
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


def source_density_derivation_rows() -> List[dict]:
    data = [
        (
            "SD4140_0_q_identity",
            "q_loc stress-divergence identity",
            "q_loc^nu=P_loc nabla_mu T_GK^{mu nu}; T_GK^{mu nu}=Gamma_eff g^{mu nu}-Khat^{mu nu}",
            "The PPN source-density problem should start from a stress object, not from an unconstrained force guess.",
            "EXACT_IDENTITY_IMPORTED",
            "current T_GK is not fully parent-response signed",
        ),
        (
            "SD4140_1_current_residual",
            "current branch residual",
            "q_loc_current=-P_loc(E_A nabla Y^A+R_boundary+R_source+nabla_mu Delta_K^{mu nu})",
            "The beta source density must be built from the retained residual pieces, especially D_A_grad/Delta_K.",
            "CURRENT_BRANCH_BOUND_OBJECT",
            "Euler, boundary, source-normalization and Delta_K pieces are not theorem-zero",
        ),
        (
            "SD4140_2_ppn_source_operator",
            "PPN 00 source operator",
            "S_q00^{(4)}=Pi_00^{PPN}[delta T_q^{00}+delta T_q^{ii}+gauge/nonlinear source terms]_{U^2}",
            "This is the object that enters L_00 h_00,q^{(4)}=S_q00^{(4)}.",
            "SOURCE_DENSITY_CONTRACT_WRITTEN",
            "delta T_q and gauge/nonlinear terms are not extracted numerically",
        ),
        (
            "SD4140_3_direct_stress_route",
            "direct stress route",
            "delta T_D^{mu nu}:=delta Gamma_eff g^{mu nu}-Delta_K^{mu nu}+delta g^{mu nu} Gamma_eff",
            "If current Khat/Gamma is live-response signed, S_q00 can be read from delta T_D without inverting the divergence.",
            "BEST_ROUTE_CONDITIONAL",
            "live Khat adoption failed in 4138",
        ),
        (
            "SD4140_4_inverse_divergence_route",
            "inverse divergence route",
            "find delta T_q such that nabla_mu delta T_q^{mu nu}=q_loc^nu",
            "This route is nonunique: improvement/gauge stresses change delta T_q while preserving the divergence.",
            "AMBIGUOUS_WITHOUT_STRESS_GAUGE",
            "requires stress reconstruction gauge and boundary convention",
        ),
        (
            "SD4140_5_divergence_current_reduction",
            "D_A_grad current form",
            "S_q00^{(4)} = partial_i J_q^i + S_q,bulk + S_q,gauge at O(U^2)",
            "For the trace-free/improvement branch the leading beta source can be tested as a divergence-current projector plus bulk/gauge remnants.",
            "DIVERGENCE_FORM_REDUCED",
            "J_q^i and bulk/gauge split are not source-backed",
        ),
        (
            "SD4140_6_adjoint_projector_identity",
            "adjoint U2 projector identity",
            "<L_00^{-1} partial_i J_q^i,U^2> = B_J[partial Omega] - <J_q^i, partial_i chi_U>",
            "Here L_00^dagger chi_U=U^2. This is the exact zero-or-bound fork for a divergence source.",
            "PROJECTOR_IDENTITY_DERIVED",
            "need boundary term B_J and current-overlap integral",
        ),
        (
            "SD4140_7_zero_condition",
            "source-density zero condition",
            "delta_beta_q_loc=0 if S_q,bulk=S_q,gauge=0, B_J=0, and <J_q^i,partial_i chi_U>=0",
            "Total divergence alone is not enough; the current must be boundary-silent and adjoint-orthogonal.",
            "ZERO_CONDITION_SHARPENED",
            "orthogonality is not proved for current MTS profiles",
        ),
        (
            "SD4140_8_bound_condition",
            "source-density bound condition",
            "|delta_beta_q_loc| <= (1/(2N_U2))(|B_J|+||J_q|| ||grad chi_U||+||L_00^{-1}S_q,bulk||_U2+||L_00^{-1}S_q,gauge||_U2)",
            "If zero fails, the beta bound is an overlap/boundary/bulk norm problem, not a vague missing coefficient.",
            "BOUND_LAW_DERIVED",
            "all norms are symbolic only",
        ),
    ]
    rows: List[dict] = []
    for derivation_id, step, formula, meaning, status, blocker in data:
        row = row_base()
        row.update(
            {
                "derivation_id": derivation_id,
                "step": step,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "blocker": blocker,
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def divergence_projector_theorem_rows() -> List[dict]:
    data = [
        (
            "TH4140_0_operator_setup",
            "operator setup",
            "L_00 h=S; L_00^dagger chi_U=U^2; N_U2=<U^2,U^2>",
            "defines the adjoint projector without choosing a toy kernel",
            "THEOREM_SETUP",
        ),
        (
            "TH4140_1_divergence_source",
            "divergence source",
            "S=partial_i J^i+S_bulk+S_gauge",
            "separates boundary/current overlap from true bulk and gauge remnants",
            "DIVERGENCE_SPLIT",
        ),
        (
            "TH4140_2_integration_by_parts",
            "adjoint integration by parts",
            "<L_00^{-1}partial_iJ^i,U^2>=int_boundary n_i J^i chi_U dS - int_Omega J^i partial_i chi_U d^3x",
            "the beta projection of a divergence is zero only if both terms vanish",
            "EXACT_IDENTITY",
        ),
        (
            "TH4140_3_zero_theorem",
            "zero theorem",
            "delta_beta_q=0 if B_J=0, I_J:=int J^i partial_i chi_U d^3x=0, and S_bulk=S_gauge=0",
            "this is the exact local beta projector-zero target",
            "ZERO_IF_ALL_SIGNED",
        ),
        (
            "TH4140_4_bound_theorem",
            "bound theorem",
            "|delta_beta_q| <= (|B_J|+|I_J|+|I_bulk|+|I_gauge|)/(2N_U2)",
            "the first honest beta bound can be built from four quantities",
            "BOUND_IF_NOT_ZERO",
        ),
    ]
    rows: List[dict] = []
    for theorem_id, item, formula, meaning, status in data:
        row = row_base()
        row.update(
            {
                "theorem_id": theorem_id,
                "item": item,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "theorem_zero_signed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def zero_proof_audit_rows() -> List[dict]:
    data = [
        (
            "ZA4140_0_live_stress",
            "live stress object",
            "delta T_D^{mu nu} is parent-owned and current Khat/Gamma adopted",
            "FAIL_CURRENT_BRANCH",
            "4138 live Khat adoption is unsigned",
        ),
        (
            "ZA4140_1_ppn_gauge",
            "PPN source gauge",
            "Pi_00^{PPN} and same-normalized U/A_source are fixed",
            "MISSING_NORMALIZATION",
            "4139 defines the contract but does not supply U or A_source",
        ),
        (
            "ZA4140_2_divergence_split",
            "divergence split",
            "S_q00^{(4)}=partial_i J_q^i+S_q,bulk+S_q,gauge with source-backed rows",
            "FORMAL_SPLIT_ONLY",
            "J_q^i, S_bulk and S_gauge not extracted",
        ),
        (
            "ZA4140_3_boundary_zero",
            "boundary silence",
            "B_J=int_boundary n_i J_q^i chi_U dS=0",
            "UNSIGNED_BOUNDARY",
            "compact collar/no-flux not mapped to this adjoint beta boundary",
        ),
        (
            "ZA4140_4_current_overlap_zero",
            "adjoint current orthogonality",
            "I_J=int_Omega J_q^i partial_i chi_U d^3x=0",
            "UNSIGNED_NEW_CORE_TEST",
            "this is the new non-circular target",
        ),
        (
            "ZA4140_5_bulk_gauge_zero",
            "bulk/gauge remainder zero",
            "S_q,bulk=0 and S_q,gauge=0 or separately bounded",
            "UNSIGNED_REMAINDER",
            "source-normalization/readout gauge remains open",
        ),
        (
            "ZA4140_6_beta_claim",
            "beta/local-GR claim",
            "all above signed or four-term absolute bound below 7.8e-05 with total beta vector controlled",
            "NO_CLAIM",
            "not score-ready",
        ),
    ]
    rows: List[dict] = []
    for audit_id, gate, pass_condition, status, blocker in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "gate": gate,
                "pass_condition": pass_condition,
                "status": status,
                "blocker": blocker,
                "gate_passed": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def first_density_rows() -> List[dict]:
    data = [
        (
            "DEN4140_0_sigma_q",
            "sigma_q_U2",
            "Pi_00^{PPN}[delta T_q^{00}+delta T_q^{ii}]_{U^2}",
            "PPN source density units",
            "derive from live delta T_D or a declared stress-reconstruction gauge",
            "MISSING_SOURCE_BACKED_DENSITY",
        ),
        (
            "DEN4140_1_current",
            "J_q^i",
            "current whose divergence supplies the D_A_grad/improvement part of S_q00^{(4)}",
            "source density times length",
            "extract from Delta_K/D_A_grad and PPN projection",
            "MISSING_CURRENT_PROFILE",
        ),
        (
            "DEN4140_2_boundary",
            "B_J",
            "int_boundary n_i J_q^i chi_U dS",
            "projected beta numerator units",
            "evaluate no-flux/collar surface term or prove zero",
            "MISSING_BOUNDARY_VALUE",
        ),
        (
            "DEN4140_3_overlap",
            "I_J",
            "int_Omega J_q^i partial_i chi_U d^3x",
            "projected beta numerator units",
            "compute or prove adjoint orthogonality",
            "MISSING_CORE_OVERLAP",
        ),
        (
            "DEN4140_4_bulk",
            "I_bulk",
            "<L_00^{-1}S_q,bulk,U^2>",
            "projected beta numerator units",
            "derive bulk remainder or prove absent",
            "MISSING_BULK_REMAINDER",
        ),
        (
            "DEN4140_5_gauge",
            "I_gauge",
            "<L_00^{-1}S_q,gauge,U^2>",
            "projected beta numerator units",
            "fix PPN gauge/readout and prove zero or bound",
            "MISSING_GAUGE_REMAINDER",
        ),
        (
            "DEN4140_6_norm",
            "N_U2",
            "<U^2,U^2>_Omega",
            "U^4 times volume/window units",
            "source-normalized U and domain/window",
            "MISSING_PROJECTION_NORM",
        ),
        (
            "DEN4140_7_beta",
            "delta_beta_q_loc",
            "-(B_J-I_J+I_bulk+I_gauge)/(2N_U2) with sign set by the chosen L_00 convention",
            "dimensionless",
            "all numerator terms and N_U2 numeric/source-backed",
            "NOT_SCORE_READY",
        ),
    ]
    rows: List[dict] = []
    for density_id, symbol, formula, units, required_input, status in data:
        row = row_base()
        row.update(
            {
                "density_id": density_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "required_input": required_input,
                "status": status,
                "numeric_value_present": "False",
                "source_backed": "False",
                "score_ready": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_gate_rows() -> List[dict]:
    data = [
        (
            "DG4140_0_source_density_reduced",
            "SOURCE_DENSITY_PROBLEM_REDUCED",
            "S_q00^{(4)} is now reduced to either direct stress extraction or a divergence-current plus bulk/gauge remainder.",
            "do not keep saying source density is missing; target the current/overlap rows",
        ),
        (
            "DG4140_1_total_divergence_not_enough",
            "TOTAL_DIVERGENCE_IS_NOT_AUTOMATIC_ZERO",
            "A divergence source still contributes to beta unless the adjoint boundary term and current-overlap vanish.",
            "prevents a fake closure shortcut",
        ),
        (
            "DG4140_2_new_core_test",
            "ADJOINT_CURRENT_OVERLAP_SELECTED",
            "The new decisive test is I_J=int J_q^i partial_i chi_U d^3x plus boundary silence.",
            "derive J_q^i for the trace-free/improvement branch next",
        ),
        (
            "DG4140_3_bound_pack",
            "FIRST_DENSITY_BOUND_ROWS_FILLED",
            "The source-ready rows for sigma_q_U2, J_q, B_J, I_J, bulk/gauge remnants and N_U2 are now explicit.",
            "can become numeric once profiles/kernels are supplied",
        ),
        (
            "DG4140_4_next",
            "NEXT_TRACEFREE_CURRENT_OVERLAP_SELECTED",
            "Use the trace-free Khat/improvement branch to derive J_q^i and test B_J=0 and I_J=0.",
            "4141-Y5-R2FR-tracefree-current-overlap-zero-or-beta-density-bound.md",
        ),
    ]
    rows: List[dict] = []
    for gate_id, decision, rationale, next_action in data:
        row = row_base()
        row.update(
            {
                "gate_id": gate_id,
                "decision": decision,
                "rationale": rationale,
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
            "status_id": "STATUS4140_0",
            "result": DECISION,
            "summary": (
                "4140 derives the source-density fork behind C_beta_qloc. The q_loc/D_A_grad source can be read directly from a parent-owned stress only if live Khat/Gamma adoption closes; otherwise the improvement branch reduces to a divergence current plus bulk/gauge remnants. "
                "Using the adjoint beta projector, a divergence source has zero beta projection only when the boundary term B_J and current-overlap I_J vanish. This gives a concrete next proof target rather than another generic missing-source note."
            ),
            "source_density_contract_written": "True",
            "divergence_projector_identity_derived": "True",
            "projector_zero_signed": "False",
            "first_density_rows_filled": "True",
            "score_ready": "False",
            "claim_state": "no S_q00 numeric row, C_beta_qloc score, q_loc beta pass, total PPN pass, local-GR pass, Newton limit claim, or public evidence claim",
            "next_target": "4141 tracefree current-overlap zero or beta-density bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4140_0",
            "target_doc": "4141-Y5-R2FR-tracefree-current-overlap-zero-or-beta-density-bound.md",
            "target_script": "scripts/Y5_R2FR_4141_tracefree_current_overlap_zero_or_beta_density_bound.py",
            "objective": (
                "derive the trace-free/improvement current J_q^i from Delta_K/D_A_grad and test whether the adjoint beta boundary term B_J and current-overlap I_J vanish; "
                "if not, emit the first beta-density bound row for |B_J|+|I_J|"
            ),
            "success_gate": "B_J=0 and I_J=0 are theorem-signed for the trace-free branch, or source-backed bound rows exist for both",
            "reason": "4140 shows total divergence is insufficient; the sharp local beta test is boundary silence plus adjoint current orthogonality.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4140_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4140_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4140_SOURCE_DENSITY_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4140_SOURCE_DENSITY_DERIVATION.csv",
        "P8_Y5_R2FR_4140_DIVERGENCE_PROJECTOR_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4140_DIVERGENCE_PROJECTOR_THEOREM.csv",
        "P8_Y5_R2FR_4140_ZERO_PROOF_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4140_ZERO_PROOF_AUDIT.csv",
        "P8_Y5_R2FR_4140_FIRST_DENSITY_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4140_FIRST_DENSITY_ROWS.csv",
        "P8_Y5_R2FR_4140_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4140_DECISION_GATES.csv",
        "P8_Y5_R2FR_4140_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4140_STATUS.csv",
        "P8_Y5_R2FR_4140_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4140_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4140 - q_loc PPN Source Density Extraction Or Projector Zero Proof",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- The missing `S_q00^{(4)}` object is no longer vague: it is either a direct parent-owned stress source or a divergence-current plus bulk/gauge remainder.",
        "- A total divergence is not automatically safe; it is beta-safe only when the adjoint boundary term and current-overlap vanish.",
        "- No beta/local-GR score is claimed.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(
        [
            "",
            "## Source-Density Fork",
            "",
            "`S_q00^{(4)}=Pi_00^{PPN}[delta T_q^{00}+delta T_q^{ii}+gauge/nonlinear source terms]_{U^2}`.",
            "",
            "If current `Khat/Gamma` is live-response signed, use",
            "",
            "`delta T_D^{mu nu}:=delta Gamma_eff g^{mu nu}-Delta_K^{mu nu}+delta g^{mu nu} Gamma_eff`.",
            "",
            "If not, reduce the retained branch to",
            "",
            "`S_q00^{(4)} = partial_i J_q^i + S_q,bulk + S_q,gauge`.",
            "",
            "## Adjoint Projector Identity",
            "",
            "Let `L_00 h=S`, `L_00^dagger chi_U=U^2`, and `N_U2=<U^2,U^2>`.",
            "",
            "`<L_00^{-1} partial_i J_q^i,U^2> = B_J[partial Omega] - <J_q^i, partial_i chi_U>`.",
            "",
            "Therefore `delta_beta_q_loc=0` requires `B_J=0`, `I_J=<J_q^i,partial_i chi_U>=0`, and no bulk/gauge remainder.",
            "",
            "## First Density Rows",
            "",
            "| symbol | status | required input |",
            "|---|---|---|",
        ]
    )
    for row in first_density_rows():
        sections.append(f"| {row['symbol']} | {row['status']} | {row['required_input']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- No `S_q00` numeric row, `C_beta_qloc` score, `q_loc` beta pass, total PPN pass, local-GR pass, Newton-limit claim, or public evidence claim follows from 4140.",
            "- The useful movement is sharp: the next proof is not generic sourcing, it is `B_J=0` and `I_J=0` for the trace-free/improvement current.",
            "",
            "## Next Target",
            "",
            "- `4141-Y5-R2FR-tracefree-current-overlap-zero-or-beta-density-bound.md`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4140_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4140_SOURCE_DENSITY_DERIVATION": source_density_derivation_rows,
        "P8_Y5_R2FR_4140_DIVERGENCE_PROJECTOR_THEOREM": divergence_projector_theorem_rows,
        "P8_Y5_R2FR_4140_ZERO_PROOF_AUDIT": zero_proof_audit_rows,
        "P8_Y5_R2FR_4140_FIRST_DENSITY_ROWS": first_density_rows,
        "P8_Y5_R2FR_4140_DECISION_GATES": decision_gate_rows,
        "P8_Y5_R2FR_4140_STATUS": status_rows,
        "P8_Y5_R2FR_4140_NEXT_TARGET": next_target_rows,
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
        "VAL4140_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add(
        "VAL4140_1_doc",
        "checkpoint markdown exists and names decision",
        DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"),
        str(DOC_PATH),
    )

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
    add("VAL4140_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    derivation_text = flatten_rows([outputs["P8_Y5_R2FR_4140_SOURCE_DENSITY_DERIVATION"]])
    derivation_ok = all(
        token in derivation_text
        for token in [
            "q_loc^nu=P_loc",
            "S_q00^{(4)}",
            "delta T_D",
            "partial_i J_q^i",
            "L_00^dagger chi_U=U^2",
            "delta_beta_q_loc=0",
            "BOUND_LAW_DERIVED",
        ]
    )
    add("VAL4140_3_density_derivation", "source-density derivation covers q identity, S_q00, direct stress, divergence current, adjoint projector, zero and bound laws", derivation_ok, "derivation tokens checked")

    theorem_text = flatten_rows([outputs["P8_Y5_R2FR_4140_DIVERGENCE_PROJECTOR_THEOREM"]])
    theorem_ok = all(
        token in theorem_text
        for token in [
            "L_00 h=S",
            "S=partial_i J^i",
            "int_boundary",
            "I_J",
            "BOUND_IF_NOT_ZERO",
        ]
    )
    add("VAL4140_4_projector_theorem", "projector theorem has operator setup, divergence split, boundary identity, zero theorem and bound theorem", theorem_ok, "theorem tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4140_ZERO_PROOF_AUDIT"]])
    audit_ok = all(
        token in audit_text
        for token in [
            "live stress object",
            "PPN source gauge",
            "divergence split",
            "boundary silence",
            "adjoint current orthogonality",
            "bulk/gauge remainder zero",
            "NO_CLAIM",
        ]
    )
    add("VAL4140_5_zero_audit", "zero audit covers live stress, PPN gauge, divergence split, boundary, adjoint overlap, bulk/gauge and no-claim", audit_ok, "audit tokens checked")

    density_text = flatten_rows([outputs["P8_Y5_R2FR_4140_FIRST_DENSITY_ROWS"]])
    density_ok = all(
        token in density_text
        for token in [
            "sigma_q_U2",
            "J_q^i",
            "B_J",
            "I_J",
            "I_bulk",
            "I_gauge",
            "N_U2",
            "delta_beta_q_loc",
        ]
    )
    add("VAL4140_6_density_rows", "density rows include sigma, current, boundary, overlap, bulk, gauge, norm and beta", density_ok, "density tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4140_DECISION_GATES"]])
    decision_ok = all(
        token in decision_text
        for token in [
            "SOURCE_DENSITY_PROBLEM_REDUCED",
            "TOTAL_DIVERGENCE_IS_NOT_AUTOMATIC_ZERO",
            "ADJOINT_CURRENT_OVERLAP_SELECTED",
            "FIRST_DENSITY_BOUND_ROWS_FILLED",
            "NEXT_TRACEFREE_CURRENT_OVERLAP_SELECTED",
        ]
    )
    add("VAL4140_7_decisions", "decisions record source-density reduction, no divergence shortcut, overlap target, density rows and next current-overlap target", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4140_STATUS"])
    status_ok = (
        bool(status)
        and status[0].get("result") == DECISION
        and status[0].get("source_density_contract_written") == "True"
        and status[0].get("divergence_projector_identity_derived") == "True"
        and status[0].get("projector_zero_signed") == "False"
        and status[0].get("first_density_rows_filled") == "True"
    )
    add("VAL4140_8_status", "status records source-density contract, derived divergence identity, unsigned zero and filled rows", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4140_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4141-Y5-R2FR-tracefree-current-overlap-zero-or-beta-density-bound.md"
    add("VAL4140_9_next_target", "next target is trace-free current-overlap zero or beta-density bound", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4140_10_no_claim_flags", "all generated rows remain no-claim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4140*")) or any(FORMALIZATION.rglob("4140-Y5-R2FR*"))
    add(
        "VAL4140_11_scope",
        "outputs stay in post-checkpoint-work and not formalization-workbench",
        in_scope and not formalization_output and not formalization_touched,
        f"doc={DOC_PATH}; csv_count={len(outputs)}",
    )

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4140_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4140_VALIDATION.csv"
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
