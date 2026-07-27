from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC_NAME = "919-Y5-R10-matter-current-silence-lemma-or-DeltaHT-bound-runner.md"
STATUS = "Y5_R10_919_matter_current_silence_lemma_conditional_only_offshell_closure_and_holonomy_unsigned_FM_bound_runner_retained"
CLAIM_CEILING = "conditional_silence_lemma_only_no_mass_gauge_coupling_pass_no_Newton_PPN_or_local_GR_claim"
NEXT_TARGET = "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells: list[str] = []
        for field in fields:
            value = str(row.get(field, "")).replace("|", "\\|").replace("\n", " ")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "918_doc",
            "path": "918-Y5-R10-nonpropagating-mass-gauge-constraint-sector-or-DeltaHT-scorepack.md",
            "role": "identifies the A_M wedge Pi_M J_H matter-variation coupling as live blocker",
            "needle": "The problem is the coupling",
        },
        {
            "source_id": "918_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_918_VALIDATION.csv",
            "role": "proves 918 handoff is clean and nonclaim",
            "needle": "V918_11_validation_rows_ready",
        },
        {
            "source_id": "447_no_species_charge",
            "path": "447-no-species-source-charge-one-coframe-theorem-attempt.md",
            "role": "one-coframe/no-species-source-charge conditional theorem and limits",
            "needle": "current_corpus_status",
        },
        {
            "source_id": "449_Ward_current",
            "path": "449-source-current-Ward-universality-theorem-attempt.md",
            "role": "Hilbert source current Ward universality and conservation limit",
            "needle": "Ward_conservation_limit",
        },
        {
            "source_id": "520_Ward_closure",
            "path": "520-Y5-source-current-Ward-closure-or-bound-row.md",
            "role": "Ward conservation is necessary but insufficient for projected mass-current closure",
            "needle": "Ward conservation alone does not prove",
        },
        {
            "source_id": "420_boundary_current",
            "path": "420-relative-current-boundary-generator-theorem-attempt.md",
            "role": "boundary-current generator route and stress-safe boundary warning",
            "needle": "stress_safe_boundary",
        },
        {
            "source_id": "422_readout_after_variation",
            "path": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
            "role": "readout-after-variation no-cheat contract",
            "needle": "readout_after_variation",
        },
        {
            "source_id": "491_no_linear_source",
            "path": "491-Yloc-no-linear-source-symmetry-or-closure.md",
            "role": "parent no-linear-source symmetry remains unsigned",
            "needle": "Current derived MTS parent symmetry: not yet.",
        },
        {
            "source_id": "492_silence_auxiliary",
            "path": "492-silence-auxiliary-parent-action-construction-or-closure.md",
            "role": "silence auxiliary construction warns about reintroduced linear source",
            "needle": "Doing both without reintroducing a linear source is the hard triangle.",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "machine-readable no-species/source-charge contract",
            "needle": "S4_source_normalization_species_blind",
        },
        {
            "source_id": "Ward_current_contract",
            "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "role": "machine-readable source-current Ward universality contract",
            "needle": "SC2_Ward_conservation_on_matter_shell",
        },
        {
            "source_id": "owner_identity_contract",
            "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "role": "owner divergence, zero flux, calibrated current requirements",
            "needle": "C2_zero_owner_flux",
        },
        {
            "source_id": "q_zero_contract",
            "path": "source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv",
            "role": "legal zero routes for retained source/force currents",
            "needle": "Q1_gauge_or_topological",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "a strong silence lemma is mathematically available, but the current corpus has not parent-signed its off-shell projected-current closure, exact A_M gauge, or zero compact holonomy",
            "what_improved": "the coupling problem is now split into exact proof clauses and executable residual rows",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def lemma_rows() -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "MSL919_0_coupling_definition",
            "claim": "mass-gauge source coupling is S_int = K_BF_H integral_D A_M wedge J_Pi with J_Pi := Pi_M J_H",
            "derivation": "variation gives delta S_int = K_BF_H integral_D A_M wedge delta J_Pi plus projector and boundary variations",
            "required_clause": "J_Pi must be parent-defined before readout and Pi_M variation must be owned",
            "current_status": "definition_clean_parent_ownership_unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "lemma_id": "MSL919_1_exact_A_boundary_reduction",
            "claim": "if A_M=d lambda_M on the compact local domain, then the coupling integrates by parts",
            "derivation": "integral_D d lambda_M wedge J_Pi = integral_boundary lambda_M J_Pi - integral_D lambda_M dJ_Pi",
            "required_clause": "A_M exact, not merely flat; compact holonomy and boundary lambda_M variation vanish or are fixed universal background",
            "current_status": "mathematical_identity_conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "lemma_id": "MSL919_2_variation_silence",
            "claim": "the matter variation is silent if dJ_Pi=0 is an off-shell parent identity and boundary variation vanishes",
            "derivation": "delta S_int = K_BF_H[integral_boundary lambda_M delta J_Pi - integral_D lambda_M delta(dJ_Pi)] = 0",
            "required_clause": "delta(dJ_Pi)=0 off shell or equals an already-owned gauge/Ward constraint with no new matter equation",
            "current_status": "conditional_theorem_not_parent_derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "lemma_id": "MSL919_3_Ward_only_limit",
            "claim": "ordinary on-shell Ward conservation is not enough for action-level silence",
            "derivation": "if dJ_Pi vanishes only after matter equations, A_M wedge delta J_Pi can modify those equations before the shell is imposed",
            "required_clause": "upgrade Ward conservation to off-shell Noether generator/canonical boundary term or keep residual",
            "current_status": "blocks_claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "lemma_id": "MSL919_4_silence_theorem_contract",
            "claim": "strong theorem: exact A_M + off-shell closed J_Pi + zero boundary flux + universal K_BF_H implies no local fifth force from S_int",
            "derivation": "the source coupling becomes a boundary/background term and does not add an independent Euler derivative for matter",
            "required_clause": "all four clauses parent-signed before any local-GR/PPN promotion",
            "current_status": "theorem_shape_written_not_MTS_derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def variation_rows() -> list[dict[str, object]]:
    return [
        {
            "case_id": "VAR919_0_strong_silence",
            "case": "A_M exact and boundary-trivial; J_Pi off-shell closed; Pi_M parent-owned; K_BF_H fixed universal",
            "matter_variation": "delta S_int = 0 modulo boundary/background term",
            "force_readout": "F_M_force = 0",
            "status": "sufficient_conditions_written_not_parent_signed",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "case_id": "VAR919_1_on_shell_Ward_only",
            "case": "dJ_Pi=0 only after matter/coframe equations",
            "matter_variation": "delta S_int can change the equations that were needed to prove dJ_Pi=0",
            "force_readout": "F_M_force retained unless coupling is shown to be a canonical gauge generator",
            "status": "not_silent_enough_for_claim",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "case_id": "VAR919_2_flat_nonexact_A",
            "case": "dA_M=0 but holonomy integral_gamma A_M is nonzero",
            "matter_variation": "local curvature vanishes but global/compact source phase or boundary impulse can remain",
            "force_readout": "A_M_holonomy and B_zero_flux retained",
            "status": "holonomy_zero_missing",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "case_id": "VAR919_3_projector_leakage",
            "case": "Pi_M depends on metric/domain/memory fields",
            "matter_variation": "delta J_Pi = Pi_M delta J_H + delta Pi_M J_H and d(Pi_M J_H) has product-rule leakage",
            "force_readout": "dPiMJ_leak retained",
            "status": "parent_projector_closure_missing",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "case_id": "VAR919_4_species_or_marker_source",
            "case": "source current carries species, marker, boundary, or connection charge",
            "matter_variation": "mass-gauge source response becomes composition dependent",
            "force_readout": "species_source_charge retained",
            "status": "no_species_charge_not_parent_derived",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def proof_clause_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "MSC919_0_exact_A",
            "required_statement": "A_M is exact on the compact local exterior domain, A_M=d lambda_M",
            "why_needed": "flat is not enough; nontrivial holonomy can couple to source charge",
            "current_evidence": "BF/nonpropagating ansatz only",
            "status": "not_parent_derived",
            "if_missing": "retain A_M_holonomy and F_M_force",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "MSC919_1_offshell_dJPi_zero",
            "required_statement": "d(Pi_M J_H)=0 before using the matter equations being varied",
            "why_needed": "action-level silence requires delta(dJ_Pi)=0 or an already-owned identity",
            "current_evidence": "Ward conservation is on-shell and projected closure remains open",
            "status": "not_parent_derived",
            "if_missing": "retain dPiMJ_leak and Delta_HT_current",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "MSC919_2_projector_variation_owned",
            "required_statement": "delta Pi_M J_H is absent, exact-owned, or included in a parent charge algebra",
            "why_needed": "projector leakage is exactly how closure becomes post-hoc",
            "current_evidence": "Pi_M closure contracts exist but remain unsigned",
            "status": "not_parent_derived",
            "if_missing": "retain C_M and dPiMJ_leak",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "MSC919_3_zero_boundary_flux",
            "required_statement": "integral_boundary lambda_M delta J_Pi and improvement flux vanish or are fixed universal background",
            "why_needed": "total divergences can still shift compact measured mass",
            "current_evidence": "boundary-current routes are contracts, not source-signed zero-flux theorems",
            "status": "not_parent_derived",
            "if_missing": "retain B_zero_flux",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "MSC919_4_universal_K",
            "required_statement": "K_BF_H is a parent level/coupling, universal and calibrated before data fitting",
            "why_needed": "a free coupling could hide fifth-force or GM-normalization errors",
            "current_evidence": "K_BF_H exists as a scorepack symbol only",
            "status": "not_parent_derived",
            "if_missing": "retain K_BF_H bound row",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "clause_id": "MSC919_5_no_species_source_charge",
            "required_statement": "J_Pi carries no material-marker, species, connection, boundary, range, or domain source charge",
            "why_needed": "mass-gauge coupling would otherwise create composition/source-channel dependence",
            "current_evidence": "one-coframe theorem is conditional and no-species contract remains open",
            "status": "not_parent_derived",
            "if_missing": "retain species_source_charge and WEP/source rows",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def no_cheat_rows() -> list[dict[str, object]]:
    return [
        {
            "test_id": "NCT919_0_no_on_shell_shell_game",
            "forbidden_shortcut": "use dJ=0 after matter equations to prove the coupling did not alter those equations",
            "why_forbidden": "circular variational logic",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "NCT919_1_no_flat_equals_exact",
            "forbidden_shortcut": "treat dA=0 as A=d lambda without checking compact holonomy",
            "why_forbidden": "flat connections can carry global charge/phase/boundary effects",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "NCT919_2_no_projector_after_readout",
            "forbidden_shortcut": "choose Pi_M after orbital readout and call d(Pi_M J_H)=0 a theorem",
            "why_forbidden": "post-hoc source normalization",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "NCT919_3_no_free_K_absorption",
            "forbidden_shortcut": "absorb K_BF_H into measured G or M_eff without parent calibration",
            "why_forbidden": "wrong-GM normalization can mimic a Newton pass",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "test_id": "NCT919_4_no_species_blind_assumption",
            "forbidden_shortcut": "assume one coframe automatically removes all source charge channels",
            "why_forbidden": "constants, boundary, connection, domain, range, and marker channels remain possible",
            "passes_as_claim": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def bound_rows() -> list[dict[str, object]]:
    return [
        {
            "bound_id": "FMB919_0_F_M_force",
            "symbol": "F_M_force",
            "residual_definition": "local matter/source force from K_BF_H A_M wedge delta(Pi_M J_H)",
            "formula_or_target": "F_M_force := |K_BF_H| ||A_M wedge delta J_Pi/delta psi|| in weak-field/local projection",
            "source_needed": "parent matter variation or local fifth-force/WEP projection",
            "arena": "WEP_PPN_clock_orbital_R10",
            "status": "MISSING_MATTER_VARIATION",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "bound_id": "FMB919_1_K_BF_H",
            "symbol": "K_BF_H",
            "residual_definition": "mass-gauge/Hilbert source coupling level",
            "formula_or_target": "coefficient of A_M wedge Pi_M J_H",
            "source_needed": "parent level/coupling coefficient and units",
            "arena": "R10_PPN_clock_orbital",
            "status": "MISSING_PARENT_COUPLING",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "bound_id": "FMB919_2_A_M_holonomy",
            "symbol": "A_M_holonomy",
            "residual_definition": "nontrivial flat mass-gauge holonomy on compact local cycles",
            "formula_or_target": "max_gamma |integral_gamma A_M|",
            "source_needed": "topology/relative cohomology theorem or bound",
            "arena": "R10_clock_orbital_boundary",
            "status": "MISSING_HOLONOMY_ZERO",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "bound_id": "FMB919_3_dPiMJ_leak",
            "symbol": "dPiMJ_leak",
            "residual_definition": "off-shell projected mass-current closure leakage",
            "formula_or_target": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "source_needed": "off-shell current identity and parent-owned Pi_M",
            "arena": "Newton_PPN_orbital_source_normalization",
            "status": "MISSING_OFFSHELL_CLOSURE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "bound_id": "FMB919_4_boundary_flux",
            "symbol": "B_zero_flux",
            "residual_definition": "boundary term from integrating exact A_M coupling by parts",
            "formula_or_target": "integral_boundary lambda_M Pi_M J_H and variation",
            "source_needed": "zero-flux theorem or boundary source bound",
            "arena": "R10_orbital_PPN",
            "status": "MISSING_ZERO_BOUNDARY_FLUX",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "bound_id": "FMB919_5_species_source_charge",
            "symbol": "species_source_charge",
            "residual_definition": "species/marker dependence of the mass-gauge source current",
            "formula_or_target": "partial_A ln(K_BF_H J_Pi/M_inertial)",
            "source_needed": "no-species source-charge theorem or WEP/source-channel bounds",
            "arena": "WEP_source_charge_clock",
            "status": "MISSING_NO_SPECIES_SOURCE_THEOREM",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD919_0_silence_lemma",
            "branch": "derive",
            "verdict": "conditional_theorem_written",
            "reason": "exact A_M plus off-shell closed J_Pi plus zero boundary flux would make the coupling silent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD919_1_current_corpus",
            "branch": "audit",
            "verdict": "not_parent_signed",
            "reason": "current sources provide same-coframe/Ward support but not off-shell projected-current closure or holonomy zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD919_2_bound_runner",
            "branch": "fallback",
            "verdict": "F_M_bound_rows_retained",
            "reason": "if any proof clause stays open, the coupling becomes an executable local-force/source residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE919_0_strong_silence",
            "claim": "A_M wedge Pi_M J_H is action-level silent",
            "blocker": "exact A_M, off-shell dJ_Pi=0, zero boundary flux, and universal K_BF_H are not all parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE919_1_no_fifth_force",
            "claim": "mass-gauge source coupling creates no local fifth force",
            "blocker": "matter variation is not zero unless the strong silence lemma closes",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE919_2_no_species_charge",
            "claim": "coupling is species/source-channel blind",
            "blocker": "one-coframe and Ward current results remain conditional and do not close all source channels",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE919_3_Newton_PPN_local_GR",
            "claim": "coupling route supports Newton/PPN/local-GR pass",
            "blocker": "projected current closure, charge calibration, first-class algebra, and local-force bounds remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to parent-sign off-shell closure d(Pi_M J_H)=0 and exact/zero-holonomy A_M; if not, make F_M_force and K_BF_H source-ready bound-runner rows",
            "include": "projector commutator, off-shell Ward identity, compact holonomy, boundary flux, K_BF_H units, weak-field force projection",
            "exclude": "on-shell-only Ward shortcut, flat-equals-exact shortcut, free coupling absorption, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    count = 0
    for path in formalization.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    for row in rows:
        for field in fields:
            if str(row.get(field, "")).strip().lower() == "true":
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    variations: list[dict[str, object]],
    clauses: list[dict[str, object]],
    no_cheat: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_path = OUT / "P8_Y5_BRR545_918_VALIDATION.csv"
    prior_ok = prior_path.exists() and "V918_11_validation_rows_ready" in read_text(prior_path)
    false_fields = ("claim_allowed", "valid_for_claim", "passes_as_claim", "score_ready")
    bound_symbols = {row["symbol"] for row in bounds}
    required_symbols = {"F_M_force", "K_BF_H", "A_M_holonomy", "dPiMJ_leak", "B_zero_flux", "species_source_charge"}
    generated_sets = lemmas + variations + clauses + no_cheat + bounds + decisions + gates
    changed_count = formalization_changed_count()
    rows = [
        {
            "check_id": "V919_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_1_prior_918_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_918_VALIDATION.csv clean" if prior_ok else "918 validation missing or incomplete",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_2_silence_lemma_conditional_only",
            "result": "pass" if all_false(lemmas, false_fields) else "fail",
            "detail": "silence theorem shape written but no claim field is true",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_3_variation_cases_guarded",
            "result": "pass" if all_false(variations, false_fields) else "fail",
            "detail": "strong, on-shell, holonomy, projector, and species cases remain guarded",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_4_missing_clauses_explicit",
            "result": "pass" if all(row["status"] == "not_parent_derived" for row in clauses) else "fail",
            "detail": "all strong-silence proof clauses remain explicitly unsigned",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_5_no_cheat_tests_block_claim",
            "result": "pass" if all_false(no_cheat, false_fields) else "fail",
            "detail": "on-shell Ward, flat-equals-exact, projector readout, free K, and species shortcuts are blocked",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_6_bound_rows_nonclaim",
            "result": "pass" if all_false(bounds, false_fields) and required_symbols <= bound_symbols else "fail",
            "detail": "all required coupling residual rows exist and remain nonclaim",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_7_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "all silence/no-fifth-force/Newton/PPN/local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_8_branch_decision_nonclaim",
            "result": "pass" if all_false(decisions, false_fields) else "fail",
            "detail": "decision selects off-shell closure/holonomy target without promotion",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_9_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated_sets, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_10_formalization_workbench_untouched",
            "result": "pass" if changed_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed_count}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_11_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("920-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V919_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]
    return rows


def write_doc(
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    variations: list[dict[str, object]],
    clauses: list[dict[str, object]],
    no_cheat: list[dict[str, object]],
    bounds: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 919 - Y5/R10 Matter-Current Silence Lemma Or DeltaHT Bound Runner

Private coupling checkpoint. This is not a public R10, WEP, fifth-force, Newton, PPN, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the coupling can be made silent by a real theorem, but the current corpus has not proved the theorem yet.**

The candidate coupling is:

```text
S_int = K_BF_H integral_D A_M wedge J_Pi,
J_Pi := Pi_M J_H.
```

The exact route is:

```text
A_M = d lambda_M
S_int = K_BF_H integral_boundary lambda_M J_Pi - K_BF_H integral_D lambda_M dJ_Pi.
```

Therefore `S_int` is locally silent only if the compact boundary term vanishes/fixes to a universal background and `dJ_Pi=0` is an off-shell parent identity, not merely an on-shell Ward fact. This is the clean version of the coupling problem: prove exact/off-shell/boundary silence, or score the remaining term as `F_M_force`.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "what_improved", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Silence Lemma Attempt

{md_table(lemmas, ["lemma_id", "claim", "derivation", "required_clause", "current_status", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Variation Case Audit

{md_table(variations, ["case_id", "case", "matter_variation", "force_readout", "status", "passes_as_claim", "valid_for_claim", "generated_utc"])}

## Missing Proof Clauses

{md_table(clauses, ["clause_id", "required_statement", "why_needed", "current_evidence", "status", "if_missing", "valid_for_claim", "generated_utc"])}

## No-Cheat Tests

{md_table(no_cheat, ["test_id", "forbidden_shortcut", "why_forbidden", "passes_as_claim", "valid_for_claim", "generated_utc"])}

## Force Bound Runner Rows

{md_table(bounds, ["bound_id", "symbol", "residual_definition", "formula_or_target", "source_needed", "arena", "status", "score_ready", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = build_sources()
    summary = summary_rows()
    lemmas = lemma_rows()
    variations = variation_rows()
    clauses = proof_clause_rows()
    no_cheat = no_cheat_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(sources, lemmas, variations, clauses, no_cheat, bounds, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_919_SOURCE_REGISTER.csv", sources, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "what_improved", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_SILENCE_LEMMA_ATTEMPT.csv", lemmas, ["lemma_id", "claim", "derivation", "required_clause", "current_status", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_VARIATION_CASE_AUDIT.csv", variations, ["case_id", "case", "matter_variation", "force_readout", "status", "passes_as_claim", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_MISSING_PROOF_CLAUSES.csv", clauses, ["clause_id", "required_statement", "why_needed", "current_evidence", "status", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_NO_CHEAT_TESTS.csv", no_cheat, ["test_id", "forbidden_shortcut", "why_forbidden", "passes_as_claim", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_FORCE_BOUND_RUNNER_ROWS.csv", bounds, ["bound_id", "symbol", "residual_definition", "formula_or_target", "source_needed", "arena", "status", "score_ready", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_919_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_919_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])

    write_doc(sources, summary, lemmas, variations, clauses, no_cheat, bounds, decisions, gates, next_target, validation)
    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
