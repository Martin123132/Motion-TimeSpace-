import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3811"
BRANCH = "MTS_R2FR_Y5_NO_HIDDEN_VISIBLE_MORPHISM_OR_FULL_RANK_PRODUCT_BRIDGE_3811"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3811-Y5-R2FR-no-hidden-visible-coupling-morphism-signature-or-full-rank-product-bridge.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3811_no_hidden_visible_coupling_morphism_signature_or_full_rank_product_bridge.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3810 = PCW / "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md"
P_1114 = PCW / "1114-Y5-R10-no-hidden-visible-coefficient-morphism-theorem-or-finite-coupling-inputs.md"
P_3271 = PCW / "3271-Y5-R2FR-hidden-visible-hom-typing-proof-or-coupling-coefficient-bound-pack-under-AX1090.md"
P_3469 = PCW / "3469-Y5-R2FR-visible-coefficient-owner-contract-or-multiarena-vector-runner.md"
P_3475 = PCW / "3475-Y5-R2FR-surviving-mass-electron-null-direction-theorem-or-clock-mu-row.md"
P_3480 = PCW / "3480-Y5-R2FR-parent-transport-and-source-normalization-owner-or-product-bound-upgrade.md"
P_3481 = PCW / "3481-Y5-R2FR-source-current-Jq-theorem-or-first-transport-normalizer-row.md"
P_3482 = PCW / "3482-Y5-R2FR-earth-source-amplitude-SEq-current-bound-or-zero-theorem.md"
P_3483 = PCW / "3483-Y5-R2FR-quadratic-DD-WEP-source-runner-or-external-SEq-lower-bound.md"

