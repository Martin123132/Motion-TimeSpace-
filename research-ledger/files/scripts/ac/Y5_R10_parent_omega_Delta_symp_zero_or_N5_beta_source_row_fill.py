from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "937-Y5-R10-parent-omega-Delta-symp-zero-or-N5-beta-source-row-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "936_doc",
            "path": "936-Y5-R10-Hamiltonian-PiM-integrability-or-N5-beta-coefficient-source-pack.md",
            "role": "immediate handoff selecting parent omega/Delta_symp gate",
            "needle": "937-Y5-R10-parent-omega-Delta-symp-zero-or-N5-beta-source-row-fill.md",
        },
        {
            "source_id": "936_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_936_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V936_12_validation_rows_ready",
        },
        {
            "source_id": "911_doc",
            "path": "911-Y5-R10-parent-symplectic-current-minimal-contract-or-Delta-symp-bound-input.md",
            "role": "sector-by-sector parent Theta/omega bill",
            "needle": "omega_total =",
        },
        {
            "source_id": "912_doc",
            "path": "912-Y5-R10-EH-core-symplectic-baseline-vs-extra-sector-omega-ledger.md",
            "role": "EH baseline versus active extra-sector omega",
            "needle": "integral_S i_tau omega_extra = 0",
        },
        {
            "source_id": "913_doc",
            "path": "913-Y5-R10-projector-omega-zero-route-or-Delta-symp-extra-source-row.md",
            "role": "projector omega zero route",
            "needle": "integral_S i_tau omega_projector = 0",
        },
        {
            "source_id": "914_doc",
            "path": "914-Y5-R10-topological-absolute-PiM-parent-clause-or-projector-source-bound-pack.md",
            "role": "topological absolute PiM parent clause attempt",
            "needle": "delta_g Pi_M = 0",
        },
        {
            "source_id": "915_doc",
            "path": "915-Y5-R10-Hilbert-topological-mass-current-equality-or-projector-bound-pack-fill.md",
            "role": "Hilbert/topological equality residual",
            "needle": "Delta_HT_current :=",
        },
        {
            "source_id": "916_doc",
            "path": "916-Y5-R10-parent-BF-mass-current-sector-or-Delta-HT-bound-input.md",
            "role": "BF mass-current candidate sector",
            "needle": "S_BF,M =",
        },
        {
            "source_id": "917_doc",
            "path": "917-Y5-R10-BF-mass-current-gauge-Noether-source-identity-or-DeltaHT-bound-fill.md",
            "role": "gauge/Noether equality route",
            "needle": "E_M := J_M^top - Pi_M J_H - dB_zero.",
        },
        {
            "source_id": "918_doc",
            "path": "918-Y5-R10-nonpropagating-mass-gauge-constraint-sector-or-DeltaHT-scorepack.md",
            "role": "coupling blocker",
            "needle": "The problem is the coupling",
        },
        {
            "source_id": "919_doc",
            "path": "919-Y5-R10-matter-current-silence-lemma-or-DeltaHT-bound-runner.md",
            "role": "matter-current silence theorem clauses",
            "needle": "off-shell parent identity",
        },
        {
            "source_id": "920_doc",
            "path": "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md",
            "role": "off-shell closure and holonomy audit",
            "needle": "d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M] J_H.",
        },
        {
            "source_id": "local_beta_bound",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "source-backed R4 beta observational envelope",
            "needle": "R4_beta",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def sector_omega_table() -> list[dict[str, str]]:
    specs = [
        (
            "OME937_0_EH_core",
            "EH metric/coframe core",
            "omega_EH",
            "zero for stationary/vacuum GR branch with fixed tau/reference and standard covariant phase-space charge",
            "conditional_baseline_only",
            "EH parent selection and full MTS equality not signed",
        ),
        (
            "OME937_1_matter_frame",
            "ordinary matter one-coframe",
            "omega_matter_frame",
            "zero in local vacuum exterior if matter has compact support and couples only to observed coframe",
            "open",
            "one-coframe/source support and same readout frame not parent-signed",
        ),
        (
            "OME937_2_projector_PiM",
            "Pi_M/projector/source-current selector",
            "omega_projector",
            "zero if Pi_M is absolute/Hamiltonian charge data and its variations are vertical gauge degeneracies",
            "open_primary",
            "delta_g Pi_M=0, [d,Pi_M]J_H=0, and source equality are not derived",
        ),
        (
            "OME937_3_BF_mass_gauge",
            "BF/topological mass-current candidate",
            "omega_BF",
            "bulk wedge sector can be metric-stress silent if topological and first-class",
            "candidate_only",
            "mass-gauge symmetry, equality constraint, source coupling silence, and level calibration are not derived",
        ),
        (
            "OME937_4_boundary_reference",
            "boundary/corner/reference",
            "omega_boundary + omega_corner",
            "zero if boundary class, reference, and compact flux are fixed/superselected",
            "open",
            "B_zero/no-flux/reference shift theorem missing",
        ),
        (
            "OME937_5_domain_selector",
            "domain/selector/homology",
            "omega_domain + omega_selector",
            "zero if domain selection is covariant, class-only, and not a dynamical readout mask",
            "open",
            "fixed local exterior/domain class and no preferred-boundary variation not parent-signed",
        ),
        (
            "OME937_6_bulk_X_memory",
            "bulk X/memory",
            "omega_X",
            "zero if no-hair/mass-gap removes compact exterior support or if source response is bounded",
            "open",
            "X theta/operator/no-hair and finite-range response not parent-derived here",
        ),
        (
            "OME937_7_source_normalization",
            "kappa/G_eff/M_eff/source normalization",
            "omega_source_norm",
            "zero if constants are superselected and Hamiltonian charge equals measured source mass",
            "open",
            "Delta_cal, tau frame, and measured-GM calibration remain missing",
        ),
        (
            "OME937_8_connection_torsion",
            "connection/torsion/nonmetricity",
            "omega_connection",
            "zero if connection variation is auxiliary and collapses to Levi-Civita in local branch",
            "open",
            "auxiliary connection/torsion no-hair condition not parent-signed in this gate",
        ),
    ]
    return [
        {
            "omega_id": omega_id,
            "sector": sector,
            "omega_piece": omega_piece,
            "zero_condition": zero_condition,
            "current_status": current_status,
            "blocker": blocker,
            "contributes_to_Delta_symp": flag(current_status != "conditional_baseline_only"),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for omega_id, sector, omega_piece, zero_condition, current_status, blocker in specs
    ]


def zero_proof_clauses() -> list[dict[str, str]]:
    specs = [
        (
            "DZ937_0_phase_space",
            "allowed local exterior phase space fixed",
            "delta[S2]=0, delta domain class=0, delta tau=0, delta H_ref=0",
            "prevents charge variation from being a moving-target/readout artifact",
            "not_parent_signed",
        ),
        (
            "DZ937_1_EH_integrability",
            "EH core integrability baseline",
            "int_S i_tau omega_EH=0 on stationary/vacuum branch with fixed reference",
            "recovers the usual GR Hamiltonian mass baseline",
            "conditional_baseline_only",
        ),
        (
            "DZ937_2_extra_vertical_degeneracy",
            "every extra sector is vertical gauge/topological or exact-flux",
            "i_tau omega_extra = d b_tau or 0, with int_S d b_tau=0",
            "would give Delta_symp_extra=0 without fitting a closure coefficient",
            "not_parent_signed",
        ),
        (
            "DZ937_3_projector_absolute_or_Hamiltonian",
            "Pi_M is absolute/Hamiltonian charge data",
            "delta_g Pi_M=0; [d,Pi_M]J_H=0; Pi_M^top=Pi_M^H+dB_zero",
            "kills the N5 projector-stress source at the root",
            "not_parent_signed",
        ),
        (
            "DZ937_4_source_current_offshell_closure",
            "projected source current closes off shell",
            "d(Pi_M J_H)=0 before using matter equations, or equals an owned first-class constraint",
            "makes mass-gauge coupling matter-silent instead of fifth-force-like",
            "not_parent_signed",
        ),
        (
            "DZ937_5_boundary_holonomy_silence",
            "boundary flux and local holonomy vanish",
            "int_boundary dB_zero=0 and flat A_M is exact on admissible local domain",
            "prevents hidden compact mass/source drift",
            "not_parent_signed",
        ),
        (
            "DZ937_6_same_source_calibration",
            "Hamiltonian/topological mass equals observed source mass",
            "M_H[S,tau]=M_eff[Pi_M J_H] with fixed G_eff and same worldtube/readout frame",
            "turns the charge theorem into Newtonian measured-GM source normalization",
            "not_parent_signed",
        ),
        (
            "DZ937_7_total_verdict",
            "Delta_symp zero theorem",
            "if DZ937_0 through DZ937_6 hold, then d alpha_tau=0 and Delta_symp_total=0",
            "precise theorem target now written; current corpus lacks multiple signatures",
            "conditional_theorem_not_current_claim",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "needed_statement": needed_statement,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "current_status": current_status,
            "parent_signed": "false" if current_status != "conditional_baseline_only" else "conditional",
            "zero_claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for clause_id, needed_statement, mathematical_form, why_needed, current_status in specs
    ]


def delta_symp_attempt() -> list[dict[str, str]]:
    specs = [
        (
            "DSA937_0_decomposition",
            "Delta_symp_total = Delta_EH + Delta_projector + Delta_BF + Delta_boundary + Delta_domain + Delta_X + Delta_source + Delta_connection",
            "exact bookkeeping identity",
            "keeps the obstruction from being hidden in a single symbol",
            "usable_nonclaim",
        ),
        (
            "DSA937_1_EH_piece",
            "Delta_EH = 0 under GR stationary/vacuum/fixed-reference assumptions",
            "conditional baseline",
            "this is comparison mathematics, not proof that MTS extra sectors vanish",
            "conditional_only",
        ),
        (
            "DSA937_2_extra_piece",
            "Delta_extra = sum_{non-EH} mass-normalized int_S i_tau omega_sector",
            "active obstruction",
            "all non-EH sectors must be shown vertical/topological/exact-flux or bounded",
            "not_zeroed",
        ),
        (
            "DSA937_3_coupling_piece",
            "Delta_coupling includes variation of A_M wedge Pi_M J_H and source-normalization charge map",
            "active obstruction",
            "off-shell d(Pi_M J_H)=0 and exact/zero-holonomy A_M are not parent-signed",
            "not_zeroed",
        ),
        (
            "DSA937_4_verdict",
            "Delta_symp_total cannot be set to zero from current evidence",
            "rejected_as_current_proof",
            "the right theorem is now explicit but unsigned; keep residual row live",
            "nonclaim_retained",
        ),
    ]
    return [
        {
            "attempt_id": attempt_id,
            "statement": statement,
            "status": status,
            "interpretation": interpretation,
            "verdict": verdict,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for attempt_id, statement, status, interpretation, verdict in specs
    ]


def beta_bound_row() -> dict[str, str]:
    rows = read_csv(LOCAL_BOUNDS)
    for row in rows:
        if row.get("row_id") == "R4_beta":
            return row
    return {}


def n5_beta_source_rows() -> list[dict[str, str]]:
    beta = beta_bound_row()
    beta_bound = beta.get("upper_bound", "")
    beta_source = beta.get("reference_path_or_url", "")
    beta_note = beta.get("reference_note", "")
    specs = [
        (
            "N5S937_0_R4_beta_observation",
            "beta_minus_one_bound",
            beta_bound,
            "dimensionless",
            beta_source,
            beta_note,
            "source_bound_loaded",
            "true",
            "false",
        ),
        (
            "N5S937_1_C_beta_N5",
            "C_beta_N5",
            "",
            "dimensionless",
            "MISSING_PARENT_PPN_PROJECTION_SOURCE",
            "second-order PPN projection of retained N5/Delta_symp vector",
            "missing_prediction_coefficient",
            "false",
            "false",
        ),
        (
            "N5S937_2_X_N5",
            "X_N5",
            "",
            "source_normalized_amplitude",
            "MISSING_SOURCE_NORMALIZED_N5_PROFILE",
            "source-normalized amplitude of retained projector/omega obstruction",
            "missing_prediction_amplitude",
            "false",
            "false",
        ),
        (
            "N5S937_3_beta_bound_formula",
            "K_BF_H_bound_from_beta",
            "|K_BF_H| <= 7.8e-05/(|C_beta_N5| X_N5)",
            "dimensionless_if_CX_dimensionless",
            "derived_from_R4_beta_row_plus_missing_CX_inputs",
            "usable only after C_beta_N5 and X_N5 are parent-derived or source-backed",
            "schema_ready_prediction_blocked",
            "false",
            "false",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "value_or_formula": value_or_formula,
            "units": units,
            "source_path_or_url": source_path_or_url,
            "note": note,
            "status": status,
            "source_bound_loaded": source_bound_loaded,
            "score_ready": score_ready,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for row_id, symbol, value_or_formula, units, source_path_or_url, note, status, source_bound_loaded, score_ready in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC937_0_Delta_symp_zero",
            "decision": "Delta_symp_zero_not_proved",
            "reason": "EH baseline can be made integrable, but omega_extra vertical degeneracy, source closure, boundary flux, and source calibration are unsigned",
            "consequence": "Pi_M^H remains promising but not parent-owned",
            "next_action": "attack vertical degeneracy of omega_extra",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC937_1_best_derivation_route",
            "decision": "vertical_gauge_degeneracy_is_best_next_route",
            "reason": "if every non-EH sector is a gauge/topological degeneracy of the presymplectic form, Delta_symp vanishes without empirical patching",
            "consequence": "derive i_tau omega_extra=d b_tau with zero compact flux, or retain bound inputs",
            "next_action": "938-Y5-R10-extra-omega-vertical-degeneracy-or-CbetaN5-source-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC937_2_beta_source_row",
            "decision": "R4_beta_bound_loaded_but_prediction_inputs_missing",
            "reason": "Will 2014 beta bound row is source-backed, but C_beta_N5 and X_N5 are absent",
            "consequence": "no N5 beta score, but the observation side of the row is now anchored",
            "next_action": "derive or source C_beta_N5 and X_N5 only if zero route fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE937_0_Delta_symp_zero",
            "claim": "Delta_symp_total=0",
            "blocker": "omega_extra vertical degeneracy, source closure, boundary flux, and calibration clauses unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE937_1_integrable_Htau",
            "claim": "H_tau is integrable for MTS local branch",
            "blocker": "d alpha_tau obstruction not zeroed for total parent omega",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE937_2_PiM_H_parent_owned",
            "claim": "Pi_M^H is parent-owned and replaces the projector mask",
            "blocker": "Hamiltonian charge map lacks source equality, topological equivalence, and measured-GM calibration",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE937_3_N5_beta_score",
            "claim": "N5 beta row is numeric/scoreable",
            "blocker": "C_beta_N5 and X_N5 are missing despite source-backed R4_beta bound",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE937_4_local_GR",
            "claim": "local GR/Newton/PPN branch is derived",
            "blocker": "integrability, source normalization, N5 projector stress, and beta readout remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "938-Y5-R10-extra-omega-vertical-degeneracy-or-CbetaN5-source-row.md",
            "objective": "prove each non-EH omega sector is a vertical gauge/topological degeneracy with zero compact flux, or fill C_beta_N5/X_N5 source rows",
            "include": "i_tau omega_extra=d b_tau conditions, sector-by-sector vertical generators, zero compact flux, coupling/off-shell closure handoff, fallback beta coefficient inputs",
            "exclude": "assuming Delta_symp=0, assuming projector stress zero, local-GR claim, beta score claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    attempt_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_936_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    sector_count_ok = len(sector_rows) == 9 and any(row["omega_id"] == "OME937_2_projector_PiM" for row in sector_rows)
    sector_nonclaim = all(row["valid_for_claim"] == "false" for row in sector_rows)
    total_theorem_conditional = any(row["clause_id"] == "DZ937_7_total_verdict" and row["current_status"] == "conditional_theorem_not_current_claim" for row in clause_rows)
    zero_claims_false = all(row["zero_claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in clause_rows)
    delta_rejected = any(row["attempt_id"] == "DSA937_4_verdict" and row["verdict"] == "nonclaim_retained" for row in attempt_rows)
    beta_observation_loaded = any(row["row_id"] == "N5S937_0_R4_beta_observation" and row["source_bound_loaded"] == "true" and row["value_or_formula"] == "7.8e-05" for row in beta_rows)
    beta_prediction_blocked = any(row["row_id"] == "N5S937_1_C_beta_N5" and row["score_ready"] == "false" for row in beta_rows) and any(row["row_id"] == "N5S937_2_X_N5" and row["score_ready"] == "false" for row in beta_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claim_gates_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("938-Y5-R10-extra-omega-vertical-degeneracy") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + sector_rows + clause_rows + attempt_rows + beta_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V937_0_sources_exist_and_needles", sources_ok, "all 937 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V937_1_prior_936_clean", prior_clean, "P8_Y5_BRR545_936_VALIDATION.csv clean")
    add("V937_2_sector_table_complete", sector_count_ok, "nine omega sectors recorded including projector/PiM")
    add("V937_3_sector_rows_nonclaim", sector_nonclaim, "sector omega rows remain nonclaim")
    add("V937_4_total_theorem_conditional", total_theorem_conditional, "Delta_symp zero theorem written only as conditional target")
    add("V937_5_zero_claims_false", zero_claims_false, "no zero-proof clause promoted")
    add("V937_6_Delta_symp_rejected_as_current_proof", delta_rejected, "Delta_symp_total=0 rejected as current proof and retained")
    add("V937_7_beta_observation_loaded", beta_observation_loaded, "source-backed R4 beta upper bound 7.8e-05 loaded")
    add("V937_8_beta_prediction_blocked", beta_prediction_blocked, "C_beta_N5 and X_N5 missing, so beta score blocked")
    add("V937_9_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V937_10_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V937_11_next_target_selected", next_selected, "938 extra-omega vertical degeneracy target selected")
    add("V937_12_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V937_13_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V937_14_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    attempt_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 937 - Y5/R10 Parent Omega Delta Symp Zero Or N5 Beta Source Row Fill

Generated: `{stamp()}`

Status: `Y5_R10_937_parent_omega_Delta_symp_zero_theorem_conditional_current_proof_rejected_R4_beta_source_loaded_nonclaim`

Claim ceiling: `Delta_symp_zero_contract_and_N5_beta_source_row_only_no_integrable_Htau_no_PiM_H_no_local_GR_pass`

## Result

The exact theorem target is now sharp:

```text
d alpha_tau = int_S i_tau omega_total + delta_tau/reference terms,
Delta_symp_total = mass-normalized int_S i_tau omega_total.
```

To prove `Delta_symp_total=0`, MTS needs all of this at once:

```text
int_S i_tau omega_EH = 0                    (GR baseline branch),
i_tau omega_extra = d b_tau or 0            (vertical/topological extra sectors),
int_S d b_tau = 0                           (zero compact flux),
delta tau = delta H_ref = 0                 (fixed generator/reference),
d(Pi_M J_H)=0 off shell or as an owned constraint,
M_H[S,tau] = M_eff[Pi_M J_H]                (same-source calibration).
```

That would make `Pi_M^H` a genuine parent charge and would kill the N5 projector-stress problem at the root.

But the current corpus does **not** sign the extra-sector vertical-degeneracy theorem, the off-shell projected-current closure, the zero-flux boundary/holonomy clause, or the measured-source calibration. So `Delta_symp_total=0` is **not proved** here.

What did improve: the proof target is no longer foggy. The next best derivation is to prove:

```text
i_tau omega_extra = d b_tau,     int_S d b_tau = 0,
```

sector by sector. If that fails, the retained beta branch now has its observational side loaded from the R4 beta row, but prediction inputs `C_beta_N5` and `X_N5` are still missing.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Sector Omega Table

{md_table(sector_rows, ["omega_id", "sector", "omega_piece", "zero_condition", "current_status", "blocker"])}

## Delta Symp Zero-Proof Clauses

{md_table(clause_rows, ["clause_id", "needed_statement", "mathematical_form", "current_status", "parent_signed", "zero_claim_allowed"])}

## Delta Symp Attempt

{md_table(attempt_rows, ["attempt_id", "statement", "status", "interpretation", "verdict"])}

## N5 Beta Source Row Fill

{md_table(beta_rows, ["row_id", "symbol", "value_or_formula", "source_path_or_url", "status", "score_ready", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def ensure_csv_roundtrip(paths: list[Path]) -> None:
    for path in paths:
        rows = read_csv(path)
        if rows and any(None in row for row in rows):
            raise SystemExit(f"malformed CSV row in {path}")


def main() -> None:
    sources = source_register()
    sector_rows = sector_omega_table()
    clause_rows = zero_proof_clauses()
    attempt_rows = delta_symp_attempt()
    beta_rows = n5_beta_source_rows()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, sector_rows, clause_rows, attempt_rows, beta_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_937_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_937_SECTOR_OMEGA_TABLE.csv",
            sector_rows,
            ["omega_id", "sector", "omega_piece", "zero_condition", "current_status", "blocker", "contributes_to_Delta_symp", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_937_DELTA_SYMP_ZERO_PROOF_CLAUSES.csv",
            clause_rows,
            ["clause_id", "needed_statement", "mathematical_form", "why_needed", "current_status", "parent_signed", "zero_claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_937_DELTA_SYMP_ATTEMPT.csv",
            attempt_rows,
            ["attempt_id", "statement", "status", "interpretation", "verdict", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_937_N5_BETA_SOURCE_ROW_FILL.csv",
            beta_rows,
            ["row_id", "symbol", "value_or_formula", "units", "source_path_or_url", "note", "status", "source_bound_loaded", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_937_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_937_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_937_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_937_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, sector_rows, clause_rows, attempt_rows, beta_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_937_parent_omega_Delta_symp_zero_theorem_conditional_current_proof_rejected_R4_beta_source_loaded_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 938-Y5-R10-extra-omega-vertical-degeneracy-or-CbetaN5-source-row.md")


if __name__ == "__main__":
    main()
