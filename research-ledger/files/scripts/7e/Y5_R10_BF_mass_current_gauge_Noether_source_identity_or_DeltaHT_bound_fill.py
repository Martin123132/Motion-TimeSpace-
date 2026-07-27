from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_917_BF_mass_current_gauge_Noether_identity_attempted_not_parent_derived_DeltaHT_bound_fill_retained_nonclaim"
CLAIM_CEILING = "BF_mass_current_gauge_Noether_identity_attempt_only_no_BF_Hilbert_equality_no_closed_PiM_flux_no_Newton_PPN_or_local_GR_claim"
DOC_NAME = "917-Y5-R10-BF-mass-current-gauge-Noether-source-identity-or-DeltaHT-bound-fill.md"
NEXT_TARGET = "918-Y5-R10-nonpropagating-mass-gauge-constraint-sector-or-DeltaHT-scorepack.md"

SOURCE_SPECS = [
    {
        "source_id": "916_doc",
        "path": ROOT / "916-Y5-R10-parent-BF-mass-current-sector-or-Delta-HT-bound-input.md",
        "needle": "a BF/closed-form mass-current sector is a good candidate engine, but it is not parent-signed",
        "role": "immediate handoff selecting gauge/Noether source identity",
    },
    {
        "source_id": "916_validation",
        "path": OUT / "P8_Y5_BRR545_916_VALIDATION.csv",
        "needle": "V916_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "916_parent_clauses",
        "path": OUT / "P8_Y5_R10_916_PARENT_SIGNING_CLAUSE_AUDIT.csv",
        "needle": "BFC916_2_Noether_equality_not_multiplier_magic",
        "role": "BF parent-signing blockers",
    },
    {
        "source_id": "916_bound_inputs",
        "path": OUT / "P8_Y5_R10_916_DELTA_HT_BOUND_INPUT_PACK.csv",
        "needle": "DHT916_1_K_BF_H",
        "role": "Delta_HT/BF-Hilbert bound inputs",
    },
    {
        "source_id": "12_gauge_noether_audit",
        "path": ROOT / "12-gauge-noether-origin-audit.md",
        "needle": "Noether structure can explain a constraint only after the parent action has",
        "role": "general no-cheat Noether warning",
    },
    {
        "source_id": "221_noether_source_doc",
        "path": ROOT / "221-Noether-source-identity-or-compact-PPN-closure-map.md",
        "needle": "the source identity has a real derivation template",
        "role": "parent response/source-identity template",
    },
    {
        "source_id": "221_parent_variation_contract",
        "path": ROOT / "runs" / "20260601-000038-Noether-source-identity-or-compact-PPN-closure-map" / "results" / "parent_variation_contract.csv",
        "needle": "parent_response_field",
        "role": "machine parent-response variation template",
    },
    {
        "source_id": "445_source_ownership_doc",
        "path": ROOT / "445-measured-GM-Ward-source-ownership-theorem-attempt.md",
        "needle": "conditional_theorem",
        "role": "Ward/source ownership warning",
    },
    {
        "source_id": "446_source_owner_doc",
        "path": ROOT / "446-source-owner-current-parent-action-contract.md",
        "needle": "A1_source_owner_decomposition",
        "role": "source-owner Noether/current decomposition contract",
    },
    {
        "source_id": "source_owner_contract",
        "path": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "needle": "A1_source_owner_decomposition",
        "role": "machine source-owner parent action contract",
    },
    {
        "source_id": "ward_owner_contract",
        "path": OUT / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "needle": "C1_exact_owner_decomposition",
        "role": "machine Ward source-owner identity contract",
    },
    {
        "source_id": "q_retained_zero_contract",
        "path": OUT / "P8_q_retained_zero_conditions_CONTRACT.csv",
        "needle": "Q1_gauge_or_topological",
        "role": "legal gauge/topological zero-route contract",
    },
    {
        "source_id": "mass_flux_euler_contract",
        "path": OUT / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "needle": "MF3_no_ad_hoc_multiplier",
        "role": "no-ad-hoc mass-flux multiplier contract",
    },
    {
        "source_id": "pim_flux_topological_contract",
        "path": OUT / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "needle": "FC5_topological_mass_current_origin",
        "role": "topological mass-current equality contract",
    },
    {
        "source_id": "287_boundary_current_doc",
        "path": ROOT / "287-boundary-current-charge-owner-attempt.md",
        "needle": "pure topological current",
        "role": "topological current inert-unless-coupled warning",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


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
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "attempted the parent gauge/Noether route for the BF-Hilbert equality E_M=J_M^top-Pi_M J_H-dB_zero",
            "best_partial_result": "a legal route exists in principle if E_M is the Euler/Gauss constraint of a nonpropagating first-class mass-gauge/source-response sector and the Hilbert current is the corresponding Noether source",
            "hard_blockers": "the corpus does not derive the mass-gauge symmetry, source-response field, universal matter charge, first-class constraint algebra, no-extra-force condition, boundary no-flux, or level/G_eff calibration",
            "what_is_not_claimed": "BF-Hilbert equality, closed Pi_M flux, Delta_HT zero, mass gauge sector, measured-GM calibration, Newtonian reduction, PPN pass, or local-GR reduction",
            "decision": "Noether identity route is a precise parent-action target but remains unsigned; Delta_HT bound rows stay live and the next target is a nonpropagating mass-gauge constraint sector",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def noether_identity_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "NIA917_0_define_equality_residual",
            "identity_target": "E_M := J_M^top - Pi_M J_H - dB_zero",
            "noether_or_gauge_form": "E_M must be the Euler/Gauss constraint generated by a parent mass-gauge/source-response sector",
            "what_would_close": "E_M=0 gives J_M^top=Pi_M J_H+dB_zero",
            "status": "target_defined_not_derived",
            "blocker": "current corpus names E_M but does not supply the gauge/source-response field that owns it",
        },
        {
            "attempt_id": "NIA917_1_mass_gauge_symmetry",
            "identity_target": "mass-source gauge symmetry",
            "noether_or_gauge_form": "delta_alpha a_M=d alpha, delta_alpha matter/source phase or clock standard gives J_H as Noether source",
            "what_would_close": "Hilbert mass current becomes the source of the BF/topological Gauss law",
            "status": "not_parent_derived",
            "blocker": "no universal mass gauge charge/action on matter is derived; adding one risks fifth force/source charge",
        },
        {
            "attempt_id": "NIA917_2_topological_Gauss_law",
            "identity_target": "BF Gauss constraint",
            "noether_or_gauge_form": "delta a_M S gives dB_M - Pi_M J_H - dB_zero = 0 or equivalent",
            "what_would_close": "turns BF closed current into Hilbert source equality",
            "status": "closure_shape_available_not_parent_signed",
            "blocker": "without independent gauge origin this is just Lambda_M closure in another coat",
        },
        {
            "attempt_id": "NIA917_3_Noether_identity_limit",
            "identity_target": "Noether identity versus equation of motion",
            "noether_or_gauge_form": "Noether identities relate EOM; they do not set E_M=0 unless E_M is already an EOM/constraint",
            "what_would_close": "prevents overclaiming a conservation identity as equality",
            "status": "warning_active",
            "blocker": "the parent constraint/Euler equation is missing",
        },
        {
            "attempt_id": "NIA917_4_no_extra_force",
            "identity_target": "nonpropagating/stress-silent source-response field",
            "noether_or_gauge_form": "mass gauge/BF field has no local propagating mode, no Hodge kinetic term, no fifth-force coupling",
            "what_would_close": "keeps local PPN branch from acquiring new vector/scalar hair",
            "status": "not_parent_derived",
            "blocker": "no degree-count/constraint-algebra proof for the mass-gauge sector",
        },
        {
            "attempt_id": "NIA917_5_boundary_and_level",
            "identity_target": "B_zero no-flux and k_M/G_eff normalization",
            "noether_or_gauge_form": "boundary terms are class-only/zero-flux and the BF level calibrates to measured GM",
            "what_would_close": "prevents topological charge from being conserved but misnormalised",
            "status": "not_parent_derived",
            "blocker": "boundary flux and absolute measured-GM calibration remain open",
        },
        {
            "attempt_id": "NIA917_6_same_sector_unification",
            "identity_target": "local silence plus cosmological memory from one sector",
            "noether_or_gauge_form": "mass-gauge/topological sector is locally constrained/trivial but can carry allowed nonlocal/cosmological class data",
            "what_would_close": "keeps the route unified rather than local-only patchwork",
            "status": "not_derived",
            "blocker": "same-sector local/FLRW branching rule is not parent-derived",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_derived": False,
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def mass_gauge_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "contract_id": "MGC917_0_parent_field",
            "required_clause": "introduce or derive a parent mass-gauge/source-response variable whose Euler equation is E_M=0",
            "mathematical_form": "delta S_parent/delta A_M -> J_M^top - Pi_M J_H - dB_zero = 0",
            "legal_success_condition": "A_M is first-class/topological/auxiliary with independent parent reason",
            "current_status": "missing_parent_field",
        },
        {
            "contract_id": "MGC917_1_universal_Hilbert_charge",
            "required_clause": "ordinary matter sources the mass-gauge constraint through the same observed-frame Hilbert current",
            "mathematical_form": "J_H = delta S_matter/delta e_obs projected by Pi_M, not species/readout charge",
            "legal_success_condition": "one coframe, selector-blind matter, universal source coupling, no species/range spurion",
            "current_status": "conditional_from_Ward_source_not_mass_gauge_signed",
        },
        {
            "contract_id": "MGC917_2_first_class_constraint",
            "required_clause": "E_M=0 is first-class or topological, not a second-class ad hoc mass-fixing constraint",
            "mathematical_form": "{E_M,E_M}=0 or BF gauge redundancy removes local degree",
            "legal_success_condition": "constraint algebra/Noether identity closes without new local hair",
            "current_status": "not_derived",
        },
        {
            "contract_id": "MGC917_3_stress_silence",
            "required_clause": "mass-gauge/BF sector has no compact-bulk metric stress and no local fifth force",
            "mathematical_form": "delta_g S_BF,M|bulk=0; no star_g/Delta_g/Green_g/kinetic vector term",
            "legal_success_condition": "topological wedge/class action plus boundary no-hair",
            "current_status": "conditional_metric_free_shape_only",
        },
        {
            "contract_id": "MGC917_4_boundary_no_flux",
            "required_clause": "B_zero and owner currents have zero compact-boundary mass flux",
            "mathematical_form": "integral_boundary dB_zero=0 and integral_boundary Pi_M K_owner=0",
            "legal_success_condition": "class-only boundary theorem or retained coefficient below locks",
            "current_status": "fail_open",
        },
        {
            "contract_id": "MGC917_5_level_calibration",
            "required_clause": "BF level/normalization maps to M_eff and measured mu_obs with constant universal G_eff",
            "mathematical_form": "mu_obs=G_eff M_eff, M_eff proportional to integral_S Pi_M J_H, partial_t/r/A/lambda mu_obs=0",
            "legal_success_condition": "Poisson/Gauss/orbital calibration plus constant coupling",
            "current_status": "not_parent_derived",
        },
        {
            "contract_id": "MGC917_6_residual_fallback",
            "required_clause": "if any clause fails, E_M becomes Delta_HT_current with executable coefficients",
            "mathematical_form": "Delta_HT_current -> c_HT, K_BF_H, Q_BF_extra, B_zero_flux, tau_BF, k_M rows",
            "legal_success_condition": "numeric/source-backed residuals only; no symbolic pass",
            "current_status": "template_only",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_signed": False,
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def no_cheat_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "test_id": "NCT917_0_Noether_not_EOM",
            "bad_move": "say Noether identity sets E_M=0 by itself",
            "legal_if": "E_M is already the Euler/Gauss equation of a first-class parent variable",
            "result": "blocked",
        },
        {
            "test_id": "NCT917_1_no_mass_gauge_fifth_force",
            "bad_move": "couple a new mass gauge field to matter and ignore the fifth-force/source-charge consequence",
            "legal_if": "field is topological/nonpropagating or force is theorem-zero/bounded",
            "result": "blocked",
        },
        {
            "test_id": "NCT917_2_no_species_source_charge",
            "bad_move": "let matter carry arbitrary BF/mass gauge charge and call it Hilbert mass",
            "legal_if": "charge is universal and equal to observed Hilbert source in one coframe",
            "result": "blocked",
        },
        {
            "test_id": "NCT917_3_no_lambda_rebrand",
            "bad_move": "rename Lambda_M closure as gauge/Noether without constraint algebra",
            "legal_if": "Lambda_M is gauge/first-class/topological with full variation ledger",
            "result": "blocked",
        },
        {
            "test_id": "NCT917_4_no_boundary_absorption",
            "bad_move": "absorb B_zero/BF boundary flux into measured GM",
            "legal_if": "flux is zero or universal constant with no observable derivatives",
            "result": "blocked",
        },
        {
            "test_id": "NCT917_5_no_topological_spectator_mass",
            "bad_move": "treat a conserved topological current as mass without source coupling/calibration",
            "legal_if": "Noether source identity and Poisson/Gauss/orbital calibration are both derived",
            "result": "blocked",
        },
    ]
    for row in rows:
        row.update(
            {
                "passes_as_claim": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def deltaht_bound_fill_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "fill_id": "DHF917_0_K_BF_H",
            "symbol": "K_BF_H",
            "definition": "BF/Hilbert source coupling coefficient in E_M",
            "required_data": "parent mass-gauge coupling or source-backed numeric coefficient",
            "units": "model_coupling",
            "current_status": "MISSING_PARENT_MASS_GAUGE_COUPLING",
        },
        {
            "fill_id": "DHF917_1_C_constraint",
            "symbol": "C_M",
            "definition": "constraint-algebra closure measure for E_M as first-class/topological",
            "required_data": "Poisson/bracket or gauge-redundancy proof; otherwise residual coefficient",
            "units": "dimensionless_constraint_closure",
            "current_status": "MISSING_FIRST_CLASS_CONSTRAINT_PROOF",
        },
        {
            "fill_id": "DHF917_2_Q_BF_extra",
            "symbol": "Q_BF_extra",
            "definition": "extra BF/topological charge not equal to Hilbert mass",
            "required_data": "charge integral, boundary subtraction, local/asymptotic support, observed-source map",
            "units": "mass_or_GM_fraction",
            "current_status": "MISSING_EXTRA_CHARGE_ZERO_OR_BOUND",
        },
        {
            "fill_id": "DHF917_3_F_mass_gauge",
            "symbol": "F_M_force",
            "definition": "local force/source residual from any non-topological mass-gauge coupling",
            "required_data": "weak-field force law, range/scale tau_BF, source charge, local bounds",
            "units": "acceleration_or_normalized_force",
            "current_status": "MISSING_NO_FIFTH_FORCE_PROOF_OR_BOUND",
        },
        {
            "fill_id": "DHF917_4_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "boundary flux of equality improvement/owner current",
            "required_data": "boundary primitive formula and no-flux/no-hair theorem or coefficient bound",
            "units": "mass_flux_or_GM_fraction",
            "current_status": "MISSING_BOUNDARY_NO_FLUX_INPUT",
        },
        {
            "fill_id": "DHF917_5_k_M_level",
            "symbol": "k_M",
            "definition": "BF level/normalization connecting topological charge to M_eff",
            "required_data": "quantization/normalization rule, calibration to G_eff, source path",
            "units": "dimensionless_or_mass_normalization",
            "current_status": "MISSING_LEVEL_AND_CALIBRATION",
        },
        {
            "fill_id": "DHF917_6_c_HT",
            "symbol": "c_HT",
            "definition": "weak-field map from Delta_HT_current to PPN/source-normalization residuals",
            "required_data": "linearized equation, PPN basis, normalization, local-bound mapping",
            "units": "model_coefficient",
            "current_status": "MISSING_WEAK_FIELD_DELTAHT_MAP",
        },
    ]
    for row in rows:
        row.update(
            {
                "score_ready": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD917_0_gauge_Noether_attempt",
            "verdict": "not_parent_derived",
            "reason": "Noether identities can support the equality only after E_M is an owned first-class/Euler constraint; current corpus lacks the mass-gauge/source-response sector",
            "action": "do not claim BF-Hilbert equality or closed Pi_M flux",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD917_1_DeltaHT_fill",
            "verdict": "bound_fill_extended",
            "reason": "failed gauge/Noether clauses map directly into K_BF_H, C_M, Q_BF_extra, F_M_force, B_zero_flux, k_M, and c_HT",
            "action": "keep all rows score_ready=false until parent proof or numeric/source-backed coefficients exist",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD917_2_next_target",
            "verdict": "select_nonpropagating_mass_gauge_constraint_sector",
            "reason": "the least-cheaty next derivation is to build or reject a nonpropagating first-class mass-gauge constraint sector with zero local force",
            "action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "CGATE917_0_mass_gauge_identity",
            "claim": "parent gauge/Noether identity derives E_M=0",
            "blocker": "no parent mass-gauge/source-response field or first-class constraint algebra",
        },
        {
            "gate_id": "CGATE917_1_BF_Hilbert_equality",
            "claim": "J_M^top = Pi_M J_H + dB_zero is derived",
            "blocker": "equality remains closure-only without owned Euler/Gauss equation",
        },
        {
            "gate_id": "CGATE917_2_no_extra_force",
            "claim": "mass-gauge sector creates no local fifth force/source charge",
            "blocker": "nonpropagating/topological degree-count proof missing",
        },
        {
            "gate_id": "CGATE917_3_boundary_level_calibration",
            "claim": "B_zero flux and k_M/G_eff normalization are harmless",
            "blocker": "boundary no-flux and measured-GM calibration remain open",
        },
        {
            "gate_id": "CGATE917_4_DeltaHT_score_ready",
            "claim": "Delta_HT bound-fill rows are executable",
            "blocker": "coefficients, force law, constraint closure, level, and weak-field maps missing",
        },
        {
            "gate_id": "CGATE917_5_local_GR",
            "claim": "Newton/PPN/local-GR reduction follows",
            "blocker": "BF-Hilbert equality, source normalization, residual bounds, and PPN stability remain unproved",
        },
    ]
    for row in rows:
        row.update(
            {
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to build a nonpropagating first-class mass-gauge constraint sector whose Euler/Gauss equation is E_M=0 and whose local force vanishes; if not, produce a Delta_HT scorepack",
            "include": "constraint algebra, degree count, BF topological action, universal Hilbert source charge, no fifth force, boundary no-flux, k_M normalization, scorepack rows",
            "exclude": "Noether identity without EOM, closure-only multiplier, new local vector force, measured-GM promotion, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    guarded_fields = ("valid_for_claim", "claim_allowed", "score_ready", "parent_derived", "parent_signed", "passes_as_claim")
    for rows in tables:
        for row in rows:
            for field in guarded_fields:
                if field in row and stringify(row[field]).lower() != "false":
                    return False
    return True


def validation_rows(
    generated_utc: str,
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    contract: list[dict[str, object]],
    no_cheat: list[dict[str, object]],
    fills: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    generated_tables: list[list[dict[str, object]]],
) -> list[dict[str, object]]:
    prior_rows = read_csv(OUT / "P8_Y5_BRR545_916_VALIDATION.csv")
    formalization_count = formalization_changed_after_cutoff()
    checks = [
        {
            "check_id": "V917_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in sources) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V917_1_prior_916_clean",
            "result": "pass" if prior_rows and all(row.get("result") == "pass" for row in prior_rows) else "fail",
            "detail": "P8_Y5_BRR545_916_VALIDATION.csv clean",
        },
        {
            "check_id": "V917_2_Noether_attempt_not_parent_derived",
            "result": "pass" if attempts and all(not row["parent_derived"] for row in attempts) else "fail",
            "detail": "all gauge/Noether equality steps remain unsigned",
        },
        {
            "check_id": "V917_3_mass_gauge_contract_unsigned",
            "result": "pass" if contract and all(not row["parent_signed"] for row in contract) else "fail",
            "detail": "mass-gauge source contract rows remain unsigned",
        },
        {
            "check_id": "V917_4_no_cheat_tests_block_claim",
            "result": "pass" if no_cheat and all(not row["passes_as_claim"] for row in no_cheat) else "fail",
            "detail": "Noether-without-EOM, lambda rebrand, and fifth-force shortcuts are blocked",
        },
        {
            "check_id": "V917_5_DeltaHT_fill_nonclaim",
            "result": "pass" if fills and all(not row["score_ready"] and not row["valid_for_claim"] and str(row["current_status"]).startswith("MISSING_") for row in fills) else "fail",
            "detail": "all Delta_HT fill rows remain missing-input and invalid for claim",
        },
        {
            "check_id": "V917_6_claim_gates_false",
            "result": "pass" if gates and all(not row["claim_allowed"] for row in gates) else "fail",
            "detail": "all Noether/equality/force/Newton/local-GR claim gates remain false",
        },
        {
            "check_id": "V917_7_all_generated_rows_nonclaim",
            "result": "pass" if all_nonclaim(generated_tables) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
        },
        {
            "check_id": "V917_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V917_9_next_target_selected",
            "result": "pass" if next_rows and next_rows[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V917_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    attempts: list[dict[str, object]],
    contract: list[dict[str, object]],
    no_cheat: list[dict[str, object]],
    fills: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    path = ROOT / DOC_NAME
    content = f"""# 917 - Y5/R10 BF Mass-Current Gauge-Noether Source Identity Or DeltaHT Bound Fill

Private post-checkpoint-work note. This is not a public Newtonian, PPN, WEP, fifth-force, local-GR, measured-GM, or unified-field claim.

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the gauge/Noether route is precise but not parent-derived.** The target residual is:

```text
E_M := J_M^top - Pi_M J_H - dB_zero.
```

The route would become real only if `E_M=0` is the Euler/Gauss equation of a nonpropagating first-class mass-gauge/source-response sector, and if `Pi_M J_H` is the universal observed-frame Hilbert source for that symmetry. A Noether identity by itself does not set `E_M=0`; it only relates equations that the parent action already owns.

So the conclusion is sharp:

```text
Noether identity + no owned E_M equation = closure only.
Owned first-class E_M equation + no local force + no boundary flux + calibration = possible derivation route.
```

Current corpus has the first line, not the second. Delta-HT remains retained.

Practical read: this is not bad news; it tells us exactly what machine must exist. If MTS can make this work, the machine is a nonpropagating mass-gauge constraint, not a loose BF label and not a multiplier with a fake moustache.

## Non-Claim Summary
{md_table(summary)}

## Source Register
{md_table(sources)}

## Gauge-Noether Identity Attempt
{md_table(attempts)}

## Mass-Gauge Source Contract
{md_table(contract)}

## No-Cheat Tests
{md_table(no_cheat)}

## DeltaHT Bound Fill
{md_table(fills)}

## Branch Decision
{md_table(decisions)}

## Claim Gate
{md_table(gates)}

## Next Target
{md_table(next_rows)}

## Validation
{md_table(validation)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    sources = source_register_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    attempts = noether_identity_attempt_rows(generated_utc)
    contract = mass_gauge_contract_rows(generated_utc)
    no_cheat = no_cheat_rows(generated_utc)
    fills = deltaht_bound_fill_rows(generated_utc)
    decisions = branch_decision_rows(generated_utc)
    gates = claim_gate_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)

    generated_tables = [sources, summary, attempts, contract, no_cheat, fills, decisions, gates, next_rows]
    validation = validation_rows(generated_utc, sources, attempts, contract, no_cheat, fills, gates, next_rows, generated_tables)
    generated_tables.append(validation)

    write_csv(OUT / "P8_Y5_R10_917_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_917_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_R10_917_GAUGE_NOETHER_IDENTITY_ATTEMPT.csv", attempts)
    write_csv(OUT / "P8_Y5_R10_917_MASS_GAUGE_SOURCE_CONTRACT.csv", contract)
    write_csv(OUT / "P8_Y5_R10_917_NO_CHEAT_TESTS.csv", no_cheat)
    write_csv(OUT / "P8_Y5_R10_917_DELTAHT_BOUND_FILL.csv", fills)
    write_csv(OUT / "P8_Y5_R10_917_BRANCH_DECISION.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_917_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_917_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_917_VALIDATION.csv", validation)
    write_doc(generated_utc, sources, summary, attempts, contract, no_cheat, fills, decisions, gates, next_rows, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
