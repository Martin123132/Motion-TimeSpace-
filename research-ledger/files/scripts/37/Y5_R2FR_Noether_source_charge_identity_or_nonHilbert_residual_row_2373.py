from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_NOETHER_SOURCE_CHARGE_IDENTITY_OR_NONHILBERT_RESIDUAL_2373"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2373-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2373_2372_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2372_NEXT_TARGET.csv", "NEXT2372_0_selected", "2372 selected Noether/source-charge route"),
        ("SRC2373_2372_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2372_VALIDATION.csv", "VAL2372_OVERALL", "2372 validation"),
        ("SRC2373_2331_identity", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2331_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv", "NSCI2331_7_verdict", "Noether/source-charge identity attempt"),
        ("SRC2373_2331_residual", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2331_NONHILBERT_RESIDUAL_ROW.csv", "NHR2331_0_total", "non-Hilbert residual row"),
        ("SRC2373_2331_impact", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2331_SOURCE_CHARGE_GATE_IMPACT.csv", "SCI2331_4_local_GR_Newton", "source charge gate impact"),
        ("SRC2373_2331_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2331_NEXT_TARGET.csv", "NEXT2331_0", "non-Hilbert trident next target"),
        ("SRC2373_2331_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2331_VALIDATION.csv", "VAL2331_OVERALL", "2331 validation"),
        ("SRC2373_2332_trident", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2332_NONHILBERT_TRIDENT_SILENCE_AUDIT.csv", "NHT2332_3_readout_reentry", "non-Hilbert trident audit"),
        ("SRC2373_2332_envelopes", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2332_NONHILBERT_RESIDUAL_ENVELOPES.csv", "NHE2332_0_total_abs", "absolute residual envelopes"),
        ("SRC2373_2332_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2332_NEXT_TARGET.csv", "NEXT2332_0", "no-hypermomentum next target"),
        ("SRC2373_2332_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2332_VALIDATION.csv", "VAL2332_OVERALL", "2332 validation"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def source_charge_identity_attempt() -> list[dict[str, object]]:
    rows = [
        (
            "NSCI2373_0_target",
            "Noether source charge identity",
            "J_active for ordinary matter equals the Hilbert/Noether source charge of the same observed matter action, with no independent gravitational source charge.",
            "TARGET_SHARPENED",
            "would derive Minimal Universal Matter Coupling rather than using it as private restriction",
        ),
        (
            "NSCI2373_1_hilbert_owner",
            "Hilbert source owner",
            "If a single observed matter action is fixed, T_H := delta S_m/delta e_obs is the active source before readout.",
            "EXACT_CONDITIONAL_THEOREM",
            "kills post-variation source-current rescaling only after the action/signature is fixed",
        ),
        (
            "NSCI2373_2_ward_noether",
            "Ward/Noether conservation",
            "Diffeomorphism/local-frame invariance of S_m gives covariant conservation of T_H on matter shell.",
            "EXACT_CONDITIONAL_CONSERVATION",
            "conservation of a chosen source does not prove source uniqueness or universal normalization",
        ),
        (
            "NSCI2373_3_canonical_improvement",
            "canonical-to-Hilbert improvement",
            "canonical stress differs from Hilbert stress by owned improvement/superpotential terms plus possible boundary flux.",
            "CONDITIONAL_IMPROVEMENT_BOUND_REQUIRED",
            "safe only if compact exterior boundary/improvement flux is zero, projected silent, or bounded",
        ),
        (
            "NSCI2373_4_pre_action_weight",
            "pre-action species weights",
            "S_m=sum_A w_A S_A has a conserved Hilbert/Noether current if w_A is legal before variation.",
            "COUNTERMODEL_SURVIVES_WITHOUT_MUMC",
            "Noether conservation preserves the weighted current; it does not forbid the weight",
        ),
        (
            "NSCI2373_5_nonhilbert_channels",
            "non-Hilbert source-current channels",
            "spin/torsion, boundary/worldtube, readout reentry, and improvement flux must vanish, be exact/projected-silent, or remain explicit residuals.",
            "OPEN_RETAIN_RESIDUAL_ROW",
            "Hilbert/Noether identity for ordinary matter does not automatically silence all source channels",
        ),
        (
            "NSCI2373_6_projected_mass_charge",
            "projected measured-GM charge",
            "M_eff must be a closed calibrated projection of Hilbert/Hamiltonian/worldtube charge before Kepler/PPN readout.",
            "PROJECTED_MASS_CHARGE_NOT_CLOSED",
            "Pi_M commutator, exchange current, boundary flux, and orbital calibration exceed unprojected Ward conservation",
        ),
        (
            "NSCI2373_7_verdict",
            "derive no independent gravitational source charge now",
            "Current active evidence derives no independent gravitational source charge beyond Hilbert/Noether stress source.",
            "NOT_DERIVED_RETAIN_NONHILBERT_ROW",
            "conditional owner is real, but pre-action weights, non-Hilbert channels, and projected mass-charge closure remain open",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "identity_piece": piece,
            "formal_statement": statement,
            "status": status,
            "proof_or_obstruction": obstruction,
        }
        for row_id, piece, statement, status, obstruction in rows
    ]


def nonhilbert_residual_row() -> list[dict[str, object]]:
    rows = [
        (
            "NHR2373_0_total",
            "P_source_J_NH_abs",
            "projected non-Hilbert source-current envelope after Hilbert matter current is extracted",
            "||P_source[J_NH]|| <= E_spin + E_boundary + E_readout + E_improvement",
            "E_spin;E_boundary;E_readout;E_improvement",
            "source-current units; arena-projected to PPN/WEP/orbit units later",
            "CONTRACT_READY_VALUES_MISSING",
            "zero theorem or envelope for every component in common units",
        ),
        (
            "NHR2373_1_spin_torsion",
            "E_spin",
            "spin, torsion, nonmetricity, or hypermomentum source-current projection",
            "E_spin >= ||P_source[J_spin/torsion/nonmetricity/hypermomentum]||",
            "torsionless theorem or P4 connection residual map",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "Levi-Civita/no-hypermomentum theorem or source-backed spin-current envelope",
        ),
        (
            "NHR2373_2_boundary_worldtube",
            "E_boundary",
            "boundary, worldtube, compact flux, or surface source-current projection",
            "E_boundary >= ||P_source[J_boundary/worldtube]||",
            "boundary no-flux theorem or source-worldtube envelope",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "boundary/falloff/orientation theorem or source-backed flux bound",
        ),
        (
            "NHR2373_3_readout_reentry",
            "E_readout",
            "post-variation readout, domain, marker, or frame map that re-enters as source-labelled current",
            "E_readout >= ||P_source[J_readout_reentry]||",
            "readout no-reentry theorem or commutator residual map",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "downstream/no-source-codomain proof per arena or finite residual",
        ),
        (
            "NHR2373_4_improvement_flux",
            "E_improvement",
            "canonical/Hilbert improvement, superpotential, edge, or Hamiltonian representative flux",
            "E_improvement >= ||P_source[J_improvement_flux]||",
            "Hamiltonian representative and compact edge projection",
            "source-current units",
            "MISSING_ZERO_OR_ENVELOPE",
            "improvement flux zero theorem or compact-flux envelope",
        ),
        (
            "NHR2373_5_projected_mass",
            "Delta_M_projected",
            "commutator/exchange term between Hilbert charge conservation and measured-GM mass projector",
            "Delta_M_projected = [d,Pi_M]J_H + Pi_M J_exchange + boundary/anomaly flux",
            "Pi_M ownership; exchange silence; Gauss/orbital calibration",
            "mass-charge or dimensionless after GM normalization",
            "PROJECTOR_CLOSURE_MISSING",
            "projected mass-charge closure checkpoint",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "bound_form": bound,
            "component_inputs": inputs,
            "units": units,
            "status": status,
            "next_input": next_input,
        }
        for row_id, quantity, definition, bound, inputs, units, status, next_input in rows
    ]


def trident_gate_update() -> list[dict[str, object]]:
    rows = [
        (
            "TRI2373_0_total",
            "total non-Hilbert source current",
            "J_NH=0 only if spin/torsion, boundary/improvement and readout reentry heads are each absent/exact/projected-silent",
            "NOT_ZERO_RETAIN_COMPONENTS",
            "absolute residual envelope, no cancellation",
        ),
        (
            "TRI2373_1_spin_torsion",
            "spin/torsion/nonmetricity/hypermomentum",
            "connection is metric-only Levi-Civita, or Palatini EH plus no matter/source/readout hypermomentum, or projection is exact/silent",
            "SELECTED_NEXT_PRIMARY_GATE",
            "closest GR-like structural route; retain P4 residual if not proved",
        ),
        (
            "TRI2373_2_boundary_improvement",
            "boundary/worldtube/improvement flux",
            "boundary charge/improvement flux fixed by differentiable Hamiltonian reference and zero compact local projection",
            "PARALLEL_GATE_OPEN",
            "cannot silently drop exact terms if improper/edge charge survives",
        ),
        (
            "TRI2373_3_readout_reentry",
            "readout/domain/frame reentry",
            "readout maps act downstream and cannot create source-labelled current terms",
            "PARALLEL_GATE_OPEN",
            "requires no-source-codomain/commutator proof per arena",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "trident_head": head,
            "zero_route": route,
            "status": status,
            "fallback_or_effect": effect,
        }
        for row_id, head, route, status, effect in rows
    ]


def source_charge_gate_impact() -> list[dict[str, object]]:
    rows = [
        (
            "SCI2373_0_MUMC_branch",
            "Minimal Universal Matter Coupling private branch",
            "under MUMC, pre-action w_A is forbidden by restriction, not derived by 2373",
            "Noether/source-charge derivation of the restriction",
            "private_condition_only",
        ),
        (
            "SCI2373_1_no_species_charge",
            "no independent gravitational source charge",
            "Hilbert/Noether source ownership works once the action is fixed",
            "proof that no pre-action species source coefficient is admissible",
            "not_derived",
        ),
        (
            "SCI2373_2_nonhilbert_gate",
            "non-Hilbert/boundary/readout source currents",
            "must be zero/bounded before source-side GR claim",
            "spin/torsion, boundary flux, readout reentry, improvement flux inputs",
            "retained_residual",
        ),
        (
            "SCI2373_3_GM_source_charge",
            "measured-GM projected source charge",
            "Ward conservation alone does not derive calibrated GM",
            "closed Pi_M J_H, exchange silence, boundary flux zero, Kepler calibration",
            "not_closed",
        ),
        (
            "SCI2373_4_local_GR_Newton",
            "full local GR/Newton recovery",
            "source-side map improved but local GR remains open",
            "left-hand EH/Newton limit, PPN/readout residuals, projector/domain closure",
            "blocked",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "impact": impact,
            "still_missing": missing,
            "claim_status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, impact, missing, status in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2373_0_sources", "source paths and needles valid", "PASS", "audit reproducible"),
        ("CG2373_1_hilbert_noether_owner", "Hilbert/Noether source owner exact conditionally", "PASS", "conditional theorem retained"),
        ("CG2373_2_no_independent_charge", "no independent gravitational source charge derived now", "FAIL", "pre-action weights remain countermodel outside MUMC"),
        ("CG2373_3_nonhilbert_silence", "non-Hilbert source current is zero", "FAIL", "trident residual gates remain"),
        ("CG2373_4_projected_GM_charge", "measured-GM charge derived from closed Hilbert projection", "FAIL", "projected mass charge not closed"),
        ("CG2373_5_local_GR_Newton", "local GR/Newton recovery derived", "FAIL", "not enough yet"),
        ("CG2373_6_github_public_update", "safe to push as public evidence", "FAIL", "private derivation/residual checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "gate_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, gate, status, effect in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        (
            "REF2373_0_conservation_as_uniqueness",
            "Ward conservation proves unique species-blind source normalization.",
            "false",
            "conservation preserves a chosen weighted current; it does not forbid pre-action weights",
        ),
        (
            "REF2373_1_hilbert_as_nonhilbert_silence",
            "Hilbert owner automatically kills non-Hilbert currents.",
            "false",
            "spin/torsion, boundary, readout reentry and improvement flux remain separate channels",
        ),
        (
            "REF2373_2_GM_from_Ward_only",
            "Ward identity derives measured GM/source-normalized Newton.",
            "false",
            "projected mass-charge closure and orbital calibration are stronger than unprojected conservation",
        ),
        (
            "REF2373_3_public_claim",
            "2373 proves local GR/Newton.",
            "false",
            "2373 records a conditional source owner and residual row only",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, allowed, reason in rows
    ]


def next_target() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT2373_0_selected",
            "2374-Y5-R2FR-noHypermomentum-LeviCivita-source-connection-or-P4-row.md",
            "scripts/Y5_R2FR_noHypermomentum_LeviCivita_source_connection_or_P4_row_2374.py",
            "prove ordinary matter/source/readout do not vary an independent connection, or that the independent connection is Palatini/EH projectively silent for the source channel",
            "if not proved, emit first P4 torsion/nonmetricity/hypermomentum residual row as nonclaim",
        ),
        (
            "NEXT2373_1_parallel",
            "2374b-Y5-R2FR-boundary-improvement-flux-zero-or-envelope.md",
            "scripts/Y5_R2FR_boundary_improvement_flux_zero_or_envelope_2374b.py",
            "prove compact boundary/improvement flux is zero/projected silent under the Hamiltonian reference",
            "otherwise retain E_boundary and E_improvement finite envelopes",
        ),
        (
            "NEXT2373_2_parallel",
            "2374c-Y5-R2FR-readout-no-reentry-commutator-or-envelope.md",
            "scripts/Y5_R2FR_readout_no_reentry_commutator_or_envelope_2374c.py",
            "prove readout/domain/frame maps have no source-current codomain and no reentry commutator per arena",
            "otherwise retain E_readout finite envelope",
        ),
        (
            "NEXT2373_3_parallel",
            "2374d-Y5-R2FR-Hilbert-Noether-mass-projector-closure.md",
            "scripts/Y5_R2FR_Hilbert_Noether_mass_projector_closure_2374d.py",
            "close d(Pi_M J_H)=0 and GM calibration rather than relying on unprojected Ward conservation",
            "otherwise retain Delta_M_projected residual",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "next_file": file_name,
            "next_script": script_name,
            "success_condition": success,
            "fallback_condition": fallback,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, file_name, script_name, success, fallback in rows
    ]


def all_output_files() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_SOURCE_REGISTER.csv",
        "identity_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv",
        "nonhilbert_residual": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_NONHILBERT_RESIDUAL_ROW.csv",
        "trident_update": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_NONHILBERT_TRIDENT_UPDATE.csv",
        "gate_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_SOURCE_CHARGE_GATE_IMPACT.csv",
        "claim_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_CLAIM_GATES.csv",
        "refusal_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_REFUSAL_RUNNER.csv",
        "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_2373_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2373_VALIDATION.csv",
    }


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    sensitive = {
        "parent_signed",
        "theorem_zero",
        "numeric_prediction_present",
        "same_branch_locked",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
        "local_gr_claim",
        "epsilon_zero_active",
        "vector_complete",
    }
    positive_values = {"true", "pass", "passed", "ready", "yes", "1"}
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in sensitive and str(value).strip().lower() in positive_values:
                    return False
    return True


def validation_rows(outputs: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(outputs["source_register"])
    generated_paths = [path for key, path in outputs.items() if key != "validation"]
    parsed_ok = True
    for path in generated_paths:
        try:
            parsed_ok = parsed_ok and bool(read_csv(path))
        except Exception:
            parsed_ok = False

    identity = read_csv(outputs["identity_attempt"])
    residual = read_csv(outputs["nonhilbert_residual"])
    trident = read_csv(outputs["trident_update"])
    impact = read_csv(outputs["gate_impact"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])

    checks = [
        ("VAL2373_00_required_sources_exist", all(row["path_exists"] == "true" for row in source_rows), "all required source paths exist"),
        ("VAL2373_01_required_needles_found", all(row["needle_found"] == "true" for row in source_rows), "all source needles found"),
        ("VAL2373_02_outputs_exist", all(path.exists() for path in generated_paths), "all 2373 output files written"),
        ("VAL2373_03_csv_parse", parsed_ok, "all generated CSV files parse and contain rows"),
        (
            "VAL2373_04_conditional_owner",
            any(row["row_id"] == "NSCI2373_1_hilbert_owner" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in identity),
            "Hilbert/Noether source owner retained conditionally",
        ),
        (
            "VAL2373_05_identity_not_overclaimed",
            any(row["row_id"] == "NSCI2373_7_verdict" and row["status"].startswith("NOT_DERIVED") for row in identity),
            "no independent source charge not overclaimed",
        ),
        (
            "VAL2373_06_residual_row_exists",
            any(row["row_id"] == "NHR2373_0_total" and row["status"] == "CONTRACT_READY_VALUES_MISSING" for row in residual),
            "non-Hilbert residual total row exists",
        ),
        (
            "VAL2373_07_trident_primary_selected",
            any(row["row_id"] == "TRI2373_1_spin_torsion" and row["status"] == "SELECTED_NEXT_PRIMARY_GATE" for row in trident),
            "spin/torsion no-hypermomentum gate selected",
        ),
        (
            "VAL2373_08_local_gr_still_blocked",
            any(row["row_id"] == "SCI2373_4_local_GR_Newton" and row["claim_status"] == "blocked" for row in impact),
            "local GR/Newton remains blocked",
        ),
        (
            "VAL2373_09_claim_gates_block",
            any(row["row_id"] == "CG2373_5_local_GR_Newton" and row["gate_status"] == "FAIL" for row in gates),
            "local GR/Newton claim gate remains false",
        ),
        (
            "VAL2373_10_no_positive_claim_flags",
            check_no_positive_claim_flags(generated_paths),
            "all generated claim/readiness flags remain negative",
        ),
        (
            "VAL2373_11_formalization_untouched",
            not any(FORMALIZATION_WORKBENCH in path.parents for path in generated_paths),
            "generator writes only under post-checkpoint-work",
        ),
        (
            "VAL2373_12_next_selected",
            any(row["row_id"] == "NEXT2373_0_selected" and "noHypermomentum" in row["next_script"] for row in next_rows),
            "2374 no-hypermomentum/Levi-Civita target selected",
        ),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2373_OVERALL",
            "status": "PASS" if overall_ok else "FAIL",
            "detail": "2373 valid: Hilbert/Noether owner conditional, no independent source charge not derived, non-Hilbert residual retained, no-hypermomentum gate selected"
            if overall_ok
            else "2373 validation failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    identity = read_csv(outputs["identity_attempt"])
    residual = read_csv(outputs["nonhilbert_residual"])
    trident = read_csv(outputs["trident_update"])
    impact = read_csv(outputs["gate_impact"])
    gates = read_csv(outputs["claim_gates"])
    next_rows = read_csv(outputs["next_target"])
    generated = [rel(path) for path in outputs.values()]

    text = f"""# 2373 - Noether Source Charge Identity Or NonHilbert Residual Row

## Result

The Noether/source-charge route gives a real theorem, but not the whole prize.

The usable theorem is conditional:

`if a single observed matter action is fixed, T_H := delta S_m/delta e_obs is the active ordinary-matter source before readout, and Ward/Noether identities conserve it on shell`.

That kills post-variation source-current rescaling.  It does **not** prove that no independent gravitational source charge exists, because pre-action species weights remain conserved if they are legal, and non-Hilbert channels can still enter through spin/torsion, boundary/worldtube flux, readout reentry, or improvement/superpotential flux.

So the live source-side envelope is:

`||P_source[J_NH]|| <= E_spin + E_boundary + E_readout + E_improvement`.

The best next structural attack is no-hypermomentum / Levi-Civita source connection.  If ordinary matter/source/readout do not vary an independent connection, the spin/torsion head can collapse.  If not, the honest route is a P4 residual row.

## Noether Source-Charge Identity Attempt

{md_table(identity, ["row_id", "identity_piece", "status", "proof_or_obstruction"])}

## NonHilbert Residual Row

{md_table(residual, ["row_id", "quantity", "bound_form", "status", "next_input"])}

## NonHilbert Trident Update

{md_table(trident, ["row_id", "trident_head", "status", "fallback_or_effect"])}

## Source Charge Gate Impact

{md_table(impact, ["row_id", "gate", "claim_status", "still_missing"])}

## Claim Gates

{md_table(gates, ["row_id", "gate", "gate_status", "claim_effect"])}

## Next Target

{md_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition"])}

## Generated Files

"""
    text += "\n".join(f"- `{path}`" for path in generated)
    text += """

## Practical Status

This is a controlled failure in the good sense.  We did not prove the source-charge identity strongly enough to derive Minimal Universal Matter Coupling, but we did stop the leak from being vague.  The source side now has a named residual envelope and a first structural gate: no-hypermomentum / Levi-Civita source connection.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    outputs = all_output_files()
    write_csv(outputs["source_register"], source_register())
    write_csv(outputs["identity_attempt"], source_charge_identity_attempt())
    write_csv(outputs["nonhilbert_residual"], nonhilbert_residual_row())
    write_csv(outputs["trident_update"], trident_gate_update())
    write_csv(outputs["gate_impact"], source_charge_gate_impact())
    write_csv(outputs["claim_gates"], claim_gates())
    write_csv(outputs["refusal_runner"], refusal_runner())
    write_csv(outputs["next_target"], next_target())
    write_csv(outputs["validation"], validation_rows(outputs))
    write_doc(outputs)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {outputs['validation']}")


if __name__ == "__main__":
    main()
