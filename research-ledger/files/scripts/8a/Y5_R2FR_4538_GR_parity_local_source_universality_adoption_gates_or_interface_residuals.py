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

CHECKPOINT = "4538"
CLAIM_ID = "L-380"
BRANCH_ID = "MTS_R2FR_Y5_GR_PARITY_HQNP_LOCAL_SOURCE_UNIVERSALITY_ROLLFORWARD_4538"
MARKER = "PPC4161_GR_PARITY_LOCAL_SOURCE_UNIVERSALITY_ADOPTION_GATES_OR_INTERFACE_RESIDUALS_4538"
PACKET_MARKER = "PPC4161_PACKET_GR_PARITY_LOCAL_SOURCE_UNIVERSALITY_ADOPTION_GATES_OR_INTERFACE_RESIDUALS_4538"
DECISION = "GR_PARITY_SOURCE_UNIVERSALITY_IMPORT_RECONCILES_4179_PRIVATE_LOCAL_GR_CHAIN_PUBLIC_CLAIM_STILL_BLOCKED_BY_PARENT_ADOPTION_SCOPE"
NEXT_TARGET = "4539-Y5-R2FR-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md"

FORMAL_PATH = FORMAL / "554-PPC4161-GR-parity-local-source-universality-adoption-gates-or-interface-residuals.md"
DOC_PATH = POST / "4538-Y5-R2FR-GR-parity-local-source-universality-adoption-gates-or-interface-residuals.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4538_SOURCE_REGISTER.csv"
BRANCH_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_GR_PARITY_HQNP_BRANCH_IMPORT.csv"
RESIDUAL_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_LOCAL_RESIDUAL_VECTOR_COLLAPSE.csv"
CLOSURE_CHAIN_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_LOCAL_GR_CLOSURE_CHAIN_UPDATE.csv"
ADOPTION_BURDEN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_PARENT_ADOPTION_BURDEN_AFTER_GR_PARITY.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4538_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4538_VALIDATION.csv"


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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4538_00_4537_rank",
            "label": "4537 GR-parity rank pass",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv",
            "needle": "RR4537_2_GR_parity_adopted_branch",
            "role": "source-weight non-common kernel zero inside imported ordinary visible branch",
        },
        {
            "source_id": "SRC4538_01_4537_adoption",
            "label": "4537 adoption scope",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4537_GR_PARITY_ADOPTION_CERTIFICATE.csv",
            "needle": "AD4537_3_interface_guard",
            "role": "private branch scope and interface guard",
        },
        {
            "source_id": "SRC4538_02_4445_import",
            "label": "4445 GR-parity matter import principle",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4445_DERIVATION_ROWS.csv",
            "needle": "SMIMP4445_0_GR_parity_import_principle",
            "role": "fair local-GR reduction uses imported standard visible matter action",
        },
        {
            "source_id": "SRC4538_03_4443_Req",
            "label": "4443 R_eq sharpening",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4443_DERIVATION_ROWS.csv",
            "needle": "NEDGE4443_2_Req_definition_sharpened_after_root",
            "role": "same-current mismatch definition before Hamiltonian bypass",
        },
        {
            "source_id": "SRC4538_04_4170_HQ",
            "label": "4170 Hamiltonian/worldtube charge glue",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4170_STATUS.csv",
            "needle": "PPC4161_TK_HQ_ADOPTS",
            "role": "same Hilbert/Hamiltonian/worldtube source charge inside private packet",
        },
        {
            "source_id": "SRC4538_05_4171_Newton",
            "label": "4171 Poisson/Gauss/Newton readout",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4171_STATUS.csv",
            "needle": "Poisson_equation_derived_private",
            "role": "first-order Newton readout from Hamiltonian source charge",
        },
        {
            "source_id": "SRC4538_06_4172_PPN",
            "label": "4172 full private PPN vector",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4172_STATUS.csv",
            "needle": "PPN_vector_closed_private",
            "role": "private PPN gamma/beta/preferred-frame/conservation vector closure",
        },
        {
            "source_id": "SRC4538_07_4173_empirical",
            "label": "4173 local empirical comparator pack",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4173_STATUS.csv",
            "needle": "all_numeric_rows_pass_private",
            "role": "source-backed local bound comparator rows pass privately, public claim false",
        },
        {
            "source_id": "SRC4538_08_4179_rollup",
            "label": "4179 local GR private closure chain",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4179_LOCAL_GR_CLOSURE_CHAIN.csv",
            "needle": "LC4179_4_PPN",
            "role": "existing private local-GR chain needing source-weight reconciliation",
        },
        {
            "source_id": "SRC4538_09_4174_selector",
            "label": "4174 parent selector and quarantine",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4174_PARENT_SELECTOR_CLAUSES.csv",
            "needle": "SEL4174_6_local_boundary_silence",
            "role": "global parent adoption burden and quarantine clauses",
        },
        {
            "source_id": "SRC4538_10_4180_matrix",
            "label": "4180 minimal parent adoption matrix",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4180_STATUS.csv",
            "needle": "MINIMAL_PARENT_ACTION_CANDIDATE",
            "role": "parent adoption not fully signed after private closure",
        },
        {
            "source_id": "SRC4538_11_packet_180",
            "label": "private packet integration",
            "path": PACKET_PATH,
            "needle": "PPC4161_PACKET_FULL_PPN_VECTOR_4172",
            "role": "current packet already contains local Newton/PPN private branch",
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


def branch_import_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "BI4538_0_define_branch",
            "branch_clause": "PPC4161-GP-HQNP := GR-parity imported standard visible matter branch + PPC4161-TK-HQNP private local packet",
            "source": "4537 plus 4170-4173",
            "status": "DEFINED_PRIVATE_BRANCH",
            "mathematical_effect": "ordinary visible source weights, Hamiltonian charge, Newton readout, PPN vector and local source-bound comparator are evaluated on one branch object",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "BI4538_1_source_weight",
            "branch_clause": "rank(M_graph)=n-1 and no source-only component prefactor",
            "source": "4537, 4445",
            "status": "PASS_PRIVATE_GR_PARITY_BRANCH",
            "mathematical_effect": "P_perp Delta_w = 0 for ordinary visible imported matter; only common calibration survives",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "BI4538_2_same_charge",
            "branch_clause": "Pi_M := Pi_M^H and Q_M=M_H^dress[W_H;tau]",
            "source": "4170",
            "status": "PASS_PRIVATE_PACKET",
            "mathematical_effect": "R_eq/topological-current shortcut is bypassed by one Hamiltonian/Hilbert/worldtube source charge",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "BI4538_3_Newton_PPN",
            "branch_clause": "EH weak-field and <=2PN readout use the same observed metric/coframe and same source",
            "source": "4171, 4172",
            "status": "PASS_PRIVATE_PACKET",
            "mathematical_effect": "nabla^2 Phi_N=4*pi G_cal rho_H, a_r=-G_cal M_H^dress/r^2, and R_PPN=(gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)=0 privately",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "BI4538_4_empirical_comparator",
            "branch_clause": "zero private predictions compared to source-backed local bounds",
            "source": "4173",
            "status": "PASS_PRIVATE_COMPARATOR_NONCLAIM",
            "mathematical_effect": "numeric local comparator rows pass, but raw reanalysis and full public claim are not performed",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "BI4538_5_parent_scope",
            "branch_clause": "global MTS parent action adoption of PPC4161-GP-HQNP",
            "source": "4174, 4180",
            "status": "BLOCKED_NOT_PARENT_SIGNED",
            "mathematical_effect": "the branch is disciplined and useful, but not the full unified parent action yet",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RV4538_0_source_weight",
            "symbolic_piece": "P_perp Delta_w",
            "pre_4538_role": "ordinary visible component source-weight/coupling ambiguity",
            "4538_status": "ZERO_PRIVATE_GR_PARITY_BRANCH",
            "closure_formula_or_bound": "rank(M_graph)=n-1 -> dim(ker M_graph cap im P_perp)=0 -> P_perp Delta_w=0",
            "reopens_if": "GR-parity branch rejected, nonstandard/hidden matter enters, or source-only prefactor/readout reentry is allowed",
            "next_if_reopened": "retain finite Delta_w projection/source-bound rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV4538_1_same_charge_worldtube",
            "symbolic_piece": "R_HQ := R_eq + B_zero_flux + worldtube/source-measure mismatch",
            "pre_4538_role": "Hilbert/Hamiltonian/topological/current/worldtube equality",
            "4538_status": "ZERO_PRIVATE_PACKET_BY_HQ_ROUTE",
            "closure_formula_or_bound": "Q_M=ell_M(Pi_M^H J_H_total)=H_tau[S_link]-H_ref=M_H^dress[W_H;tau]",
            "reopens_if": "Hamiltonian Pi_M selector, fixed reference, radial closure, or same-worldtube source support is rejected",
            "next_if_reopened": "source-backed R_eq or B_zero compact-test bound row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV4538_2_Newton_readout",
            "symbolic_piece": "R_N := nabla^2 Phi_N - 4*pi G_cal rho_H",
            "pre_4538_role": "first-order Newton/Poisson/Gauss bridge from source charge",
            "4538_status": "ZERO_PRIVATE_PACKET",
            "closure_formula_or_bound": "G_00^lin=kappa_eff T_00 -> nabla^2 Phi_N=4*pi G_cal rho_H; a_r=-G_cal M_H^dress/r^2",
            "reopens_if": "EH weak-field block or source-charge integral is rejected",
            "next_if_reopened": "orbital/source residual pack without importing observed GM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV4538_3_PPN_readout",
            "symbolic_piece": "R_PPN := (gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot/G)",
            "pre_4538_role": "full local GR/PPN vector",
            "4538_status": "ZERO_PRIVATE_PACKET",
            "closure_formula_or_bound": "R_PPN=0 inside PPC4161-TK-HQNP with same metric, source, boundary silence and side-channel silence",
            "reopens_if": "scalar/disformal/vector/projector/hidden flux/boundary clause fails",
            "next_if_reopened": "source-backed PPN residual bound rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV4538_4_empirical_local",
            "symbolic_piece": "R_emp := local bound/raw-data robustness gap",
            "pre_4538_role": "data-facing local validation",
            "4538_status": "PRIVATE_COMPARATOR_PASS_NOT_PUBLIC",
            "closure_formula_or_bound": "4173 numeric rows satisfy abs(private zero prediction)<=source-backed bound; R10 curve/raw reanalysis not complete",
            "reopens_if": "a bound source is updated, raw data reanalysis fails, or a nonzero reopened residual appears",
            "next_if_reopened": "real R10 curve, raw PPN/orbital/clock/WEP pack, no claim from anchor-only rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV4538_5_global_parent_adoption",
            "symbolic_piece": "R_global := full parent action adoption of PPC4161-GP-HQNP",
            "pre_4538_role": "turning private local selector into actual MTS parent theorem",
            "4538_status": "OPEN_MAIN_BLOCKER",
            "closure_formula_or_bound": "need parent action selector for EH block, GR-parity source functor, Hamiltonian charge, boundary silence, quotient naturality and nonlocal sector separation",
            "reopens_if": "always active until parent action signs the selector clauses",
            "next_if_reopened": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RV4538_6_off_branch_hidden",
            "symbolic_piece": "R_off := hidden/nonstandard matter/source-label/readout reentry residuals",
            "pre_4538_role": "everything not covered by imported ordinary visible GR-parity branch",
            "4538_status": "RETAIN_BOUND_ROUTE",
            "closure_formula_or_bound": "no zero theorem is asserted outside PPC4161-GP-HQNP",
            "reopens_if": "a test uses hidden sectors, nonstandard matter, or late source labels",
            "next_if_reopened": "finite C_src/Delta_w/source projection rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def closure_chain_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "CCU4538_0_replace_fog",
            "old_frontier": "source coupling fog / component weight ambiguity",
            "new_frontier": "parent adoption of the GR-parity HQNP local selector",
            "theorem": "On PPC4161-GP-HQNP, Delta_local = R_emp + R_global + R_off because P_perp Delta_w, R_HQ, R_N and R_PPN are zero/private-pass branch components.",
            "status": "ROLLFORWARD",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "update_id": "CCU4538_1_4179_patch",
            "old_frontier": "4179 private local GR closure chain had source-measure/source-weight burden",
            "new_frontier": "4537 adds rank-backed source-weight universality for imported ordinary visible matter",
            "theorem": "The 4179 link `single Hilbert source measure` is upgraded inside the GR-parity branch by the 4537 rank pass: only common calibration remains.",
            "status": "PRIVATE_CHAIN_STRENGTHENED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "update_id": "CCU4538_2_do_not_overclaim",
            "old_frontier": "private local selector could be mistaken for full unified theory",
            "new_frontier": "explicit public firewall",
            "theorem": "Private branch pass does not derive the Standard Model, numerical G, full parent action, or galaxy/cosmology memory transition.",
            "status": "FIREWALL_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def adoption_burden_rows() -> list[dict[str, Any]]:
    return [
        {
            "burden_id": "AB4538_0_parent_action_selector",
            "burden": "derive S_parent -> PPC4161-GP-HQNP in compact local collars",
            "status": "OPEN",
            "needed_signature": "parent-owned local selector, not just checkpoint adoption",
            "best_next_attack": "write exact parent-action contract with branch projector, support separation and no-reentry clauses",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "burden_id": "AB4538_1_global_sector_separation",
            "burden": "show galaxy/cosmology/open-memory sectors do not leak into <=2PN compact local readout",
            "status": "OPEN",
            "needed_signature": "support/no-flux/projector theorem linking global sectors to local collar silence",
            "best_next_attack": "formalize sector projectors P_loc, P_gal, P_cos and boundary flux zero conditions",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "burden_id": "AB4538_2_empirical_upgrade",
            "burden": "upgrade private local comparator to stronger raw-data validation",
            "status": "OPEN_BUT_NOT_THEORY_BLOCKER",
            "needed_signature": "digitized R10 curve/raw orbital/clock/WEP rows with source provenance",
            "best_next_attack": "run empirical pack after parent-action contract is stable",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "burden_id": "AB4538_3_off_branch_materials",
            "burden": "hidden/nonstandard matter and late readout labels",
            "status": "RETAIN_BOUND_ROUTE",
            "needed_signature": "finite projection/source-bound rows or a stronger no-extension theorem",
            "best_next_attack": "do not let off-branch uncertainty contaminate the ordinary visible GR-parity branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4538_0_GRparity_source_universality",
            "gate": "GR-parity ordinary visible source universality",
            "status": "PASS_PRIVATE_BRANCH",
            "meaning": "4537 rank pass kills non-common source weights inside imported standard visible matter",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4538_1_HQNP_local_GR",
            "gate": "Hamiltonian/Newton/PPN private local GR chain",
            "status": "PASS_PRIVATE_BRANCH",
            "meaning": "4170-4173 chain remains coherent after source-weight roll-forward",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4538_2_parent_adoption",
            "gate": "full parent action adopts branch",
            "status": "BLOCKED_UNSIGNED",
            "meaning": "the exact parent selector is the real remaining theory gate",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4538_3_public_local_GR",
            "gate": "public local GR/Newton/PPN claim",
            "status": "BLOCKED_NONCLAIM",
            "meaning": "private branch and comparator pass are not a public claim until parent adoption and validation standard are settled",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4538_4_unified_field_theory",
            "gate": "full unified field theory",
            "status": "BLOCKED",
            "meaning": "local GR compatibility looks much healthier, but cosmology/galaxy/EM/time sectors still need one parent action spine",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4538_0",
            "decision": DECISION,
            "meaning": "4538 reconciles the late source-coupling work with the earlier private local-GR closure chain. Inside the private GR-parity/HQNP branch, source-weight ambiguity is no longer the live local blocker; the live blocker is parent-action adoption and off-branch/global sector control.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4538_0",
            "target": NEXT_TARGET,
            "objective": "try to derive the parent action selector that adopts PPC4161-GP-HQNP locally without smuggling a closure axiom",
            "derive_first": "write the exact action-level contract and check which clauses are already parent-owned versus merely branch-adopted",
            "fallback": "if adoption cannot be derived, freeze PPC4161-GP-HQNP as an explicitly effective/local GR branch and move testing to the global sector interfaces",
            "avoid": "re-opening source coupling generally after 4537 unless a test leaves the ordinary visible GR-parity branch",
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
            "GR_parity_source_weight_zero_private": "True",
            "HQNP_local_GR_chain_private_pass": "True",
            "local_comparator_private_pass": "True",
            "global_parent_action_adoption_proved": "False",
            "public_local_GR_claim_allowed": "False",
            "numeric_G_predicted": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    chain_update: list[dict[str, Any]],
    burdens: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4538_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    imports_ok = all(
        any(row["gate_id"] == gate_id for row in branch_rows)
        for gate_id in ["BI4538_1_source_weight", "BI4538_2_same_charge", "BI4538_3_Newton_PPN", "BI4538_4_empirical_comparator"]
    )
    checks.append({"validation_id": "VAL4538_01_branch_imports", "status": "PASS" if imports_ok else "FAIL", "detail": "GR-parity source, HQ charge, Newton/PPN and comparator imports recorded"})

    closed_count = sum(1 for row in residuals if row["4538_status"].startswith("ZERO_PRIVATE") or row["4538_status"].startswith("PRIVATE_COMPARATOR"))
    open_ok = any(row["residual_id"] == "RV4538_5_global_parent_adoption" and row["4538_status"] == "OPEN_MAIN_BLOCKER" for row in residuals)
    residual_ok = closed_count >= 5 and open_ok
    checks.append({"validation_id": "VAL4538_02_residual_vector", "status": "PASS" if residual_ok else "FAIL", "detail": "residual vector collapses to parent/global/off-branch burden without public claim"})

    chain_ok = any(row["update_id"] == "CCU4538_0_replace_fog" and "Delta_local" in row["theorem"] for row in chain_update)
    checks.append({"validation_id": "VAL4538_03_chain_update", "status": "PASS" if chain_ok else "FAIL", "detail": "closure chain update states the new theorem frontier"})

    burden_ok = any(row["burden_id"] == "AB4538_0_parent_action_selector" and row["status"] == "OPEN" for row in burdens)
    checks.append({"validation_id": "VAL4538_04_parent_burden", "status": "PASS" if burden_ok else "FAIL", "detail": "parent action selector remains the main open burden"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    public_blocked = any(row["claim_gate_id"] == "CG4538_3_public_local_GR" and row["status"] == "BLOCKED_NONCLAIM" for row in gates)
    checks.append({"validation_id": "VAL4538_05_claim_firewall", "status": "PASS" if gates_ok and public_blocked else "FAIL", "detail": "all claim gates remain nonclaim and public local-GR gate is blocked"})

    csv_paths = [
        SOURCE_REGISTER,
        BRANCH_IMPORT_CSV,
        RESIDUAL_VECTOR_CSV,
        CLOSURE_CHAIN_UPDATE_CSV,
        ADOPTION_BURDEN_CSV,
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
    checks.append({"validation_id": "VAL4538_06_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4538_07_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4538_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4538 GR-parity/HQNP local source universality roll-forward"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    chain_update: list[dict[str, Any]],
    burdens: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4538 - GR-parity local source universality adoption gates or interface residuals

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

- 4537 is now wired into the existing local-GR chain instead of living as a separate source-coupling audit.
- Define the private branch `PPC4161-GP-HQNP := GR-parity imported standard visible matter + PPC4161-TK-HQNP`.
- Inside that branch, the remaining ordinary-visible source-weight ambiguity is removed: `P_perp Delta_w=0`.
- Combining 4537 with 4170-4173 gives a sharper residual identity:

```text
Delta_local = P_perp Delta_w + R_HQ + R_N + R_PPN + R_emp + R_global + R_off.
```

On `PPC4161-GP-HQNP`:

```text
P_perp Delta_w = 0,
R_HQ = 0,
R_N = 0,
R_PPN = 0,
```

so the honest live frontier is:

```text
Delta_local | PPC4161-GP-HQNP = R_emp + R_global + R_off.
```

`R_emp` has a private source-backed comparator pass from 4173, but not raw-data/public-claim status. `R_global` is the big one: the full MTS parent action still has to adopt the branch rather than merely quarantining it. `R_off` covers hidden/nonstandard matter and readout reentry outside the GR-parity ordinary-visible branch.

## Branch Import Gates

{markdown_table(branch_rows)}

## Residual Vector Collapse

{markdown_table(residuals)}

## Closure Chain Update

{markdown_table(chain_update)}

## Parent Adoption Burden

{markdown_table(burdens)}

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
        "domain": "local_gr_source_coupling",
        "claim": "4538 reconciles the 4537 GR-parity source-weight rank pass with the PPC4161-TK-HQNP private local-GR chain: inside the private branch P_perp Delta_w, same-charge/worldtube, Newton readout and PPN residuals are zero/pass, leaving parent adoption, empirical upgrade and off-branch residuals.",
        "current_evidence": "Generated source register, branch import gates, residual vector collapse, closure-chain update, parent adoption burden, claim gates, status and validation CSVs.",
        "status": "private_branch_rollforward_nonclaim_parent_adoption_open",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking a private GR-parity/HQNP branch pass for a full MTS parent-action theorem or public local-GR claim.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Hidden/nonstandard sectors, readout reentry, global sector leakage, or parent selector failure reopens explicit residual rows.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    branch_rows = branch_import_rows()
    residuals = residual_vector_rows()
    chain_update = closure_chain_update_rows()
    burdens = adoption_burden_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BRANCH_IMPORT_CSV, branch_rows)
    write_csv(RESIDUAL_VECTOR_CSV, residuals)
    write_csv(CLOSURE_CHAIN_UPDATE_CSV, chain_update)
    write_csv(ADOPTION_BURDEN_CSV, burdens)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, branch_rows, residuals, chain_update, burdens, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, branch_rows, residuals, chain_update, burdens, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4538 GR-Parity Local Source Universality Roll-Forward

Marker: `{MARKER}`  
4538 reconciles the 4537 source-weight rank result with the earlier PPC4161-TK-HQNP private local-GR chain. On the private `PPC4161-GP-HQNP` branch, `P_perp Delta_w=0`, the Hamiltonian/worldtube charge glue is active, Newton and PPN readouts stay closed privately, and 4173 local comparator rows remain private passes. The live frontier is no longer generic source-coupling fog; it is parent-action adoption plus empirical/raw-data upgrade and off-branch hidden/readout residuals. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4538 Packet Integration - GR-Parity/HQNP Source Universality

Marker: `{PACKET_MARKER}`  
The packet now carries a reconciled private branch `PPC4161-GP-HQNP`: GR-parity imported ordinary visible matter supplies `P_perp Delta_w=0`, while the HQNP local packet supplies same-charge, Newton and PPN private closures. Public local-GR and unified-theory claims remain blocked until parent adoption and off-branch/global interfaces are signed.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
