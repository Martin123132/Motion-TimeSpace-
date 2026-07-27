import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3807"
BRANCH = "MTS_R2FR_Y5_CSA3806_PARENT_SIGNATURE_OR_EFFECTIVE_READOUT_CLOSURE_3807"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3807-Y5-R2FR-CSA3806-parent-signature-or-effective-readout-closure-audit.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3807_CSA3806_parent_signature_or_effective_readout_closure_audit.py"

P_3806 = PCW / "3806-Y5-R2FR-qX-coefficient-subquotient-action-clause-or-balpha-tau-normalization.md"
P_3805 = PCW / "3805-Y5-R2FR-no-XQ-visible-coefficient-sequester-theorem-or-component-bound-acquisition.md"
P_1050 = PCW / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
P_1057 = PCW / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
P_1091 = PCW / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md"
P_1098 = PCW / "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md"
P_1049 = PCW / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md"
P_1058 = PCW / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3807_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3807_CSA3806_PARENT_SIGNATURE_THEOREM.csv",
    "nogos": RESIDUALS / "P8_Y5_R2FR_3807_COUNTEREXAMPLE_NO_GO_AUDIT.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_3807_EFFECTIVE_READOUT_CLOSURE_CONTRACT.csv",
    "strict_audit": RESIDUALS / "P8_Y5_R2FR_3807_STRICT_CORPUS_SIGNATURE_AUDIT.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3807_COMPONENT_ROUTE_DECISION.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3807_CLAIM_GATES.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3807_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3807_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3807_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3807_0_3806_CSA", P_3806, "CSA3806", "3806 action-level clause and chain-rule zero"),
    ("SRC3807_1_3805_counterexample", P_3805, "q_X-basic", "3805 q_X-basic counterexample"),
    ("SRC3807_2_1050_product_functor", P_1050, "Product functor theorem attempt", "visible-hidden product functor conditional theorem"),
    ("SRC3807_3_1057_F2", P_1057, "lambda_A F_Q^2", "independent F2 counterterm obstruction"),
    ("SRC3807_4_1091_no_hom", P_1091, "RADIATIVE_READOUT_CLOSURE_UNSIGNED", "no-hidden-visible hom theorem and readout obstruction"),
    ("SRC3807_5_1098_owner_signature", P_1098, "OWNER_ACTION_SIGNATURE_NOT_DERIVED", "ordinary-constant owner action signature failure"),
    ("SRC3807_6_1049_readout", P_1049, "radiative_readout_closure", "operator classification readout closure warning"),
    ("SRC3807_7_1058_operator_domain", P_1058, "Radiative/readout closure gate", "visible operator domain exhaustion gate"),
    ("SRC3807_8_spine_handoff", P_SPINE, "3807-Y5-R2FR-CSA3806-parent-signature-or-effective-readout-closure-audit.md", "live spine target"),
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
            "PST3807_0_no_go",
            "q_X ownership is insufficient",
            "Assume locality, diffeo covariance, U(1) gauge covariance, and q_X=(q_obs,X_Q). The term DeltaS=-1/4 int sqrt(-g_obs) f(X_Q) F_Q^2 is local, gauge invariant, and q_X-basic. Therefore those assumptions do not imply CSA3806.",
            "EXACT_COUNTEREXAMPLE_NO_GO",
            "CSA3806 cannot be obtained by saying X_Q is quotient-owned; a stronger typed coefficient-domain rule is necessary.",
            "none; this is a negative theorem",
        ),
        (
            "PST3807_1_sufficient_type_split",
            "typed coefficient subquotient is sufficient",
            "Let Coeff_vis be a functor over ObsRep with objects (q_obs,theta_rep), and let the only XGeom-to-visible morphism be the declared connection constructor B_Q[Y_Q]->A_Q,F_Q. Then every c_J in Coeff_vis factors as c_J=cbar_J(pi_obs(q_X),theta_rep).",
            "EXACT_CONDITIONAL_FACTORISATION_THEOREM",
            "The CSA3806 chain-rule zero partial_XQ c_J=0 follows for Z_EM, masses, source weights, kappa, clock/readout markers, and boundary coefficients outside B_Q.",
            "parent must sign the type split and no extra hidden-visible coefficient morphisms",
        ),
        (
            "PST3807_2_BQ_exception",
            "B_Q is the only allowed X_Q readout",
            "X_Q may influence visible EM through Y_Q=Pi4(X_Q), B_Q=B_Q[Y_Q], and A_Q(B_Q). This path changes the field/readout object, not the coefficient c_J multiplying an independent visible operator.",
            "EXACT_CONDITIONAL_ROUTE_SEPARATION",
            "Keeps the EM-geometric route alive while forbidding f(X_Q)F^2 as a coefficient-leak shortcut.",
            "same-current/Hilbert stress and B_Q normalization still separate gates",
        ),
        (
            "PST3807_3_effective_functor",
            "effective/readout closure is required",
            "The renormalization and readout maps R_mu and Read must preserve the subquotient: R_mu(Coeff_vis) subset pullback(pi_obs)Coeff_obs and Read(O_vis) must not introduce X_Q coefficient slots.",
            "EXACT_CONDITIONAL_STABILITY_REQUIREMENT",
            "Tree-level CSA3806 is not enough; observed constants and clock/readout outputs inherit the zero only if the closure map commutes with the subquotient.",
            "radiative/effective/readout closure not strict-current signed",
        ),
        (
            "PST3807_4_strict_verdict",
            "strict current promotion",
            "The current source set contains conditional product-functor and ordinary-constant owner contracts, but also records that they are not parent-signed and that independent scalar F2/mass/source/readout vertices remain legal.",
            "FAIL_STRICT_CURRENT_PROMOTION",
            "CSA3806 is now the exact contract to derive, not a claimed theorem of the present corpus.",
            "MISSING_PARENT_TYPE_SPLIT_SIGNATURE;MISSING_EFFECTIVE_READOUT_CLOSURE",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "theorem_id": rid,
            "claim_piece": piece,
            "mathematical_statement": statement,
            "status": status,
            "consequence": consequence,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for rid, piece, statement, status, consequence, missing in rows
    ]