P_3475_RANK = RESIDUALS / "P8_Y5_R2FR_3475_RANK_LEDGER.csv"
P_3475_CLOCK = RESIDUALS / "P8_Y5_R2FR_3475_CLOCK_MU_SENSITIVITY_SOURCE.csv"
P_3475_NULL = RESIDUALS / "P8_Y5_R2FR_3475_NULLSPACE_BASIS.csv"
P_3480_INV = RESIDUALS / "P8_Y5_R2FR_3480_FULL_RANK_INVERSION_THEOREM.csv"
P_3480_REQ = RESIDUALS / "P8_Y5_R2FR_3480_TRANSPORT_SOURCE_REQUIREMENT_MATRIX.csv"
P_3481_WEP = RESIDUALS / "P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv"
P_3482_BRANCH = RESIDUALS / "P8_Y5_R2FR_3482_SEQ_BRANCH_LOGIC.csv"
P_3483_THEOREM = RESIDUALS / "P8_Y5_R2FR_3483_QUADRATIC_WEP_THEOREM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3811_SOURCE_REGISTER.csv",
    "morphism": RESIDUALS / "P8_Y5_R2FR_3811_MORPHISM_BAN_DERIVATION_AUDIT.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_3811_PARENT_SIGNATURE_SEARCH.csv",
    "product_bridge": RESIDUALS / "P8_Y5_R2FR_3811_FULL_RANK_PRODUCT_BRANCH_BRIDGE.csv",
    "transport": RESIDUALS / "P8_Y5_R2FR_3811_TRANSPORT_SOURCE_REQUIREMENT_BRIDGE.csv",
    "branch_logic": RESIDUALS / "P8_Y5_R2FR_3811_SOURCE_AMPLITUDE_BRANCH_LOGIC.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3811_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3811_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3811_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3811_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3811_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3811_0_3810", P_3810, "POC3810_3_no_hidden_visible_coefficients", "3810 selects no-hidden-visible coefficient morphism as the hardest clause"),
    ("SRC3811_1_1114", P_1114, "NHV1114_6_verdict", "1114 exact theorem attempt and scalar obstruction"),
    ("SRC3811_2_3271", P_3271, "QFT3271_2_typed_visible_algebra", "3271 quotient/fibre-constant theorem and typed visible algebra"),
    ("SRC3811_3_3469", P_3469, "VCO3469_6_contract_verdict", "3469 visible coefficient owner contract"),
    ("SRC3811_4_3475_doc", P_3475, "RANK3475_0_WEP_alpha_clock_plus_SrCs_mu", "3475 full sensitivity rank result"),
    ("SRC3811_5_3480_doc", P_3480, "FIT3480_0_full_rank_visible_inversion", "3480 inverse theorem and transport bottleneck"),
    ("SRC3811_6_3481_doc", P_3481, "WEN3481_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "3481 WEP normalizers collapse to shared Earth source amplitude"),
    ("SRC3811_7_3482_doc", P_3482, "BR3482_1_same_visible_vector_DD", "3482 external-amplitude versus same-vector branch split"),
    ("SRC3811_8_3483_doc", P_3483, "THM3483_0_same_vector_substitution", "3483 same-vector WEP quadratic theorem"),
    ("SRC3811_9_3475_rank", P_3475_RANK, "RANK3475_0_WEP_alpha_clock_plus_SrCs_mu", "rank-four sensitivity ledger"),
    ("SRC3811_10_3475_clock", P_3475_CLOCK, "CLK3475_0_SrCs_mu_q_alpha", "Sr/Cs sensitivity row"),
    ("SRC3811_11_3475_null", P_3475_NULL, "NULL3475_NONE", "full-rank nullspace closure"),
    ("SRC3811_12_3480_inverse", P_3480_INV, "FIT3480_0_full_rank_visible_inversion", "full-rank inverse theorem csv"),
    ("SRC3811_13_3480_req", P_3480_REQ, "REQ3480_Y_0", "transport/source normalizer requirements"),
    ("SRC3811_14_3481_wep", P_3481_WEP, "WEN3481_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "WEP normalizer row"),
    ("SRC3811_15_3482_branch", P_3482_BRANCH, "BR3482_1_same_visible_vector_DD", "source amplitude branch logic"),
    ("SRC3811_16_3483_theorem", P_3483_THEOREM, "THM3483_0_same_vector_substitution", "quadratic WEP theorem csv"),
    ("SRC3811_17_spine", SPINE_PATH, "3811-Y5-R2FR-no-hidden-visible-coupling-morphism-signature-or-first-alpha-product-row.md", "live spine 3811 handoff"),
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


def bool_text(value):
    return str(bool(value)).lower()


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
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def morphism_rows(timestamp):
    rows = [
        (
            "MB3811_0_exact_equivalence",
            "no hidden-visible coefficient morphism",
            "For each visible coefficient c_vis:P->Coeff, c_vis descends through q_obs iff it is constant on q_obs-fibres; then L_v c_vis=0 for v in ker(Dq_obs).",
            "EXACT_THEOREM",
            "This converts the coupling problem into a fibre-constancy/type-domain statement, not a vague naturalness demand.",
            "none for the mathematics; parent evidence must prove the premise coefficient-by-coefficient",
        ),
        (
            "MB3811_1_typed_visible_algebra",
            "sufficient object-language signature",
            "If A_ord=q_obs^*A_Q tensor A_fixed and ordinary coefficient slots are sections of A_ord only, then Hom(A_hid,Coeff_vis) has no nonconstant vertical component.",
            "EXACT_CONDITIONAL_TYPED_THEOREM",
            "This would zero b_alpha, b_mhat, b_me, source weights, kappa drifts, and readout coefficient slopes on the local branch.",
            "parent-signed visible coefficient algebra; fixed representation data; readout/radiative preservation",
        ),
        (
            "MB3811_2_scalar_countermodel",
            "why covariance/gauge symmetry cannot finish it",
            "If a nonconstant hidden/local scalar I_hid survives and Coeff_vis accepts scalar functions, then c=c0+epsilon I_hid is a legal coefficient and f(I_hid)F^2, y(I_hid)H psi psi, kappa(I_hid)T, or readout(I_hid) can be formed.",
            "COUNTERMODEL_THEOREM_RETAINED",
            "The parent must either trivialize hidden invariant algebra or type hidden invariants out of visible coefficient slots.",
            "no hidden invariant target; no extension/marker slot; no readout return path",
        ),
        (
            "MB3811_3_current_signature_result",
            "strict-current parent signature",
            "The corpus contains the exact theorem and exact contract, but not a parent action signature proving A_ord=q_obs^*A_Q tensor A_fixed for every visible coefficient slot.",
            "NOT_PARENT_SIGNED",
            "Do not repeat the morphism-ban hunt as if the proof were missing; the missing object is a parent signature, not the theorem shape.",
            "MISSING_PARENT_VISIBLE_COEFFICIENT_ALGEBRA_SIGNATURE",
        ),
        (
            "MB3811_4_bridge_result",
            "fallback is full-rank product discipline",
            "Existing 3475/3480 work gives full sensitivity rank and C=A^{-1}Y on the visible coefficient vector, so the empirical route is no longer symbolic; the bottleneck is transport/source normalization.",
            "DERIVED_BRIDGE",
            "The next work should attack row normalizers/source amplitude, not add another loose missing ledger.",
            "MISSING_PARENT_TRANSPORT_NORMALIZERS;MISSING_SOURCE_AMPLITUDE_BRANCH_DECISION",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "audit_id": audit_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "result": result,
            "advance": advance,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for audit_id, claim_piece, statement, result, advance, missing in rows
    ]


def signature_rows(timestamp):
    rows = [
        ("SIG3811_0_1114", "typed/product-category theorem", "EXACT_CONDITIONAL", "not parent-derived from current corpus"),
        ("SIG3811_1_3271", "A_ord=q*A_Q tensor A_fixed", "EXACT_TYPED_DOMAIN_THEOREM", "parent visible coefficient algebra not signed"),
        ("SIG3811_2_3469", "VisibleCoefficientOwner contract", "CONTRACT_READY_NOT_PARENT_SIGNED", "contract sharp but not a parent theorem"),
        ("SIG3811_3_3472", "VisibleSourceOwner theorem", "NO_PARENT_SIGNED_ZERO_USE_FULL_DD_VECTOR", "source coefficients require full DD/product branch"),
        ("SIG3811_4_3810", "Z_Q_eff/readout descent", "SUFFICIENT_CONTRACT_UNSIGNED", "depends on no-hidden-visible coefficient clause plus radiative/readout closure"),
        ("SIG3811_5_verdict", "morphism ban promotion", "FAIL_STRICT_CURRENT_PARENT_SIGNATURE", "route remains conditional; switch active work to transport/source normalization bridge"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "signature_id": signature_id,
            "object": obj,
            "source_status": source_status,
            "strict_result": strict_result,
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for signature_id, obj, source_status, strict_result in rows
    ]


def product_bridge_rows(timestamp):
    rank_rows = load_csv(P_3475_RANK)
    null_rows = load_csv(P_3475_NULL)
    inverse_rows = load_csv(P_3480_INV)
    clock_rows = load_csv(P_3475_CLOCK)
    rank = rank_rows[0] if rank_rows else {}
    null = null_rows[0] if null_rows else {}
    inverse = inverse_rows[0] if inverse_rows else {}
    alpha_clock = [row for row in clock_rows if row.get("clock_row_id") == "CLK3475_0_SrCs_mu_q_alpha"]
    alpha_clock_row = alpha_clock[0] if alpha_clock else (clock_rows[0] if clock_rows else {})
    rows = [
        (
            "FPB3811_0_full_sensitivity_rank",
            "visible coefficient vector",
            "WEP rows plus Yb alpha clock plus Sr/Cs mass-ratio clock",
            f"rank={rank.get('rank','MISSING')};nullspace_dimension={rank.get('nullspace_dimension','MISSING')};status={rank.get('status','MISSING')}",
            "This kills the algebraic null-direction excuse at sensitivity level.",
            "rank geometry only; product rows still need parent transport/source normalization",
        ),
        (
            "FPB3811_1_nullspace_status",
            "source coefficient nullspace",
            "four-channel visible DD-style basis",
            f"basis={null.get('basis_id','MISSING')};status={null.get('status','MISSING')}",
            "No algebraic nullspace remains in the external-amplitude sensitivity matrix.",
            "same-vector Earth-source branch still has a quadratic blind family unless separately closed",
        ),
        (
            "FPB3811_2_inverse_theorem",
            "C=A^{-1}Y",
            "full-rank visible sensitivity matrix",
            f"status={inverse.get('status','MISSING')};numeric={inverse.get('numeric_evidence','MISSING')}",
            "The finite branch can now be written as product-bound formulae rather than symbolic placeholders.",
            "Y rows have mixed units; row normalizers N_r are not parent-owned",
        ),
        (
            "FPB3811_3_sr_cs_clock_row",
            "Sr/Cs mass-ratio clock sensitivity",
            alpha_clock_row.get("published_formula", "MISSING"),
            f"bound={alpha_clock_row.get('bound_expression','MISSING')};rank_use={alpha_clock_row.get('rank_use','MISSING')}",
            "This is the row that closed the last sensitivity-rank hole.",
            "published clock product only; no standalone MTS coefficient without transport/time/source map",
        ),
        (
            "FPB3811_4_3810_alpha_product_status",
            "first alpha/product row under 3810 contract",
            "clock/visible coefficient product rows exist as source-backed rank rows, not MTS predictions",
            "SOURCE_BACKED_BOUND_SIDE_NONCLAIM",
            "This satisfies the demand that fallback rows be concrete rather than placeholders.",
            "MTS numerator, tau/transport, source amplitude, and same-branch readout are still missing",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "bridge_id": bridge_id,
            "object": obj,
            "input_branch": input_branch,
            "evidence": evidence,
            "advance": advance,
            "remaining_blocker": blocker,
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for bridge_id, obj, input_branch, evidence, advance, blocker in rows
    ]


def transport_rows(timestamp):
    rows = []
    for req in load_csv(P_3480_REQ):
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "requirement_id": "TBR3811_" + req["requirement_id"],
                "row_symbol": req["row_symbol"],
                "arena": req["arena"],
                "required_normalizer": req["required_normalizer"],
                "missing_parent_inputs": req["missing_parent_inputs"],
                "current_status": req["status"],
                "next_action": "derive or source-fill this normalizer without setting it to unity",
                "valid_for_claim": "false",
            }
        )
    return rows


def branch_logic_rows(timestamp):
    branch_rows = load_csv(P_3482_BRANCH)
    theorem_rows = load_csv(P_3483_THEOREM)
    rows = []
    for branch in branch_rows:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "logic_id": "SBL3811_" + branch["branch_id"],
                "branch_assumption": branch["assumption"],
                "math_form": branch["math_form"],
                "what_it_changes": branch["what_3481_buys"],
                "needed_for_claim": branch["needed_for_claim"],
                "current_status": branch["status"],
                "valid_for_claim": "false",
            }
        )
    for theorem in theorem_rows:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "logic_id": "SBL3811_" + theorem["theorem_id"],
                "branch_assumption": "same-vector DD WEP theorem",
                "math_form": theorem["statement"],
                "what_it_changes": theorem["consequence"],
                "needed_for_claim": "respect branch split before using WEP rows as coefficient bounds",
                "current_status": "THEOREM_CARRIED_FORWARD",
                "valid_for_claim": "false",
            }
        )
    return rows


