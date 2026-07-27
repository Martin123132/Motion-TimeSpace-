from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "938-Y5-R10-extra-omega-vertical-degeneracy-or-CbetaN5-source-row.md"
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
            "source_id": "937_doc",
            "path": "937-Y5-R10-parent-omega-Delta-symp-zero-or-N5-beta-source-row-fill.md",
            "role": "immediate handoff selecting extra omega vertical degeneracy",
            "needle": "i_tau omega_extra = d b_tau",
        },
        {
            "source_id": "937_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_937_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V937_14_validation_rows_ready",
        },
        {
            "source_id": "937_sector_omega",
            "path": "source-intake/mts_residuals/P8_Y5_R10_937_SECTOR_OMEGA_TABLE.csv",
            "role": "sector list for omega_extra",
            "needle": "OME937_2_projector_PiM",
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
            "role": "projector omega zero route clauses",
            "needle": "integral_S i_tau omega_projector = 0",
        },
        {
            "source_id": "914_doc",
            "path": "914-Y5-R10-topological-absolute-PiM-parent-clause-or-projector-source-bound-pack.md",
            "role": "absolute topological PiM route",
            "needle": "delta_g Pi_M = 0",
        },
        {
            "source_id": "916_doc",
            "path": "916-Y5-R10-parent-BF-mass-current-sector-or-Delta-HT-bound-input.md",
            "role": "BF mass-current candidate",
            "needle": "S_BF,M =",
        },
        {
            "source_id": "918_doc",
            "path": "918-Y5-R10-nonpropagating-mass-gauge-constraint-sector-or-DeltaHT-scorepack.md",
            "role": "coupling blocker for BF/source sector",
            "needle": "The problem is the coupling",
        },
        {
            "source_id": "919_doc",
            "path": "919-Y5-R10-matter-current-silence-lemma-or-DeltaHT-bound-runner.md",
            "role": "strong silence lemma clauses",
            "needle": "off-shell parent identity",
        },
        {
            "source_id": "920_doc",
            "path": "920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md",
            "role": "off-shell closure product-rule obstruction",
            "needle": "d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M] J_H.",
        },
        {
            "source_id": "local_beta_bound",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "R4 beta observation row",
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


def vertical_theorem_contract() -> list[dict[str, str]]:
    specs = [
        (
            "VTC938_0_parent_action_sectorization",
            "parent action splits into EH plus constrained/topological extra sectors",
            "S_parent = S_EH[g] + sum_A S_A[z_A,g;lambda_A] + S_matter[Psi,e_obs]",
            "needed so omega_extra has owned sector pieces rather than post-fit readout masks",
            "not_parent_signed",
        ),
        (
            "VTC938_1_vertical_generators",
            "each extra sector has an owned vertical generator",
            "delta_v z_A = R_A epsilon_A, delta_v g=0 or E_g-proportional",
            "makes extra-sector motion gauge/topological rather than physical local stress",
            "not_parent_signed",
        ),
        (
            "VTC938_2_presymplectic_degeneracy",
            "vertical generator lies in presymplectic kernel up to an exact flux",
            "i_{delta_v} omega_A = d b_A + E_A terms",
            "is the mathematical core of Delta_symp_A=0 on shell",
            "not_parent_signed",
        ),
        (
            "VTC938_3_zero_compact_flux",
            "exact flux integrates to zero on the compact local surface",
            "int_S d b_A = 0",
            "prevents a pure-gauge statement from hiding a boundary/corner mass",
            "not_parent_signed",
        ),
        (
            "VTC938_4_source_coupling_silence",
            "extra-sector source couplings do not vary matter/source equations",
            "delta S_extra/delta Psi = 0 or is an owned Ward/Gauss constraint",
            "blocks fifth-force/source-distortion leakage",
            "not_parent_signed",
        ),
        (
            "VTC938_5_same_source_calibration",
            "the resulting Hamiltonian charge is the measured source mass",
            "H_tau^MTS = G_eff M_eff[Pi_M J_H] in one readout/worldtube frame",
            "connects the theorem to Newton/PPN rather than only formal charge conservation",
            "not_parent_signed",
        ),
        (
            "VTC938_6_total_theorem",
            "if VTC938_0 through VTC938_5 hold sector-by-sector, Delta_symp_extra=0",
            "sum_A int_S i_tau omega_A = sum_A int_S d b_A = 0",
            "would let Pi_M^H inherit the GR Hamiltonian integrability branch",
            "conditional_theorem_not_current_claim",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "statement": statement,
            "mathematical_form": mathematical_form,
            "why_needed": why_needed,
            "current_status": current_status,
            "parent_signed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for clause_id, statement, mathematical_form, why_needed, current_status in specs
    ]


def sector_vertical_audit() -> list[dict[str, str]]:
    specs = [
        (
            "SVA938_0_matter_frame",
            "ordinary matter one-coframe",
            "compact-support local-vacuum degeneracy",
            "omega_matter_frame|_S=0 if matter support does not cross S and e_obs is the sole matter coframe",
            "plausible_conditional",
            "source support/worldtube and one-coframe ownership are not signed here",
            "medium",
        ),
        (
            "SVA938_1_projector_PiM",
            "Pi_M/projector/source-current selector",
            "absolute/Hamiltonian charge verticality",
            "delta_v Pi_M is gauge/representative change with delta_g Pi_M=0 and [d,Pi_M]J_H=0",
            "primary_blocker",
            "Pi_M is not yet parent-owned as absolute/Hamiltonian charge; source equality still missing",
            "critical",
        ),
        (
            "SVA938_2_BF_bulk",
            "pure BF/topological bulk",
            "topological gauge degeneracy",
            "S_BF=k int B wedge F gives omega_BF=delta B wedge delta A; gauge directions are degenerate up to boundary flux",
            "partial_positive_candidate",
            "bulk topological piece can be vertical, but source coupling/equality/level are not parent-derived",
            "high",
        ),
        (
            "SVA938_3_BF_source_coupling",
            "A_M wedge Pi_M J_H source coupling",
            "off-shell current closure silence",
            "d(Pi_M J_H)=0 off shell and A_M=d lambda_M with zero holonomy",
            "open_blocker",
            "product-rule term Pi_M dJ_H + [d,Pi_M]J_H is not zero by parent identity",
            "critical",
        ),
        (
            "SVA938_4_boundary_reference",
            "boundary/corner/reference",
            "fixed class and zero exact flux",
            "delta H_ref=0 and int_S d b_boundary=0",
            "open_blocker",
            "reference superselection and B_zero flux theorem missing",
            "high",
        ),
        (
            "SVA938_5_domain_selector",
            "domain/selector/homology",
            "class-only covariant selector",
            "delta domain is vertical relabeling, not physical preferred-boundary motion",
            "open_blocker",
            "fixed exterior/domain class and no readout-mask variation not signed",
            "high",
        ),
        (
            "SVA938_6_bulk_X_memory",
            "bulk X/memory",
            "no-hair/mass-gap degeneracy or bounded residual",
            "omega_X has no compact exterior support after X equation/no-hair theorem",
            "open_blocker",
            "X operator/theta/no-hair theorem not derived inside this branch",
            "medium",
        ),
        (
            "SVA938_7_source_normalization",
            "G_eff/M_eff/source normalization",
            "superselection and same-source calibration",
            "delta G_eff=0, delta k_M=0, H_tau=M_eff[Pi_M J_H]",
            "open_blocker",
            "Delta_cal and measured-GM calibration remain absent",
            "critical",
        ),
        (
            "SVA938_8_connection_torsion",
            "connection/torsion/nonmetricity",
            "auxiliary collapse to Levi-Civita",
            "connection equation algebraically sets nonmetricity/torsion residuals to zero",
            "open_blocker",
            "auxiliary connection no-hair/collapse theorem not signed here",
            "medium",
        ),
    ]
    return [
        {
            "sector_id": sector_id,
            "sector": sector,
            "candidate_vertical_route": candidate_vertical_route,
            "mathematical_form": mathematical_form,
            "status": status,
            "blocker": blocker,
            "priority": priority,
            "vertical_degeneracy_claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for sector_id, sector, candidate_vertical_route, mathematical_form, status, blocker, priority in specs
    ]


def partial_result_ledger() -> list[dict[str, str]]:
    return [
        {
            "result_id": "PRL938_0_good_news",
            "finding": "pure BF/topological bulk can be a legitimate vertical-degeneracy candidate",
            "meaning": "this supports the route aesthetically and mathematically; it is not silly closure-mud",
            "limit": "the source coupling A_M wedge Pi_M J_H reintroduces matter variation unless off-shell closure and zero holonomy are proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "result_id": "PRL938_1_bad_news",
            "finding": "the full omega_extra vertical theorem does not close",
            "meaning": "Delta_symp_extra cannot be set to zero from current corpus evidence",
            "limit": "projector ownership, coupling silence, boundary flux, and source calibration all remain live",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "result_id": "PRL938_2_best_next",
            "finding": "projector-PiM vertical generator is the next surgical target",
            "meaning": "if Pi_M itself becomes an owned vertical/Hamiltonian generator, several downstream blockers collapse together",
            "limit": "must not assume delta_g Pi_M=0 or [d,Pi_M]J_H=0; those are what must be proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def beta_bound_row() -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == "R4_beta":
            return row
    return {}


def cbeta_source_rows() -> list[dict[str, str]]:
    beta = beta_bound_row()
    beta_bound = beta.get("upper_bound", "")
    beta_source = beta.get("reference_path_or_url", "")
    specs = [
        (
            "CBN938_0_R4_beta_bound",
            "beta_minus_one_bound",
            beta_bound,
            "dimensionless",
            beta_source,
            "source observational envelope",
            "loaded",
            "true",
            "false",
        ),
        (
            "CBN938_1_C_beta_N5_definition",
            "C_beta_N5",
            "partial(beta-1)/partial epsilon_N5 evaluated on GR exterior branch",
            "dimensionless",
            "MISSING_SECOND_ORDER_WEAK_FIELD_SOLVER",
            "formal definition only",
            "definition_only",
            "false",
            "false",
        ),
        (
            "CBN938_2_X_N5_definition",
            "X_N5",
            "|Delta_projector + Delta_BF_source + Delta_boundary + Delta_domain + Delta_source| normalized by M_ref",
            "dimensionless",
            "MISSING_PARENT_NORMALIZED_RESIDUAL_PROFILE",
            "formal residual amplitude only",
            "definition_only",
            "false",
            "false",
        ),
        (
            "CBN938_3_score_formula",
            "beta_score_gate",
            "score_ready iff numeric C_beta_N5 and X_N5 exist and |C_beta_N5 X_N5| <= 7.8e-05",
            "dimensionless",
            "derived_gate_no_numeric_prediction",
            "claim remains blocked",
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
            "decision_id": "DEC938_0_vertical_theorem",
            "decision": "full_extra_omega_vertical_degeneracy_not_proved",
            "reason": "pure BF bulk has a clean vertical candidate, but projector ownership, source coupling silence, boundary flux, and calibration remain unsigned",
            "consequence": "Delta_symp_extra remains active and Pi_M^H is not yet parent-owned",
            "next_action": "attack projector-PiM vertical generator first",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC938_1_partial_positive",
            "decision": "BF_bulk_route_kept_as_candidate",
            "reason": "metric-free BF/topological bulk is the least ugly extra-sector mechanism for vertical degeneracy",
            "consequence": "do not throw away the coupling route, but keep it gated by off-shell closure and zero holonomy",
            "next_action": "carry BF source-coupling blocker into projector/source closure work",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC938_2_beta_fallback",
            "decision": "C_beta_N5_and_X_N5_defined_but_not_filled",
            "reason": "the observation bound is loaded, but prediction requires a second-order weak-field projection and source-normalized residual amplitude",
            "consequence": "no beta score; fallback is prepared only as a nonclaim schema",
            "next_action": "only fill beta coefficients if projector vertical proof stalls",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE938_0_extra_omega_vertical",
            "claim": "omega_extra is pure vertical/topological exact flux",
            "blocker": "only pure BF bulk is partially supported; projector/source/boundary/calibration clauses are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE938_1_Delta_symp_extra_zero",
            "claim": "Delta_symp_extra=0",
            "blocker": "sector vertical degeneracy and zero compact flux not proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE938_2_projector_vertical",
            "claim": "Pi_M/projector variation is an owned vertical generator",
            "blocker": "delta_g Pi_M=0, [d,Pi_M]J_H=0, and Pi_M^top/Pi_M^H equivalence remain unproved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE938_3_beta_score",
            "claim": "N5 beta row is scoreable",
            "blocker": "C_beta_N5 and X_N5 are formal definitions only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE938_4_local_GR",
            "claim": "local GR/Newton reduction follows",
            "blocker": "Delta_symp_extra, source normalization, and beta/PPN readout are still open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "939-Y5-R10-projector-PiM-vertical-generator-or-CbetaN5-weak-field-map.md",
            "objective": "prove Pi_M/projector variation is an owned vertical Hamiltonian/topological generator, or derive the weak-field C_beta_N5 map",
            "include": "delta_g Pi_M=0 conditions, [d,Pi_M]J_H chain-map proof, Pi_M^top/Pi_M^H zero-flux equivalence, source equality handoff, fallback C_beta_N5 weak-field definition",
            "exclude": "assuming projector stress zero, assuming Delta_symp_extra zero, beta pass claim, local-GR claim, GitHub action, formalization-workbench edits",
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
    theorem_rows: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    partial_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_937_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_conditional = any(row["clause_id"] == "VTC938_6_total_theorem" and row["current_status"] == "conditional_theorem_not_current_claim" for row in theorem_rows)
    theorem_no_claim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in theorem_rows)
    sector_primary = any(row["sector_id"] == "SVA938_1_projector_PiM" and row["status"] == "primary_blocker" for row in sector_rows)
    partial_bf_positive = any(row["sector_id"] == "SVA938_2_BF_bulk" and row["status"] == "partial_positive_candidate" for row in sector_rows)
    source_coupling_blocker = any(row["sector_id"] == "SVA938_3_BF_source_coupling" and row["status"] == "open_blocker" for row in sector_rows)
    partial_rows_nonclaim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in partial_rows)
    cbeta_bound_loaded = any(row["row_id"] == "CBN938_0_R4_beta_bound" and row["value_or_formula"] == "7.8e-05" for row in cbeta_rows)
    cbeta_blocked = any(row["row_id"] == "CBN938_1_C_beta_N5_definition" and row["score_ready"] == "false" for row in cbeta_rows) and any(row["row_id"] == "CBN938_2_X_N5_definition" and row["score_ready"] == "false" for row in cbeta_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("939-Y5-R10-projector-PiM-vertical-generator") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + theorem_rows + sector_rows + partial_rows + cbeta_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V938_0_sources_exist_and_needles", sources_ok, "all 938 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V938_1_prior_937_clean", prior_clean, "P8_Y5_BRR545_937_VALIDATION.csv clean")
    add("V938_2_theorem_conditional_only", theorem_conditional, "vertical-degeneracy theorem remains conditional only")
    add("V938_3_theorem_no_claim", theorem_no_claim, "no vertical theorem clause promoted")
    add("V938_4_projector_primary_blocker", sector_primary, "projector/PiM sector selected as primary blocker")
    add("V938_5_BF_bulk_partial_positive", partial_bf_positive, "pure BF bulk kept as partial positive candidate")
    add("V938_6_source_coupling_blocker", source_coupling_blocker, "BF/source coupling remains open blocker")
    add("V938_7_partial_rows_nonclaim", partial_rows_nonclaim, "partial result ledger is nonclaim")
    add("V938_8_cbeta_bound_loaded", cbeta_bound_loaded, "R4 beta bound 7.8e-05 loaded")
    add("V938_9_cbeta_prediction_blocked", cbeta_blocked, "C_beta_N5 and X_N5 remain unfilled")
    add("V938_10_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V938_11_claim_gates_false", claims_false, "all claim gates remain false")
    add("V938_12_next_target_selected", next_selected, "939 projector-PiM vertical-generator target selected")
    add("V938_13_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V938_14_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V938_15_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    sector_rows: list[dict[str, str]],
    partial_rows: list[dict[str, str]],
    cbeta_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 938 - Y5/R10 Extra Omega Vertical Degeneracy Or CbetaN5 Source Row

Generated: `{stamp()}`

Status: `Y5_R10_938_extra_omega_vertical_degeneracy_not_proved_BF_bulk_partial_positive_projector_PiM_primary_blocker_nonclaim`

Claim ceiling: `vertical_degeneracy_contract_and_CbetaN5_schema_only_no_Delta_symp_zero_no_beta_score_no_local_GR_pass`

## Result

The clean theorem would be:

```text
omega_total = omega_EH + omega_extra,
i_tau omega_extra = d b_tau + E_A terms,
int_S d b_tau = 0,
therefore Delta_symp_extra = 0.
```

This would let the MTS local branch inherit the GR Hamiltonian charge/integrability structure without smuggling in a plateau axiom.

The good news: a **pure BF/topological bulk** sector is a real candidate for this kind of vertical degeneracy. That is a useful structural clue, not fluff.

The bad news: the full theorem still fails as a current claim because the live obstruction is not the pure BF bulk. It is the projector/source side:

```text
delta_g Pi_M = 0,
[d,Pi_M]J_H = 0,
d(Pi_M J_H)=0 off shell,
A_M = d lambda_M with zero compact holonomy,
M_H[S,tau] = M_eff[Pi_M J_H].
```

Those are not parent-signed. Therefore `Delta_symp_extra=0`, `Pi_M^H` ownership, beta safety, and local-GR reduction remain blocked.

The next best derivation target is the projector-PiM vertical generator itself. If that closes, several blockers fall together; if it fails, we pivot to an honest weak-field `C_beta_N5` map.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Vertical Degeneracy Theorem Contract

{md_table(theorem_rows, ["clause_id", "statement", "mathematical_form", "current_status", "parent_signed", "claim_allowed"])}

## Sector Vertical Audit

{md_table(sector_rows, ["sector_id", "sector", "candidate_vertical_route", "mathematical_form", "status", "blocker", "priority"])}

## Partial Result Ledger

{md_table(partial_rows, ["result_id", "finding", "meaning", "limit", "claim_allowed"])}

## CbetaN5 Source Rows

{md_table(cbeta_rows, ["row_id", "symbol", "value_or_formula", "source_path_or_url", "status", "score_ready", "claim_allowed"])}

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
    theorem_rows = vertical_theorem_contract()
    sector_rows = sector_vertical_audit()
    partial_rows = partial_result_ledger()
    cbeta_rows = cbeta_source_rows()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, theorem_rows, sector_rows, partial_rows, cbeta_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_938_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_938_VERTICAL_THEOREM_CONTRACT.csv",
            theorem_rows,
            ["clause_id", "statement", "mathematical_form", "why_needed", "current_status", "parent_signed", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_938_SECTOR_VERTICAL_AUDIT.csv",
            sector_rows,
            ["sector_id", "sector", "candidate_vertical_route", "mathematical_form", "status", "blocker", "priority", "vertical_degeneracy_claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_938_PARTIAL_RESULT_LEDGER.csv",
            partial_rows,
            ["result_id", "finding", "meaning", "limit", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_938_CBETA_N5_SOURCE_ROWS.csv",
            cbeta_rows,
            ["row_id", "symbol", "value_or_formula", "units", "source_path_or_url", "note", "status", "source_bound_loaded", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_938_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_938_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_938_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_938_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, theorem_rows, sector_rows, partial_rows, cbeta_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_938_extra_omega_vertical_degeneracy_not_proved_BF_bulk_partial_positive_projector_PiM_primary_blocker_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 939-Y5-R10-projector-PiM-vertical-generator-or-CbetaN5-weak-field-map.md")


if __name__ == "__main__":
    main()