def nogo_rows(timestamp):
    rows = [
        (
            "NG3807_0_qX_basic",
            "q_X-basicness",
            "f(X_Q) is q_X-basic because X_Q is part of q_X",
            "visible coefficient leakage survives",
            "requires pi_obs subquotient, not full q_X coefficient access",
        ),
        (
            "NG3807_1_gauge",
            "U(1) gauge invariance",
            "f(X_Q)F_Q^2 is gauge invariant",
            "gauge symmetry alone cannot protect alpha/Z_EM",
            "requires unique kinetic owner or no coefficient slot",
        ),
        (
            "NG3807_2_diffeo",
            "diffeomorphism covariance",
            "sqrt(-g_obs) f(X_Q)F_Q^2 is a scalar density",
            "covariance alone allows the counterterm",
            "requires typed operator-domain exhaustion",
        ),
        (
            "NG3807_3_locality",
            "local action locality",
            "local functions f(X_Q(x)) multiply local visible operators",
            "locality alone makes the bad term easier, not harder",
            "requires hidden-visible coefficient hom ban",
        ),
        (
            "NG3807_4_tree_level",
            "bare tree-level separation",
            "loops/effective reductions/readout can regenerate deltaZ_eff(X_Q)F^2 or nu_i(X_Q)",
            "bare closure does not imply observed closure",
            "requires R_mu/Read commuting with the subquotient",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "nogo_id": rid,
            "tested_route": route,
            "counterexample": counterexample,
            "result": result,
            "repair_needed": repair,
            "valid_for_claim": "false",
        }
        for rid, route, counterexample, result, repair in rows
    ]


