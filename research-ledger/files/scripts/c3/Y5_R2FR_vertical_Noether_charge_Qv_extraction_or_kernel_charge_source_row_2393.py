from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_VERTICAL_NOETHER_CHARGE_QV_EXTRACTION_OR_KERNEL_CHARGE_SOURCE_ROW_2393"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2393_00_2392_doc",
            "source_key": "2392_charge_handoff",
            "source_path": POST_ROOT / "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
            "needles": ["2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md", "Theta_parent", "Q_v"],
            "source_role": "2392 selects vertical Noether charge extraction",
        },
        {
            "row_id": "SRC2393_01_2392_certificates",
            "source_key": "2392_vertical_kernel_certificates",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv",
            "needles": ["VKC2392_2_theta_Qv", "MISSING_THETA_PARENT_AND_QV", "VKC2392_3_zero_compact_flux"],
            "source_role": "Theta/Qv and compact-flux gaps",
        },
        {
            "row_id": "SRC2393_02_2392_leaks",
            "source_key": "2392_kernel_charge_leaks",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2392_KERNEL_CHARGE_LEAK_VALUES.csv",
            "needles": ["epsilon_kernel_charge", "MISSING_THETA_PARENT", "MISSING_Q_V"],
            "source_role": "kernel-charge leak schema to refine",
        },
        {
            "row_id": "SRC2393_03_1008_doc",
            "source_key": "1008_theta_Qtau_extraction",
            "source_path": POST_ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needles": ["parent `theta_MTS` and `Q_tau^MTS` extraction attempted; not closed", "delta L_parent = E_A delta Phi^A + d theta_MTS", "piece_split_not_promoted"],
            "source_role": "parent symplectic potential and Noether charge extraction precedent",
        },
        {
            "row_id": "SRC2393_04_1007_doc",
            "source_key": "1007_Htau_integrability",
            "source_path": POST_ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            "needles": ["theta_MTS and Q_tau^MTS", "fail_current_claim", "delta H_tau"],
            "source_role": "Hamiltonian integrability blocked by missing parent theta/Q",
        },
        {
            "row_id": "SRC2393_05_771_owner_audit",
            "source_key": "771_theta_Qtau_owner_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv",
            "needles": ["TQ771_0_parent_variation", "TQ771_1_Noether_current", "TQ771_6_owner_verdict"],
            "source_role": "machine owner audit for parent variation and Noether current",
        },
        {
            "row_id": "SRC2393_06_771_noether_test",
            "source_key": "771_noether_extraction_test",
            "source_path": RESIDUALS / "P8_Y5_R10_771_NOETHER_EXTRACTION_TEST.csv",
            "needles": ["NET771_0_parent_variation", "NET771_2_X_current", "NET771_4_verdict"],
            "source_role": "vertical/representative Noether extraction test",
        },
        {
            "row_id": "SRC2393_07_583_momentum_map",
            "source_key": "583_momentum_map_contract",
            "source_path": RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
            "needles": ["NMC583_0_symplectic_potential", "NMC583_1_vertical_generator", "NMC583_5_boundary_zero"],
            "source_role": "Noether momentum-map and boundary-zero contract",
        },
        {
            "row_id": "SRC2393_08_parent_noether_chain",
            "source_key": "parent_noether_chain",
            "source_path": RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "needles": ["D505_2_charge_form", "Q_M[τ]", "D505_4_zero_premises"],
            "source_role": "parent Noether charge closure chain",
        },
        {
            "row_id": "SRC2393_09_1008_variation_audit",
            "source_key": "1008_parent_variation_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            "needles": ["PVA1008_0_parent_action", "PVA1008_1_theta_MTS", "PVA1008_6_verdict"],
            "source_role": "parent action/theta extraction audit",
        },
        {
            "row_id": "SRC2393_10_1008_piece_ledger",
            "source_key": "1008_charge_piece_ledger",
            "source_path": RESIDUALS / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            "needles": ["QTA1008_0_L_parent", "QTA1008_1_theta_total", "QTA1008_5_Q_extra"],
            "source_role": "current charge pieces not extracted",
        },
        {
            "row_id": "SRC2393_11_993_qtau_ledger",
            "source_key": "993_Qtau_decomposition",
            "source_path": RESIDUALS / "P8_Y5_R10_993_QTAU_DECOMPOSITION_LEDGER.csv",
            "needles": ["QDEC993_1_boundary_reference", "QDEC993_2_extra", "QDEC993_5_total"],
            "source_role": "Q_tau decomposition precedent and missing pieces",
        },
    ]
    rows: list[dict[str, object]] = []
    for source in sources:
        path = Path(source["source_path"])
        needles = list(source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": source["row_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": str(path.exists()).lower(),
                "required": "true",
                "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                "needles": "; ".join(needles),
                "source_role": source["source_role"],
                "valid_for_claim": no_claim(),
            }
        )
    return rows


