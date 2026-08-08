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

CHECKPOINT = "4545"
CLAIM_ID = "L-387"
BRANCH_ID = "MTS_R2FR_Y5_ATTRACTOR_STATIONARITY_BOUNDARY_HAMILTONIAN_4545"
MARKER = "PPC4161_ATTRACTOR_STATIONARITY_AND_BOUNDARY_SILENCE_FROM_BIANCHI_HAMILTONIAN_LOCAL_CONSERVATION_4545"
PACKET_MARKER = "PPC4161_PACKET_ATTRACTOR_STATIONARITY_AND_BOUNDARY_SILENCE_FROM_BIANCHI_HAMILTONIAN_LOCAL_CONSERVATION_4545"
DECISION = "HAMILTONIAN_STATIONARY_BRANCH_GIVES_DERIVATIVE_SILENCE_FULL_BOUNDARY_NOHAIR_REMAINS_OPEN"
NEXT_TARGET = "4546-Y5-R2FR-source-silence-and-attractor-homogeneity-from-compact-support-or-U_B-power-bound.md"

FORMAL_PATH = FORMAL / "561-PPC4161-attractor-stationarity-and-boundary-silence-from-Bianchi-Hamiltonian-local-conservation.md"
DOC_PATH = POST / "4545-Y5-R2FR-attractor-stationarity-and-boundary-silence-from-Bianchi-Hamiltonian-local-conservation.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4545_SOURCE_REGISTER.csv"
WARD_HAMILTONIAN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_WARD_HAMILTONIAN_DERIVATION.csv"
STATIONARITY_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_ATTRACTOR_STATIONARITY_MAP.csv"
BOUNDARY_SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_BOUNDARY_SILENCE_SPLIT.csv"
GDOT_BUDGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_GDOT_REDUCED_BUDGET.csv"
RETAINED_RESIDUALS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_RETAINED_RESIDUALS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4545_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4545_VALIDATION.csv"


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
            "source_id": "SRC4545_00_4544_status",
            "label": "4544 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4544_STATUS.csv",
            "needle": "DTXI_ZERO_THEOREM_DERIVED_CONDITIONAL_TT_GDOT_SILENCE_SPLIT_BOUND_FORM_ACTIVE_NONCLAIM",
            "role": "imports the D_t Xi zero theorem and tensor split",
        },
        {
            "source_id": "SRC4545_01_4544_finite_budget",
            "label": "4544 finite budget",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4544_DTXI_TPERP_FINITE_BOUND.csv",
            "needle": "FB4544_2_product_budget",
            "role": "sets the Gdot source-budget expression",
        },
        {
            "source_id": "SRC4545_02_4544_clause_map",
            "label": "4544 Jres clause map",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4544_JRES_ZERO_CLAUSE_MAP.csv",
            "needle": "PZ4544_3_attractor_stationarity",
            "role": "selects attractor stationarity as a target clause",
        },
        {
            "source_id": "SRC4545_03_429_doc",
            "label": "429 Ward/Bianchi owner",
            "path": POST / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
            "needle": "It does not by itself prove that each owned force vanishes",
            "role": "anti-shortcut: ownership is not absence",
        },
        {
            "source_id": "SRC4545_04_variation_chain",
            "label": "domain parent action variation chain",
            "path": SOURCE_DIR / "P8_DOMAIN_SELECTOR_PARENT_ACTION_VARIATION_CHAIN.csv",
            "needle": "V3_Ward_force",
            "role": "on-shell Ward force vanishes only with local zero and no boundary flux",
        },
        {
            "source_id": "SRC4545_05_boundary_owner",
            "label": "boundary scalar owner attempt",
            "path": SOURCE_DIR / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv",
            "needle": "O6_constant_monopole",
            "role": "constant boundary monopole is safe for derivative/Gdot only if owned",
        },
        {
            "source_id": "SRC4545_06_boundary_premises",
            "label": "boundary premise ownership",
            "path": SOURCE_DIR / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P4_Ward_flux_closure",
            "role": "Ward flux closure remains conditional identity, not zero",
        },
        {
            "source_id": "SRC4545_07_repair_ledger",
            "label": "boundary repair ledger",
            "path": SOURCE_DIR / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv",
            "needle": "R5_constant_monopole_derivative_silence",
            "role": "points to derivative silence of constant monopole",
        },
        {
            "source_id": "SRC4545_08_domain_no_vector",
            "label": "domain no-vector theorem attempt",
            "path": SOURCE_DIR / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T5_Ward_counterexample_blocker",
            "role": "blocks using Ward covariance alone as a no-vector/no-flux proof",
        },
        {
            "source_id": "SRC4545_09_boundary_nohair_doc",
            "label": "353 boundary no-hair contract",
            "path": POST / "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
            "needle": "pure conserved boundary monopole trace",
            "role": "supports the constant-monopole calibration route",
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


def ward_hamiltonian_rows() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "WH4545_0_Ward_ledger",
            "statement": "Diffeomorphism invariance gives an owned force ledger: F_hidden^nu + F_projector^nu + F_boundary^nu + F_domain^nu + F_nonmetric^nu balances the local divergence.",
            "derivation": "429 supplies the Ward/Bianchi owner identity; it assigns every force to a retained sector.",
            "what_it_proves": "conservation bookkeeping and no hidden unowned force",
            "what_it_does_not_prove": "individual force absence",
            "status": "owned_identity_not_zero",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "step_id": "WH4545_1_Hamiltonian_balance",
            "statement": "For local time flow tau, dH_loc/dtau = -Phi_boundary + integral(E_A L_tau Phi^A) over the collar.",
            "derivation": "Hamiltonian variation of the local collar: on shell, time dependence is carried by boundary symplectic flux and explicit time-dependent sources.",
            "what_it_proves": "if E_A=0, L_tau external sources=0 and Phi_boundary=0, H_loc is constant",
            "what_it_does_not_prove": "that boundary charge amplitude is zero",
            "status": "conditional_conservation_theorem",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "step_id": "WH4545_2_attractor_chain_rule",
            "statement": "If m_L = m_*(I_A,Q_B) with no explicit tau dependence, L_tau I_A=0 and L_tau Q_B=0 imply P_loc[D_t m_L]=0.",
            "derivation": "D_t m_L = (partial m_*/partial I_A) D_t I_A + (partial m_*/partial Q_B) D_t Q_B.",
            "what_it_proves": "PZ4544_3 can close inside a stationary compact branch",
            "what_it_does_not_prove": "global stationarity, source silence, or spatial homogeneity",
            "status": "conditional_branch_stationarity",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "step_id": "WH4545_3_boundary_derivative_silence",
            "statement": "If the boundary carries only a homogeneous scalar conserved monopole Q_B and no incoming flux, then D_t b_Xi=0 and the Gdot derivative boundary piece is zero.",
            "derivation": "The boundary data depend only on Q_B; Hamiltonian no-flux gives D_t Q_B=0, so D_t b_Xi = (db_Xi/dQ_B)D_t Q_B = 0.",
            "what_it_proves": "Gdot derivative-budget boundary term can vanish",
            "what_it_does_not_prove": "boundary vector/shear/trace amplitude absence for alpha3, xi, R11 or full local GR",
            "status": "conditional_derivative_silence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "step_id": "WH4545_4_counterexample_guard",
            "statement": "A covariant domain or boundary vector can satisfy Ward/Bianchi conservation while still producing preferred-frame or flux residuals.",
            "derivation": "Imported from 429 and the domain no-vector theorem attempt.",
            "what_it_proves": "Ward/Bianchi conservation cannot be used as a no-vector/no-flux theorem",
            "what_it_does_not_prove": "nothing is promoted; this is a firewall",
            "status": "active_no_smuggling_guard",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def stationarity_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PZ4545_3_attractor_stationarity",
            "target_from_4544": "P_loc[D_t m_L]=0",
            "4545_result": "conditional_branch_pass",
            "proof_route": "m_L=m_*(I_A,Q_B), local time-flow stationarity L_tau I_A=0, Hamiltonian no-flux L_tau Q_B=0",
            "remaining_gap": "stationary compact branch and scalar conserved boundary charge are not universal parent theorems",
            "effect_on_Gdot": "removes the attractor-drift part of P_loc D_t J_res in the Gdot derivative budget",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PZ4545_4_boundary_derivative_silence",
            "target_from_4544": "D_t b_Xi=0 and derivative boundary contribution to Gdot vanishes",
            "4545_result": "conditional_branch_pass_for_derivative_channel",
            "proof_route": "Hamiltonian no-flux plus homogeneous scalar conserved monopole",
            "remaining_gap": "full P_loc[boundary_in]=0 is not proved; trace/shear/vector/boundary amplitude channels remain",
            "effect_on_Gdot": "removes D_t b_Xi and T_boundary_dot if the branch premises are accepted",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "clause_id": "PZ4545_4_full_boundary_silence",
            "target_from_4544": "P_loc[boundary_in]=0",
            "4545_result": "not_closed",
            "proof_route": "would require O0-O6 parent ownership or numeric coefficient rows",
            "remaining_gap": "no-marker, flux-zero, scalar-only and full metric-variation owner gaps remain",
            "effect_on_Gdot": "constant monopole can be derivative-silent, but full PPN/local-GR boundary silence remains open",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def boundary_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "BS4545_0_constant_monopole",
            "boundary_piece": "homogeneous scalar conserved monopole",
            "Hamiltonian_result": "D_t Q_B=0 under no-flux stationary collar",
            "Gdot_status": "derivative_silent_if_owned",
            "PPN_status": "constant measured-GM calibration only if source/species/range independent",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "split_id": "BS4545_1_trace_scalar_amplitude",
            "boundary_piece": "trace/scalar amplitude",
            "Hamiltonian_result": "can be conserved without being zero",
            "Gdot_status": "no Gdot drift if constant",
            "PPN_status": "retained for beta/xi/R11 unless calibrated or bounded",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "split_id": "BS4545_2_vector_marker_flux",
            "boundary_piece": "tangent vector, spin marker, active-domain velocity or normal flux",
            "Hamiltonian_result": "Ward-owned but not absent",
            "Gdot_status": "can contribute if time-varying or fluxing",
            "PPN_status": "retained alpha3/preferred-frame channel",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "split_id": "BS4545_3_shear_TT_boundary",
            "boundary_piece": "shear/tracefree boundary stress",
            "Hamiltonian_result": "not killed by scalar charge conservation unless scalar-only homogeneous action is parent-owned",
            "Gdot_status": "pure TT monopole remains scalar-Gdot silent from 4544",
            "PPN_status": "retained xi/lensing-slip style channel if non-monopole or metric-coupled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def gdot_budget_rows() -> list[dict[str, Any]]:
    return [
        {
            "budget_id": "GB4545_0_full_4544",
            "budget_form": "|c_Gamma| K_t (||P_loc D_t J_res||/mu_Xi + ||D_t b_Xi||/beta_Xi + ||D_t h_ker||) + T_trace + T_boundary <= 2.42e-14 yr^-1",
            "condition": "no stationarity simplification",
            "4545_effect": "starting point",
            "status": "imported",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "budget_id": "GB4545_1_stationary_derivative_reduction",
            "budget_form": "If L_tau I_A=0, L_tau Q_B=0, D_t h_ker=0 and scalar homogeneous no-flux boundary holds, the derivative part of the Gdot budget reduces to 0.",
            "condition": "stationary compact local branch plus Hamiltonian no-flux and no incoming homogeneous mode",
            "4545_effect": "conditional Gdot derivative silence",
            "status": "conditional_branch_reduction",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "budget_id": "GB4545_2_retained_amplitude_warning",
            "budget_form": "P_loc J_res can still be nonzero as a static amplitude through U_B S_cg, D_m Delta_h m_L or boundary trace/shear terms.",
            "condition": "static amplitudes need source support/homogeneity/no-hair, not just time conservation",
            "4545_effect": "blocks full local-GR promotion",
            "status": "retained_residual",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def retained_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RR4545_0_source_silence",
            "object": "P_loc[U_B S_cg]",
            "status_after_4545": "open_static_amplitude",
            "why_retained": "Hamiltonian stationarity can make its time derivative zero without proving local source amplitude vanishes",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RR4545_1_attractor_homogeneity",
            "object": "P_loc[D_m Delta_h m_L]",
            "status_after_4545": "open_spatial_amplitude",
            "why_retained": "D_t m_L=0 does not imply D_m m_L=0",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RR4545_2_boundary_nohair",
            "object": "P_loc[boundary_in]",
            "status_after_4545": "partial_derivative_silence_only",
            "why_retained": "constant monopole may be safe for Gdot drift, but vector/shear/trace amplitude rows are not theorem-zero",
            "next_action": "keep alpha3/xi/R11 boundary rows retained or source numeric coefficients",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RR4545_3_kernel_mode",
            "object": "D_t h_ker",
            "status_after_4545": "zero_if_no_incoming_homogeneous_mode",
            "why_retained": "Hamiltonian no-flux must also exclude incoming memory/kernel modes",
            "next_action": "tie to boundary/topological no-influx theorem or numeric mode amplitude",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4545_0_attractor_stationarity",
            "gate": "P_loc[D_t m_L]=0",
            "status": "PASS_CONDITIONAL_STATIONARY_BRANCH",
            "meaning": "derived by chain rule from stationary local invariants and Hamiltonian no-flux conserved boundary charge",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4545_1_boundary_derivative_silence",
            "gate": "D_t b_Xi=0 for Gdot derivative budget",
            "status": "PASS_CONDITIONAL_CONSTANT_MONOPOLE",
            "meaning": "constant scalar monopole gives derivative silence, not full no-hair",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4545_2_full_boundary_silence",
            "gate": "P_loc[boundary_in]=0",
            "status": "BLOCKED_NO_MARKER_FLUX_TRACE_OWNER_GAPS",
            "meaning": "Ward/Bianchi ownership and Hamiltonian conservation do not prove boundary force absence",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4545_3_full_local_GR",
            "gate": "full local GR/Newton/PPN",
            "status": "BLOCKED_SOURCE_HOMOGENEITY_AND_BOUNDARY_AMPLITUDES",
            "meaning": "Gdot derivative silence improves the branch, but source silence, spatial homogeneity and retained boundary/operator rows remain",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4545_0",
            "decision": DECISION,
            "meaning": "4545 gets a real conditional win: in a stationary compact branch, Hamiltonian no-flux and scalar conserved boundary charge give P_loc[D_t m_L]=0 and derivative boundary silence for Gdot. But Ward/Bianchi/Hamiltonian conservation does not prove full boundary no-hair; static amplitudes and vector/shear/operator rows remain retained.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4545_0",
            "target": NEXT_TARGET,
            "objective": "try to close the remaining static source-silence and attractor-homogeneity clauses, or convert them into U_B power bounds",
            "derive_first": "prove P_loc[U_B S_cg]=0 and P_loc[D_m Delta_h m_L]=0 from compact support/topological projector/local trivial class",
            "fallback": "derive explicit U_B^n source and spatial-gradient bounds for PPN/local residual rows",
            "avoid": "using time-stationarity as if it were spatial/source silence",
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
            "attractor_stationarity_conditional": "True",
            "boundary_derivative_silence_conditional": "True",
            "full_boundary_silence": "False",
            "Gdot_derivative_budget_reduced": "True",
            "source_static_amplitude_closed": "False",
            "attractor_spatial_homogeneity_closed": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    stationarity: list[dict[str, Any]],
    boundary_split: list[dict[str, Any]],
    gdot_budget: list[dict[str, Any]],
    retained: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4545_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    ward_guard = any(row["step_id"] == "WH4545_0_Ward_ledger" and row["what_it_does_not_prove"] == "individual force absence" for row in ward_rows)
    checks.append({"validation_id": "VAL4545_01_ward_guard", "status": "PASS" if ward_guard else "FAIL", "detail": "Ward/Bianchi ownership is not treated as absence"})

    hamiltonian = any(row["step_id"] == "WH4545_1_Hamiltonian_balance" and "dH_loc" in row["statement"] for row in ward_rows)
    checks.append({"validation_id": "VAL4545_02_hamiltonian_balance", "status": "PASS" if hamiltonian else "FAIL", "detail": "Hamiltonian balance theorem written"})

    stationarity_ok = any(row["clause_id"] == "PZ4545_3_attractor_stationarity" and row["4545_result"] == "conditional_branch_pass" for row in stationarity)
    boundary_partial = any(row["clause_id"] == "PZ4545_4_boundary_derivative_silence" and row["4545_result"] == "conditional_branch_pass_for_derivative_channel" for row in stationarity)
    full_boundary_block = any(row["clause_id"] == "PZ4545_4_full_boundary_silence" and row["4545_result"] == "not_closed" for row in stationarity)
    checks.append({"validation_id": "VAL4545_03_stationarity_split", "status": "PASS" if stationarity_ok and boundary_partial and full_boundary_block else "FAIL", "detail": "attractor stationarity is split from full boundary no-hair"})

    constant_monopole = any(row["split_id"] == "BS4545_0_constant_monopole" and row["Gdot_status"] == "derivative_silent_if_owned" for row in boundary_split)
    vector_retained = any(row["split_id"] == "BS4545_2_vector_marker_flux" and "retained" in row["PPN_status"] for row in boundary_split)
    checks.append({"validation_id": "VAL4545_04_boundary_split", "status": "PASS" if constant_monopole and vector_retained else "FAIL", "detail": "constant-monopole Gdot safety is separated from retained vector/shear channels"})

    budget_reduction = any(row["budget_id"] == "GB4545_1_stationary_derivative_reduction" and row["status"] == "conditional_branch_reduction" for row in gdot_budget)
    amplitude_warning = any(row["budget_id"] == "GB4545_2_retained_amplitude_warning" for row in gdot_budget)
    checks.append({"validation_id": "VAL4545_05_gdot_budget", "status": "PASS" if budget_reduction and amplitude_warning else "FAIL", "detail": "Gdot derivative budget is reduced without deleting static amplitudes"})

    retained_ok = any(row["residual_id"] == "RR4545_0_source_silence" and row["status_after_4545"] == "open_static_amplitude" for row in retained) and any(row["residual_id"] == "RR4545_1_attractor_homogeneity" and row["status_after_4545"] == "open_spatial_amplitude" for row in retained)
    checks.append({"validation_id": "VAL4545_06_retained_residuals", "status": "PASS" if retained_ok else "FAIL", "detail": "source and spatial homogeneity residuals remain active next targets"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    local_block = any(row["claim_gate_id"] == "CG4545_3_full_local_GR" and row["status"].startswith("BLOCKED") for row in gates)
    checks.append({"validation_id": "VAL4545_07_claim_firewall", "status": "PASS" if gates_ok and local_block else "FAIL", "detail": "no local GR/Newton/PPN promotion from conditional derivative silence"})

    csv_paths = [
        SOURCE_REGISTER,
        WARD_HAMILTONIAN_CSV,
        STATIONARITY_MAP_CSV,
        BOUNDARY_SPLIT_CSV,
        GDOT_BUDGET_CSV,
        RETAINED_RESIDUALS_CSV,
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
    checks.append({"validation_id": "VAL4545_08_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4545_09_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4545_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4545 attractor stationarity and boundary derivative-silence split"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    stationarity: list[dict[str, Any]],
    boundary_split: list[dict[str, Any]],
    gdot_budget: list[dict[str, Any]],
    retained: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4545 - Attractor stationarity and boundary silence from Bianchi/Hamiltonian local conservation

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4544 left the live route:

```text
P_loc[D_t m_L] = 0,
D_t b_Xi = 0,
T_perp,Gdot = 0 or bounded.
```

4545 proves the useful part and refuses the fake part.

Ward/Bianchi ownership gives the force ledger, but not force absence. Hamiltonian local conservation gives the sharper statement:

```text
dH_loc/dtau = -Phi_boundary + integral(E_A L_tau Phi^A).
```

On shell, with stationary local source/readout invariants and no symplectic boundary flux:

```text
D_t H_loc = 0,
D_t Q_B = 0.
```

If the local attractor is a smooth branch function

```text
m_L = m_*(I_A, Q_B)
```

with no explicit local-time dependence, then:

```text
D_t m_L = (partial m_*/partial I_A) D_t I_A
        + (partial m_*/partial Q_B) D_t Q_B = 0.
```

So `P_loc[D_t m_L]=0` is conditionally derived inside the stationary compact branch. A conserved homogeneous scalar boundary monopole also gives derivative silence for the Gdot budget:

```text
D_t b_Xi = 0.
```

But this does **not** prove full `P_loc[boundary_in]=0`. Static boundary amplitude, vector/marker flux, trace/shear stress, source support and spatial attractor gradients remain retained. Translation: we got a real Gdot derivative-silence win, not a full local-GR knockout.

## Ward/Hamiltonian Derivation

{markdown_table(ward_rows)}

## Attractor Stationarity Map

{markdown_table(stationarity)}

## Boundary Silence Split

{markdown_table(boundary_split)}

## Gdot Reduced Budget

{markdown_table(gdot_budget)}

## Retained Residuals

{markdown_table(retained)}

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
        "claim": "4545 derives conditional attractor stationarity and boundary derivative silence for the Gdot budget from Hamiltonian no-flux local conservation, while retaining full boundary no-hair, source silence, spatial homogeneity and operator rows as open.",
        "current_evidence": "Generated source register, Ward/Hamiltonian derivation, stationarity map, boundary split, Gdot reduced budget, retained residuals, claim gates, status and validation CSVs.",
        "status": "conditional_Gdot_derivative_silence_no_full_boundary_nohair",
        "next_test": NEXT_TARGET,
        "key_risk": "Using conservation of a boundary monopole as if it proved boundary force absence.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Local GR remains unclaimed until static source support, spatial homogeneity and retained boundary/operator amplitudes close or are bounded.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    ward_rows = ward_hamiltonian_rows()
    stationarity = stationarity_map_rows()
    boundary_split = boundary_split_rows()
    gdot_budget = gdot_budget_rows()
    retained = retained_residual_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(WARD_HAMILTONIAN_CSV, ward_rows)
    write_csv(STATIONARITY_MAP_CSV, stationarity)
    write_csv(BOUNDARY_SPLIT_CSV, boundary_split)
    write_csv(GDOT_BUDGET_CSV, gdot_budget)
    write_csv(RETAINED_RESIDUALS_CSV, retained)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, ward_rows, stationarity, boundary_split, gdot_budget, retained, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, ward_rows, stationarity, boundary_split, gdot_budget, retained, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4545 Attractor Stationarity And Boundary Derivative Silence

Marker: `{MARKER}`  
4545 derives a conditional Hamiltonian result: in a stationary compact local branch with no symplectic boundary flux, `D_t Q_B=0`; if `m_L=m_*(I_A,Q_B)`, then `P_loc[D_t m_L]=0`. A conserved homogeneous scalar boundary monopole gives `D_t b_Xi=0` for the Gdot derivative budget. This is not full boundary no-hair: static source amplitudes, spatial gradients, vector/shear boundary pieces and R11/operator rows remain retained. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4545 Packet Integration - Hamiltonian Stationarity Without Fake Boundary No-Hair

Marker: `{PACKET_MARKER}`  
The local packet now distinguishes derivative silence from amplitude silence. Gdot drift can be conditionally quiet in the stationary compact branch, but full local GR still needs source silence, attractor homogeneity and retained boundary/operator amplitudes to be zero or bounded.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