def closure_rows(timestamp):
    rows = [
        (
            "ERC3807_0_bare",
            "bare parent action",
            "S_bare contains CSA3806 and no mixed coefficient ideal I_mix",
            "written in 3806 but not strict-current signed",
            "tree-level coefficient leakage zero only conditionally",
        ),
        (
            "ERC3807_1_quantum",
            "Wilsonian/effective action",
            "R_mu must map allowed coefficient slots to allowed coefficient slots and must not create c_J(X_Q)",
            "unsigned",
            "otherwise alpha/mass/source residuals return as effective counterterms",
        ),
        (
            "ERC3807_2_readout",
            "clock/material/source readout",
            "Read_i must factor through q_obs, theta_rep, and declared B_Q field observables, not hidden coefficient maps",
            "unsigned",
            "otherwise clock nu_i(X_Q), source weights, or material markers re-enter after variation",
        ),
        (
            "ERC3807_3_boundary",
            "boundary/domain projection",
            "domain and boundary weights must be pi_obs-owned or fixed; no X_Q-dependent support weights",
            "unsigned",
            "otherwise local source tubes and R10/orbital projections can fake extra force",
        ),
        (
            "ERC3807_4_verdict",
            "closure package",
            "CSA3806 plus ERC3807_1 through ERC3807_3",
            "not promoted",
            "needed before local GR, WEP, R10, clock, or EM alpha claim",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "closure_id": rid,
            "layer": layer,
            "required_form": form,
            "current_status": status,
            "if_missing": if_missing,
            "valid_for_claim": "false",
        }
        for rid, layer, form, status, if_missing in rows
    ]


def strict_audit_rows(timestamp):
    checks = [
        ("SA3807_0_1050_product", P_1050, "Current verdict:", "product functor conditional, not parent-signed"),
        ("SA3807_1_1098_owner", P_1098, "OWNER_ACTION_SIGNATURE_NOT_DERIVED", "ordinary constant owner action signature not derived"),
        ("SA3807_2_1057_F2", P_1057, "lambda_A F_Q^2", "independent F2 branch retained unless operator domain closes"),
        ("SA3807_3_1091_hom", P_1091, "scalar obstruction survives", "hidden scalar obstruction/no-hom closure not signed"),
        ("SA3807_4_3806_clause", P_3806, "CLAUSE_WRITTEN_HERE_NOT_STRICT_CORPUS_SIGNED", "CSA3806 written here, not found as prior strict theorem"),
    ]
    rows = []
    for audit_id, path, needle, interpretation in checks:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "audit_id": audit_id,
                "source_path": str(path),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "interpretation": interpretation,
                "strict_parent_signature_found": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def decision_rows(timestamp):
    rows = [
        (
            "DEC3807_0_proof_result",
            "CSA3806 has an exact sufficient theorem and an exact no-go boundary.",
            "q_X/gauge/diffeo/locality cannot prove it, but a typed ObsRep coefficient functor plus B_Q-only exception does.",
            "Use this as the contract for the parent-action derivation.",
        ),
        (
            "DEC3807_1_strict_current",
            "Do not promote CSA3806 as current MTS theorem.",
            "Existing 1050/1098/1091/1057 rows explicitly keep product functor, owner signature, no-hom, and radiative closure unsigned.",
            "Keep every local arena blocked until parent signature or sourced components exist.",
        ),
        (
            "DEC3807_2_best_route",
            "Attack representation/superselection ownership next.",
            "The least-scrutiny route is not fitting coefficients; it is deriving that visible constants and coefficient slots are representation/superselection data, while X_Q only builds B_Q.",
            "Move to 3808 typed visible-coefficient owner from representation/superselection or finite bounds.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": rid,
            "decision": decision,
            "because": because,
            "next_action": action,
            "valid_for_claim": "false",
        }
        for rid, decision, because, action in rows
    ]


def gate_rows(timestamp, grouped):
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    all_audit_needles = all(row["needle_found"] == "true" for row in grouped["strict_audit"])
    theorem_ready = any(row["theorem_id"] == "PST3807_1_sufficient_type_split" for row in grouped["theorem"])
    no_go_ready = all(row["result"] for row in grouped["nogos"])
    closure_signed = False
    strict_signed = False
    rows = [
        ("CG3807_0_sources", all_sources, False, "all source needles found" if all_sources else "missing source or needle"),
        ("CG3807_1_no_go", no_go_ready, False, "counterexample no-go audit emitted"),
        ("CG3807_2_sufficient_theorem", theorem_ready, False, "conditional typed coefficient theorem emitted"),
        ("CG3807_3_strict_parent_signed", strict_signed, False, "strict corpus does not sign CSA3806"),
        ("CG3807_4_effective_readout_signed", closure_signed, False, "effective/readout closure remains unsigned"),
        ("CG3807_5_strict_audit_needles", all_audit_needles, False, "audit needles support non-promotion"),
        ("CG3807_6_claims_closed", False, False, "no local-GR/EM/WEP/R10/clock claim allowed"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": rid,
            "pass": str(passed).lower(),
            "claim_allowed": str(claim).lower(),
            "details": details,
            "valid_for_claim": "false",
        }
        for rid, passed, claim, details in rows
    ]


