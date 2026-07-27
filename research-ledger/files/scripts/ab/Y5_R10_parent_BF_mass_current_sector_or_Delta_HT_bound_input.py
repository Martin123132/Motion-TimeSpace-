from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_916_parent_BF_mass_current_sector_constructed_as_candidate_not_parent_signed_Delta_HT_bound_inputs_retained_nonclaim"
CLAIM_CEILING = "BF_mass_current_sector_candidate_and_Delta_HT_bound_input_only_no_Hilbert_topological_equality_no_closed_PiM_flux_no_Newton_PPN_or_local_GR_claim"
DOC_NAME = "916-Y5-R10-parent-BF-mass-current-sector-or-Delta-HT-bound-input.md"
NEXT_TARGET = "917-Y5-R10-BF-mass-current-gauge-Noether-source-identity-or-DeltaHT-bound-fill.md"

SOURCE_SPECS = [
    {
        "source_id": "915_doc",
        "path": ROOT / "915-Y5-R10-Hilbert-topological-mass-current-equality-or-projector-bound-pack-fill.md",
        "needle": "the equality route is exact but not parent-derived",
        "role": "immediate handoff selecting parent BF mass-current sector",
    },
    {
        "source_id": "915_validation",
        "path": OUT / "P8_Y5_BRR545_915_VALIDATION.csv",
        "needle": "V915_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "915_residual_pack",
        "path": OUT / "P8_Y5_R10_915_CURRENT_MISMATCH_RESIDUAL_PACK.csv",
        "needle": "MRP915_0_Delta_HT_current",
        "role": "Delta_HT_current fallback rows",
    },
    {
        "source_id": "252_topological_projector_skeleton_doc",
        "path": ROOT / "252-topological-projector-parent-action-skeleton.md",
        "needle": "int Xi wedge d_rel J_rel",
        "role": "wedge/topological parent-action skeleton",
    },
    {
        "source_id": "252_skeleton_terms",
        "path": ROOT / "runs" / "20260601-000069-topological-projector-parent-action-skeleton" / "results" / "parent_action_skeleton_terms.csv",
        "needle": "S_rel_closure",
        "role": "machine wedge/topological action terms",
    },
    {
        "source_id": "252_open_obligations",
        "path": ROOT / "runs" / "20260601-000069-topological-projector-parent-action-skeleton" / "results" / "open_parent_obligations.csv",
        "needle": "source_normalization",
        "role": "open obligations after topological skeleton",
    },
    {
        "source_id": "420_relative_current_doc",
        "path": ROOT / "420-relative-current-boundary-generator-theorem-attempt.md",
        "needle": "BF_multiplier_integral_surfaces",
        "role": "relative current/BF multiplier route warning",
    },
    {
        "source_id": "287_boundary_current_doc",
        "path": ROOT / "287-boundary-current-charge-owner-attempt.md",
        "needle": "relative current machinery is good conservation/support structure",
        "role": "relative boundary current support and normalization obstruction",
    },
    {
        "source_id": "328_support_projector_doc",
        "path": ROOT / "328-topological-MTS-support-projector-gate.md",
        "needle": "derive a nondegenerate conserved MTS sector charge",
        "role": "future parent sector charge requirement",
    },
    {
        "source_id": "348_projector_stress_doc",
        "path": ROOT / "348-N5-projector-stress-conservation-theorem.md",
        "needle": "metric-independent wedge/chain projector has `delta_g S_projector|bulk=0`",
        "role": "topological no-bulk-stress theorem",
    },
    {
        "source_id": "446_source_owner_doc",
        "path": ROOT / "446-source-owner-current-parent-action-contract.md",
        "needle": "A4_mass_flux_projector",
        "role": "source-owner parent action mass-flux block",
    },
    {
        "source_id": "446_source_owner_contract",
        "path": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "needle": "A4_mass_flux_projector",
        "role": "machine source-owner parent action contract",
    },
    {
        "source_id": "q_retained_zero_conditions",
        "path": OUT / "P8_q_retained_zero_conditions_CONTRACT.csv",
        "needle": "Q1_gauge_or_topological",
        "role": "legal gauge/topological zero route",
    },
    {
        "source_id": "455_flux_contract",
        "path": OUT / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "needle": "FC5_topological_mass_current_origin",
        "role": "topological mass-current equality requirement",
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
            "what_changed": "constructed the minimal BF/closed-form mass-current candidate and audited whether it can sign the Hilbert/topological equality",
            "best_partial_result": "a BF/closed-form sector can naturally produce a closed topological current without local Hodge stress, e.g. J_M^top=dB_M plus possible harmonic class data",
            "hard_blockers": "the current corpus does not derive the mass-sector gauge symmetry, coupling of the BF current to the Hilbert source, equality to Pi_M J_H, zero B_zero boundary flux, normalization, or measured-GM calibration",
            "what_is_not_claimed": "parent BF mass-current sector, Hilbert/topological equality, closed Pi_M flux, Delta_HT zero, Newtonian source normalization, PPN pass, or local-GR reduction",
            "decision": "BF sector is a good candidate engine but not parent-signed; keep Delta_HT_current bound inputs live and target the gauge/Noether source identity next",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def bf_sector_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "candidate_id": "BF916_0_closed_form_current",
            "sector_piece": "closed-form mass current",
            "schematic_form": "J_M^top = dB_M + J_M^harm",
            "variation_or_identity": "dJ_M^top=0 by d^2=0 and dJ_M^harm=0",
            "what_it_would_buy": "closed topological current without Hodge/DeWitt metric projector stress",
            "status": "mathematically_available_not_parent_motivated",
        },
        {
            "candidate_id": "BF916_1_BF_topological_action",
            "sector_piece": "BF action",
            "schematic_form": "S_BF,M = k_M integral B_M wedge F_M plus boundary/class terms",
            "variation_or_identity": "delta B_M gives F_M=0 or flat/topological sector; delta A_M gives dB_M plus sources",
            "what_it_would_buy": "metric-free topological source of closed classes",
            "status": "candidate_skeleton_only",
        },
        {
            "candidate_id": "BF916_2_source_equality_constraint",
            "sector_piece": "Hilbert/topological equality coupling",
            "schematic_form": "S_eq = integral Lambda_M wedge (J_M^top - Pi_M J_H - dB_zero)",
            "variation_or_identity": "delta Lambda_M would impose J_M^top = Pi_M J_H + dB_zero",
            "what_it_would_buy": "d(Pi_M J_H)=0 if zero boundary flux also holds",
            "status": "closure_only_unless_Lambda_M_has_independent_gauge_Noether_origin",
        },
        {
            "candidate_id": "BF916_3_boundary_improvement",
            "sector_piece": "exact improvement/no-flux term",
            "schematic_form": "dB_zero with integral_boundary dB_zero=0",
            "variation_or_identity": "exact term changes local representative without shifting compact/measured monopole",
            "what_it_would_buy": "prevents the equality from hiding boundary mu_extra",
            "status": "not_parent_derived",
        },
        {
            "candidate_id": "BF916_4_mass_charge_normalization",
            "sector_piece": "mass level/coupling normalization",
            "schematic_form": "M_eff proportional to integral_S2 Pi_M J_H and mu_obs=G_eff M_eff",
            "variation_or_identity": "constant universal k_M/G_eff and orbital/asymptotic calibration",
            "what_it_would_buy": "turns a closed current into measured Newtonian source mass",
            "status": "not_parent_derived",
        },
        {
            "candidate_id": "BF916_5_no_extra_local_degrees",
            "sector_piece": "topological/no-hair guard",
            "schematic_form": "delta_g S_BF,M|bulk=0, no propagating BF stress, no Hodge star",
            "variation_or_identity": "all BF/projector/domain terms are wedge/chain/class data or retained",
            "what_it_would_buy": "keeps local exterior from becoming modified-gravity stress by construction",
            "status": "conditional_if_metric_free_and_boundary_safe",
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


def parent_signing_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "BFC916_0_independent_mass_sector_reason",
            "needed_parent_clause": "the BF/closed-form mass-current sector is required by an independent symmetry/topology/source principle, not appended to repair GM",
            "mathematical_test": "there is a parent gauge/Noether identity whose current is J_M^top before local residual scoring",
            "current_status": "missing",
            "failure_if_missing": "BF sector is a useful closure skeleton, not a derivation",
        },
        {
            "clause_id": "BFC916_1_same_degree_same_frame_current",
            "needed_parent_clause": "J_M^top and Pi_M J_H live in the same observed-frame exterior current complex",
            "mathematical_test": "deg(J_M^top)=deg(Pi_M J_H), same e_obs/coframe, same orientation/domain, no readout mask",
            "current_status": "conditional_Hilbert_current_available_not_BF_current_derived",
            "failure_if_missing": "equality compares objects from different complexes",
        },
        {
            "clause_id": "BFC916_2_Noether_equality_not_multiplier_magic",
            "needed_parent_clause": "the equality J_M^top=Pi_M J_H+dB_zero is a Noether/source identity, not just a Lagrange multiplier inserted after the problem is found",
            "mathematical_test": "delta_Lambda S_eq is tied to first-class/gauge redundancy or source-owner identity",
            "current_status": "not_parent_derived",
            "failure_if_missing": "lambda/equality term remains closure-only",
        },
        {
            "clause_id": "BFC916_3_metric_free_no_Hodge_stress",
            "needed_parent_clause": "the BF sector and projector use wedge/chain/class data only in the compact local bulk",
            "mathematical_test": "delta_g S_BF,M|bulk=0 and no star_g, Delta_g, Green_g, DeWitt inner product, or sqrt(-g) bulk potential",
            "current_status": "conditional_from_252_348_not_mass_current_signed",
            "failure_if_missing": "BF/topological label can still hide local projector stress",
        },
        {
            "clause_id": "BFC916_4_boundary_Bzero_no_flux",
            "needed_parent_clause": "B_zero and BF boundary terms carry no compact/measured mass flux, shear, vector, radial, time, range, or source hair",
            "mathematical_test": "integral_boundary dB_zero=0 or constant_global with all observable derivatives zero",
            "current_status": "fail_open",
            "failure_if_missing": "Delta_HT leaks into mu_extra, dln_Meff_dt, or radial/source residuals",
        },
        {
            "clause_id": "BFC916_5_no_extra_BF_charge_leakage",
            "needed_parent_clause": "BF sector contributes no extra asymptotic/compact mass charge beyond Pi_M J_H unless explicitly retained",
            "mathematical_test": "Q_BF_extra=0 or Q_BF_extra maps to Delta_HT/mu_extra residual rows",
            "current_status": "not_parent_derived",
            "failure_if_missing": "conserved topological charge is not automatically the Newton source charge",
        },
        {
            "clause_id": "BFC916_6_absolute_level_and_GM_calibration",
            "needed_parent_clause": "the topological level/coupling calibrates to measured M_eff and constant universal G_eff",
            "mathematical_test": "mu_obs=G_eff M_eff, M_eff proportional to integral_S2 Pi_M J_H, partial_t/r/A/lambda mu_obs=0",
            "current_status": "not_parent_derived",
            "failure_if_missing": "closed BF current may be normalized but not measured Newtonian mass",
        },
        {
            "clause_id": "BFC916_7_FLRW_local_same_sector",
            "needed_parent_clause": "the same sector can support nontrivial cosmological memory while remaining locally trivial/silent",
            "mathematical_test": "local branch [J_M^top-Pi_MJ_H]=0, FLRW branch allowed nontrivial class without new sidecar rule",
            "current_status": "not_derived",
            "failure_if_missing": "BF sector becomes a local patch rather than unified theory spine",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_signed": False,
                "equality_claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def no_cheat_test_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "test_id": "NCT916_0_no_BF_after_the_fact",
            "bad_move": "add BF/equality fields only after seeing that d(Pi_M J_H)=0 is missing",
            "legal_if": "the BF sector follows from an independent parent symmetry/topological sector already needed elsewhere",
            "current_result": "not_satisfied",
        },
        {
            "test_id": "NCT916_1_no_lambdaM_magic",
            "bad_move": "use Lambda_M wedge (J_top-Pi_MJ_H) as a bare constraint and call it a derivation",
            "legal_if": "Lambda_M is first-class/gauge/Noether-owned, with full variation and stress ledger",
            "current_result": "not_satisfied",
        },
        {
            "test_id": "NCT916_2_no_topological_name_metric_action",
            "bad_move": "call the sector topological while using Hodge star, DeWitt metric, Green operator, or sqrt(-g) bulk norm",
            "legal_if": "all compact-bulk terms are wedge/chain/class data or the metric stress is retained",
            "current_result": "guardrail_pass_written",
        },
        {
            "test_id": "NCT916_3_no_boundary_flux_absorption",
            "bad_move": "hide B_zero or BF boundary flux inside measured GM",
            "legal_if": "boundary flux is zero or one universal constant with no derivative/source/range/frame dependence",
            "current_result": "fail_open",
        },
        {
            "test_id": "NCT916_4_no_conserved_charge_equals_mass_by_name",
            "bad_move": "treat any conserved BF charge as the observed Hilbert/Newton mass",
            "legal_if": "source equality plus Poisson/Gauss/orbital calibration are derived",
            "current_result": "blocked_by_915_and_PG_stack",
        },
        {
            "test_id": "NCT916_5_no_local_patch_sidecar",
            "bad_move": "invent a local BF silence rule unrelated to the cosmology/time/field-theory spine",
            "legal_if": "the same sector explains local silence and the nonlocal/cosmological memory branch under one parent rule",
            "current_result": "not_derived",
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


def delta_ht_bound_input_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "DHT916_0_Delta_HT_current",
            "symbol": "Delta_HT_current",
            "definition": "mismatch current J_M^top - Pi_M J_H - dB_zero",
            "units": "current_form_or_normalized_mass_flux",
            "needed_for_scoring": "explicit BF/topological current, Pi_M Hilbert current formula, B_zero convention, normalization",
            "arena": "source-normalization, Newtonian measured-GM, PPN/local-GR",
            "current_status": "MISSING_PARENT_BF_EQUALITY_OR_NUMERIC_CURRENT_MAP",
        },
        {
            "input_id": "DHT916_1_K_BF_H",
            "symbol": "K_BF_H",
            "definition": "coefficient coupling the BF/topological current to the Hilbert source current",
            "units": "model_coupling",
            "needed_for_scoring": "parent coupling term, gauge/Noether source identity, sign/normalization",
            "arena": "Delta_HT_current and measured-GM calibration",
            "current_status": "MISSING_BF_HILBERT_COUPLING",
        },
        {
            "input_id": "DHT916_2_Q_BF_extra",
            "symbol": "Q_BF_extra",
            "definition": "extra compact/asymptotic BF mass charge not equal to Pi_M J_H",
            "units": "mass_charge_or_dimensionless_GM_fraction",
            "needed_for_scoring": "charge integral, boundary conditions, local/asymptotic subtraction, observational map",
            "arena": "mu_extra, orbital GM, PPN",
            "current_status": "MISSING_EXTRA_CHARGE_ZERO_OR_BOUND",
        },
        {
            "input_id": "DHT916_3_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "boundary flux of the exact improvement in the Hilbert/topological equality",
            "units": "mass_flux_or_GM_fraction",
            "needed_for_scoring": "B_zero formula, boundary orientation, no-hair theorem or bound",
            "arena": "radial/source hair, Gdot/orbital tests",
            "current_status": "MISSING_BZERO_BOUNDARY_FLUX_INPUT",
        },
        {
            "input_id": "DHT916_4_c_HT",
            "symbol": "c_HT",
            "definition": "weak-field coefficient mapping Delta_HT_current into metric/source residuals",
            "units": "model_coefficient",
            "needed_for_scoring": "linearized field equations, source-normalization map, PPN basis, local bounds",
            "arena": "PPN, clocks, orbital, R10",
            "current_status": "MISSING_WEAK_FIELD_MAP",
        },
        {
            "input_id": "DHT916_5_tau_BF",
            "symbol": "tau_BF",
            "definition": "characteristic length/time/range scale of BF equality mismatch if not topological-zero",
            "units": "length_or_time",
            "needed_for_scoring": "profile or kernel, compact exterior scale, relation to lambda/R10/orbital arenas",
            "arena": "R10, orbital/range, clock drift",
            "current_status": "MISSING_SCALE_OR_TOPOLOGICAL_ZERO_PROOF",
        },
        {
            "input_id": "DHT916_6_level_kM",
            "symbol": "k_M",
            "definition": "topological level/normalization of the mass-current sector",
            "units": "dimensionless_or_mass_normalization",
            "needed_for_scoring": "quantization/normalization rule and relation to G_eff M_eff",
            "arena": "measured-GM calibration, cosmology/local unification",
            "current_status": "MISSING_LEVEL_NORMALIZATION",
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
            "branch_id": "BD916_0_BF_sector_candidate",
            "verdict": "candidate_constructed_not_parent_signed",
            "reason": "BF/closed-form terms can provide a closed topological current and stress silence, but do not by themselves prove equality to the observed Hilbert mass current",
            "action": "do not claim d(Pi_M J_H)=0 or local-GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD916_1_Delta_HT_bound_inputs",
            "verdict": "bound_pack_extended",
            "reason": "if the BF equality remains unsigned, Delta_HT_current is the honest residual linking the failed derivation to source-normalization and PPN/local tests",
            "action": "keep all rows score_ready=false until coefficients, units, profiles, and source paths are real",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD916_2_next_derivation_target",
            "verdict": "select_gauge_Noether_source_identity",
            "reason": "the next derivation must show why the BF current couples to/equalizes with the Hilbert mass source through a parent gauge or Noether identity, not an added constraint",
            "action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "CGATE916_0_parent_BF_sector",
            "claim": "independent parent BF/closed-form mass-current sector exists",
            "blocker": "sector is candidate only; no parent gauge/Noether origin or level normalization",
        },
        {
            "gate_id": "CGATE916_1_Hilbert_topological_equality",
            "claim": "J_M^top = Pi_M J_H + dB_zero is derived",
            "blocker": "BF equality coupling is closure-only unless gauge/Noether source identity is derived",
        },
        {
            "gate_id": "CGATE916_2_closed_PiM_flux",
            "claim": "d(Pi_M J_H)=0 follows from BF topology",
            "blocker": "closed J_M^top does not close Pi_M J_H without equality and zero boundary flux",
        },
        {
            "gate_id": "CGATE916_3_BF_stress_silence",
            "claim": "BF sector is locally stress-silent and boundary-safe",
            "blocker": "bulk wedge terms are conditionally silent, but boundary/no-flux and equality variation remain unsigned",
        },
        {
            "gate_id": "CGATE916_4_Delta_HT_scored",
            "claim": "Delta_HT_current bound inputs are executable",
            "blocker": "current formula, coefficients, level, units, and arena projections are missing",
        },
        {
            "gate_id": "CGATE916_5_Newton_PPN_local_GR",
            "claim": "measured GM/Newton/PPN/local-GR branch is promoted",
            "blocker": "mass-current equality, source normalization, calibration, and residual bounds remain open",
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
            "objective": "try to derive the BF/Hilbert equality from a parent gauge or Noether source identity; if not, fill Delta_HT_current coefficient and bound inputs",
            "include": "BF gauge symmetry, source coupling, Noether identity, Lambda_M legality, k_M normalization, B_zero no-flux, Delta_HT coefficients",
            "exclude": "adding closure-only multiplier, claiming conserved BF charge equals mass by name, formalization-workbench edits, GitHub action",
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
    guarded_fields = (
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "parent_signed",
        "equality_claim_allowed",
        "passes_as_claim",
    )
    for rows in tables:
        for row in rows:
            for field in guarded_fields:
                if field in row and stringify(row[field]).lower() != "false":
                    return False
    return True


def validation_rows(
    generated_utc: str,
    sources: list[dict[str, object]],
    candidates: list[dict[str, object]],
    clauses: list[dict[str, object]],
    no_cheat: list[dict[str, object]],
    bound_inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    generated_tables: list[list[dict[str, object]]],
) -> list[dict[str, object]]:
    prior_rows = read_csv(OUT / "P8_Y5_BRR545_915_VALIDATION.csv")
    formalization_count = formalization_changed_after_cutoff()
    checks = [
        {
            "check_id": "V916_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in sources) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V916_1_prior_915_clean",
            "result": "pass" if prior_rows and all(row.get("result") == "pass" for row in prior_rows) else "fail",
            "detail": "P8_Y5_BRR545_915_VALIDATION.csv clean",
        },
        {
            "check_id": "V916_2_BF_candidate_not_parent_signed",
            "result": "pass" if candidates and all(not row["parent_signed"] for row in candidates) else "fail",
            "detail": "all BF mass-current candidate rows remain unsigned",
        },
        {
            "check_id": "V916_3_parent_signing_blockers_recorded",
            "result": "pass" if clauses and all(not row["parent_signed"] for row in clauses) and any(row["clause_id"] == "BFC916_2_Noether_equality_not_multiplier_magic" for row in clauses) else "fail",
            "detail": "Noether/equality and boundary/no-flux blockers recorded",
        },
        {
            "check_id": "V916_4_no_cheat_tests_block_claim",
            "result": "pass" if no_cheat and all(not row["passes_as_claim"] for row in no_cheat) else "fail",
            "detail": "BF after-the-fact, lambda magic, and conserved-charge naming shortcuts are blocked",
        },
        {
            "check_id": "V916_5_Delta_HT_bound_inputs_nonclaim",
            "result": "pass" if bound_inputs and all(not row["score_ready"] and not row["valid_for_claim"] and str(row["current_status"]).startswith("MISSING_") for row in bound_inputs) else "fail",
            "detail": "all Delta_HT/BF bound inputs remain missing-input and invalid for claim",
        },
        {
            "check_id": "V916_6_claim_gates_false",
            "result": "pass" if gates and all(not row["claim_allowed"] for row in gates) else "fail",
            "detail": "all BF/equality/flux/Newton/local-GR claim gates remain false",
        },
        {
            "check_id": "V916_7_all_generated_rows_nonclaim",
            "result": "pass" if all_nonclaim(generated_tables) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
        },
        {
            "check_id": "V916_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V916_9_next_target_selected",
            "result": "pass" if next_rows and next_rows[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V916_10_validation_rows_ready",
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
    candidates: list[dict[str, object]],
    clauses: list[dict[str, object]],
    no_cheat: list[dict[str, object]],
    bound_inputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    path = ROOT / DOC_NAME
    content = f"""# 916 - Y5/R10 Parent BF Mass-Current Sector Or Delta-HT Bound Input

Private post-checkpoint-work note. This is not a public Newtonian, PPN, WEP, fifth-force, local-GR, measured-GM, or unified-field claim.

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **a BF/closed-form mass-current sector is a good candidate engine, but it is not parent-signed.** The clean construction can make a closed topological current without Hodge-projector stress:

```text
J_M^top = dB_M + J_M^harm,
dJ_M^top = 0.
```

But closed topology is not yet source mass. The missing parent move is still:

```text
J_M^top = Pi_M J_H + dB_zero
```

and this cannot be earned by simply adding a multiplier after the gap is visible. It needs a parent gauge/Noether/source identity, zero `B_zero` boundary flux, no extra BF mass charge, and measured-GM normalization. Current corpus gives wedge/topological projector-silence machinery, not a signed BF/Hilbert mass-source equality.

Practical read: this is a proper candidate, not a dud. But the current has to shake hands with Hilbert mass through a real symmetry/Noether identity. Otherwise it is just a beautifully behaved spectator current wearing a mass badge.

## Non-Claim Summary
{md_table(summary)}

## Source Register
{md_table(sources)}

## BF Mass-Current Candidate
{md_table(candidates)}

## Parent-Signing Clause Audit
{md_table(clauses)}

## No-Cheat Variation Tests
{md_table(no_cheat)}

## Delta-HT Bound Input Pack
{md_table(bound_inputs)}

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
    candidates = bf_sector_candidate_rows(generated_utc)
    clauses = parent_signing_clause_rows(generated_utc)
    no_cheat = no_cheat_test_rows(generated_utc)
    bound_inputs = delta_ht_bound_input_rows(generated_utc)
    decisions = branch_decision_rows(generated_utc)
    gates = claim_gate_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)

    generated_tables = [sources, summary, candidates, clauses, no_cheat, bound_inputs, decisions, gates, next_rows]
    validation = validation_rows(generated_utc, sources, candidates, clauses, no_cheat, bound_inputs, gates, next_rows, generated_tables)
    generated_tables.append(validation)

    write_csv(OUT / "P8_Y5_R10_916_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_916_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_R10_916_BF_MASS_CURRENT_CANDIDATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_916_PARENT_SIGNING_CLAUSE_AUDIT.csv", clauses)
    write_csv(OUT / "P8_Y5_R10_916_NO_CHEAT_VARIATION_TESTS.csv", no_cheat)
    write_csv(OUT / "P8_Y5_R10_916_DELTA_HT_BOUND_INPUT_PACK.csv", bound_inputs)
    write_csv(OUT / "P8_Y5_R10_916_BRANCH_DECISION.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_916_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_916_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_916_VALIDATION.csv", validation)
    write_doc(generated_utc, sources, summary, candidates, clauses, no_cheat, bound_inputs, decisions, gates, next_rows, validation)

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
