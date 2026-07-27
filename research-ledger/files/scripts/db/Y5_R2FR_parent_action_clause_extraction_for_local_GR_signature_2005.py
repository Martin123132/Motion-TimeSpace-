from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2005-Y5-R2FR-parent-action-clause-extraction-for-local-GR-signature.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
    except csv.Error:
        return False
    return True


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2005_00_2004_handoff",
            "2004-Y5-R2FR-parent-Hilbert-source-signature-or-finite-nonmetric-coefficient-ledger.md",
            ["SIG2004_0_single_observed_metric", "NEXT2004_0_2005", "VAL2004_OVERALL"],
            "2004 local-GR/Newton/WEP conditional chain and clause audit handoff.",
        ),
        (
            "SRC2005_01_1030_spm",
            "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            ["SPM1030_0_public_metric_object", "SPM1030_6_contract_verdict", "SPD1030_6_verdict"],
            "single-public-metric and no-shadow-frame parent-action contract.",
        ),
        (
            "SRC2005_02_1065_no_source_slot",
            "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
            ["PGG1065_1_no_inert_species_scalar", "PGG1065_5_verdict", "CG1065_1_theorem_zero_Delta_w"],
            "no-source-only species slot grammar and WEP weight gate.",
        ),
        (
            "SRC2005_03_1066_source_scalar",
            "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
            ["SSE1066_5_verdict", "OLT1066_4_inert_source_scalar", "FMQ1066_4_verdict"],
            "source-scalar exclusion and action-scale/measure obstruction.",
        ),
        (
            "SRC2005_04_1078_owner_stack",
            "1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md",
            ["OL1078_4_verdict", "AM1078_4_verdict", "CO1078_4_verdict"],
            "object-language, action-measure, and current-owner proof stack.",
        ),
        (
            "SRC2005_05_1090_MOMS",
            "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
            ["SYN1090_8_verdict", "AX1090_4_variation_domain_order", "CLOS1090_0_MOMS"],
            "MOMS synthesis and missing-axiom ledger.",
        ),
        (
            "SRC2005_06_1937_hilbert",
            "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
            ["ACT1937_1_minimal_matter_action", "HST1937_3_verdict", "NMC1937_0_species_source_weight"],
            "candidate Hilbert-source matter action and nonmetric source ledger.",
        ),
        (
            "SRC2005_07_1938_ward_newton",
            "1938-Y5-R2FR-Bianchi-Ward-conservation-and-Newtonian-limit-of-candidate-Hilbert-action.md",
            ["WB1938_0_matter_ward_identity", "NL1938_1_EH_to_Poisson", "GOB1938_0_operator_owner"],
            "Ward/Bianchi conservation and conditional Newtonian source limit.",
        ),
        (
            "SRC2005_08_1939_operator",
            "1939-Y5-R2FR-parent-gravity-operator-EH-or-R11-residual-Newtonian-law.md",
            ["EH1939_2_Poisson", "R111939_0_field_equation", "CG1939_1_parent_EH_derivation"],
            "EH/kappa candidate and explicit R11 residual slot.",
        ),
        (
            "SRC2005_09_1940_lovelock",
            "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md",
            ["LOV1940_1_metric_only", "EHU1940_2_local_GR_branch", "CG1940_2_parent_assumptions"],
            "Lovelock/EH uniqueness assumptions and residual branch.",
        ),
        (
            "SRC2005_10_1956_variation",
            "1956-Y5-R2FR-parent-action-variation-signature-for-local-EH-map.md",
            ["SIG1956_1_EH_operator", "SIG1956_4_extra_sector_silence", "CG1956_6_local_GR_Newton"],
            "local EH same-source variation signature audit.",
        ),
        (
            "SRC2005_11_1959_bypass",
            "1959-Y5-R2FR-torsion-boundary-readout-current-silence-or-envelope.md",
            ["SIL1959_1_torsion_Levi_Civita_route", "SIL1959_6_verdict", "ENV1959_0_combined_nonHilbert"],
            "torsion/boundary/readout bypass-current silence or envelope.",
        ),
        (
            "SRC2005_12_1960_connection",
            "1960-Y5-R2FR-Levi-Civita-no-hypermomentum-proof-or-P4-current-envelope.md",
            ["LC1960_1_metric_only_parent_route", "LC1960_6_verdict", "P4C1960_5_hypermomentum"],
            "Levi-Civita/no-hypermomentum fork and P4 fallback.",
        ),
        (
            "SRC2005_13_1962_ownership",
            "1962-Y5-R2FR-parent-q-metric-matter-ownership-or-P4-fallback.md",
            ["OWN1962_2_owned_coframe_branch", "OWN1962_5_no_Gamma_variation", "EHI1962_4_best_route"],
            "owned-coframe/q-metric-matter ownership route.",
        ),
        (
            "SRC2005_14_1963_action",
            "1963-Y5-R2FR-minimal-owned-coframe-parent-action-or-P4-hypermomentum-row.md",
            ["ACT1963_0_target", "NGT1963_0_theorem", "CG1963_3_EH_operator"],
            "minimal owned-coframe parent action skeleton and no-Gamma theorem.",
        ),
        (
            "SRC2005_15_1964_legitimacy",
            "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md",
            ["LEG1964_3_MTS_readout_contract", "EH2_1964_2_central_blocker", "R11X1964_0_R2_fR_scalar"],
            "owned-coframe legitimacy and EH second-order/R11 fork.",
        ),
        (
            "SRC2005_16_1983_review",
            "1983-Y5-R2FR-top-parent-action-candidate-review.md",
            ["PROM1983_0_promoted_sources", "DEC1983_2_best_next", "VAL1983_OVERALL"],
            "wider-corpus parent action candidate review rejecting shortcut promotions.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2005 parent-action clause extraction for local-GR signature",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def clause_extraction_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SIG2004_0_single_observed_metric",
            "single observed metric/coframe for ordinary matter",
            "Parent must own one local observed coframe/metric object used by rods, clocks, photons, matter, source variation, and readout.",
            "1963 writes a minimal owned-coframe branch; 1964 finds prior observer/readout support; 1030 has the terminal-public-metric contract.",
            "ACT1963_1_variable_list; LEG1964_3_MTS_readout_contract; SPM1030_0_public_metric_object",
            "CANDIDATE_ACTION_BRANCH_WRITTEN_NOT_CANONICAL",
            "missing parent map e_obs=E[q(Phi_MTS)] and canonical adoption of the owned-coframe branch",
            "frame_leak_or_shadow_metric_coefficient",
            "derive the E[q(Phi_MTS)] coframe readout map or demote ACT1963 to closure-only",
        ),
        (
            "SIG2004_1_hilbert_source_owner",
            "source is Hilbert stress-energy of same matter action",
            "The active gravitational source must be the variation of the same matter action that controls inertial dynamics.",
            "1937/1938 prove the Hilbert-source theorem conditionally; 1956 keeps source-map/current-owner clauses unsigned.",
            "ACT1937_3_source_definition; HST1937_0_variational_source_owner; SIG1956_2_total_Hilbert_source",
            "EXACT_CONDITIONAL_IF_MATTER_FUNCTOR_SIGNED",
            "source-functor domain, current owner, and variation-before-readout are not parent-signed",
            "DeltaT_nonHilbert_l2_or_source_current_residual",
            "sign the matter functor/current owner or retain source-current residual envelopes",
        ),
        (
            "SIG2004_2_no_species_prefactor",
            "no independent w_A/material source prefactor",
            "No source-only species scalar may multiply active gravitational source strength after matter variation.",
            "1065/1066 isolate the no-source-slot theorem; 1078 shows object-language, measure, and current-owner proofs remain unsigned.",
            "PGG1065_1_no_inert_species_scalar; SSE1066_5_verdict; OL1078_4_verdict; AM1078_4_verdict; CO1078_4_verdict",
            "EXACT_IF_OBJECT_LANGUAGE_MEASURE_CURRENT_OWNER_SIGNED",
            "disconnected species constants and action-scale normalization counterexamples survive without a parent grammar",
            "DeltaW_TiPt_times_tau_WEP",
            "derive parent object-language/action-measure/current owner or source finite DeltaW and tau_WEP rows",
        ),
        (
            "SIG2004_3_binding_energy_included",
            "binding/rest/internal energies included in same source functional",
            "All rest, kinetic, binding, internal, field, and material energies must enter the same Hilbert source functional.",
            "1937 writes total Hilbert source route; 1956 marks same-source normalization as unsigned; 2004 keeps binding anomaly fallback active.",
            "ACT1937_1_minimal_matter_action; SIG1956_3_same_source_normalization; NMC2004_2_binding_anomaly",
            "CONTRACT_PRESENT_NOT_INDEPENDENTLY_SIGNED",
            "material/source-worldtube mapping and current normalization are not derived through detector/readout order",
            "b_bind_A_or_material_source_anomaly",
            "derive same-source material/worldtube map or keep binding anomaly as finite coefficient",
        ),
        (
            "SIG2004_4_EH_operator_or_residual_zero",
            "EH/Lovelock local operator or bounded residual",
            "The local exterior operator must reduce to EH+Lambda with kappa normalization, or all non-EH/R11 operators must be executable residuals.",
            "1939/1940 give EH/kappa and Lovelock conditional theorem; 1964 says R2/fR and extra-sector terms remain legal.",
            "EH1939_2_Poisson; EHU1940_2_local_GR_branch; EH2_1964_2_central_blocker; R11X1964_0_R2_fR_scalar",
            "EH_CONDITIONAL_R11_ACTIVE",
            "second-order/no-extra-sector/local-exterior assumptions and R11 residual silence are not parent-signed",
            "Xi_R11_R2_fR_Ricci2_Weyl2_nonlocal_residual_vector",
            "prove second-order/no-extra-sector selection or fill executable R11/R2-fR bound rows",
        ),
        (
            "SIG2004_5_Levi_Civita_connection",
            "observed connection is Levi-Civita/no hypermomentum",
            "The observed local connection must be induced by the observed coframe/metric, with no independent hypermomentum source.",
            "1962/1963 give a clean no-Gamma theorem inside the owned-coframe branch; 1960 keeps the full framework unsigned.",
            "LC1960_6_verdict; OWN1962_5_no_Gamma_variation; NGT1963_0_theorem; CG1964_2_LC_branch",
            "NO_GAMMA_THEOREM_VALID_IN_BRANCH_NOT_CANONICAL",
            "owned-coframe branch is not canonicalized and independent-connection alternatives are not globally excluded",
            "P4_hypermomentum_torsion_nonmetricity_residual",
            "canonicalize ACT1963 or source P4 hypermomentum/torsion/nonmetricity rows",
        ),
        (
            "SIG2004_6_readout_preservation",
            "readout/boundary maps do not reintroduce species labels",
            "Projection, calibration, boundary, and detector readout must not reintroduce species, representative, source, or connection markers.",
            "1030/1959/1962 identify no-shadow/no-readout-reentry routes; none are parent-signed through detector order.",
            "SPM1030_5_hidden_current_silence; SIL1959_4_readout_reentry_route; OWN1962_6_chain_rule_zero",
            "QUOTIENT_READOUT_CONTRACT_PRESENT_NOT_SIGNED",
            "q descent, boundary flux, detector readout order, and marker/no-spurion rules remain unsigned",
            "readout_weight_or_boundary_marker_current",
            "derive readout-after-variation/no-marker theorem or retain readout/boundary envelope",
        ),
        (
            "SIG2004_7_residual_silence",
            "extra sectors have zero/common-mode/bounded local residuals",
            "Motion/time/domain/memory/projector/boundary/connection sectors must be zero, common-mode, topological, no-haired, or numerically bounded locally.",
            "1956/1959/1964/1983 reject shortcut silence; they make the residual families explicit instead.",
            "SIG1956_4_extra_sector_silence; SIL1959_6_verdict; EH2_1964_3_no_extra_sector; PROM1983_0_promoted_sources",
            "UNSIGNED_OR_BOUND_MISSING",
            "extra-sector no-hair/topological/no-flux theorems and executable residual amplitudes are missing",
            "extra_sector_l2_boundary_R11_P4_residual_vector",
            "prove local no-extra-sector silence or build source-backed residual envelopes",
        ),
    ]
    rows: list[dict[str, object]] = []
    for clause_id, name, required, extracted, anchors, status, failure, fallback, next_action in specs:
        row = base_row()
        row.update(
            {
                "clause_id": clause_id,
                "clause_name": name,
                "required_parent_contract": required,
                "extracted_corpus_clause": extracted,
                "source_anchors": anchors,
                "extracted_status": status,
                "parent_signed": "false",
                "claim_status": "NONCLAIM_CONDITIONAL_OR_BLOCKED",
                "failure_mode": failure,
                "finite_fallback": fallback,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def signature_decision_rows(clauses: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for clause in clauses:
        status = str(clause["extracted_status"])
        if "EXACT_CONDITIONAL" in status or "NO_GAMMA_THEOREM" in status:
            verdict = "MATHEMATICALLY_USEFUL_CONDITIONAL"
        elif "CANDIDATE" in status or "CONTRACT" in status:
            verdict = "ACTION_CONTRACT_AVAILABLE_UNSIGNED"
        else:
            verdict = "ACTIVE_BLOCKER_OR_BOUND_ROUTE"
        row = base_row()
        row.update(
            {
                "decision_id": "DECISION_" + str(clause["clause_id"]),
                "clause_id": clause["clause_id"],
                "parent_signed": clause["parent_signed"],
                "decision": verdict,
                "promote_to_local_GR": "false",
                "reason": clause["failure_mode"],
                "required_before_claim": clause["next_action"],
            }
        )
        rows.append(row)
    return rows


def signed_subset_theorem_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SSET2005_0_WEP_source_side",
            "SIG2004_0;SIG2004_1;SIG2004_2;SIG2004_3;SIG2004_6",
            "If the observed coframe, Hilbert source, no-species-prefactor, binding inclusion, and readout-preservation clauses are parent-signed, the 2003 eta map gives eta_AB=0 for source-weight WEP channels.",
            "EXACT_CONDITIONAL_SUBSET",
            "not active because all antecedent signatures remain unsigned",
        ),
        (
            "SSET2005_1_LC_connection",
            "SIG2004_0;SIG2004_5;SIG2004_6",
            "Inside the owned-coframe branch, absence of an independent Gamma variable makes observed hypermomentum zero and the connection Levi-Civita by variable signature.",
            "VALID_IN_ACT1963_BRANCH",
            "not active because ACT1963 is not canonicalized and E[q(Phi_MTS)] is missing",
        ),
        (
            "SSET2005_2_EH_Newton",
            "SIG2004_0;SIG2004_1;SIG2004_4;SIG2004_5;SIG2004_7",
            "If the local exterior is 4D, metric/coframe-only, Levi-Civita, second-order, divergence-free, and residual-silent, EH+Lambda with kappa gives Poisson/Newton conditionally.",
            "STANDARD_CONDITIONAL_GR_BRIDGE",
            "not active because second-order/no-extra-sector and residual-silence clauses are unsigned",
        ),
        (
            "SSET2005_3_full_local_GR",
            "SIG2004_0;SIG2004_1;SIG2004_2;SIG2004_3;SIG2004_4;SIG2004_5;SIG2004_6;SIG2004_7",
            "All eight parent clauses together would turn the 2004 proof chain into a local GR/Newton/WEP reduction theorem.",
            "TARGET_THEOREM_SHARP",
            "not active; this is the exact contract a future parent action must satisfy",
        ),
    ]
    rows: list[dict[str, object]] = []
    for subset_id, clauses, theorem, status, blocker in specs:
        row = base_row()
        row.update(
            {
                "subset_id": subset_id,
                "clause_ids": clauses,
                "conditional_theorem": theorem,
                "status": status,
                "parent_signed": "false",
                "blocker": blocker,
            }
        )
        rows.append(row)
    return rows


def finite_fallback_rows() -> list[dict[str, object]]:
    specs = [
        ("FB2005_0_frame_leak", "SIG2004_0", "c_g_or_shadow_frame", "non-public metric/coframe or shadow-frame coupling", "coefficient; units; source path; R10/PPN/clock/orbit projection", "MISSING_THEOREM_ZERO_OR_NUMERIC_BOUND"),
        ("FB2005_1_nonHilbert_source", "SIG2004_1", "DeltaT_nonHilbert_l2", "non-Hilbert source current in local source map", "current norm; projection kernel; arena readout; source path", "MISSING_SOURCE_CURRENT_ENVELOPE"),
        ("FB2005_2_species_weight", "SIG2004_2", "DeltaW_TiPt*tau_WEP", "material/source prefactor WEP product", "DeltaW_TiPt; tau_WEP; MICROSCOPE readout convention; source path", "MISSING_DELTAW_OR_TAU"),
        ("FB2005_3_binding_anomaly", "SIG2004_3", "b_bind_A", "binding/internal energy source anomaly", "material response map; energy convention; bound path", "MISSING_MATERIAL_SOURCE_MAP"),
        ("FB2005_4_R11_operator", "SIG2004_4", "Xi_R11", "non-EH local weak-field source residual", "operator coefficient; divergence law; weak-field map; PPN/R10 bound", "MISSING_EXECUTABLE_R11_ROW"),
        ("FB2005_5_R2_fR", "SIG2004_4", "c_R2_or_fRR", "higher-curvature scalar mode residual", "mass/range; alpha(lambda); gamma/beta projection; source path", "MISSING_R2FR_ZERO_OR_BOUND"),
        ("FB2005_6_P4_connection", "SIG2004_5", "Delta_lambda_mu_nu", "hypermomentum/torsion/nonmetricity connection current", "coupling; units; source species; clock/light/orbit projection", "MISSING_P4_HYPERMOMENTUM_BOUND"),
        ("FB2005_7_readout_marker", "SIG2004_6", "r_A_or_marker_current", "readout/species/representative marker re-entry", "readout kernel; marker coefficient; material pair; source path", "MISSING_READOUT_NO_REENTRY_OR_BOUND"),
        ("FB2005_8_extra_sector_l2", "SIG2004_7", "R_extra_l2", "extra motion/time/domain/memory/projector local l=2 residual", "sector coefficient; no-hair status; projection norm; source path", "MISSING_EXTRA_SECTOR_SILENCE_OR_BOUND"),
        ("FB2005_9_boundary_flux", "SIG2004_7", "Omega_boundary_extra_l2", "boundary/symplectic/improvement l=2 residual", "boundary term; flux norm; W_STF/K2 projection; source path", "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND"),
    ]
    rows: list[dict[str, object]] = []
    for fallback_id, clause_id, symbol, meaning, required_inputs, status in specs:
        row = base_row()
        row.update(
            {
                "fallback_id": fallback_id,
                "linked_clause": clause_id,
                "symbol": symbol,
                "meaning": meaning,
                "required_inputs": required_inputs,
                "status": status,
                "numeric_value": "MISSING",
                "units": "MISSING",
                "source_path": "MISSING",
                "valid_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows(clauses: list[dict[str, object]], fallbacks: list[dict[str, object]]) -> list[dict[str, object]]:
    all_signed = all(str(row.get("parent_signed", "")).lower() == "true" for row in clauses)
    any_fallback_valid = any(str(row.get("valid_for_claim", "")).lower() == "true" for row in fallbacks)
    specs = [
        ("CG2005_0_clause_extraction", "all 2004 parent-signature clauses represented", "PASS_NONCLAIM", "extraction is complete but not a claim"),
        ("CG2005_1_all_parent_signed", "all eight local-GR clauses are parent-signed", "FAIL_BLOCKED" if not all_signed else "PASS", "no clause is parent-signed as a full MTS theorem yet"),
        ("CG2005_2_finite_residual_route", "fallback residual rows are numeric/source-backed", "FAIL_BLOCKED" if not any_fallback_valid else "PASS_NONCLAIM", "fallback rows remain placeholders, not scoreable predictions"),
        ("CG2005_3_local_GR_Newton_WEP", "MTS derives local GR/Newton/WEP", "FAIL_BLOCKED", "requires either all parent clauses signed or bounded residual envelope"),
        ("CG2005_4_public_claim", "2005 supports a public local-GR claim", "FAIL_BLOCKED", "private clause extraction only"),
        ("CG2005_5_next_leap", "next target is not another rescan", "PASS_NONCLAIM", "derive E[q(Phi_MTS)] or demote owned-coframe route to explicit closure"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, gate, status, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "status": status,
                "reason": reason,
                "passed_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def decision_ledger_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2005_0_not_circling",
            "The project has moved from vague suppression/plateau language to a concrete parent-action clause contract.",
            "ACT1963 provides a real owned-coframe branch and NGT1963 gives a conditional no-Gamma theorem; 2005 extracts exactly what remains unsigned.",
            "stop rescanning generic parent-action hits; attack the missing parent map and second-order/R11 fork",
        ),
        (
            "DEC2005_1_best_current_route",
            "The least-scrutinizable theorem route is owned coframe -> universal matter functor -> no independent Gamma -> EH second-order/no-extra-sector selection.",
            "This avoids smuggling a plateau axiom and turns LC/no-hypermomentum into variable absence, but still needs MTS legitimacy and EH/R11 closure.",
            "derive e_obs=E[q(Phi_MTS)] first, then decide R2/fR/R11 zero or executable bound rows",
        ),
        (
            "DEC2005_2_claim_discipline",
            "No local GR/Newton/WEP claim is allowed from the conditional chain alone.",
            "Every extracted clause is either candidate, exact-if-signed, or blocked; no finite fallback row is numeric/source-backed.",
            "keep all rows private/nonclaim until parent signatures or residual envelopes are live",
        ),
        (
            "DEC2005_3_project_health",
            "This is not grim, but it is not finished: the branch now has a clean route and a hard blocker.",
            "The hard blocker is specific: parent-owned coframe legitimacy plus second-order/no-extra-sector selection, not galaxy data or WEP toy rows.",
            "try a constructive derivation before fallback acquisition",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, verdict, rationale, next_action in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "verdict": verdict,
                "rationale": rationale,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2005_0_2006",
            "selected": "true",
            "next_doc": "2006-Y5-R2FR-parent-EqPhi-coframe-readout-map-or-owned-coframe-closure-demotion.md",
            "next_script": "scripts/Y5_R2FR_parent_EqPhi_coframe_readout_map_or_owned_coframe_closure_demotion_2006.py",
            "objective": "derive the parent map e_obs=E[q(Phi_MTS)] that legitimizes the owned-coframe branch; if it fails, demote ACT1963 to explicit closure and route local-GR tests through R11/P4/source residual rows",
            "include": "MTS flow/readout variables; q map; coframe nondegeneracy; Lorentz gauge equivalence; universal matter functor; no-Gamma theorem reuse; R2/fR fork awareness",
            "exclude": "claiming local GR; re-running galaxy/cosmology; inventing numeric residual coefficients; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2005_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    expected = {
        "SIG2004_0_single_observed_metric",
        "SIG2004_1_hilbert_source_owner",
        "SIG2004_2_no_species_prefactor",
        "SIG2004_3_binding_energy_included",
        "SIG2004_4_EH_operator_or_residual_zero",
        "SIG2004_5_Levi_Civita_connection",
        "SIG2004_6_readout_preservation",
        "SIG2004_7_residual_silence",
    }
    found = {str(row.get("clause_id", "")) for row in clauses}
    checks = [
        (
            "VAL2005_00_sources",
            all(str(row.get("status")) == "EXISTS_NEEDLES_CONFIRMED" for row in sources),
            "all cited source paths exist and needles are found",
        ),
        (
            "VAL2005_01_clause_coverage",
            expected == found,
            "all eight 2004 signature clauses are represented exactly once",
        ),
        (
            "VAL2005_02_no_false_parent_signing",
            all(str(row.get("parent_signed", "")).lower() == "false" for row in clauses),
            "no extracted clause is falsely promoted to parent-signed",
        ),
        (
            "VAL2005_03_fallbacks_nonclaim",
            all(str(row.get("valid_for_claim", "")).lower() == "false" and str(row.get("numeric_value")) == "MISSING" for row in fallbacks),
            "all finite fallback rows remain nonclaim placeholders",
        ),
        (
            "VAL2005_04_claim_gates_blocked",
            all(str(row.get("passed_for_claim", "")).lower() == "false" for row in claim_gates),
            "local GR/Newton/WEP/public claim gates remain blocked",
        ),
        (
            "VAL2005_05_csv_parse",
            all(path.exists() and csv_rows_parse(path) for path in output_paths),
            "all generated CSV outputs parse cleanly",
        ),
        (
            "VAL2005_06_branch_copies",
            all(path.exists() for path in branch_paths),
            "branch-copy CSVs exist",
        ),
        (
            "VAL2005_07_no_formalization_edits",
            count_formalization_modified_since_start() == 0,
            "formalization-workbench modified-file count remains 0 for this run",
        ),
        (
            "VAL2005_08_output_scope",
            all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]),
            "all outputs are under post-checkpoint-work",
        ),
    ]
    rows: list[dict[str, object]] = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
        rows.append(row)
    overall = all(row["status"] == "PASS" for row in rows)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2005_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2005 parent-action clause extraction for local-GR signature",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    clauses: list[dict[str, object]],
    decisions: list[dict[str, object]],
    subsets: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    ledger: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2005 Y5 R2FR: Parent Action Clause Extraction For Local GR Signature

Private checkpoint. This extracts the actual current-corpus clauses that would have to sign the 2004 local GR/Newton/WEP conditional chain.

## Current Verdict

The good news: the route is no longer vague. The strongest branch is now explicit: parent-owned coframe/readout map, universal matter functor, no independent observed connection, Hilbert source, and EH/second-order local exterior.

The hard limit: none of the eight 2004 parent-signature clauses is fully parent-signed in the current corpus. The owned-coframe/no-Gamma branch is the best leap so far, but it still needs `e_obs=E[q(Phi_MTS)]` and EH/R11 closure before it can be called a derived local-GR reduction.

No GitHub action, no formalization-workbench edits, and no local-GR/Newton/WEP public claim follows from 2005.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## Clause Extraction Ledger
{md_table(clauses, ["clause_id", "clause_name", "extracted_status", "parent_signed", "failure_mode", "finite_fallback", "next_action"])}

## Signature Decision Matrix
{md_table(decisions, ["decision_id", "clause_id", "decision", "promote_to_local_GR", "required_before_claim"])}

## Signed Subset Theorems
{md_table(subsets, ["subset_id", "clause_ids", "conditional_theorem", "status", "blocker"])}

## Finite Fallback Ledger
{md_table(fallbacks, ["fallback_id", "linked_clause", "symbol", "status", "required_inputs", "valid_for_claim"])}

## Claim Gates
{md_table(claim_gates, ["gate_id", "gate", "status", "reason", "passed_for_claim"])}

## Decision Ledger
{md_table(ledger, ["decision_id", "verdict", "rationale", "next_action"])}

## Branch Copies
{md_table(branch_copies, ["copy_id", "copy_path", "exists", "note"])}

## Next Target
{md_table(next_target, ["target_id", "next_doc", "objective", "include", "exclude"])}

## Validation
{md_table(validation, ["check_id", "status", "detail"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    clauses = clause_extraction_rows()
    decisions = signature_decision_rows(clauses)
    subsets = signed_subset_theorem_rows()
    fallbacks = finite_fallback_rows()
    claim_gates = claim_gate_rows(clauses, fallbacks)
    ledger = decision_ledger_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2005_SOURCE_REGISTER.csv",
        "clauses": OUT / "P8_Y5_PARENT_QLOC_2005_CLAUSE_EXTRACTION_LEDGER.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2005_SIGNATURE_DECISION_MATRIX.csv",
        "subsets": OUT / "P8_Y5_PARENT_QLOC_2005_SIGNED_SUBSET_THEOREM.csv",
        "fallbacks": OUT / "P8_Y5_PARENT_QLOC_2005_FINITE_FALLBACK_LEDGER.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2005_CLAIM_GATE.csv",
        "ledger": OUT / "P8_Y5_PARENT_QLOC_2005_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2005_NEXT_TARGET.csv",
    }

    write_csv(output_map["sources"], sources)
    write_csv(output_map["clauses"], clauses)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["subsets"], subsets)
    write_csv(output_map["fallbacks"], fallbacks)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["ledger"], ledger)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "PARENT_ACTION_CLAUSE_EXTRACTION_2005_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2005_LOCAL_GR_SIGNATURE_DECISION_NONCLAIM.csv",
        QUEUE / "JR2005_PARENT_CLAUSE_OR_FINITE_RESIDUAL_QUEUE.csv",
    ]
    branch_paths[0].parent.mkdir(parents=True, exist_ok=True)
    branch_paths[1].parent.mkdir(parents=True, exist_ok=True)
    branch_paths[2].parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["clauses"], branch_paths[0])
    shutil.copyfile(output_map["decisions"], branch_paths[1])
    shutil.copyfile(output_map["fallbacks"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "parent-action clause extraction nonclaim copy",
            "local-GR signature decision nonclaim copy",
            "finite residual fallback queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2005_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, clauses, fallbacks, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2005_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, clauses, decisions, subsets, fallbacks, claim_gates, ledger, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2005_OVERALL"][0]["status"]
    print(f"VAL2005_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
