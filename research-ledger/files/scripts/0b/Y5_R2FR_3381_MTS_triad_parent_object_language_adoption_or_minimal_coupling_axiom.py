from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3381-Y5-R2FR-MTS-triad-parent-object-language-adoption-or-minimal-coupling-axiom-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3381_SOURCE_REGISTER.csv",
    "triad_anchor": OUT / "P8_Y5_R2FR_3381_MTS_TRIAD_ANCHOR_EXTRACT.csv",
    "adoption_attempt": OUT / "P8_Y5_R2FR_3381_TRIAD_TO_TYPE_SYSTEM_ADOPTION_ATTEMPT.csv",
    "no_go": OUT / "P8_Y5_R2FR_3381_SCALAR_TRIAD_NO_GO_COUNTERMODEL.csv",
    "minimal_axiom": OUT / "P8_Y5_R2FR_3381_MINIMAL_UNIVERSAL_COUPLING_AXIOM.csv",
    "local_gr_chain": OUT / "P8_Y5_R2FR_3381_LOCAL_GR_CHAIN_CONSEQUENCE.csv",
    "residual_policy": OUT / "P8_Y5_R2FR_3381_RESIDUAL_POLICY_AFTER_AXIOM.csv",
    "runner": OUT / "P8_Y5_R2FR_3381_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3381_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3381_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3381_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3381_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3381_0_3380_doc", ROOT / "3380-Y5-R2FR-parent-type-system-or-source-prefactor-bound-acquisition-under-AX1090.md", "3380 candidate object-language/type-system theorem"),
    ("SRC3381_1_3380_object_language", OUT / "P8_Y5_R2FR_3380_PARENT_OBJECT_LANGUAGE.csv", "3380 object language"),
    ("SRC3381_2_3380_rules", OUT / "P8_Y5_R2FR_3380_ACTION_FORMATION_RULES.csv", "3380 action formation rules"),
    ("SRC3381_3_3380_type_theorem", OUT / "P8_Y5_R2FR_3380_TYPE_SYSTEM_THEOREM_ATTEMPT.csv", "3380 type-system theorem"),
    ("SRC3381_4_unified_programme", FW / "03-unified-field-theory-programme.md", "programme primitive spine"),
    ("SRC3381_5_variable_audit", FW / "04-variable-audit.csv", "canonical primitive status audit"),
    ("SRC3381_6_equation_register", FW / "05-equation-register.md", "equation register GR/Newton source chain"),
    ("SRC3381_7_fundamental_action", REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "core MTS action source"),
    ("SRC3381_8_motion_timespace_action", REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "MTS action principle source"),
    ("SRC3381_9_effective_field_theory", REPO / "core-mts-framework" / "field-theory" / "the-effective-field-theory-of-motion-timespace.md", "effective field theory source"),
    ("SRC3381_10_gravity_core", REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md", "gravity core source"),
    ("SRC3381_11_owner_current_primitive", FW / "141-doubled-owner-connection-current-primitive.md", "owner-current primitive obstruction source"),
    ("SRC3381_12_3377_kappa", OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv", "weak-field kappa/G_ref source normalization"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def triad_anchor_rows() -> list[dict[str, str]]:
    return [
        {
            "anchor_id": "TRIAD3381_0_programme_spine",
            "source_path": str(FW / "03-unified-field-theory-programme.md"),
            "line_anchor": "lines 21-29",
            "extracted_claim": "candidate primitives include psi, g_mu_nu, Gamma, chi, tau and S_memory",
            "use_in_3381": "defines the MTS primitive/effective object pool to test against OBJ3380",
            "adoption_strength": "PROGRAMME_ANCHOR_NOT_FORMAL_AXIOM",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "TRIAD3381_1_required_chain",
            "source_path": str(FW / "03-unified-field-theory-programme.md"),
            "line_anchor": "lines 38-40",
            "extracted_claim": "MTS microscopic dynamics -> emergent metric -> GR in the infrared -> Newtonian limit",
            "use_in_3381": "sets required local-GR correspondence chain",
            "adoption_strength": "TARGET_CHAIN",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "TRIAD3381_2_core_emergent_metric",
            "source_path": str(REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"),
            "line_anchor": "lines 19-26",
            "extracted_claim": "g_munu = eta_munu + <partial_mu psi partial_nu psi>, action includes L_matter, variation gives extended Einstein equation",
            "use_in_3381": "anchors psi-to-geometry but also exposes that matter coupling is inserted as L_matter",
            "adoption_strength": "PARTIAL_DERIVATION_PLUS_INSERTED_MATTER",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "TRIAD3381_3_action_principle",
            "source_path": str(REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"),
            "line_anchor": "lines 13-29",
            "extracted_claim": "derivation defines psi, constructs emergent metric, builds action with Einstein-Hilbert term and standard matter coupling",
            "use_in_3381": "shows standard matter coupling is assumed as part of the effective action",
            "adoption_strength": "STANDARD_COUPLING_POSTULATED",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "TRIAD3381_4_variable_audit",
            "source_path": str(FW / "04-variable-audit.csv"),
            "line_anchor": "psi/g_mu_nu/Gamma/tau rows",
            "extracted_claim": "psi and g_mu_nu remain candidate/emergent with unit/signature/EH derivation gaps; tau and Gamma are overloaded",
            "use_in_3381": "prevents overclaiming that the primitive language is already canonical",
            "adoption_strength": "AUDIT_WARNING",
            "valid_for_claim": "false",
        },
        {
            "anchor_id": "TRIAD3381_5_owner_current_warning",
            "source_path": str(FW / "141-doubled-owner-connection-current-primitive.md"),
            "line_anchor": "lines 205-287",
            "extracted_claim": "metric-independent owner current exists formally but spacetime projection/solder theorem is not derived",
            "use_in_3381": "shows why source coupling cannot be hidden in an internal owner current without a projection theorem",
            "adoption_strength": "OBSTRUCTION_ANCHOR",
            "valid_for_claim": "false",
        },
    ]


def adoption_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "ADOPT3381_0_psi_to_geometry",
            "target": "derive OBJ3380 Geom_obs from MTS triad",
            "derivation_attempt": "If psi is the sole microscopic motion/curvature-exchange field and macroscopic geometry is the smoothed covariance q(psi), then there is a natural observed geometry g_obs=q(psi).",
            "result": "PARTIAL_SUCCESS",
            "why": "This can motivate a unique observed geometry, but the source docs still need normalization, Lorentzian signature, diffeomorphism/EH derivation and canonical psi ontology.",
            "residual": "R_metric_emergence;R_EH_induction",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ADOPT3381_1_geometry_to_matter",
            "target": "derive OBJ3380 matter functor from MTS triad",
            "derivation_attempt": "Try to force all matter bundles to couple only through e_obs(qPhi), nabla_obs and one common dmu_obs because all physical rods/clocks are excitations of the same motion-time-space substrate.",
            "result": "MOTIVATED_NOT_DERIVED",
            "why": "The corpus states standard matter coupling, but does not derive the matter bundle categories, representation labels, masses, charges or a no-source-prefactor theorem from psi dynamics.",
            "residual": "E_universal_coupling_axiom",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ADOPT3381_2_single_metric_no_shadow",
            "target": "forbid hidden source metric",
            "derivation_attempt": "If all operational spacetime measurements and matter actions are quotient maps of q(psi), a second source metric e_source is not a legal object.",
            "result": "CONDITIONAL_SUCCESS",
            "why": "Works after imposing quotient-only operational geometry; fails as a theorem from scalar covariance alone because one can add a universal hidden conformal factor without breaking covariance.",
            "residual": "c_g_b_dis",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ADOPT3381_3_no_species_weight",
            "target": "forbid w_A S_A",
            "derivation_attempt": "Species labels are representation data, not parent geometry; therefore they should not map to active gravitational source scales.",
            "result": "CONDITIONAL_SUCCESS",
            "why": "This is exact inside OBJ3380, but not derived from current psi/g/Gamma/tau primitives because the matter-sector ontology is not derived.",
            "residual": "Delta_w_AB;b_marker",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ADOPT3381_4_readout_no_reentry",
            "target": "forbid readout/projector reentry before variation",
            "derivation_attempt": "Readout maps should be maps from solutions to observables, so they cannot alter S_matter before Hilbert variation.",
            "result": "DISCIPLINE_RULE_NOT_DERIVED",
            "why": "This is a clean field-theory discipline rule, but current MTS has not derived it from primitive dynamics; it must be declared as part of the parent action contract.",
            "residual": "C_eff_source_tail;epsilon_Wchan",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "ADOPT3381_5_verdict",
            "target": "adopt OBJ3380/FORM3380 from MTS triad",
            "derivation_attempt": "Combine psi->g_obs emergence, quotient-only operational geometry, matter-as-excitation universality, and variation-before-readout.",
            "result": "NOT_FULLY_DERIVED_MINIMAL_AXIOM_REQUIRED",
            "why": "The triad supports the route, but scalar motion/geometry alone does not determine the matter functor or exclude weighted covariant matter sectors.",
            "residual": "E_UOC_minimal_axiom_or_empirical_bounds",
            "valid_for_claim": "false",
        },
    ]


def no_go_rows() -> list[dict[str, str]]:
    return [
        {
            "no_go_id": "NOGO3381_0_weighted_matter_family",
            "statement": "The scalar psi-to-metric triad alone cannot forbid S_matter=sum_A w_A S_A[g(psi),psi_A].",
            "construction": "Choose constants or quotient-invariant scalars w_A; the action remains a scalar functional of g_obs and matter fields and yields a conserved weighted stress tensor.",
            "what_it_preserves": "covariance, Bianchi-compatible conservation, same emergent metric relation, same formal Einstein equation shape",
            "what_it_breaks": "universal active source normalization and WEP/source universality",
            "conclusion": "matter universality is independent unless a parent matter-coupling rule is added or derived",
            "valid_for_claim": "false",
        },
        {
            "no_go_id": "NOGO3381_1_hidden_common_frame",
            "statement": "The triad alone cannot exclude a universal source frame e_source=A(X) e_obs if X is quotient-invariant.",
            "construction": "Let all matter couple to e_source while geometry/readout uses e_obs; composition WEP can survive while PPN/clocks/R10 shift.",
            "what_it_preserves": "common free fall in some limits and covariance",
            "what_it_breaks": "single metric/source frame identity",
            "conclusion": "no-shadow metric requires a quotient-only coupling axiom or a projection theorem",
            "valid_for_claim": "false",
        },
        {
            "no_go_id": "NOGO3381_2_marker_relabeling",
            "statement": "Matter markers cannot be removed by scalar geometry alone.",
            "construction": "Allow theta_A(qPhi,I_A) where I_A is an internal material/isotope/preparation label.",
            "what_it_preserves": "ordinary matter-sector covariance and local action form",
            "what_it_breaks": "no-marker source universality",
            "conclusion": "material labels must be superselected/inertial-only or bounded",
            "valid_for_claim": "false",
        },
        {
            "no_go_id": "NOGO3381_3_owner_current_projection",
            "statement": "A metric-independent owner current does not by itself derive spacetime source coupling.",
            "construction": "Define internal balance in owner variables; projection to spacetime still needs a solder map E_I^nu or Pi tensor.",
            "what_it_preserves": "internal balance without g_loc",
            "what_it_breaks": "direct Hilbert source equality unless solder/projection theorem is supplied",
            "conclusion": "owner-current branch remains useful but cannot replace universal coupling yet",
            "valid_for_claim": "false",
        },
    ]


def minimal_axiom_rows() -> list[dict[str, str]]:
    return [
        {
            "axiom_id": "UOC3381_0_name",
            "axiom_piece": "Universal Observed-Geometry Coupling (UOC)",
            "statement": "All non-gravitational matter fields used for local tests are sections of bundles over the same observed geometry Geom_obs=q(Phi), not over a separate source geometry.",
            "why_minimal": "It adds matter coupling universality only; it does not add galaxy/cosmology phenomenology, PPN fitting freedom, or a plateau assumption.",
            "what_it_buys": "kills hidden source metric as an independent local source-coupling degree of freedom",
            "status": "MINIMAL_AXIOM_CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "axiom_id": "UOC3381_1_single_measure",
            "axiom_piece": "single observed measure",
            "statement": "Every ordinary matter sector uses dmu_obs[q(Phi)] and the observed connection compatible with e_obs/q(Phi), unless explicitly declared as beyond-local-test physics.",
            "why_minimal": "This is the ordinary minimal-coupling slot needed for local GR recovery.",
            "what_it_buys": "forbids species-dependent source measures and second source tetrads",
            "status": "MINIMAL_AXIOM_CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "axiom_id": "UOC3381_2_no_active_species_prefactor",
            "axiom_piece": "representation-only species data",
            "statement": "Species labels, masses, charges and material constants may enter inertial/gauge/matter terms, but not as multiplicative active gravitational source weights outside the common action normalization.",
            "why_minimal": "Without this clause w_A S_A is a legal covariant countermodel.",
            "what_it_buys": "kills Delta_w_AB as a theorem-zero if accepted",
            "status": "MINIMAL_AXIOM_CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "axiom_id": "UOC3381_3_universal_kappa",
            "axiom_piece": "single source normalization",
            "statement": "There is one kappa_MTS=8*pi*G_ref/c^4 in the local weak-field branch; G_ref is calibrated once and is not species/readout dependent.",
            "why_minimal": "GR itself uses an empirical universal coupling constant; MTS need not derive its SI value before recovering local GR.",
            "what_it_buys": "links 3377 weak-field source normalization to Newtonian limit without per-channel backfill",
            "status": "MINIMAL_AXIOM_CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "axiom_id": "UOC3381_4_variation_before_readout",
            "axiom_piece": "readout firewall",
            "statement": "WEP, PPN, R10, clock, orbital and other arena maps are applied after solving the parent equations and cannot reenter S_matter as source coefficients.",
            "why_minimal": "It is a field-theory well-posedness condition, not an empirical fit.",
            "what_it_buys": "blocks epsilon_Wchan and C_eff_source_tail from being hidden closure knobs",
            "status": "MINIMAL_AXIOM_CANDIDATE_NOT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "axiom_id": "UOC3381_5_public_wording",
            "axiom_piece": "honest claim wording",
            "statement": "With UOC, MTS has an effective universal-coupling branch analogous to GR minimal coupling; without UOC, local-GR source coupling remains an empirical residual problem.",
            "why_minimal": "It prevents pretending the coupling was derived while still allowing a rigorous branch to be tested.",
            "what_it_buys": "clean publishable distinction between derived geometry and postulated universal matter coupling",
            "status": "HONEST_BRANCH_LABEL",
            "valid_for_claim": "false",
        },
    ]


def local_gr_chain_rows() -> list[dict[str, str]]:
    return [
        {
            "chain_id": "CHAIN3381_0_geometry",
            "step": "MTS primitive/coarse graining",
            "formula_or_contract": "Phi -> q(Phi) -> g_obs approximately eta + <d psi d psi>_smooth",
            "status_after_3381": "PARTIAL_DERIVATION_FROM_CORE_DOCS",
            "remaining_gap": "normalization, Lorentzian signature, covariance/EH induction",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CHAIN3381_1_action",
            "step": "effective local action",
            "formula_or_contract": "S_eff = integral[(1/2 kappa_MTS) R[g_obs] + L_MTS_ir + L_matter(psi_A,e_obs,nabla_obs,A_obs,theta_A)] dmu_obs",
            "status_after_3381": "VALID_AS_UOC_BRANCH_CONTRACT",
            "remaining_gap": "EH term induction and UOC adoption/axiom label",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CHAIN3381_2_hilbert_source",
            "step": "source definition",
            "formula_or_contract": "T_munu = -(2/sqrt(-g_obs)) delta S_matter / delta g_obs^munu with no source-only prefactors",
            "status_after_3381": "FOLLOWS_IF_UOC_ACCEPTED",
            "remaining_gap": "not derived from psi-only matter ontology",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CHAIN3381_3_einstein_limit",
            "step": "IR field equation",
            "formula_or_contract": "G_munu[g_obs] + MTS_IR_terms = kappa_MTS T_munu",
            "status_after_3381": "CONDITIONAL_EFFECTIVE_BRANCH",
            "remaining_gap": "MTS_IR_terms must be PPN/local-safe or bounded",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CHAIN3381_4_newton",
            "step": "weak-field Newton limit",
            "formula_or_contract": "kappa_MTS=8*pi*G_ref/c^4 plus same Hilbert source gives Poisson/Newton as in 3377",
            "status_after_3381": "CONDITIONAL_ON_UOC_AND_3377_OWNER",
            "remaining_gap": "G_ref is calibrated parameter; no per-source backfill",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "CHAIN3381_5_em_stress",
            "step": "Maxwell/EM stress entry",
            "formula_or_contract": "EM/Poynting stress belongs in public Hilbert T_munu or remains explicit R_Poynting_worldtube",
            "status_after_3381": "UOC_REQUIRES_PUBLIC_STRESS_OR_RESIDUAL",
            "remaining_gap": "derive EM sector/current and stress tensor from MTS rather than importing Maxwell only",
            "valid_for_claim": "false",
        },
    ]


def residual_policy_rows() -> list[dict[str, str]]:
    return [
        {
            "policy_id": "POL3381_0_if_UOC_adopted",
            "branch": "UOC effective branch",
            "residual_treatment": "Delta_w_AB, epsilon_Wchan, c_g_b_dis, b_marker and C_eff_source_tail are theorem-zero only inside UOC.",
            "claim_wording": "MTS recovers local GR under an explicit universal observed-geometry coupling principle.",
            "next_test": "derive/bound MTS_IR_terms and PPN vector",
            "valid_for_claim": "false",
        },
        {
            "policy_id": "POL3381_1_if_UOC_refused",
            "branch": "pure derivation branch",
            "residual_treatment": "source-prefactor families remain live and must be bounded by WEP, PPN, R10, clock and orbital data.",
            "claim_wording": "pure MTS geometry alone has not recovered local GR source coupling.",
            "next_test": "numeric nonclaim bound runner",
            "valid_for_claim": "false",
        },
        {
            "policy_id": "POL3381_2_public_safety",
            "branch": "any public-facing WIP",
            "residual_treatment": "do not say source coupling is derived unless UOC is declared or an actual matter-ontology proof exists.",
            "claim_wording": "geometry-emergence route is under development; universal matter coupling is a stated branch assumption.",
            "next_test": "keep theorem/axiom labels explicit",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3381_0_triad_to_geom",
            "test": "derive observed geometry from MTS primitive triad",
            "result": "PARTIAL_PASS",
            "detail": "psi covariance motivates g_obs but does not yet prove all metric/EH properties",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3381_1_triad_to_matter",
            "test": "derive universal matter coupling from psi/g/Gamma/tau alone",
            "result": "FAILS_AS_FULL_DERIVATION",
            "detail": "core docs insert standard L_matter; weighted covariant matter remains a countermodel",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3381_2_minimal_axiom",
            "test": "isolate smallest honest extra assumption",
            "result": "PASS_MINIMAL_UOC_AXIOM_DEFINED",
            "detail": "UOC adds universal observed-geometry matter coupling, not a phenomenological fit or plateau closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3381_3_local_GR_chain",
            "test": "state local-GR/Newton consequence under UOC",
            "result": "PASS_CONDITIONAL_CHAIN",
            "detail": "with UOC and 3377 kappa/G_ref owner, Hilbert source route to Newton is cleanly specified",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3381_4_firewall",
            "test": "prevent overclaim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "all outputs remain nonclaim until UOC is accepted as axiom or derived from deeper matter ontology",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3381_0_sources",
            "claim": "all 3381 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register covers 3380, core MTS action docs, primitive audit and local-GR obstruction docs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3381_1_geometry_adoption",
            "claim": "MTS motivates one observed geometry",
            "gate_pass": "partial",
            "reason": "psi covariance route exists but metric/EH properties remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3381_2_universal_matter_coupling_derivation",
            "claim": "universal matter coupling is derived from the triad",
            "gate_pass": "false",
            "reason": "standard matter coupling is inserted in source docs and weighted matter countermodel survives",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3381_3_minimal_axiom",
            "claim": "minimal honest UOC axiom is defined",
            "gate_pass": "true",
            "reason": "UOC is isolated as the smallest local-GR coupling addition rather than hidden inside prose",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3381_4_local_GR_claim",
            "claim": "local GR/source coupling is fully derived",
            "gate_pass": "false",
            "reason": "requires deriving UOC from matter ontology or explicitly using UOC as an axiom plus testing residual MTS_IR terms",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3381_0_core_answer",
            "decision": "MTS is closer, but the source coupling is not derivable from the current triad alone.",
            "because": "The corpus has psi-to-metric and effective Einstein-action language, but matter coupling enters as standard L_matter rather than being derived.",
            "next_action": "use UOC as an explicit minimal branch axiom or derive matter ontology next",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3381_1_not_bad_news",
            "decision": "This is not fatal.",
            "because": "GR itself uses universal coupling/G as physical input; the problem is only fatal if MTS hides the input while claiming full derivation.",
            "next_action": "label the branch honestly and test it hard",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3381_2_best_route",
            "decision": "Best route is UOC-local-GR branch plus ongoing derivation hunt.",
            "because": "It lets the framework recover GR/Newton cleanly while keeping the deeper matter-coupling derivation as an open theorem rather than a smuggled assumption.",
            "next_action": "push UOC through the PPN/Newton/EM stress chain and separately hunt a deeper matter-origin proof",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3382-Y5-R2FR-UOC-local-GR-Newton-PPN-EM-stress-chain-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3382_UOC_local_GR_Newton_PPN_EM_stress_chain.py",
            "objective": "push the explicit UOC branch through local GR, Newtonian source normalization, PPN residual vector and EM/Poynting Hilbert stress without pretending UOC is derived",
            "why_next": "3381 isolates the smallest honest coupling axiom; the next test is whether that branch is mathematically clean and empirically bounded",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3383-Y5-R2FR-matter-ontology-from-MTS-excitations-or-UOC-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3383_matter_ontology_from_MTS_excitations_or_UOC_demotion.py",
            "objective": "try to derive UOC from matter-as-MTS-excitation ontology; if not, keep UOC as a declared equivalence-principle axiom",
            "why_next": "this is the true Grossmann-level derivation route if we refuse to leave universal coupling as an axiom",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3381*")
        if hit.name.startswith(("3381-Y5", "P8_Y5_R2FR_3381", "P8_Y5_BRR545_3381", "Y5_R2FR_3381"))
    ] if FW.exists() else []
    anchor_ids = {row["anchor_id"] for row in rows_by_name["triad_anchor"]}
    attempt_results = {row["result"] for row in rows_by_name["adoption_attempt"]}
    no_go_ids = {row["no_go_id"] for row in rows_by_name["no_go"]}
    axiom_ids = {row["axiom_id"] for row in rows_by_name["minimal_axiom"]}
    chain_ids = {row["chain_id"] for row in rows_by_name["local_gr_chain"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3381_0_sources_exist_parse", "all cited 3381 source paths exist and parse", source_ok, ""),
        ("VAL3381_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3381_2_triad_anchors", "triad anchors cover programme spine, required chain, core action, action principle, audit and owner-current warning", {"TRIAD3381_0_programme_spine", "TRIAD3381_1_required_chain", "TRIAD3381_2_core_emergent_metric", "TRIAD3381_3_action_principle", "TRIAD3381_4_variable_audit", "TRIAD3381_5_owner_current_warning"}.issubset(anchor_ids), ""),
        ("VAL3381_3_adoption_attempt", "adoption attempt includes partial geometry success, failed matter derivation and minimal axiom verdict", {"PARTIAL_SUCCESS", "MOTIVATED_NOT_DERIVED", "CONDITIONAL_SUCCESS", "DISCIPLINE_RULE_NOT_DERIVED", "NOT_FULLY_DERIVED_MINIMAL_AXIOM_REQUIRED"}.issubset(attempt_results), ""),
        ("VAL3381_4_no_go_countermodels", "no-go covers weighted matter, hidden common frame, marker relabeling and owner-current projection", {"NOGO3381_0_weighted_matter_family", "NOGO3381_1_hidden_common_frame", "NOGO3381_2_marker_relabeling", "NOGO3381_3_owner_current_projection"}.issubset(no_go_ids), ""),
        ("VAL3381_5_minimal_axiom", "UOC axiom covers observed geometry, single measure, no active species prefactor, universal kappa, readout firewall and public wording", {"UOC3381_0_name", "UOC3381_1_single_measure", "UOC3381_2_no_active_species_prefactor", "UOC3381_3_universal_kappa", "UOC3381_4_variation_before_readout", "UOC3381_5_public_wording"}.issubset(axiom_ids), ""),
        ("VAL3381_6_local_chain", "local chain covers geometry, action, Hilbert source, Einstein limit, Newton and EM stress", {"CHAIN3381_0_geometry", "CHAIN3381_1_action", "CHAIN3381_2_hilbert_source", "CHAIN3381_3_einstein_limit", "CHAIN3381_4_newton", "CHAIN3381_5_em_stress"}.issubset(chain_ids), ""),
        ("VAL3381_7_runner", "runner records partial geometry pass, failed full derivation, minimal axiom, conditional chain and firewall", {"PARTIAL_PASS", "FAILS_AS_FULL_DERIVATION", "PASS_MINIMAL_UOC_AXIOM_DEFINED", "PASS_CONDITIONAL_CHAIN", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3381_8_gates", "gates keep local GR claim blocked while defining UOC", gate_map.get("GATE3381_2_universal_matter_coupling_derivation") == "false" and gate_map.get("GATE3381_3_minimal_axiom") == "true" and gate_map.get("GATE3381_4_local_GR_claim") == "false", ""),
        ("VAL3381_9_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3381_10_next_target", "next target pushes UOC through local GR/Newton/PPN/EM stress", rows_by_name["next"][0]["target_id"].startswith("3382-Y5-R2FR-UOC-local-GR"), ""),
        ("VAL3381_11_write_scope_outside_formalization", "no 3381 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3381_12_overall", "3381 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3381 - Y5/R2FR MTS triad parent object-language adoption or minimal coupling axiom under AX1090",
        "",
        "## Summary",
        "- 3381 tests whether the 3380 parent type-system can be derived from the existing MTS motion/time/space primitive language.",
        "- Result: partial win, honest stop. The corpus supports `psi -> emergent metric -> effective GR`, but it inserts `L_matter` / standard matter coupling rather than deriving the matter functor from `psi`.",
        "- No-go result: scalar `psi`/emergent-geometry data alone cannot forbid covariant weighted matter `sum_A w_A S_A`, a hidden common source frame, marker relabeling, or owner-current projection ambiguity.",
        "- Progress: the missing coupling is now isolated as a minimal Universal Observed-Geometry Coupling axiom, not a cloud of hidden closure assumptions.",
        "- Under UOC, the local branch has a clean route: one observed metric, one measure, one Hilbert source, one `kappa_MTS`, variation before readout, then 3377 gives the Newton/Poisson normalization condition.",
        "- Current claim status: MTS local-GR source coupling is not fully derived; it is either a declared UOC branch or a future matter-ontology theorem.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## MTS Triad Anchors",
        md_table(rows_by_name["triad_anchor"]),
        "## Triad To Type-system Adoption Attempt",
        md_table(rows_by_name["adoption_attempt"]),
        "## No-go Countermodel",
        md_table(rows_by_name["no_go"]),
        "## Minimal Universal Coupling Axiom",
        md_table(rows_by_name["minimal_axiom"]),
        "## Local GR Chain Consequence",
        md_table(rows_by_name["local_gr_chain"]),
        "## Residual Policy",
        md_table(rows_by_name["residual_policy"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "triad_anchor": triad_anchor_rows(),
        "adoption_attempt": adoption_attempt_rows(),
        "no_go": no_go_rows(),
        "minimal_axiom": minimal_axiom_rows(),
        "local_gr_chain": local_gr_chain_rows(),
        "residual_policy": residual_policy_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
