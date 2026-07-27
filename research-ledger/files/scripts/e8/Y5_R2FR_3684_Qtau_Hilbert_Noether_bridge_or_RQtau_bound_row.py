from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3684"
BRANCH_ID = "MTS_R2FR_Y5_QTAU_HILBERT_NOETHER_BRIDGE_OR_RQTAU_BOUND_3684"
DOC = ROOT / "3684-Y5-R2FR-Qtau-Hilbert-Noether-bridge-or-RQtau-bound-row.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        return True, len(load_csv(path))
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3683", RESIDUALS / "P8_Y5_R2FR_3683_NEXT_TARGET.csv", "R_Qtau_owner", "3683 selected Q_tau/Hilbert Noether bridge"),
        ("identity_1818", RESIDUALS / "P8_Y5_PARENT_QLOC_1818_HILBERT_WORLDTUBE_CHARGE_IDENTITY_THEOREM.csv", "HCI1818_1_noether_charge", "parent covariant phase-space Q_tau gate"),
        ("hta_1007", RESIDUALS / "P8_Y5_R10_1007_HTAU_INTEGRABILITY_THEOREM_AUDIT.csv", "HTA1007_1_parent_theta_Qtau", "H_tau integrability audit identifies missing theta/Q_tau"),
        ("schema_1007", RESIDUALS / "P8_Y5_R10_1007_SYMPLECTIC_RESIDUAL_SCHEMA.csv", "SRS1007_0_integrability_formula", "finite symplectic/reference residual schema"),
        ("cdc_1008", RESIDUALS / "P8_Y5_R10_1008_CANDIDATE_CHARGE_DECOMPOSITION_TEMPLATE.csv", "CDC1008_0_missing_parent_L", "charge decomposition candidates reject missing parent L"),
        ("noether_505", RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv", "D505_2_charge_form", "parent Noether closure chain and charge form"),
        ("charge_current", RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv", "CC4_boundary_variation_equals_projected_source_variation", "boundary variation equals projected source variation target"),
        ("pim_htau_3514", RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv", "PHCR3514_3_C_curl", "H_tau curl and source-current square residual components"),
        ("sectors_2939", RESIDUALS / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv", "SEC2939_8_tau_surface", "sector certificate ledger keeps tau/surface lock unsigned"),
        ("matrix_2940", RESIDUALS / "P8_Y5_R2FR_2940_SECTOR_CERTIFICATE_MATRIX.csv", "SEC2940_5_worldtube", "sector matrix identifies worldtube source glue and parent action blockers"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def bridge_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "QHB3684_0_target",
            "prove the Q_tau/Hilbert source bridge",
            "G_ref^-1 Q_tau^MTS = ell_M(Pi_M^H J_H^dress) + dB_H, equivalently R_Qtau_owner=0",
            "TARGET_NOT_PROVED",
            "this is the exact parent source-bridge target, not a fit-level GM substitution",
            False,
        ),
        (
            "QHB3684_1_exact_conditional_theorem",
            "conditional Noether-Hamiltonian bridge theorem",
            "If L_parent is signed, theta_MTS and Q_tau^MTS are extracted, H_tau is integrable with fixed tau/reference, the Hamiltonian constraint has the same Hilbert source, extra sectors are zero/bounded, and the improvement policy is fixed, then R_Qtau_owner=0.",
            "EXACT_CONDITIONAL_THEOREM_NOT_LIVE",
            "we have the exact theorem contract, but not the parent certificates needed to fire it",
            False,
        ),
        (
            "QHB3684_2_EH_reference_guard",
            "EH covariant charge can only be a reference pattern",
            "Q_tau^EH cannot be substituted for Q_tau^MTS unless MTS-to-EH reduction plus silent-sector certificates are signed.",
            "ANTI_SMUGGLING_GUARD",
            "prevents proving GR by assuming the GR charge",
            False,
        ),
        (
            "QHB3684_3_fitted_reference_guard",
            "reference/counterterm cannot be fitted after readout",
            "H_ref, B_ref and counterterm convention must be fixed before source/orbital/R10 readout; fitted cancellation rows are refused.",
            "ANTI_LAUNDERING_GUARD",
            "prevents denominator/reference laundering",
            False,
        ),
        (
            "QHB3684_4_constraint_glue",
            "boundary charge variation must equal projected Hilbert source variation",
            "delta(G_ref^-1 Q_tau^MTS) = delta ell_M(Pi_M^H J_H^dress) + delta dB_H only if the Hamiltonian constraint/source equation uses the same Hilbert stress and no residual operators.",
            "CONDITIONAL_CONSTRAINT_GLUE",
            "this is the positive route from parent charge to Newtonian source mass",
            False,
        ),
        (
            "QHB3684_5_current_verdict",
            "current corpus proves R_Qtau_owner=0",
            "The live corpus lacks a signed total parent action/theta/Q_tau extraction, integrable H_tau, fixed reference, tau lock, matter-source glue and improvement policy.",
            "RQTAU_ZERO_NOT_PROVED_BOUND_SCHEMA_PROMOTED",
            "R_Qtau_owner becomes a finite no-cancellation residual vector",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "audit_id": audit_id,
            "claim": claim,
            "mathematical_statement": mathematical_statement,
            "status": status,
            "consequence": consequence,
            "zero_subslot": zero_subslot,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for audit_id, claim, mathematical_statement, status, consequence, zero_subslot in specs
    ]


def component_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "RQT3684_0_definition",
            "R_Qtau_owner",
            "G_ref^-1 Q_tau^MTS - ell_M(Pi_M^H J_H^dress) - dB_H",
            "exact Noether/Hilbert source equality residual",
            "DEFINITION_NONCLAIM",
            "mass-charge or source-current units",
            "RHS3683_3_Qtau_owner",
            "the direct bridge between parent Q_tau and Hilbert source charge",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_1_parent_action",
            "R_parent_LthetaQ",
            "failure to extract L_parent -> theta_MTS,Q_tau^MTS,C_tau",
            "parent action / symplectic potential / Noether charge extraction residual",
            "MISSING_PARENT_L_THETA_QTAU_EXTRACTION",
            "mass-charge units",
            "HTA1007_1_parent_theta_Qtau;CDC1008_0_missing_parent_L",
            "first upstream certificate; EH-only import is refused",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_2_integrability",
            "R_Htau_integrability",
            "curl(delta H_tau) + Delta_symp + B_zero_flux",
            "H_tau nonintegrability and symplectic/boundary flux residual",
            "MISSING_HTAU_INTEGRABILITY_OR_BOUND",
            "mass-charge units",
            "SRS1007_0_integrability_formula;PHCR3514_3_C_curl",
            "must be zero or bounded before Q_tau becomes a source charge",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_3_constraint_source",
            "R_constraint_source",
            "delta(G_ref^-1 Q_tau^MTS) - delta ell_M(Pi_M^H J_H^dress) - delta dB_H",
            "Hamiltonian constraint/source-equation glue residual",
            "MISSING_CONSTRAINT_SOURCE_GLUE",
            "mass-charge units",
            "CC2_EH_constraint_source_link;CC4_boundary_variation_equals_projected_source_variation",
            "positive route to derive Newton source without importing GM",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_4_tau_frame",
            "R_tau_lock",
            "Delta(tau_source,tau_charge,tau_clock,tau_orbit,tau_R10)",
            "same observed time generator/frame/surface lock residual",
            "MISSING_TAU_FRAME_LOCK",
            "mass-charge units or dimensionless after N_H normalization",
            "HTA1007_4_tau_lock;SEC2939_8_tau_surface",
            "same clock/climbing-gear intuition has to be one branch, not arena-dependent tau",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_5_reference",
            "R_ref_fixed",
            "D(H_ref,B_ref,counterterm) before readout plus Delta_ref",
            "fixed reference/counterterm residual",
            "MISSING_FIXED_REFERENCE_CERTIFICATE_OR_BOUND",
            "mass-charge units",
            "HTA1007_3_fixed_reference;SRS1007_3_no_fitted_reference",
            "reference constants are harmless only when fixed before readout",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_6_improvement",
            "R_improvement_policy",
            "Q_tau^MTS -> Q_tau^MTS + dY ambiguity not fixed",
            "Noether charge improvement/corner policy residual",
            "MISSING_IMPROVEMENT_AMBIGUITY_CERTIFICATE",
            "mass-charge units",
            "CDC1008_0_missing_parent_L;D505_2_charge_form",
            "exact terms cannot be chosen after seeing the arena",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_7_reduced_RQtau",
            "R_Qtau_owner",
            "R_parent_LthetaQ + R_Htau_integrability + R_constraint_source + R_tau_lock + R_ref_fixed + R_improvement_policy",
            "reduced no-cancellation vector for the Q_tau/Hilbert bridge",
            "REDUCED_NO_CANCELLATION_VECTOR",
            "mass-charge units",
            "RQT3684_1_parent_action;RQT3684_2_integrability;RQT3684_3_constraint_source;RQT3684_4_tau_frame;RQT3684_5_reference;RQT3684_6_improvement",
            "finite executable residual rather than vague missing coupling",
            "MISSING_COMPONENT_VALUE",
        ),
        (
            "RQT3684_8_normalized_envelope",
            "abs(z_RQtau,A)",
            "(|R_parent_LthetaQ|+|R_Htau_integrability|+|R_constraint_source|+|R_tau_lock|+|R_ref_fixed|+|R_improvement_policy|)/N_H",
            "dimensionless no-cancellation envelope with N_H=||ell_M(Pi_M^H J_H^dress)||",
            "FORMULA_READY_INPUTS_MISSING",
            "dimensionless",
            "RQT3684_7_reduced_RQtau",
            "score only after N_H and every numerator row are source-backed",
            "MISSING_COMPONENT_VALUE",
        ),
    ]
    rows: list[dict[str, object]] = []
    for split_id, symbol, formula_or_value, meaning, status, units, source_anchor, interpretation, numeric_value in specs:
        rows.append(
            {
                **base(ts),
                "component_id": split_id,
                "symbol": symbol,
                "formula_or_value": formula_or_value,
                "meaning": meaning,
                "status": status,
                "units": units,
                "source_anchor": source_anchor,
                "interpretation": interpretation,
                "numeric_value": numeric_value,
                "valid_for_claim": False,
                "claim_allowed": False,
                "score_ready": False,
            }
        )
    return rows


def bound_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("RQB3684_0_parent_action", "abs(R_parent_LthetaQ)/N_H", "MISSING_PARENT_L_THETA_Q_BOUND_VALUE", "dimensionless", "needs signed L_parent, theta_MTS, Q_tau^MTS, C_tau and sector certificates", "MISSING_PARENT_NOETHER_SOURCE_PATH"),
        ("RQB3684_1_integrability", "abs(R_Htau_integrability)/N_H", "abs(delta_H_tau_nonintegrable_over_MH)+abs(Delta_symp_over_MH)+abs(B_zero_flux_over_MH)", "dimensionless", "schema-ready from 1007 but not numeric until parent theta/Q_tau and boundary rows are sourced", "SRS1007_0_integrability_formula"),
        ("RQB3684_2_constraint_source", "abs(R_constraint_source)/N_H", "MISSING_CONSTRAINT_SOURCE_GLUE_BOUND_VALUE", "dimensionless", "needs Hamiltonian constraint/source equation using same Hilbert stress and no residual operator", "MISSING_CONSTRAINT_SOURCE_EQUATION_PATH"),
        ("RQB3684_3_tau_lock", "abs(R_tau_lock)/N_H", "MISSING_TAU_FRAME_LOCK_BOUND_VALUE", "dimensionless", "needs one tau/frame/surface branch for source, charge, clock, orbit and R10", "MISSING_TAU_LOCK_SOURCE_PATH"),
        ("RQB3684_4_reference", "abs(R_ref_fixed)/N_H", "MISSING_FIXED_REFERENCE_BOUND_VALUE", "dimensionless", "needs source-blind fixed-before-readout H_ref/B_ref/counterterm convention", "MISSING_FIXED_REFERENCE_SOURCE_PATH"),
        ("RQB3684_5_improvement", "abs(R_improvement_policy)/N_H", "MISSING_IMPROVEMENT_BOUND_VALUE", "dimensionless", "needs Noether improvement/corner ambiguity policy fixed before arena readout", "MISSING_IMPROVEMENT_POLICY_SOURCE_PATH"),
        ("RQB3684_6_total", "abs(z_RQtau,A)", "(abs(R_parent_LthetaQ)+abs(R_Htau_integrability)+abs(R_constraint_source)+abs(R_tau_lock)+abs(R_ref_fixed)+abs(R_improvement_policy))/N_H", "dimensionless no-cancellation envelope", "source-ready total bridge envelope; nonclaim until every numerator and N_H are finite and sourced", "RQT3684_8_normalized_envelope"),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "status": "FORMULA_READY_INPUTS_MISSING",
            "interpretation": interpretation,
            "source_path_or_missing": source_path_or_missing,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, interpretation, source_path_or_missing in specs
    ]


def certificate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CERT3684_0_parent_action", "parent Lagrangian and variation", "L_parent, theta_MTS, Q_tau^MTS, C_tau extracted for all retained sectors", "MISSING_PARENT_CERTIFICATE", "R_parent_LthetaQ"),
        ("CERT3684_1_EH_reduction", "EH reference legality", "MTS exterior reduces to EH plus topological/silent/bounded sectors before using Q_tau^EH", "MISSING_EH_REDUCTION_CERTIFICATE", "R_parent_LthetaQ"),
        ("CERT3684_2_integrability", "Hamiltonian integrability", "delta H_tau finite, differentiable, path-independent with zero/bounded symplectic flux", "MISSING_INTEGRABILITY_CERTIFICATE", "R_Htau_integrability"),
        ("CERT3684_3_constraint_source", "constraint/source glue", "same Hamiltonian constraint uses same Hilbert stress current J_H^dress", "MISSING_CONSTRAINT_SOURCE_CERTIFICATE", "R_constraint_source"),
        ("CERT3684_4_tau_frame", "same tau/frame/surface", "tau_source=tau_charge=tau_clock=tau_orbit=tau_R10 with fixed linked surfaces", "MISSING_TAU_FRAME_CERTIFICATE", "R_tau_lock"),
        ("CERT3684_5_reference", "fixed reference/counterterm", "H_ref, B_ref, corner and counterterm convention fixed before readout", "MISSING_REFERENCE_CERTIFICATE", "R_ref_fixed"),
        ("CERT3684_6_improvement", "Noether improvement policy", "exact/corner improvements fixed by parent boundary class, not fitted per arena", "MISSING_IMPROVEMENT_CERTIFICATE", "R_improvement_policy"),
        ("CERT3684_7_denominator", "positive same-frame N_H", "N_H=||ell_M(Pi_M^H J_H^dress)|| positive, sourced, same frame and not orbital-GM imported", "MISSING_NH_DENOMINATOR_CERTIFICATE", "all normalized rows"),
    ]
    return [
        {
            **base(ts),
            "certificate_id": certificate_id,
            "certificate": certificate,
            "required_content": required_content,
            "status": status,
            "closes_component": closes_component,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for certificate_id, certificate, required_content, status, closes_component in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3684_0_result", "R_Qtau_owner=0 is not derived", "BOUND_SCHEMA_PROMOTED", "parent Noether/Hamiltonian source bridge certificates are missing", "carry executable R_Qtau_owner vector"),
        ("DEC3684_1_real_progress", "the bridge is now certificate-factorized", "COUPLING_THROAT_DECOMPOSED", "we know exactly which parent objects must be supplied instead of saying coupling is vague", "attack parent L/theta/Q first"),
        ("DEC3684_2_guardrail", "EH import and fitted reference are refused", "ANTI_SMUGGLING_GUARD_ACTIVE", "GR charge/reference cannot be used as its own proof", "allow EH only after MTS reduction certificates"),
        ("DEC3684_3_next_route", "parent Noether extraction is the best next target", "NEXT_BEST_TARGET", "without L_parent -> theta_MTS,Q_tau^MTS,C_tau no downstream source bridge can close", "attempt parent current-chain extraction or closure axiom"),
        ("DEC3684_4_private", "no local-GR/Newton/source claim", "PRIVATE_NONCLAIM", "a bound schema is not a pass", "continue privately"),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "status": status,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, decision, status, reason, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3684_0_RQtau_zero", "claim R_Qtau_owner=0", "BLOCKED_PARENT_CERTIFICATES", "parent action/theta/Q, integrability, constraint glue, tau, reference and improvement certificates are missing"),
        ("CG3684_1_EH_import", "use EH covariant charge as MTS Q_tau", "BLOCKED_EH_SMUGGLING", "EH is reference-only until MTS-to-EH plus silent-sector reduction is signed"),
        ("CG3684_2_fitted_reference", "fit H_ref or counterterm after readout", "BLOCKED_REFERENCE_LAUNDERING", "reference must be fixed before source/orbital/R10 readout"),
        ("CG3684_3_Newton_GR", "claim Newton/local-GR source bridge", "BLOCKED_RQTAU_AND_CALIBRATION", "Q_tau/Hilbert equality and Poisson/Gauss calibration remain unproved"),
        ("CG3684_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private derivation checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "RQTAU_ZERO_NOT_DERIVED_BRIDGE_CERTIFICATES_AND_BOUND_SCHEMA_PROMOTED_NONCLAIM",
            "summary": "3684 does not close R_Qtau_owner. It converts the Q_tau/Hilbert source bridge into a precise certificate contract and finite no-cancellation bound schema, with explicit anti-smuggling guards against EH-only import and fitted reference/counterterm laundering.",
            "claim_ceiling": "no R_Qtau_owner zero, R_Hsrc zero, Newton/local-GR source bridge, PPN/orbital calibration, WEP/R10/clock pass, or public claim is made",
            "useful_result": "R_Qtau_owner is now R_parent_LthetaQ + R_Htau_integrability + R_constraint_source + R_tau_lock + R_ref_fixed + R_improvement_policy, normalized by N_H only after every source row exists",
            "next_missing_piece": "extract or explicitly close/adopt L_parent -> theta_MTS, Q_tau^MTS, C_tau for retained sectors",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3684_0",
            "target_doc": "3685-Y5-R2FR-parent-Ltheta-Qtau-current-chain-extraction-or-closure-axiom.md",
            "target_script": "scripts/Y5_R2FR_3685_parent_Ltheta_Qtau_current_chain_extraction_or_closure_axiom.py",
            "objective": "attempt to extract L_parent -> theta_MTS, Q_tau^MTS and C_tau for the retained current-chain sectors; if extraction fails, write the exact closure-only axiom and keep R_Qtau_owner nonclaim",
            "success_gate": "R_parent_LthetaQ is theorem-zero from explicit parent variation with sector certificates, or a closure-only axiom/residual row is staged without local-GR/Newton claims",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    components: list[dict[str, object]],
    bounds: list[dict[str, object]],
    certificates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3684 - Q_tau Hilbert Noether bridge or R_Qtau bound row",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint attacks `R_Qtau_owner`, the bridge from parent Noether/Hamiltonian charge to the dressed Hilbert source. The result is not a closure claim; it is an exact conditional bridge theorem plus an executable residual contract.",
        "",
        "## Main result",
        "",
        "`R_Qtau_owner = G_ref^-1 Q_tau^MTS - ell_M(Pi_M^H J_H^dress) - dB_H`.",
        "",
        "The current corpus does **not** prove `R_Qtau_owner=0`.",
        "",
        "The reduced bridge residual is:",
        "",
        "`R_Qtau_owner = R_parent_LthetaQ + R_Htau_integrability + R_constraint_source + R_tau_lock + R_ref_fixed + R_improvement_policy`.",
        "",
        "The normalized no-cancellation envelope is:",
        "",
        "`abs(z_RQtau,A) <= (|R_parent_LthetaQ|+|R_Htau_integrability|+|R_constraint_source|+|R_tau_lock|+|R_ref_fixed|+|R_improvement_policy|)/N_H`.",
        "",
        "Two hard guards are now explicit: `Q_tau^EH` is reference-only until MTS-to-EH reduction is signed, and `H_ref/B_ref` cannot be fitted after readout.",
        "",
        "## Bridge audit rows",
    ]
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['status']} - {row['claim']} -> {row['consequence']}")
    lines.extend(["", "## Component rows"])
    for row in components:
        lines.append(f"- `{row['component_id']}`: {row['status']} - `{row['symbol']}` -> `{row['formula_or_value']}`")
    lines.extend(["", "## Bound rows"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## Certificate contract"])
    for row in certificates:
        lines.append(f"- `{row['certificate_id']}`: {row['status']} - {row['certificate']} closes `{row['closes_component']}`")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    audit: list[dict[str, object]],
    components: list[dict[str, object]],
    bounds: list[dict[str, object]],
    certificates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + audit + components + bounds + certificates + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3684*", "3684-Y5-R2FR-*", "P8_Y5*3684*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    audit_by_id = {str(row["audit_id"]): row for row in audit}
    component_by_id = {str(row["component_id"]): row for row in components}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}
    cert_ids = {str(row["certificate_id"]) for row in certificates}

    add("VAL3684_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3684_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3684_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3684 outputs written")
    add("VAL3684_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3684_4_conditional_theorem", audit_by_id["QHB3684_1_exact_conditional_theorem"]["status"] == "EXACT_CONDITIONAL_THEOREM_NOT_LIVE", "exact conditional bridge theorem is recorded without claim")
    add("VAL3684_5_not_zero", audit_by_id["QHB3684_5_current_verdict"]["status"] == "RQTAU_ZERO_NOT_PROVED_BOUND_SCHEMA_PROMOTED", "R_Qtau_owner zero is not claimed")
    add("VAL3684_6_reduced_formula", component_by_id["RQT3684_7_reduced_RQtau"]["formula_or_value"] == "R_parent_LthetaQ + R_Htau_integrability + R_constraint_source + R_tau_lock + R_ref_fixed + R_improvement_policy", "R_Qtau_owner reduced to certificate components")
    add("VAL3684_7_bound_schema", "R_parent_LthetaQ" in str(bound_by_id["RQB3684_6_total"]["bound_or_formula"]) and "N_H" in str(component_by_id["RQT3684_8_normalized_envelope"]["formula_or_value"]), "normalized no-cancellation envelope is recorded")
    add("VAL3684_8_certificates", {"CERT3684_0_parent_action", "CERT3684_2_integrability", "CERT3684_3_constraint_source", "CERT3684_4_tau_frame", "CERT3684_5_reference", "CERT3684_6_improvement", "CERT3684_7_denominator"}.issubset(cert_ids), "certificate contract covers all bridge components and denominator")
    add("VAL3684_9_guards", any(row["claim_gate_id"] == "CG3684_1_EH_import" and row["status"] == "BLOCKED_EH_SMUGGLING" for row in gates) and any(row["claim_gate_id"] == "CG3684_2_fitted_reference" for row in gates), "EH import and fitted reference guards are active")
    add("VAL3684_10_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3684_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3684_12_doc_written", "R_Qtau_owner = G_ref^-1 Q_tau^MTS" in doc_text and "Q_tau^EH" in doc_text and "H_ref/B_ref" in doc_text, "doc records bridge residual and anti-smuggling guards")
    add("VAL3684_13_next_target", next_target[0]["target_doc"].startswith("3685-") and "theta_MTS" in next_target[0]["objective"], "3685 targets parent L/theta/Q extraction")
    add("VAL3684_14_no_formalization_leak", not leaks, "no 3684 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    audit = bridge_audit_rows(ts)
    components = component_rows(ts)
    bounds = bound_rows(ts)
    certificates = certificate_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3684_SOURCE_REGISTER.csv",
        "audit": RESIDUALS / "P8_Y5_R2FR_3684_QTAU_HILBERT_BRIDGE_AUDIT.csv",
        "components": RESIDUALS / "P8_Y5_R2FR_3684_RQTAU_COMPONENT_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3684_RQTAU_BOUND_SCHEMA_ROWS.csv",
        "certificates": RESIDUALS / "P8_Y5_R2FR_3684_BRIDGE_CERTIFICATE_CONTRACT_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3684_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3684_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3684_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3684_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3684_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["components"], components)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["certificates"], certificates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, audit, components, bounds, certificates, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, audit, components, bounds, certificates, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3684 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3684 checkpoint: R_Qtau_owner bridge contract and bound schema promoted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