def charge_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "VNC2393_0_parent_variation",
            "step": "parent variation",
            "statement": "Start from a parent local form L_parent with delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi). Without this, no vertical Noether charge is owned.",
            "derivation_status": "CONDITIONAL_VARIATION_IDENTITY",
            "current_gain": "identifies the minimum object required before any Q_v extraction",
            "remaining_gap": "explicit total L_parent and Theta_parent across EH/matter/extra/projector/boundary sectors are missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VNC2393_1_vertical_current",
            "step": "vertical Noether current",
            "statement": "For a parent vertical generator v_epsilon, if delta_v L_parent = dmu_v + E_A v^A, define J_v := Theta_parent(v_epsilon) - mu_v. On shell dJ_v=0.",
            "derivation_status": "CONDITIONAL_NOETHER_CURRENT",
            "current_gain": "turns a vertical kernel direction into a charge-bearing or charge-silent current test",
            "remaining_gap": "v_epsilon, mu_v, and action on all parent fields are not supplied",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VNC2393_2_charge_decomposition",
            "step": "vertical charge decomposition",
            "statement": "The kernel is Noether-null only if J_v = dQ_v + C_v with C_v proportional to constraints, and the allowed compact local charge integral of Q_v plus improvements vanishes.",
            "derivation_status": "CONDITIONAL_CHARGE_DECOMPOSITION",
            "current_gain": "gives a precise route from parent symmetry to zero kernel charge",
            "remaining_gap": "Q_v, C_v, improvement B_v, and compact boundary conditions are not extracted",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VNC2393_3_kernel_Hamiltonian",
            "step": "kernel Hamiltonian variation",
            "statement": "For the 2392 kernel test, require delta H_v[S] = integral_S(delta Q_v - i_v Theta_parent + delta B_v) to be finite, integrable, and zero on the allowed local surfaces.",
            "derivation_status": "CONDITIONAL_KERNEL_HAMILTONIAN_TEST",
            "current_gain": "matches the exact epsilon_kernel_charge numerator instead of handwaving gauge",
            "remaining_gap": "integrability, B_v convention, surface class, denominator, and zero-flux proof are missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VNC2393_4_piece_split",
            "step": "sector piece split",
            "statement": "Q_v must split into EH/reference, matter/source, extra/residual, projector, and boundary pieces; every piece must vanish by theorem or be included in epsilon_kernel_charge.",
            "derivation_status": "REQUIRED_SECTOR_LEDGER",
            "current_gain": "prevents hiding extra-sector or boundary charge inside a total-zero slogan",
            "remaining_gap": "piecewise vertical charge extraction is absent",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VNC2393_5_verdict",
            "step": "current verdict",
            "statement": "2393 derives the formal vertical Noether charge contract but does not extract Q_v for current MTS. The kernel-charge row remains nonclaim until parent L, Theta_parent, mu_v, Q_v, B_v, constraints, and M_H_ref are sourced.",
            "derivation_status": "ROUTE_EXACT_NOT_CLAIMED",
            "current_gain": "the next bottleneck is a sector-by-sector parent variation ledger for vertical v",
            "remaining_gap": "no Q_v pass, no kernel-nullness pass",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_0_L_parent",
            "certificate": "explicit total parent action",
            "required_test": "write L_parent including EH/local geometry, matter/source, extra/residual, projector, boundary/reference, and coupling sectors",
            "status": "MISSING_TOTAL_PARENT_ACTION",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_1_Theta_parent",
            "certificate": "parent symplectic potential",
            "required_test": "derive Theta_parent from delta L_parent = E delta Phi + dTheta_parent with all sector contributions",
            "status": "MISSING_THETA_PARENT",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_2_v_generator",
            "certificate": "vertical generator action",
            "required_test": "define v_epsilon on every parent field and prove it is the tested element of ker(Dq)",
            "status": "MISSING_VERTICAL_GENERATOR_ACTION",
            "residual_if_missing": "epsilon_q_rank_or_integrability",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_3_mu_v",
            "certificate": "Noether improvement mu_v",
            "required_test": "derive delta_v L_parent = dmu_v + E_A v^A and fix improvement ambiguity",
            "status": "MISSING_MU_V_IMPROVEMENT",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_4_Qv",
            "certificate": "vertical charge form Q_v",
            "required_test": "derive J_v = Theta_parent(v)-mu_v = dQ_v + C_v and list all sector pieces",
            "status": "MISSING_VERTICAL_QV",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_5_Bv_boundary",
            "certificate": "boundary/improvement convention",
            "required_test": "fix B_v/counterterm/reference convention and prove allowed dB improvements have zero compact local flux",
            "status": "MISSING_BV_BOUNDARY_CONVENTION",
            "residual_if_missing": "epsilon_boundary_history",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_6_zero_flux",
            "certificate": "zero compact kernel flux",
            "required_test": "prove integral_S(delta Q_v - i_v Theta_parent + delta B_v)=0 on linked local surfaces or source-bound it",
            "status": "MISSING_ZERO_KERNEL_FLUX",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQC2393_7_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "derive same-frame denominator before normalizing kernel charge",
            "status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "kernel charge cannot be scored",
            "valid_for_claim": no_claim(),
        },
    ]


