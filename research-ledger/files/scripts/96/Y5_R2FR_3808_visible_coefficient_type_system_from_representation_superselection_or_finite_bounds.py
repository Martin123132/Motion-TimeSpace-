import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3808"
BRANCH = "MTS_R2FR_Y5_VISIBLE_COEFFICIENT_TYPE_SYSTEM_REP_SUPERSELECTION_3808"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3808-Y5-R2FR-visible-coefficient-type-system-from-representation-superselection-or-finite-bounds.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3808_visible_coefficient_type_system_from_representation_superselection_or_finite_bounds.py"

P_3807 = PCW / "3807-Y5-R2FR-CSA3806-parent-signature-or-effective-readout-closure-audit.md"
P_3806 = PCW / "3806-Y5-R2FR-qX-coefficient-subquotient-action-clause-or-balpha-tau-normalization.md"
P_3790 = PCW / "3790-Y5-R2FR-charge-unit-superselection-or-betaq-bound.md"
P_3791 = PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"
P_1097 = PCW / "1097-Y5-R10-constant-sector-universality-theorem-or-finite-coefficient-source-prior.md"
P_1098 = PCW / "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md"
P_1050 = PCW / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
P_1058 = PCW / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3808_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3808_OBSREP_TYPE_SYSTEM_THEOREM.csv",
    "classification": RESIDUALS / "P8_Y5_R2FR_3808_VISIBLE_COEFFICIENT_CLASSIFICATION.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3808_SUPERSELECTION_PROMOTION_AUDIT.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3808_FINITE_BOUND_REQUIREMENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3808_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3808_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3808_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3808_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3808_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3808_0_3807_type_split", P_3807, "PST3807_1_sufficient_type_split", "3807 sufficient ObsRep type theorem"),
    ("SRC3808_1_3806_action_clause", P_3806, "CSA3806_1_action_clause", "3806 action grammar"),
    ("SRC3808_2_3790_qstar", P_3790, "QST3790_1_compact_lattice_route", "charge-unit superselection theorem"),
    ("SRC3808_3_3791_ZEM", P_3791, "ZFT3791_1_conditional_zero", "Z_EM fixed-normalization theorem"),
    ("SRC3808_4_1097_constant", P_1097, "CSU1097_1_descent_superselection", "constant-sector descent/superselection theorem"),
    ("SRC3808_5_1098_owner", P_1098, "OCS1098_0_parent_domain", "ordinary-constant owner action signature"),
    ("SRC3808_6_1050_product", P_1050, "PFT1050_1_visible_action_pullback", "visible action pullback theorem"),
    ("SRC3808_7_1058_exhaustion", P_1058, "VOE1058_0_target", "visible operator-domain exhaustion target"),
    ("SRC3808_8_spine", P_SPINE, "3808-Y5-R2FR-visible-coefficient-type-system-from-representation-superselection-or-finite-bounds.md", "live spine target"),
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows(timestamp):
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    rows = [
        (
            "ORT3808_0_domain",
            "ObsRep coefficient domain",
            "Define ObsRep_U=(q_obs|_U,theta_rep,rho_vis,q_star,kappa_star,C_P,N_Q,boundary_class,source_domain_class) with theta_rep, rho_vis, q_star, kappa_star, C_P, and N_Q either q_obs-owned or superselected before local arena fitting.",
            "DEFINITION_SHARP",
            "This separates universal visible coefficient data from local X_Q geometry.",
            "strict current corpus has not signed the full ObsRep object",
        ),
        (
            "ORT3808_1_constant_value_vs_variation",
            "constant value need not be numerically derived to be locally safe",
            "For a visible coefficient c_J, local-GR coupling tests require Lie_v c_J=0 for admissible local vertical variations v, not a derivation of the numerical value of c_J. A parent universal parameter or superselection label is acceptable only if it is fixed before source/readout selection and has no X_Q dependence.",
            "EXACT_DISTINCTION",
            "This is the GR/Newton-style constant route: the number can be empirical, but its universality and vertical silence must be derived.",
            "does not by itself prove any MTS coefficient is universal",
        ),
        (
            "ORT3808_2_chain_rule",
            "ObsRep chain-rule zero",
            "If c_J(Phi)=cbar_J(ObsRep_U(Phi)) and D ObsRep_U[v]=0 for v in ker(Dq_obs) at fixed representation/superselection labels, then Lie_v c_J = D cbar_J[D ObsRep_U[v]]=0.",
            "EXACT_CONDITIONAL_THEOREM",
            "This derives CSA3806 coefficient silence without deriving each coefficient's numerical value.",
            "requires parent-signed ObsRep vertical silence and no hidden-visible coefficient morphisms",
        ),
        (
            "ORT3808_3_XQ_exception",
            "X_Q may build fields but not coefficients",
            "The allowed X_Q path is X_Q -> Y_Q=Pi4(X_Q) -> B_Q[Y_Q] -> A_Q,F_Q. This path changes the EM field object and its Hilbert stress; it does not create c_J(X_Q) multiplying independent visible operators.",
            "EXACT_CONDITIONAL_ROUTE_SPLIT",
            "Keeps the MTS EM construction alive while forbidding hidden coefficient tuning.",
            "requires same-current stress, unique Maxwell normalization, and readout closure",
        ),
        (
            "ORT3808_4_partial_promotion",
            "charge-unit q_star is the closest current partial win",
            "3790 gives an exact conditional theorem: if q_star is a compact U(1) charge-lattice/superselection datum, beta_q,A=0 and d beta_q,A=0.",
            "PARTIAL_CONDITIONAL_WIN_UNSIGNED",
            "The representation/superselection strategy is mathematically viable for charge units.",
            "current parent U(1) bundle/generator/lattice owner is still unsigned",
        ),
        (
            "ORT3808_5_ZEM_guard",
            "q_star does not derive Z_EM or alpha",
            "Even if q_star is superselected, Z_EM and alpha require fixed C_P/N_Q or generator norm, no independent F^2 slot, same-current normalization, and readout closure.",
            "OVERCLAIM_GUARD",
            "Do not use q_star to claim alpha, clock, WEP, R10, or local-GR closure.",
            "Z_EM/alpha remains finite or theorem-zero pending 3809",
        ),
        (
            "ORT3808_6_verdict",
            "CSA3806 from representation/superselection",
            "ObsRep vertical silence plus B_Q-only X_Q bridge plus effective/readout stability implies CSA3806. The strict current corpus supports the theorem shape but not the full signature.",
            "PASS_CONDITIONAL_FAIL_STRICT_CURRENT",
            "The route is not dead; it is now a type-system/signature problem rather than a vague coupling problem.",
            "MISSING_OBSREP_SIGNATURE;MISSING_ZEM_OWNER;MISSING_MATTER_SPECTRUM_OWNER;MISSING_SOURCE_WEIGHT_OWNER;MISSING_READOUT_CLOSURE",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "mathematical_statement": statement,
            "status": status,
            "consequence": consequence,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for theorem_id, claim_piece, statement, status, consequence, missing in rows
    ]


def classification_rows(timestamp):
    rows = [
        (
            "VCC3808_0_qstar",
            "q_star",
            "charge unit / compact U(1) lattice scale",
            "representation/superselection label if parent U(1) lattice is signed",
            "CONDITIONAL_ZERO_ROUTE_AVAILABLE",
            "beta_q,A=0 if signed",
            "parent U(1) bundle/generator/lattice owner",
        ),
        (
            "VCC3808_1_ZEM",
            "Z_EM or g_EM^{-2}",
            "Maxwell kinetic normalization",
            "not fixed by charge lattice alone; needs parent inner product/generator norm and no extra F2",
            "UNSIGNED_RETAINS_FINITE_BRANCH",
            "beta_Z,A=0 only after unique Maxwell owner and readout closure",
            "fixed C_P/N_Q; no lambda_A; no f(X_Q)F2; readout/current owner",
        ),
        (
            "VCC3808_2_alpha",
            "alpha_EM readout",
            "dimensionless spectroscopy/readout coefficient",
            "observed readout, Hodge/coframe, hbar*c, current normalization",
            "UNSIGNED_RETAINS_PRODUCT_BRANCH",
            "b_alpha=0 only after Z_EM plus readout descent",
            "tau_clock and readout closure; no radiative alpha counterterm",
        ),
        (
            "VCC3808_3_masses",
            "m_A,y_A,Lambda_QCD,binding fractions",
            "matter spectrum and composition coefficients",
            "fixed representation/matter-sector data if parent matter functor is signed",
            "UNSIGNED_RETAINS_FINITE_BRANCH",
            "b_mu,b_mA,b_nuc=0 only under matter spectrum owner",
            "no m_A(X_Q), no y_A(X_Q), no binding-response X_Q slots",
        ),
        (
            "VCC3808_4_source_weights",
            "w_A,kappa_A,source normalization",
            "source and WEP/Newton coupling weights",
            "single Hilbert/coframe source owner if source functor forgets species labels before coupling selection",
            "UNSIGNED_RETAINS_FINITE_BRANCH",
            "source-label leakage zero only under same-source owner",
            "source-label forgetting and no source-only material multiplier",
        ),
        (
            "VCC3808_5_kappa",
            "kappa_star or G_eff coefficient",
            "gravity/EH coupling coefficient",
            "q_obs-owned or global/superselected coupling",
            "UNSIGNED_RETAINS_GDOT_PPN_BRANCH",
            "Lie_v kappa=0 if global/superselected and calibration co-descends",
            "absolute G value may be empirical, but local variation/source normalization must be controlled",
        ),
        (
            "VCC3808_6_clocks",
            "nu_i and clock/readout markers",
            "clock transition/readout coefficients",
            "readout functor from q_obs plus owned constants",
            "UNSIGNED_RETAINS_CLOCK_BRANCH",
            "clock coefficient silence only after readout naturality",
            "no nu_i(X_Q), no clock-frame hidden marker, tau_clock normalization",
        ),
        (
            "VCC3808_7_boundary",
            "D_boundary and source-domain weights",
            "boundary/support/domain coefficients",
            "fixed boundary_class/source_domain_class in ObsRep",
            "UNSIGNED_RETAINS_BOUNDARY_BRANCH",
            "boundary coefficient silence only if support/domain classes are fixed before readout",
            "no X_Q-dependent source tubes or boundary weights",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "class_id": class_id,
            "symbol": symbol,
            "role": role,
            "proposed_type_owner": owner,
            "current_status": status,
            "zero_condition": zero_condition,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for class_id, symbol, role, owner, status, zero_condition, missing in rows
    ]


def audit_rows(timestamp):
    rows = [
        (
            "SPA3808_0_qstar",
            "q_star charge unit",
            "3790 exact conditional superselection theorem",
            "PARTIAL_TYPE_ROUTE_AVAILABLE",
            "do not promote strict current; parent U(1) owner unsigned",
        ),
        (
            "SPA3808_1_ZEM",
            "Z_EM/Maxwell normalization",
            "3791 exact conditional theorem but no independent F2 ban missing",
            "BLOCKED",
            "next sharp target: fixed parent inner product/generator norm plus no extra F2",
        ),
        (
            "SPA3808_2_constants",
            "ordinary constants and material coefficients",
            "1097/1098 exact chain-rule theorem but owner signature not derived",
            "BLOCKED",
            "need parent matter spectrum and source-weight exclusion",
        ),
        (
            "SPA3808_3_readout",
            "clock/material/source readout",
            "1050/1058 keep radiative/readout closure unsigned",
            "BLOCKED",
            "need readout-after-variation/naturality theorem",
        ),
        (
            "SPA3808_4_strict_verdict",
            "strict current CSA3806",
            "the theorem shape is exact but full type signature is not signed",
            "NONCLAIM",
            "retain finite bound rows for all unsigned components",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "audit_id": audit_id,
            "object": obj,
            "evidence": evidence,
            "status": status,
            "action": action,
            "valid_for_claim": "false",
        }
        for audit_id, obj, evidence, status, action in rows
    ]


def bound_rows(timestamp):
    rows = [
        (
            "FBR3808_0_beta_ZA",
            "beta_Z,A or lambda_A",
            "alpha/EM kinetic leakage",
            "MISSING_ZEM_OWNER_OR_ALPHA_COUNTERTERM_BOUND",
            "clock;WEP;R10;EM spectra;PPN",
            "highest",
        ),
        (
            "FBR3808_1_b_alpha",
            "b_alpha*tau_clock_time product",
            "clock alpha readout leakage",
            "PRODUCT_ONLY_2.1e-18_PER_YEAR_NO_STANDALONE_BALPHA",
            "clock;WEP;R10",
            "highest",
        ),
        (
            "FBR3808_2_mass_binding",
            "b_mu,b_mA,b_nuc,b_binding",
            "matter spectrum/composition leakage",
            "MISSING_MATTER_SPECTRUM_OWNER_OR_SOURCE_BACKED_COEFFICIENTS",
            "WEP;clock;R10;composition",
            "high",
        ),
        (
            "FBR3808_3_source_weight",
            "qbar_source_label,w_A,kappa_A",
            "source normalization/WEP/Newton leakage",
            "MISSING_SOURCE_LABEL_FORGETTING_OR_RELATIVE_SOURCE_WEIGHT_BOUND",
            "WEP;Newton_GM;R10;PPN",
            "high",
        ),
        (
            "FBR3808_4_kappa",
            "beta_kappa,A",
            "gravitational coupling drift",
            "MISSING_KAPPA_SUPERSELECTION_OR_GDOT_PPN_PROJECTION",
            "Gdot;PPN;orbital",
            "medium",
        ),
        (
            "FBR3808_5_clock_readout",
            "b_clock_i",
            "direct clock/readout residual",
            "MISSING_READOUT_NATURALITY_OR_CLOCK_MODEL",
            "clock;redshift;alpha spectra",
            "medium",
        ),
        (
            "FBR3808_6_boundary",
            "epsilon_boundary_XQ",
            "source-domain/boundary leakage",
            "MISSING_BOUNDARY_CLASS_OWNER_OR_FLUX_BOUND",
            "R10;orbital;Newton_GM;PPN",
            "medium",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "bound_id": bound_id,
            "component": component,
            "role": role,
            "required_input": required,
            "arenas": arenas,
            "priority": priority,
            "valid_for_claim": "false",
        }
        for bound_id, component, role, required, arenas, priority in rows
    ]


def gate_rows(timestamp, grouped):
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    theorem_present = any(row["theorem_id"] == "ORT3808_2_chain_rule" for row in grouped["theorem"])
    distinction_present = any(row["theorem_id"] == "ORT3808_1_constant_value_vs_variation" for row in grouped["theorem"])
    qstar_partial = any(row["class_id"] == "VCC3808_0_qstar" and row["current_status"] == "CONDITIONAL_ZERO_ROUTE_AVAILABLE" for row in grouped["classification"])
    all_claims_closed = True
    rows = [
        ("CG3808_0_sources", all_sources, False, "all source needles found" if all_sources else "missing source or needle"),
        ("CG3808_1_type_theorem", theorem_present, False, "ObsRep chain-rule theorem emitted"),
        ("CG3808_2_constant_distinction", distinction_present, False, "constant-value versus vertical-silence distinction emitted"),
        ("CG3808_3_qstar_partial", qstar_partial, False, "q_star has exact conditional superselection route but remains unsigned"),
        ("CG3808_4_ZEM_alpha_closed", False, False, "Z_EM/alpha owner remains unsigned"),
        ("CG3808_5_matter_source_closed", False, False, "matter/source/clock owners remain unsigned"),
        ("CG3808_6_effective_readout_closed", False, False, "effective/readout closure remains unsigned"),
        ("CG3808_7_claims_closed", all_claims_closed, False, "no local-GR/EM/WEP/R10/clock claim allowed"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": gate_id,
            "pass": str(passed).lower(),
            "claim_allowed": str(claim_allowed).lower(),
            "details": details,
            "valid_for_claim": "false",
        }
        for gate_id, passed, claim_allowed, details in rows
    ]


def decision_rows(timestamp):
    rows = [
        (
            "DEC3808_0_real_progress",
            "The coupling problem is now a type/signature problem.",
            "3808 proves exact vertical silence if visible coefficients are ObsRep/superselection data and X_Q only constructs B_Q.",
            "Stop treating every missing number as fatal; require universality/vertical-silence first, numerical values second.",
        ),
        (
            "DEC3808_1_partial_win",
            "q_star is the closest legitimate superselection win.",
            "3790 already proves the conditional compact charge-lattice theorem.",
            "Try to parent-sign U(1) lattice/generator ownership, but do not promote alpha from it.",
        ),
        (
            "DEC3808_2_next",
            "Attack Maxwell normalization next.",
            "Z_EM/alpha is the first high-leverage coefficient after q_star and controls clock/WEP/R10/EM leakage.",
            "Derive fixed parent inner product/generator norm plus no extra F2, or retain finite beta_Z/lambda_A rows.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": action,
            "valid_for_claim": "false",
        }
        for decision_id, decision, because, action in rows
    ]


def next_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3809-Y5-R2FR-Maxwell-normalization-from-parent-inner-product-or-alpha-finite-branch.md",
            "target_script": "scripts/Y5_R2FR_3809_Maxwell_normalization_from_parent_inner_product_or_alpha_finite_branch.py",
            "objective": "Try to derive Z_EM/alpha vertical silence from a parent fixed inner product/generator norm, compact charge lattice, unique Maxwell subblock, no independent F2 operator, and readout/current closure; if it fails, keep beta_Z/lambda_A/b_alpha finite rows explicit.",
            "avoid": "do not claim q_star derives alpha; do not use unit rescaling to hide dimensionless alpha drift; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_OBSREP_TYPE_SYSTEM_THEOREM_DERIVED_QSTAR_PARTIAL_ONLY_FINITE_ROWS_RETAINED",
            "summary": "3808 derives the exact ObsRep/superselection type-system theorem, separates numerical constant values from vertical silence, identifies q_star as a partial conditional win, and keeps Z_EM/alpha, matter/source, kappa, clock, and boundary branches nonclaim.",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(timestamp, grouped):
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            load_csv(path)
    fwb_hits = list(FWB.rglob("*3808*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3808 markdown document written"),
        ("obsrep_theorem_present", any(row["theorem_id"] == "ORT3808_2_chain_rule" for row in grouped["theorem"]), "ObsRep chain-rule theorem emitted"),
        ("constant_distinction_present", any(row["theorem_id"] == "ORT3808_1_constant_value_vs_variation" for row in grouped["theorem"]), "constant-value versus vertical-silence distinction emitted"),
        ("qstar_partial_only", any(row["class_id"] == "VCC3808_0_qstar" for row in grouped["classification"]), "q_star partial conditional route recorded"),
        ("ZEM_not_promoted", any(row["class_id"] == "VCC3808_1_ZEM" and "UNSIGNED" in row["current_status"] for row in grouped["classification"]), "Z_EM remains unsigned"),
        ("finite_rows_retained", len(grouped["bounds"]) >= 6, "finite bound requirement rows retained"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("formalization_clean", not fwb_hits, "no 3808 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def row_bullet(row, key_fields):
    label = " ".join(f"`{row[field]}`" for field in key_fields if field in row and row[field])
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped):
    lines = [
        "# 3808 - Visible Coefficient Type System From Representation/Superselection Or Finite Bounds",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_OBSREP_TYPE_SYSTEM_THEOREM_DERIVED_QSTAR_PARTIAL_ONLY_FINITE_ROWS_RETAINED`.",
        "",
        "3808 makes the next important distinction: local-GR safety does not require deriving the numerical value of every constant today. It requires deriving that visible coefficients are universal, parent-owned, and vertically silent under local hidden/X_Q variations.",
        "",
        "The exact theorem is: if visible coefficient slots are `ObsRep` objects and `X_Q` only enters through the declared `B_Q -> A_Q,F_Q` construction, then `c_J=cbar_J(ObsRep)` and `Lie_v c_J=0` for admissible local vertical variations. This is the clean route to `CSA3806`.",
        "",
        "Current status is still nonclaim. `q_star` has a real conditional superselection route, but `Z_EM/alpha`, matter masses/binding, source weights, kappa, clock readout, and boundary/domain coefficients remain unsigned or finite-bound branches.",
        "",
        "## Human Read",
        "",
        "This is the GR/Newton-constant style move: a constant can be empirical without being post-hoc garbage, provided the theory owns why it is universal and not secretly a local hidden-field function. For MTS the next fight is not 'derive the number 1/137 immediately'; it is 'prove alpha's coefficient slot cannot be f(X_Q)'.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("ObsRep Type-System Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("Visible Coefficient Classification", "classification", ["class_id", "symbol"]),
        ("Superselection Promotion Audit", "audit", ["audit_id", "object"]),
        ("Finite Bound Requirements", "bounds", ["bound_id", "component"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decision Rows", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
        lines.append("")
    DOC_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "classification": classification_rows(timestamp),
        "audit": audit_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    write_markdown(grouped)
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