def gate_rows(timestamp, grouped):
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    full_rank = any("rank=4" in row["evidence"] and "nullspace_dimension=0" in row["evidence"] for row in grouped["product_bridge"])
    inverse = any(row["bridge_id"] == "FPB3811_2_inverse_theorem" and "DERIVED" in row["evidence"] for row in grouped["product_bridge"])
    signature_failed = any(row["signature_id"] == "SIG3811_5_verdict" and row["source_status"] == "FAIL_STRICT_CURRENT_PARENT_SIGNATURE" for row in grouped["signature"])
    rows = [
        ("CG3811_0_sources", all_sources, False, "all source paths and needles resolve" if all_sources else "source/needle blocker"),
        ("CG3811_1_morphism_theorem_exact", True, False, "fibre-constancy and typed visible algebra theorem carried forward"),
        ("CG3811_2_parent_signature_signed", False, False, "no strict-current parent visible coefficient algebra signature found"),
        ("CG3811_3_countermodel_retained", True, False, "hidden scalar coefficient countermodel retained"),
        ("CG3811_4_full_rank_bridge", full_rank, False, "3475 full sensitivity rank imported"),
        ("CG3811_5_inverse_bridge", inverse, False, "3480 inverse theorem imported"),
        ("CG3811_6_transport_normalizers_owned", False, False, "row normalizers/source amplitude remain unsigned"),
        ("CG3811_7_claims_closed", signature_failed, False, "no local-GR/WEP/R10/clock/alpha claim allowed"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": gate_id,
            "pass": bool_text(passed),
            "claim_allowed": bool_text(claim_allowed),
            "details": details,
            "valid_for_claim": "false",
        }
        for gate_id, passed, claim_allowed, details in rows
    ]