def leak_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQL2393_0_kernel_charge",
            "quantity": "epsilon_kernel_charge",
            "formula": "abs(integral_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece))/M_H_ref",
            "units": "dimensionless Hamiltonian charge leakage",
            "current_value": "MISSING_THETA_PARENT;MISSING_Q_V;MISSING_B_V;MISSING_C_V;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQL2393_1_theta_piece",
            "quantity": "epsilon_theta_piece_missing",
            "formula": "abs(integral_S i_v(Theta_EH+Theta_matter+Theta_extra+Theta_projector+Theta_boundary)_missing)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_SECTOR_THETA_SPLIT;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQL2393_2_Qv_piece",
            "quantity": "epsilon_Qv_piece_missing",
            "formula": "abs(integral_S (Q_v_EH+Q_v_matter+Q_v_extra+Q_v_projector+Q_v_boundary)_missing)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_QV_SECTOR_LEDGER;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQL2393_3_improvement_ambiguity",
            "quantity": "epsilon_Bv_ambiguity",
            "formula": "abs(integral_S delta B_v_unfixed)/M_H_ref",
            "units": "dimensionless",
            "current_value": "MISSING_BV_CONVENTION;MISSING_REFERENCE_LOCK;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQL2393_4_integrability",
            "quantity": "epsilon_Hv_integrability",
            "formula": "curl_fieldspace integral_S(delta Q_v - i_v Theta_parent + delta B_v)/M_H_ref",
            "units": "dimensionless field-space curl",
            "current_value": "MISSING_FIELDSPACE_CURL_TEST;MISSING_SURFACE_CLASS;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VQL2393_5_total",
            "quantity": "Delta_vertical_Noether_charge_total_over_MH",
            "formula": "epsilon_kernel_charge + epsilon_theta_piece_missing + epsilon_Qv_piece_missing + epsilon_Bv_ambiguity + epsilon_Hv_integrability",
            "units": "dimensionless",
            "current_value": "COMPONENTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2393_0_accept_formal_contract",
            "decision": "accept vertical Noether charge extraction contract",
            "reason": "the covariant phase-space shape J_v=Theta_parent(v)-mu_v=dQ_v+C_v is the correct charge test for kernel nullness",
            "consequence": "kernel nullness can no longer be claimed without Q_v and compact flux control",
            "status": "CONDITIONAL_VERTICAL_CHARGE_CONTRACT_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2393_1_no_promotion",
            "decision": "do not promote Q_v extraction for current MTS",
            "reason": "total parent action, Theta_parent, v action, mu_v, Q_v, B_v, sector split, zero flux, integrability, and M_H_ref remain missing",
            "consequence": "vertical kernel nullness and q/Obs_e promotion remain blocked",
            "status": "VERTICAL_QV_NOT_EXTRACTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2393_2_next",
            "decision": "attack sector-by-sector parent variation ledger next",
            "reason": "without sector Theta/Qv pieces, Q_v is only a formal symbol",
            "consequence": "2394 should build the vertical sector variation ledger or keep Qv piece leaks nonclaim",
            "status": "SELECT_2394_VERTICAL_SECTOR_VARIATION_LEDGER",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2393_0_formal_shape",
            "gate": "vertical Noether charge formal shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "use as extraction contract, not current-MTS proof",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2393_1_parent_variation",
            "gate": "total L_parent and Theta_parent extracted",
            "gate_status": "FAIL",
            "claim_effect": "Q_v not owned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2393_2_Qv_sector_split",
            "gate": "Q_v sector split and constraints extracted",
            "gate_status": "FAIL",
            "claim_effect": "kernel charge cannot be zeroed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2393_3_zero_flux",
            "gate": "zero compact vertical flux",
            "gate_status": "FAIL",
            "claim_effect": "epsilon_kernel_charge remains live",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2393_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "kernel charge cannot be scored",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2393_5_GR_Newton",
            "gate": "local GR/Newton from vertical Q_v",
            "gate_status": "BLOCKED",
            "claim_effect": "no GR/Newton reduction claim from 2393",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2393_0_claim_Qv_extracted",
            "claim": "vertical Q_v is extracted for current MTS",
            "allowed": "false",
            "reason": "L_parent, Theta_parent, v action, mu_v, Q_v, sector split, boundary convention, and M_H_ref are missing",
            "blocking_rows": "VQC2393_0_L_parent;VQC2393_1_Theta_parent;VQC2393_4_Qv;VQC2393_7_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2393_1_claim_zero_flux",
            "claim": "vertical kernel charge vanishes",
            "allowed": "false",
            "reason": "formal Noether shape does not prove compact flux zero or integrability",
            "blocking_rows": "VQC2393_5_Bv_boundary;VQC2393_6_zero_flux;VQL2393_4_integrability",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2393_2_EH_import",
            "claim": "EH Noether charge alone supplies MTS vertical Q_v",
            "allowed": "false",
            "reason": "EH charge can be a reference only after MTS parent reduction and silent-sector clauses are signed",
            "blocking_rows": "VQC2393_0_L_parent;VQC2393_4_Qv;VQL2393_2_Qv_piece",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2393_3_claim_GR_Newton",
            "claim": "local GR/Newton follows from formal vertical Noether machinery",
            "allowed": "false",
            "reason": "Q_v extraction is only one upstream lock; q/Obs_e, source charge, M_H_ref, EH exterior, Poisson/Gauss, PPN, and boundary locks remain required",
            "blocking_rows": "CG2393_5_GR_Newton;VQC2393_7_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2393_0_selected",
            "next_file": "2394-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md",
            "success_condition": "derive sector pieces of Theta_parent(v), mu_v, Q_v and constraints for EH/local geometry, matter/source, extra/residual, projector, and boundary/reference sectors",
            "fallback_condition": "fill epsilon_theta_piece_missing and epsilon_Qv_piece_missing with sector source paths and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2393_1_parallel",
            "next_file": "2394b-Y5-R2FR-Bv-boundary-improvement-convention-or-compact-flux-bound.md",
            "success_condition": "fix B_v/reference convention and prove zero compact local flux",
            "fallback_condition": "fill epsilon_Bv_ambiguity and epsilon_kernel_charge boundary-improvement terms",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2393_2_parallel",
            "next_file": "2394c-Y5-R2FR-Hv-integrability-fieldspace-curl-or-kernel-Hamiltonian-bound.md",
            "success_condition": "prove delta H_v is integrable and zero for vertical kernel directions",
            "fallback_condition": "fill epsilon_Hv_integrability with field-space curl/source rows",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2393_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2393_VERTICAL_NOETHER_CHARGE_THEOREM.csv": charge_theorem_rows,
    "P8_Y5_PARENT_QLOC_2393_VERTICAL_QV_CERTIFICATE.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2393_KERNEL_CHARGE_SOURCE_ROWS.csv": leak_rows,
    "P8_Y5_PARENT_QLOC_2393_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2393_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2393_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2393_NEXT_TARGET.csv": next_target_rows,
}


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                return False
    return True