def next_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3808-Y5-R2FR-visible-coefficient-type-system-from-representation-superselection-or-finite-bounds.md",
            "target_script": "scripts/Y5_R2FR_3808_visible_coefficient_type_system_from_representation_superselection_or_finite_bounds.py",
            "objective": "Try to derive the CSA3806 type split from parent representation/superselection data: visible constants and coefficients are ObsRep objects, X_Q only constructs B_Q/A_Q/F_Q; if that fails, emit finite component-bound rows for alpha, mass, source, kappa, clock, and boundary channels.",
            "avoid": "do not claim CSA3806 from q_X ownership alone; do not fit coefficients without source-backed priors; do not edit formalization-workbench",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_CSA3806_EXACT_CONTRACT_DERIVED_STRICT_PARENT_SIGNATURE_UNSIGNED",
            "summary": "3807 proves the exact no-go for weak assumptions, writes the exact sufficient parent type-split theorem, and keeps claims closed because strict corpus and effective/readout closure are unsigned.",
            "valid_for_claim": "false",
        }
    ]


def validation_rows(timestamp, grouped):
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            load_csv(path)
    fwb_hits = list(FWB.rglob("*3807*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    text_paths = [DOC_PATH, SCRIPT_PATH]
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in text_paths if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("strict_audit_needles", all(row["needle_found"] == "true" for row in grouped["strict_audit"]), "strict audit needles found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3807 markdown document written"),
        ("no_go_present", any(row["theorem_id"] == "PST3807_0_no_go" for row in grouped["theorem"]), "exact q_X no-go theorem emitted"),
        ("sufficient_theorem_present", any(row["theorem_id"] == "PST3807_1_sufficient_type_split" for row in grouped["theorem"]), "typed coefficient sufficient theorem emitted"),
        ("effective_readout_unsigned", any(row["current_status"] == "unsigned" for row in grouped["closure"]), "effective/readout closure remains explicit unsigned gate"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("formalization_clean", not fwb_hits, "no 3807 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": cid,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for cid, passed, detail in checks
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
        "# 3807 - CSA3806 Parent Signature Or Effective Readout Closure Audit",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_CSA3806_EXACT_CONTRACT_DERIVED_STRICT_PARENT_SIGNATURE_UNSIGNED`.",
        "",
        "3807 takes the leap rather than only saying 'missing'. The result is sharp:",
        "",
        "- Weak assumptions fail: q_X ownership, locality, covariance, and U(1) gauge symmetry all allow `f(X_Q)F_Q^2`.",
        "- Strong typed action-domain succeeds conditionally: if visible coefficients are `ObsRep` objects and the only `X_Q` bridge is `B_Q -> A_Q,F_Q`, then `c_J=cbar_J(pi_obs(q_X),theta_rep)` and `partial_XQ c_J=0`.",
        "- Effective/readout closure is mandatory: the same split must survive RG/effective action and clock/material/source readout.",
        "- Strict current MTS has not signed that package, so this is a contract to derive, not a local-GR or alpha claim.",
        "",
        "## Human Read",
        "",
        "This is progress. The coupling problem is no longer foggy; it is now exactly the same kind of structural move as an equivalence-principle/minimal-coupling clause. The theory does not need to numerically derive every constant to be serious, but it does need to derive why the constants and visible coefficient slots are universal representation data rather than hidden local `X_Q` functions.",
        "",
        "The next best attack is therefore representation/superselection ownership: prove visible constants live in `ObsRep`, while `X_Q` only builds EM geometry through `B_Q`.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Parent Signature Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("Counterexample No-Go Audit", "nogos", ["nogo_id", "tested_route"]),
        ("Effective Readout Closure Contract", "closure", ["closure_id", "layer"]),
        ("Strict Corpus Signature Audit", "strict_audit", ["audit_id"]),
        ("Decision Rows", "decisions", ["decision_id"]),
        ("Claim Gates", "gates", ["gate_id"]),
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
        "nogos": nogo_rows(timestamp),
        "closure": closure_rows(timestamp),
        "strict_audit": strict_audit_rows(timestamp),
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