def decision_rows(timestamp):
    rows = [
        (
            "DEC3811_0_no_repeat",
            "Do not keep redoing the no-hidden-visible theorem from scratch.",
            "The theorem shape is exact; the strict-current failure is the parent signature, not the mathematics.",
            "Use the contract as a target, but stop spending the main route on another missing-ledger audit.",
        ),
        (
            "DEC3811_1_empirical_bridge",
            "Carry forward the full-rank product branch as the empirical route.",
            "3475 gives rank four and 3480 gives C=A^{-1}Y, so the fallback is now a serious product-bound bridge.",
            "Treat source/clock transport normalizers as the active bottleneck.",
        ),
        (
            "DEC3811_2_branch_guard",
            "Split external source amplitude from same-visible-vector Earth-source branch.",
            "3482/3483 show that if S_Eq=Q_Earth dot C, WEP becomes quadratic and the linear rank story must be branch-limited.",
            "Next work must preserve this branch split.",
        ),
        (
            "DEC3811_3_next",
            "Attack parent transport/source normalization next.",
            "This is the shortest path from full-rank sensitivity geometry to an actual local-GR/WEP/clock coefficient test.",
            "Move to 3812 transport/source normalizer or same-vector DD branch bridge.",
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
            "target_doc": "3812-Y5-R2FR-parent-transport-source-normalizer-or-same-vector-DD-branch-bridge.md",
            "target_script": "scripts/Y5_R2FR_3812_parent_transport_source_normalizer_or_same_vector_DD_branch_bridge.py",
            "objective": "Use the 3811 bridge to attack the real bottleneck: derive/source-fill row normalizers N_r and the Earth/source amplitude branch without setting them to unity; carry the same-vector quadratic DD guard so WEP rows are not misused as independent linear constraints.",
            "success_gate": "At least one transport/source normalizer is parent-derived or source-filled with units, or the same-vector DD branch has an executable nonclaim runner that respects the Q_Earth dot C blind-family theorem.",
            "avoid": "do not redo no-Hom theorem unless a new parent signature source appears; do not claim local GR/WEP/R10/clock; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_MORPHISM_SIGNATURE_NOT_PARENT_SIGNED_FULL_RANK_PRODUCT_BRIDGE_IMPORTED",
            "summary": "3811 confirms the no-hidden-visible morphism theorem is exact but not parent-signed, imports the 3475 full-rank and 3480 inverse product branch, and redirects the live work to transport/source normalizers and source-amplitude branch logic rather than another morphism-ledger loop.",
            "valid_for_claim": "false",
        }
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
        "# 3811 - No Hidden-Visible Coupling Morphism Signature Or Full-Rank Product Bridge",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_MORPHISM_SIGNATURE_NOT_PARENT_SIGNED_FULL_RANK_PRODUCT_BRIDGE_IMPORTED`.",
        "",
        "3811 stops the loop. The no-hidden-visible theorem is not vague anymore: visible coefficients descend exactly when they are fibre-constant, and the typed visible algebra `A_ord=q_obs^*A_Q tensor A_fixed` would prove the coupling ban. Current MTS still does not parent-sign that algebra, so the theorem remains conditional.",
        "",
        "The useful forward move is that the fallback is no longer symbolic. The 3475/3480 branch already gives full sensitivity rank and an exact inverse `C=A^{-1}Y`; the real remaining throat is transport/source normalization, not another coefficient-morphism audit.",
        "",
        "No claim is made. The branch split from 3482/3483 is carried forward: external source amplitude gives a linear inverse only after a source lower/normalizer theorem; same-visible-vector Earth source makes WEP quadratic and cannot be used as independent linear rank evidence.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Morphism Ban Derivation Audit", "morphism", ["audit_id", "claim_piece"]),
        ("Parent Signature Search", "signature", ["signature_id"]),
        ("Full-Rank Product Branch Bridge", "product_bridge", ["bridge_id", "object"]),
        ("Transport Source Requirement Bridge", "transport", ["requirement_id", "row_symbol"]),
        ("Source Amplitude Branch Logic", "branch_logic", ["logic_id"]),
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


def update_spine():
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    lines = text.splitlines()
    if lines and lines[0].startswith("# Local GR Coupling Spine - Current State After "):
        lines[0] = "# Local GR Coupling Spine - Current State After 3811"
        text = "\n".join(lines) + "\n"

    paragraph = (
        "`3811` resolves the coupling-fork bookkeeping. The no-hidden-visible morphism theorem is exact as a fibre-constancy/type-domain statement, but the strict corpus still does not parent-sign the visible coefficient algebra `A_ord=q_obs^*A_Q tensor A_fixed`. "
        "The important progress is the bridge to the older full-rank product branch: 3475 gives rank-four visible sensitivity geometry and 3480 gives `C=A^{-1}Y`; therefore the live empirical throat is row transport/source normalization, plus the 3482/3483 branch split between external source amplitude and same-vector quadratic WEP."
    )
    if "`3811` resolves the coupling-fork bookkeeping." not in text:
        marker = "`3810` writes the full parent-owned `Z_Q_eff`/readout descent contract."
        idx = text.find(marker)
        if idx >= 0:
            next_blank = text.find("\n\n", idx)
            if next_blank >= 0:
                text = text[: next_blank + 2] + paragraph + "\n\n" + text[next_blank + 2 :]

    bullet = "- `3811 morphism/product bridge`: no-Hom remains parent-unsigned, but the finite branch is full-rank at sensitivity level; the active bottleneck is transport/source normalizers `N_r` and the `S_Eq` branch, not another symbolic alpha row."
    if bullet not in text:
        anchor = "- `3810 Z_Q_eff/readout contract`: alpha/readout silence follows by chain rule only if the full effective normalization, readout map, same-current source branch, and arena projections descend through the same parent-owned quotient."
        text = text.replace(anchor, anchor + "\n" + bullet)

    nonclaim = "- The 3811 morphism/product bridge is nonclaim for the strict current corpus; `A_ord=q_obs^*A_Q tensor A_fixed` is not parent-signed, and full-rank product rows remain nonclaim until transport/source normalizers and source-amplitude branch logic are derived or source-filled."
    if nonclaim not in text:
        anchor = "- The 3810 parent-owned Z_Q_eff/readout contract is nonclaim for the strict current corpus; it gives the exact theorem-zero contract, but parent norm descent, no hidden-visible coefficient morphisms, radiative/readout naturality, same-current source ownership, and arena maps remain unsigned."
        text = text.replace(anchor, anchor + "\n" + nonclaim)

    old_target = (
        "`3811-Y5-R2FR-no-hidden-visible-coupling-morphism-signature-or-first-alpha-product-row.md`\n\n"
        "Target: try to parent-sign the object-language/type theorem forbidding nonconstant hidden-to-visible coefficient morphisms for `Z_EM`, masses, kappa, source weights, clock markers, and readout coefficients; if it fails, source one complete finite alpha product row under the 3810 strict runner contract.\n\n"
        "This is the best next move because 3810 shows the global descent/readout contract is sufficient but unsigned. The hardest live clause is the coupling morphism ban: without it, `f(X_Q)F^2`, mass/source/clock coefficient leaks, and arena products remain legal."
    )
    new_target = (
        "`3812-Y5-R2FR-parent-transport-source-normalizer-or-same-vector-DD-branch-bridge.md`\n\n"
        "Target: use the 3811 bridge to attack transport/source normalizers `N_r` and the Earth/source amplitude branch without setting them to unity; preserve the same-vector quadratic DD guard so WEP rows are not misused as independent linear constraints.\n\n"
        "This is the best next move because the no-Hom theorem shape is already exact but parent-unsigned, while the finite branch has full sensitivity rank. The remaining path to a real local test is deriving/source-filling compatible row normalizers or proving a source-amplitude theorem."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3811_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3811_MORPHISM_BAN_DERIVATION_AUDIT.csv",
        "P8_Y5_R2FR_3811_PARENT_SIGNATURE_SEARCH.csv",
        "P8_Y5_R2FR_3811_FULL_RANK_PRODUCT_BRANCH_BRIDGE.csv",
        "P8_Y5_R2FR_3811_TRANSPORT_SOURCE_REQUIREMENT_BRIDGE.csv",
        "P8_Y5_R2FR_3811_SOURCE_AMPLITUDE_BRANCH_LOGIC.csv",
        "P8_Y5_R2FR_3811_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3811_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3811_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3811_STATUS.csv",
        "P8_Y5_BRR545_3811_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp, grouped):
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            load_csv(path)
    fwb_hits = list(FWB.rglob("*3811*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3811 markdown document written"),
        ("morphism_exact", any(row["audit_id"] == "MB3811_0_exact_equivalence" for row in grouped["morphism"]), "morphism theorem equivalence emitted"),
        ("signature_not_claimed", any(row["signature_id"] == "SIG3811_5_verdict" and row["source_status"] == "FAIL_STRICT_CURRENT_PARENT_SIGNATURE" for row in grouped["signature"]), "parent signature failure explicit"),
        ("full_rank_imported", any("rank=4" in row["evidence"] and "nullspace_dimension=0" in row["evidence"] for row in grouped["product_bridge"]), "3475 full-rank result imported"),
        ("inverse_imported", any(row["bridge_id"] == "FPB3811_2_inverse_theorem" and "DERIVED" in row["evidence"] for row in grouped["product_bridge"]), "3480 inverse theorem imported"),
        ("transport_requirements", len(grouped["transport"]) == 4, "four row normalizer requirements carried forward"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("spine_updated", "Current State After 3811" in spine_text and "3812-Y5-R2FR-parent-transport-source-normalizer-or-same-vector-DD-branch-bridge.md" in spine_text, "live spine updated to 3811 and 3812 target"),
        ("formalization_clean", not fwb_hits, "no 3811 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
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


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_rows(timestamp),
        "morphism": morphism_rows(timestamp),
        "signature": signature_rows(timestamp),
        "product_bridge": product_bridge_rows(timestamp),
        "transport": transport_rows(timestamp),
        "branch_logic": branch_logic_rows(timestamp),
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
    update_spine()
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