def validation_rows() -> list[dict[str, object]]:
    csv_paths = [RESIDUALS / name for name in CSV_BUILDERS]
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": no_claim(),
            }
        )

    sources = source_register()
    add("VAL2393_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2393_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = charge_theorem_rows()
    add(
        "VAL2393_02_parent_variation_present",
        any("delta L_parent = E_A delta Phi^A + dTheta_parent" in row["statement"] for row in theorem),
        "parent variation identity is present",
    )
    add(
        "VAL2393_03_vertical_current_present",
        any("J_v := Theta_parent(v_epsilon) - mu_v" in row["statement"] for row in theorem),
        "vertical Noether current formula is present",
    )
    add(
        "VAL2393_04_kernel_charge_present",
        any("delta H_v[S]" in row["statement"] and "delta Q_v" in row["statement"] for row in theorem),
        "kernel Hamiltonian variation test is present",
    )
    certs = certificate_rows()
    add(
        "VAL2393_05_required_gaps_explicit",
        all("MISSING" in row["status"] for row in certs),
        "L/theta/v/mu/Qv/Bv/flux/MHref gaps explicit",
    )
    values = leak_rows()
    add(
        "VAL2393_06_value_rows_nonready",
        all(
            row["score_ready"] == "false"
            and (("MISSING" in row["current_value"]) or row["current_value"] == "COMPONENTS_MISSING")
            for row in values
        ),
        "kernel charge source rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2393_07_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2393_0_formal_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2393_08_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths),
        "generated CSVs parse and have rows",
    )
    add("VAL2393_09_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2393_10_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2393_11_next_selected",
        any(row["row_id"] == "NEXT2393_0_selected" for row in next_target_rows()),
        "vertical sector variation ledger selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2393_OVERALL",
        overall,
        "2393 states the vertical Noether charge extraction contract, refuses Qv/zero-flux claims without sector parent variation, and selects sector variation ledger next",
    )
    return rows


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_VERTICAL_NOETHER_CHARGE_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_VERTICAL_QV_CERTIFICATE.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_KERNEL_CHARGE_SOURCE_ROWS.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2393_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2393_VALIDATION.csv")

    body = f"""# 2393 - vertical Noether charge Qv extraction or kernel-charge source row

## Result

2393 attacks the vertical charge object selected by 2392.

The formal extraction route is:

1. Parent variation:
   `delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi)`.
2. For a parent vertical generator `v_epsilon`, derive
   `delta_v L_parent = dmu_v + E_A v^A`.
3. Define the vertical Noether current:
   `J_v := Theta_parent(v_epsilon) - mu_v`.
4. Decompose on shell:
   `J_v = dQ_v + C_v`.
5. Test the compact local kernel Hamiltonian:
   `delta H_v[S] = integral_S(delta Q_v - i_v Theta_parent + delta B_v)`.

If that object is finite, integrable, and zero on the allowed compact local surfaces, the vertical kernel can pass the
presymplectic-null part of 2392.  If not, the kernel carries a real charge residual.

Current MTS does not yet provide the total parent action, `Theta_parent`, vertical generator action on all fields,
`mu_v`, `Q_v`, sector split, boundary convention `B_v`, zero compact flux, integrability, or positive same-frame
`M_H_ref`.

So 2393 is a formal extraction contract, not a `Q_v` extraction claim.  No vertical-kernel-nullness pass, parent
`q/Obs_e` pass, same-frame pass, local-GR pass, Newton pass, PPN, clock, orbital, R10, or public/GitHub claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Vertical Noether Charge Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "derivation_status", "current_gain", "remaining_gap", "valid_for_claim"])}

## Vertical Qv Certificate

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## Kernel Charge Source Rows

{markdown_table(values, ["row_id", "quantity", "formula", "units", "current_value", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is another useful narrowing.  The project now knows exactly what a non-smuggled kernel proof needs: not a word
like gauge, but a sector-derived `Q_v` with zero compact flux.  The next lock is sector bookkeeping: EH/local geometry,
matter/source, extra/residual, projector, and boundary/reference pieces must each be varied or retained as explicit
leaks.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2393_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2393_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
