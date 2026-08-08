from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    literal = str(FORMALIZATION).replace("'", "''")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + literal
        + "' -Recurse -File | Where-Object { $_.LastWriteTime -gt $since } | Measure-Object).Count; "
        + "Write-Output $count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    try:
        return int(completed.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return -2


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "965_doc",
            "path": "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
            "role": "immediate handoff: generator elimination selected as next hinge",
            "needle": "DEC965_3_next_hinge",
        },
        {
            "source_id": "414_invariant_algebra",
            "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
            "role": "exact local invariant algebra burden and generator list",
            "needle": "I_loc(Q) = I_geom[J^k(e_obs)] tensor constants",
        },
        {
            "source_id": "415_local_class",
            "path": "415-local-trivial-class-selector-theorem-attempt.md",
            "role": "relative/domain class conditional zero theorem and missing selector gates",
            "needle": "physical_local_class_selector_derived",
        },
        {
            "source_id": "416_domain_selector",
            "path": "416-binding-invariant-domain-selector-repair.md",
            "role": "Cexp/chi_D auxiliary selector route and Bianchi blockers",
            "needle": "parent_selector_derived",
        },
        {
            "source_id": "417_boundary_exchange",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "boundary exchange and memory no-hair blockers",
            "needle": "boundary_exchange_nohair_derived",
        },
        {
            "source_id": "421_finite_fibre",
            "path": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
            "role": "finite-cell fibre spectrum decoupling theorem attempt",
            "needle": "finite_cell_fibre_spectrum",
        },
        {
            "source_id": "422_readout",
            "path": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
            "role": "readout-after-variation no-cheat theorem contract",
            "needle": "readout_after_variation_contract_written",
        },
        {
            "source_id": "953_species_functor",
            "path": "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md",
            "role": "conditional no-species-label source functor theorem",
            "needle": "NSF953_5_verdict",
        },
        {
            "source_id": "955_minimal_matter",
            "path": "955-Y5-R10-minimal-matter-action-source-coupling-lemma-or-species-weight-residual-runner.md",
            "role": "minimal matter action/no-source-prefactor lemma contract",
            "needle": "MMA955_6_verdict",
        },
        {
            "source_id": "963_no_extra_scalar",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "no-marker/no-extra-scalar and R2/fR finite branch blocker",
            "needle": "NES963_4_no_marker_extension",
        },
        {
            "source_id": "573_generator_debt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
            "role": "prior invariant-generator debt ledger",
            "needle": "IG573_5_readout_projector",
        },
        {
            "source_id": "574_generator_attempts",
            "path": "source-intake/mts_residuals/P8_Y5_R10_574_GENERATOR_ELIMINATION_ATTEMPTS.csv",
            "role": "prior generator elimination attempt forms",
            "needle": "GE574_0_readout_projector",
        },
    ]
    rows = []
    for spec in specs:
        absolute_path = source_path(spec["path"])
        exists = absolute_path.exists()
        needle_found = spec["needle"] in read_text(absolute_path) if exists else False
        rows.append(
            {
                **spec,
                "absolute_path": str(absolute_path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def generator_elimination_ledger() -> list[dict[str, str]]:
    specs = [
        {
            "rank": 1,
            "generator_id": "GE966_0_readout_projector",
            "generator": "post-readout projector",
            "attempted_elimination": "define readout only as R_read: Sol(S_parent)->Obs and forbid readout-selected reduced actions from being varied",
            "conditional_theorem": "if P_read is not an argument of S_parent, delta S_parent/delta P_read is undefined/zero by domain and no source term can be produced",
            "current_status": "schema_lock_candidate_not_parent_signed",
            "blocker": "parent action domain and no-reduced-action-backreaction theorem have not been signed",
            "residual_if_fails": "R0/R11 closure-zero can re-enter as a reduced-action source",
            "unlock_if_closed": "removes the fastest hidden projector loophole before source and fibre proofs",
        },
        {
            "rank": 2,
            "generator_id": "GE966_1_species_constants",
            "generator": "species/source constants",
            "attempted_elimination": "use one total matter functional on one observed coframe and take the total Hilbert/coframe derivative",
            "conditional_theorem": "if species labels and source-only prefactors are absent from the source functor domain, only one common kappa_univ can multiply T_total",
            "current_status": "conditional_uniqueness_not_parent_signed",
            "blocker": "relative prefactors w_A and hidden source spurions are still legal unless parent schema forbids extra slots",
            "residual_if_fails": "WEP/source-normalization/clock residuals via beta_source_normalized or epsilon_A",
            "unlock_if_closed": "collapses relative source coupling to one calibrated common mode",
        },
        {
            "rank": 3,
            "generator_id": "GE966_2_relative_domain_class",
            "generator": "relative boundary/domain class",
            "attempted_elimination": "selected stationary local domain plus trivial relative cohomology and zero boundary exchange",
            "conditional_theorem": "if D is parent-selected, H_rel(D,dD)=0/no-defect holds, and boundary exchange is exact/zero, then Q_rel=[J_rel]=0 locally",
            "current_status": "conditional_zero_class_not_selector_derived",
            "blocker": "parent domain selector, topology/no-defect premise, and boundary exchange no-hair are not derived",
            "residual_if_fails": "domain/source class marker and boundary charge rows remain retained",
            "unlock_if_closed": "removes the local relative class from I_loc(Q_MTS)",
        },
        {
            "rank": 4,
            "generator_id": "GE966_3_domain_selector",
            "generator": "chi_D/domain selector",
            "attempted_elimination": "promote C_exp/C_coh to an auxiliary or topological selector with no local stress",
            "conditional_theorem": "if E_chi=0 selects D before scoring and T_chi is topological or Bianchi-cancelled, chi_D is not a matter-visible generator",
            "current_status": "best_contract_not_parent_derived",
            "blocker": "candidate domains, epsilon/threshold origin, and Bianchi boundary ownership remain open",
            "residual_if_fails": "preferred-frame/domain projector/source normalization leakage",
            "unlock_if_closed": "gives a non-posthoc local/FLRW branch separator",
        },
        {
            "rank": 5,
            "generator_id": "GE966_4_memory_class_scalar",
            "generator": "memory/class scalar",
            "attempted_elimination": "positive-operator local silence lemma in the selected local exterior",
            "conditional_theorem": "if L_X=-nabla^2+m_X^2 is positive, J_X=0 in the compact local branch, and boundary data are zero/topological, then int(|grad X|^2+m_X^2 X^2)=0 and X=0",
            "current_status": "lemma_shape_written_inputs_unsigned",
            "blocker": "parent L_X, source term J_X, boundary conditions, and coupling to chi_D are not derived",
            "residual_if_fails": "clock drift, Gdot, gamma, R10 finite scalar, or non-EH prefactor",
            "unlock_if_closed": "kills the local scalar hair route without a plateau axiom",
        },
        {
            "rank": 6,
            "generator_id": "GE966_5_finite_fibre_spectrum",
            "generator": "finite-cell fibre spectrum",
            "attempted_elimination": "unique gapped stationary fibre solution h0, source-independent and integrated out to universal constants",
            "conditional_theorem": "if delta S/delta h=0 has a unique source-independent h0 and no matter vertex to fluctuations, spec(h) renormalizes constants only",
            "current_status": "not_decoupled_depends_on_matter_blindness",
            "blocker": "no parent fibre potential, mass gap, uniqueness theorem, or h-blind matter functor is signed",
            "residual_if_fails": "composition charge, finite-range scalar, or local source dial",
            "unlock_if_closed": "removes the hardest quotient-invariant scalar generator",
        },
        {
            "rank": 7,
            "generator_id": "GE966_6_orientation_time_arrow",
            "generator": "orientation/time-arrow marker",
            "attempted_elimination": "classify orientation as part of observed coframe/spin structure or as a constant discrete superselection datum",
            "conditional_theorem": "if the arrow is contained in e_obs or is a nondynamical global orientation with no local stress/current, it adds no independent local generator",
            "current_status": "classified_conditional_dynamic_arrow_not_excluded",
            "blocker": "dynamic torsion/vector/time-arrow residual has not been excluded by the parent connection sector",
            "residual_if_fails": "preferred-frame, parity/time-asymmetry, or torsion residual rows",
            "unlock_if_closed": "keeps orientation from becoming a hidden PPN/preferred-frame source",
        },
        {
            "rank": 8,
            "generator_id": "GE966_7_verdict",
            "generator": "I_loc(Q_MTS) generator set",
            "attempted_elimination": "combine the seven eliminations into I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor universal constants",
            "conditional_theorem": "all non-geometric generators must be absent, pure gauge, topological/no-stress, universal constants, or explicitly retained",
            "current_status": "NOT_ELIMINATED_CURRENT_CORPUS",
            "blocker": "several conditional contracts exist, but no parent schema signs all premises",
            "residual_if_fails": "local-GR derivation remains closure/residual rather than theorem-zero",
            "unlock_if_closed": "would activate the no-marker side of the local GR/Newton route",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "claim_allowed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def dependency_graph() -> list[dict[str, str]]:
    specs = [
        ("DG966_0", "readout-after-variation schema", "matter/source factorization", "prevents reduced-action projectors from creating fake parent source terms", "schema proof target"),
        ("DG966_1", "no source-only species prefactors", "species/source constant universality", "removes kappa_A/kappa_B as admissible active source data", "parent matter schema target"),
        ("DG966_2", "parent-selected chi_D/domain", "relative boundary/domain class triviality", "turns fixed local class closure into a selected local branch", "selector theorem target"),
        ("DG966_3", "Bianchi-safe chi_D and boundary ownership", "memory/class scalar silence", "stops T_memory grad chi_D and exchange currents from sourcing local hair", "no-hair theorem target"),
        ("DG966_4", "matter blindness and species universality", "finite fibre decoupling", "prevents spec(h) from becoming a matter/source dial after integration", "fibre theorem target"),
        ("DG966_5", "connection/torsion silence", "orientation/time-arrow classification", "decides whether the arrow is geometry-contained or a preferred-frame residual", "connection theorem target"),
        ("DG966_6", "all generator eliminations", "local invariant algebra triviality", "only observed geometry and universal constants remain", "local-GR prerequisite"),
        ("DG966_7", "R2/fR finite branch input", "R2/fR curve digitizer usefulness", "curve data are only useful after an actual MTS finite alpha/lambda prediction exists", "defer digitizer"),
    ]
    rows = []
    for edge_id, prerequisite, dependent, reason, status in specs:
        rows.append(
            {
                "edge_id": edge_id,
                "prerequisite": prerequisite,
                "dependent": dependent,
                "reason": reason,
                "status": status,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def partial_theorem_contracts() -> list[dict[str, str]]:
    specs = [
        {
            "contract_id": "PTC966_0_readout_domain",
            "contract": "R_read: Sol(S_parent)->Obs only after variation",
            "proof_value": "turns readout into an observational map rather than an action variable",
            "missing_signature": "parent action domain excludes P_read and no reduced EFT is varied",
            "if_signed": "post-readout projector generator eliminated",
            "if_unsigned": "closure-zero remains policy only",
        },
        {
            "contract_id": "PTC966_1_single_matter_functional",
            "contract": "S_matter is one total functional of one observed coframe with no source-only species weights",
            "proof_value": "total Hilbert derivative yields T_total and one calibrated kappa_univ",
            "missing_signature": "no independent w_A slots and no hidden source spurions",
            "if_signed": "relative species/source constants eliminated from the source side",
            "if_unsigned": "epsilon_A/beta_source_normalized retained",
        },
        {
            "contract_id": "PTC966_2_zero_class",
            "contract": "selected local D, trivial H_rel, exact/zero boundary exchange",
            "proof_value": "Q_rel=[J_rel]=0 in the local branch",
            "missing_signature": "parent selector, topology/no-defect, and exchange no-hair",
            "if_signed": "relative/domain class generator eliminated",
            "if_unsigned": "fixed-class closure only",
        },
        {
            "contract_id": "PTC966_3_positive_memory_operator",
            "contract": "positive L_X with zero source and zero/topological boundary data",
            "proof_value": "energy identity forces X=0 and grad X=0 without a plateau axiom",
            "missing_signature": "actual parent L_X, J_X=0, boundary conditions, and chi_D coupling",
            "if_signed": "memory/class scalar local hair eliminated",
            "if_unsigned": "clock/Gdot/R10 scalar rows retained or bounded",
        },
        {
            "contract_id": "PTC966_4_unique_fibre_ground_state",
            "contract": "unique source-independent gapped h0 and no matter vertex to fibre fluctuations",
            "proof_value": "finite fibre spectra renormalize constants only",
            "missing_signature": "parent fibre potential, mass gap, uniqueness, and h-blind matter functor",
            "if_signed": "finite-cell fibre generator eliminated",
            "if_unsigned": "finite fibre remains a scalar/source dial",
        },
        {
            "contract_id": "PTC966_5_geometry_contained_arrow",
            "contract": "orientation/time arrow is contained in observed coframe/spin structure or a global discrete datum",
            "proof_value": "no independent local preferred-frame or parity/time source",
            "missing_signature": "dynamic connection/torsion/vector arrow exclusion",
            "if_signed": "orientation marker removed from I_loc",
            "if_unsigned": "preferred-frame residual remains",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "parent_signed": "false", "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def closure_or_residual_router() -> list[dict[str, str]]:
    specs = [
        ("ROUT966_0_readout_projector", "post-readout projector", "parent_schema_theorem_or_policy_closure", "R0/R11 no-cheat closure rows", "false"),
        ("ROUT966_1_species_constants", "species/source constants", "parent_no_prefactor_theorem_or_residual_runner", "epsilon_A beta_source_normalized WEP/source bounds", "false"),
        ("ROUT966_2_relative_class", "relative boundary/domain class", "selected_zero_class_theorem_or_fixed_class_closure", "domain/source class residual and boundary charge", "false"),
        ("ROUT966_3_chiD_selector", "chi_D/domain selector", "Bianchi_safe_auxiliary_theorem_or_retained_selector", "preferred-frame/domain projector residual", "false"),
        ("ROUT966_4_memory_scalar", "memory/class scalar", "positive_operator_zero_theorem_or_scalar_bound", "clock/Gdot/R10 scalar bound rows", "false"),
        ("ROUT966_5_finite_fibre", "finite-cell fibre spectrum", "unique_h0_decoupling_theorem_or_finite_scalar_runner", "composition/fifth-force finite-fibre residual", "false"),
        ("ROUT966_6_orientation_arrow", "orientation/time-arrow marker", "geometry_containment_theorem_or_connection_residual", "PPN preferred-frame/torsion residual", "false"),
    ]
    rows = []
    for router_id, generator, route, retained_row, claim_allowed in specs:
        rows.append(
            {
                "router_id": router_id,
                "generator": generator,
                "route_if_theorem_fails": route,
                "retained_row_or_bound_target": retained_row,
                "claim_allowed": claim_allowed,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def r2fr_curve_digitizer_decision() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "R2DIG966_0_selected_route",
            "topic": "R2/fR curve digitizer",
            "decision": "defer_digitizer_this_checkpoint",
            "reason": "derivation-first still dominates: without parent-sourced MTS alpha/lambda or a signed finite scalar branch, a full curve cannot score MTS",
            "future_trigger": "run digitizer only after a finite R2/fR or MTS scalar row has numeric alpha_predicted and lambda_predicted with sources",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "R2DIG966_1_data_policy",
            "topic": "Lee2020 full curve",
            "decision": "keep_full_curve_required_nonclaim",
            "reason": "anchor-only thresholds are provenance and smoke data, not scoring rows",
            "future_trigger": "digitize or source machine-readable alpha(lambda) rows before any retained finite-branch comparison",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def claim_gates() -> list[dict[str, str]]:
    specs = [
        ("CGATE966_0_local_invariant_algebra", "I_loc(Q_MTS)=I_geom plus constants", "all non-geometric generators eliminated", "not_eliminated"),
        ("CGATE966_1_no_marker_theorem", "no-natural-marker theorem", "primitive quotient and generator elimination parent-signed", "not_proven"),
        ("CGATE966_2_readout_projector", "readout projector removed as parent source", "readout-after-variation parent schema theorem", "contract_only"),
        ("CGATE966_3_species_constants", "species/source constants universalized", "no-source-prefactor parent lemma signed", "contract_only"),
        ("CGATE966_4_memory_fibre_scalar", "memory/fibre scalar local silence", "positive operator and unique h0 theorems signed", "not_proven"),
        ("CGATE966_5_R2FR_curve_score", "R2/fR finite branch score", "numeric MTS alpha/lambda plus full bound curve", "not_ready"),
        ("CGATE966_6_local_GR", "local GR/Newton/PPN promotion", "no-marker, same-frame EH/source, and residual closure all pass", "not_proven"),
    ]
    rows = []
    for gate_id, claim, required, evidence in specs:
        rows.append(
            {
                "gate_id": gate_id,
                "claim": claim,
                "required_condition": required,
                "current_evidence": evidence,
                "gate_pass": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    specs = [
        (
            "DEC966_0_generator_audit",
            "local invariant generator elimination",
            "not_closed_but_ranked",
            "seven generators were attacked with exact conditional contracts; none is parent-signed enough for theorem-zero",
            "go after the smallest high-leverage lock: readout-after-variation as a parent schema theorem",
        ),
        (
            "DEC966_1_new_math_gain",
            "memory/class scalar route",
            "positive_operator_zero_lemma_shape_written",
            "the cleanest non-plateau way to kill local scalar hair is an energy identity, but parent operator/source/boundary data are missing",
            "derive or reject the parent positive operator and boundary conditions after readout is locked",
        ),
        (
            "DEC966_2_data_route",
            "R2/fR full curve",
            "deferred_nonclaim",
            "curve digitization is useful only after the retained finite branch has sourced alpha/lambda inputs",
            "do not spend claim energy on data plumbing until a finite branch actually exists",
        ),
        (
            "DEC966_3_project_status",
            "local GR route",
            "still_alive_not_claimed",
            "the obstruction is no longer woolly; it is a finite ordered list of parent-schema locks and no-hair theorems",
            "try to actually remove one generator next, starting with the readout projector",
        ),
    ]
    rows = []
    for decision_id, topic, result, reason, next_action in specs:
        rows.append(
            {
                "decision_id": decision_id,
                "topic": topic,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
            "objective": "try to remove the first generator for real: prove readout is outside the parent action domain and cannot be varied as a reduced EFT source; if that closes, move to the positive-operator local memory-silence lemma",
            "include": "parent action domain; solution-space readout map; no reduced-action backreaction; chain-rule source silence; memory positive operator fallback",
            "exclude": "local-GR claim, invented coefficients, R2/fR curve claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    generator_rows: list[dict[str, str]],
    dependency_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    router_rows: list[dict[str, str]],
    digitizer_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_paths_ok = all(row["exists"] == "true" for row in sources)
    source_needles_ok = all(row["needle_found"] == "true" for row in sources)
    attacked_count = sum(1 for row in generator_rows if row["generator_id"].startswith("GE966_") and row["generator_id"] != "GE966_7_verdict")
    verdict_not_eliminated = any(row["generator_id"] == "GE966_7_verdict" and row["current_status"] == "NOT_ELIMINATED_CURRENT_CORPUS" for row in generator_rows)
    no_generator_claims = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in generator_rows)
    dependency_ready = len(dependency_rows) >= 8 and all(row["valid_for_claim"] == "false" for row in dependency_rows)
    contracts_unsigned = len(contract_rows) >= 6 and all(row["parent_signed"] == "false" for row in contract_rows)
    router_nonclaim = len(router_rows) >= 7 and all(row["claim_allowed"] == "false" for row in router_rows)
    digitizer_deferred = any(row["decision"] == "defer_digitizer_this_checkpoint" and row["claim_allowed"] == "false" for row in digitizer_rows)
    no_claim_gates = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in decision_rows)
    target_written = bool(target_rows) and target_rows[0]["valid_for_claim"] == "false"
    no_formalization_edits = formalization_changed_after_start() == 0
    rows = []
    checks = [
        ("V966_0_source_paths_exist", source_paths_ok, "all cited local source paths exist"),
        ("V966_1_source_needles_found", source_needles_ok, "all source needles found"),
        ("V966_2_generators_attacked", attacked_count >= 7, f"{attacked_count} non-geometric generators attacked"),
        ("V966_3_verdict_not_overclaimed", verdict_not_eliminated, "local invariant algebra is explicitly not eliminated"),
        ("V966_4_no_generator_claims", no_generator_claims, "no generator elimination row is claim-allowed"),
        ("V966_5_dependency_graph_written", dependency_ready, "dependency graph covers generator ordering and digitizer deferral"),
        ("V966_6_contracts_unsigned", contracts_unsigned, "partial theorem contracts remain unsigned parent clauses"),
        ("V966_7_router_nonclaim", router_nonclaim, "closure/residual router keeps all rows nonclaim"),
        ("V966_8_digitizer_deferred_nonclaim", digitizer_deferred, "R2/fR digitizer deferred until finite MTS inputs exist"),
        ("V966_9_claim_gates_false", no_claim_gates, "all claim gates are false"),
        ("V966_10_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim"),
        ("V966_11_next_target_written", target_written, "967 next target selected"),
        ("V966_12_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "check_id": "V966_13_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "966 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    generator_rows: list[dict[str, str]],
    dependency_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    router_rows: list[dict[str, str]],
    digitizer_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 966 Y5 R10: Local Invariant Generator Elimination Or R2/fR Curve Digitizer

Status: `Y5_R10_966_local_invariant_generators_ranked_not_eliminated_R2FR_digitizer_deferred_nonclaim`

Claim ceiling: no local invariant algebra triviality, no no-marker theorem, no R2/fR finite branch score, no R10 pass, no PPN pass, no EH/Newton/local-GR claim is made.

## Readout

This checkpoint attacks the surviving generators instead of waving at "coupling" as a fog bank. The result is useful but not yet a win: every dangerous generator now has an exact kill route, a blocker, and a residual route, but none is parent-signed enough to remove it from `I_loc(Q_MTS)`.

The most promising next tactical lock is the readout projector. If readout can be made a map on solution space only, not a variable or reduced action inside `S_parent`, then one generator can genuinely drop out. The next-best math move after that is the positive-operator memory lemma: kill local scalar hair by an energy identity rather than a plateau axiom.

R2/fR curve digitization is deliberately deferred. The full curve is still required for a finite branch, but a curve cannot score MTS until the parent produces numeric alpha/lambda inputs. Tiny gremlin door remains shut.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Generator Elimination Ledger

{md_table(generator_rows, ["rank", "generator_id", "generator", "current_status", "blocker", "unlock_if_closed"])}

## Dependency Graph

{md_table(dependency_rows, ["edge_id", "prerequisite", "dependent", "reason", "status"])}

## Partial Theorem Contracts

{md_table(contract_rows, ["contract_id", "contract", "proof_value", "missing_signature", "if_signed", "if_unsigned"])}

## Closure Or Residual Router

{md_table(router_rows, ["router_id", "generator", "route_if_theorem_fails", "retained_row_or_bound_target", "claim_allowed"])}

## R2/fR Curve Digitizer Decision

{md_table(digitizer_rows, ["decision_id", "topic", "decision", "reason", "future_trigger"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    generator_rows = generator_elimination_ledger()
    dependency_rows = dependency_graph()
    contract_rows = partial_theorem_contracts()
    router_rows = closure_or_residual_router()
    digitizer_rows = r2fr_curve_digitizer_decision()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        generator_rows,
        dependency_rows,
        contract_rows,
        router_rows,
        digitizer_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_966_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER.csv",
        generator_rows,
        [
            "rank",
            "generator_id",
            "generator",
            "attempted_elimination",
            "conditional_theorem",
            "current_status",
            "blocker",
            "residual_if_fails",
            "unlock_if_closed",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_DEPENDENCY_GRAPH.csv",
        dependency_rows,
        ["edge_id", "prerequisite", "dependent", "reason", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_PARTIAL_THEOREM_CONTRACTS.csv",
        contract_rows,
        ["contract_id", "contract", "proof_value", "missing_signature", "if_signed", "if_unsigned", "parent_signed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_CLOSURE_OR_RESIDUAL_ROUTER.csv",
        router_rows,
        ["router_id", "generator", "route_if_theorem_fails", "retained_row_or_bound_target", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_R2FR_CURVE_DIGITIZER_DECISION.csv",
        digitizer_rows,
        ["decision_id", "topic", "decision", "reason", "future_trigger", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_966_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_966_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, generator_rows, dependency_rows, contract_rows, router_rows, digitizer_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
