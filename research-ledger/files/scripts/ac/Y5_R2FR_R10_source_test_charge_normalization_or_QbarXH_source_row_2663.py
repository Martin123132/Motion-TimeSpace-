from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2663"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2663-Y5-R2FR-R10-source-test-charge-normalization-or-QbarXH-source-row.md"

CHECKPOINT = "2663"
BRANCH_ID = "Y5_R2FR_R10_SOURCE_TEST_CHARGE_NORMALIZATION_2663"
PARENT_BRANCH = "Y5_R2FR_R10_PROFILE_TAU_MAP_2662"
PREFIX = "P8_Y5_R10_CHARGE_NORMALIZATION_2663"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "PLACEHOLDER",
    "NOT_DERIVED",
    "NOT_PARENT",
    "BLOCKED",
    "FORBIDDEN",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "charge_derivation": RESIDUALS / f"{PREFIX}_CHARGE_DERIVATION.csv",
    "qbar_source_template": RESIDUALS / f"{PREFIX}_QBAR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
    "kx_normalization_gate": RESIDUALS / f"{PREFIX}_KX_NORMALIZATION_GATE.csv",
    "zero_switch_gate": RESIDUALS / f"{PREFIX}_ZERO_SWITCH_GATE.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_CHARGE_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2663_R10_SOURCE_TEST_CHARGE_INPUT_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "R10_source_test_charge_normalization_2663_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "R10_SOURCE_TEST_CHARGE_NORMALIZATION_2663_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2663_R10_QBAR_SOURCE_ROW_TEMPLATE.csv",
    "quarantine": QUARANTINE / "P8_Y5_2663_CHARGE_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2662_doc": {
        "path": ROOT / "2662-Y5-R2FR-R10-profile-normalization-and-tau-map-or-bound-curve-digitizer.md",
        "needles": ["TAU2662_2_extended_profile", "ID2662_5_tau_one_verdict", "NEXT2662_0_selected"],
        "role": "immediate handoff deriving tau_R10 as a profile functional and selecting source/test charge normalization",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["PHA1025_7_prefactor", "ASR1025_3_Hamiltonian_projection", "DEC1025_3_coupling"],
        "role": "alpha prefactor, Qbar_XH projection and coupling-normalization gap",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["SP1019_0_M_H_ref", "SP1019_3_bulk_R10_projection", "PO1019_4_conditional_zero"],
        "role": "source-pack schema, Hamiltonian denominator and edge/source projector zero conditions",
    },
    "1024_doc": {
        "path": ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
        "needles": ["ALPHA1024_3_bulk_R10_projection", "RUN1024_3_bulk_R10_projection", "BV1024_2_coupling_status"],
        "role": "bulk alpha coefficient row and runner refusal for missing projection inputs",
    },
    "1027_doc": {
        "path": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
        "needles": ["QZ1027_0_chain_rule", "DEP1027_0_alpha_product", "BV1027_0_conditional_zero"],
        "role": "test-side qbar_XT zero theorem target and alpha product dependency",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def has_missing(row: dict[str, Any]) -> bool:
    joined = " ".join(str(value) for value in row.values())
    return any(token in joined for token in MISSING_TOKENS)


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2663_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def charge_derivation_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "derivation_id": "CHG2663_0_target",
            "object": "R10 source/test charge normalization",
            "statement": "R10 scoring needs the parent X-channel charge of the source, the test response, the field normalization prefactor and the same-convention profile map in one frame.",
            "derived_form": "alpha_R10(lambda)=K_X(lambda) Qbar_XH(lambda) qbar_XT tau_R10(lambda)+alpha_tail_abs(lambda)",
            "status": "TARGET_SHARP",
            "missing_for_claim": "Z_X, sign s_X, G_obs frame, Q_X^H, Pi_M^H, M_H_ref, qbar_XT, tau_R10 numeric profile and tail bound",
        },
        {
            "derivation_id": "CHG2663_1_parent_charge_definition",
            "object": "source charge Q_X[B]",
            "statement": "The only honest source charge is an integral of the parent source current over the same Hamiltonian/body domain used by the R10 projection, with edge terms separated.",
            "derived_form": "Q_X[B]=integral_B rho_X dV_H + Q_edge_X[B]",
            "status": "CONDITIONAL_DEFINITION_SCHEMA",
            "missing_for_claim": "parent source current rho_X, Hamiltonian volume/coframe descent, body domain B, and edge split",
        },
        {
            "derivation_id": "CHG2663_2_Qbar_XH",
            "object": "mass-normalized source charge",
            "statement": "The source factor entering alpha(lambda) is the mass-normalized Hamiltonian projection already requested by 1025 and 1019.",
            "derived_form": "Qbar_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/M_H_ref",
            "status": "EXACT_SCHEMA_NOT_PARENT_FILLED",
            "missing_for_claim": "Pi_M^H, Q_X^H(lambda), M_H_ref, units and source path",
        },
        {
            "derivation_id": "CHG2663_3_KX_prefactor",
            "object": "field normalization prefactor",
            "statement": "If the static X block is normalized as in 1025, the Yukawa alpha prefactor is fixed by the same branch Z_X and the observed Newton frame.",
            "derived_form": "K_X=s_X/(4*pi*Z_X*G_obs)",
            "status": "CONDITIONAL_EXACT_PREFAC_NOT_PARENT_FILLED",
            "missing_for_claim": "parent-signed Z_X, sign s_X, same-frame G_obs and dimensional ledger",
        },
        {
            "derivation_id": "CHG2663_4_test_response",
            "object": "test charge qbar_XT",
            "statement": "The test-side response is zero only if the visible-domain/matter-descent clauses from 1027 close; otherwise it is a finite source coefficient.",
            "derived_form": "qbar_XT=0 only under parent-signed q-kernel, observed coframe functor, matter descent, no-marker constants and no hidden tails",
            "status": "ZERO_SWITCH_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_claim": "visible-domain certificate or sourced finite qbar_XT coefficient",
        },
        {
            "derivation_id": "CHG2663_5_mass_proportional_identity",
            "object": "charge-to-mass proportionality",
            "statement": "A clean tau/profile simplification would follow if source/test X-charge densities were proportional to the mass densities used by the published Yukawa bound.",
            "derived_form": "rho_X^source/M_source = constant and rho_X^test/M_test = constant in the same frame",
            "status": "USEFUL_IDENTITY_NOT_DERIVED",
            "missing_for_claim": "parent Ward identity or sourced material-charge ledger",
        },
        {
            "derivation_id": "CHG2663_6_no_cancellation_split",
            "object": "bulk, edge and tail policy",
            "statement": "Bulk source, edge source, test response and hidden-tail terms must be bounded separately; a cancellation between them is not evidence.",
            "derived_form": "abs(alpha_total)<=abs(alpha_bulk)+abs(alpha_edge)+abs(alpha_tail)",
            "status": "ABSOLUTE_ENVELOPE_POLICY",
            "missing_for_claim": "separate theorem-zero or bound row for every component",
        },
        {
            "derivation_id": "CHG2663_7_verdict",
            "object": "source/test charge normalization",
            "statement": "2663 derives the exact normalization contract, but no R10 source/test charge coefficient is parent-filled.",
            "derived_form": "Qbar_XH, K_X, qbar_XT and tau_R10 are now wired but remain nonclaim inputs",
            "status": "SOURCE_TEST_CHARGE_NORMALIZATION_NOT_PARENT_DERIVED",
            "missing_for_claim": "first real Q_X^H/source-current row or a signed zero theorem",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def qbar_source_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "QROW2663_0_bulk_Qbar_XH",
            "factor": "Qbar_XH(lambda)",
            "formula_or_definition": "Pi_M^H[Q_X^H(lambda)]/M_H_ref",
            "required_inputs": "Q_X^H(lambda); Pi_M^H; M_H_ref; source body; units; source_path",
            "current_status": "MISSING_ARENA_PROJECTION",
            "units": "charge_per_mass_in_parent_X_normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "This is the first source-side row needed before R10 alpha(lambda) can be evaluated.",
        },
        {
            "row_id": "QROW2663_1_test_qbar_XT",
            "factor": "qbar_XT or visible-domain zero",
            "formula_or_definition": "test response to X-channel; zero only by signed matter-descent theorem",
            "required_inputs": "q-kernel; observed coframe; matter action descent; no-marker constants; finite coefficient fallback",
            "current_status": "MISSING_VISIBLE_DOMAIN_CERTIFICATE_OR_BOUND",
            "units": "charge_per_mass_or_dimensionless_alpha_response",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "Do not set qbar_XT=0 from covariance/WEP alone.",
        },
        {
            "row_id": "QROW2663_2_KX",
            "factor": "K_X(lambda)",
            "formula_or_definition": "s_X/(4*pi*Z_X*G_obs)",
            "required_inputs": "Z_X; sign s_X; G_obs frame; field normalization; dimensional ledger",
            "current_status": "MISSING_ALPHA_NORMALIZATION",
            "units": "inverse_field_stiffness_over_G_obs",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "Field rescaling guard blocks choosing K_X after the fact.",
        },
        {
            "row_id": "QROW2663_3_tau_R10",
            "factor": "tau_R10(lambda)",
            "formula_or_definition": "I_MTS_X(lambda;rho_s,rho_t,W_readout)/I_unit_Yukawa(lambda;rho_s,rho_t,W_readout)",
            "required_inputs": "source density; test density; readout kernel; geometry/separation modulation",
            "current_status": "SYMBOLIC_PROFILE_FUNCTIONAL_ONLY",
            "units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "tau=1 shortcut remains forbidden unless identity gates close.",
        },
        {
            "row_id": "QROW2663_4_tail_abs",
            "factor": "alpha_tail_abs(lambda)",
            "formula_or_definition": "absolute upper envelope for all residual non-Yukawa or hidden-tail pieces",
            "required_inputs": "theorem-zero or sourced bound per tail component",
            "current_status": "MISSING_TAIL_ZERO_OR_BOUND",
            "units": "dimensionless alpha envelope",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "No cancellation against the bulk term is permitted.",
        },
        {
            "row_id": "QROW2663_5_alpha_product",
            "factor": "alpha_R10(lambda)",
            "formula_or_definition": "K_X Qbar_XH qbar_XT tau_R10 + alpha_tail_abs",
            "required_inputs": "all previous factors plus claim-valid bound curve",
            "current_status": "BLOCKED_BY_FACTOR_INPUTS",
            "units": "dimensionless Yukawa strength",
            "score_ready": False,
            "valid_for_claim": False,
            "notes": "Schema-ready only; not a pass claim.",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "source_path": "NONCLAIM_TEMPLATE",
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def kx_normalization_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("KX2663_0_ZX", "parent-signed Z_X from the same static X branch", "MISSING_PARENT_HESSIAN_ZX"),
        ("KX2663_1_sign", "sign s_X fixed by the parent source convention", "MISSING_SIGN_CONVENTION"),
        ("KX2663_2_Gframe", "G_obs locked to the same Newton/PPN frame as the source masses", "MISSING_G_OBS_FRAME_LOCK"),
        ("KX2663_3_units", "dimensional ledger maps parent X units into alpha(lambda)", "MISSING_DIMENSIONAL_LEDGER"),
        ("KX2663_4_rescaling", "field rescaling invariant fixes Z_X f_X^2 or equivalent normalization", "INVARIANT_NORMALIZATION_NOT_PARENT_FIXED"),
        ("KX2663_5_verdict", "K_X can be used in an R10 alpha row", "K_X_NOT_CLAIM_READY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "condition": condition,
            "current_status": status,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, condition, status in rows
    ]


def zero_switch_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "gate_id": "ZERO2663_0_test_visible_domain",
            "zero_candidate": "qbar_XT=0",
            "required_theorem": "q-kernel + observed coframe functor + matter descent + no-marker constants + no hidden tails",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
        },
        {
            "gate_id": "ZERO2663_1_source_current",
            "zero_candidate": "Qbar_XH=0",
            "required_theorem": "parent source current J_X/rho_X vanishes on the R10 source domain",
            "current_status": "MISSING_SOURCE_CURRENT_ZERO",
        },
        {
            "gate_id": "ZERO2663_2_edge_projector",
            "zero_candidate": "Qbar_edge_XH=0",
            "required_theorem": "projector orthogonality and reference-mass independence from 1019 close parent-signed",
            "current_status": "CONDITIONAL_PROJECTOR_ZERO_NOT_PARENT_SIGNED",
        },
        {
            "gate_id": "ZERO2663_3_tail",
            "zero_candidate": "alpha_tail_abs=0",
            "required_theorem": "no hidden visible hom, no disformal/Weyl representative coefficient and no boundary projection silence",
            "current_status": "MISSING_TAIL_ZERO_THEOREM",
        },
        {
            "gate_id": "ZERO2663_4_verdict",
            "zero_candidate": "any R10 source/test zero switch",
            "required_theorem": "at least one complete theorem-zero certificate or sourced finite bound row",
            "current_status": "NO_ZERO_SWITCH_CLOSED",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def runner_results_rows(template_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in template_rows:
        missing = has_missing(row) or not row["score_ready"] or not row["valid_for_claim"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2663_{row['row_id'].split('_')[1]}",
                "row_id": row["row_id"],
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_MISSING_SOURCE_TEST_CHARGE_INPUTS" if missing else "READY_NONCLAIM",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2663_0_Qbar", "Qbar_XH is numeric, sourced or theorem-zero", "FAIL_QBAR_XH_MISSING", "QROW2663_0_bulk_Qbar_XH"),
        ("CG2663_1_KX", "K_X normalization is parent-signed", "FAIL_KX_NORMALIZATION_MISSING", "KX2663_5_verdict"),
        ("CG2663_2_qbarXT", "qbar_XT is sourced or visibly zero", "FAIL_QBAR_XT_MISSING", "ZERO2663_0_test_visible_domain"),
        ("CG2663_3_tau", "tau_R10 profile map is numeric or theorem-collapsed", "FAIL_TAU_SYMBOLIC_ONLY", "QROW2663_3_tau_R10"),
        ("CG2663_4_verdict", "R10/local finite-range channel can be scored or claimed", "CLAIM_BLOCKED", "source/test charge normalization contract derived, factors still missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "evidence_ref": evidence_ref,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, requirement, status, evidence_ref in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2663_0_contract",
            "decision": "the source/test charge contract is now explicit",
            "reason": "R10 alpha(lambda) has been decomposed into K_X, Qbar_XH, qbar_XT, tau_R10 and absolute tails",
            "next_action": "fill or prove zero for the first source current factor Q_X^H",
        },
        {
            "decision_id": "DEC2663_1_best_route",
            "decision": "go after Qbar_XH/source-current first",
            "reason": "K_X and qbar_XT both need parent normalization too, but Qbar_XH is the cleanest source-side row that feeds every R10 product",
            "next_action": "try a source-current zero theorem; if it fails, create first nonclaim finite Q_X^H source row",
        },
        {
            "decision_id": "DEC2663_2_no_claim",
            "decision": "no R10, PPN, clock, orbital or local-GR pass is claimed",
            "reason": "all source/test charge factors remain missing, unsigned or symbolic",
            "next_action": "keep every new row valid_for_claim=false",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2663_0_selected",
            "status": "selected",
            "next_doc": "2664-Y5-R2FR-source-current-zero-or-QbarXH-first-source-row.md",
            "next_script": "scripts/Y5_R2FR_source_current_zero_or_QbarXH_first_source_row_2664.py",
            "task": "attempt the source-current zero theorem for Q_X^H; if it fails, stage the first Qbar_XH source row with all missing parent inputs explicit",
            "must_include": "parent source current J_X/rho_X, Hamiltonian source domain, Pi_M^H, M_H_ref, units, edge split, no-cancellation policy",
            "must_exclude": "invented Qbar_XH values, tau=1 shortcut, alpha pass claim, curve-digitization victory, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2663_0_progress", "R10 source/test charges", "CONTRACT_DERIVED_NONCLAIM", "R10 alpha(lambda) is no longer vague; it is a product of named factors with gates"),
        ("STAT2663_1_gap", "coupling gap", "LOCALIZED_TO_COEFFICIENTS", "the live gap is Qbar_XH, K_X, qbar_XT, tau_R10 numeric profile and tails"),
        ("STAT2663_2_best_next", "next route", "SOURCE_CURRENT_ZERO_OR_QBAR_ROW", "Q_X^H is the next concrete source-side object to derive or demote to finite row"),
        ("STAT2663_3_project", "GR/local route", "STILL_BLOCKED_BUT_SHARPER", "no local-GR claim yet, but the finite-range leakage gate is now more executable"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for status_id, topic, status, detail in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["qbar_source_template"], BRANCH_COPIES["queue"], "R10 source/test charge input queue"),
        "local_bounds": (OUTPUTS["charge_derivation"], BRANCH_COPIES["local_bounds"], "charge normalization derivation"),
        "source_weight": (OUTPUTS["kx_normalization_gate"], BRANCH_COPIES["source_weight"], "K_X normalization gate"),
        "microscope": (OUTPUTS["qbar_source_template"], BRANCH_COPIES["microscope"], "Qbar source row template"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "charge runner refusal results"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                read_csv(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2663_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2663-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2663*",
        "*Y5_R2FR_R10_source_test_charge_normalization_or_QbarXH_source_row_2663*",
        "*JR2663*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    derivation_ok = any(
        row["derivation_id"] == "CHG2663_7_verdict"
        and row["status"] == "SOURCE_TEST_CHARGE_NORMALIZATION_NOT_PARENT_DERIVED"
        for row in rows["charge_derivation"]
    )
    qbar_ok = all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["qbar_source_template"]) and any(
        row["row_id"] == "QROW2663_0_bulk_Qbar_XH" for row in rows["qbar_source_template"]
    )
    kx_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["kx_normalization_gate"]) and any(
        row["gate_id"] == "KX2663_5_verdict" and row["current_status"] == "K_X_NOT_CLAIM_READY"
        for row in rows["kx_normalization_gate"]
    )
    zero_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["zero_switch_gate"]) and any(
        row["gate_id"] == "ZERO2663_4_verdict" and row["current_status"] == "NO_ZERO_SWITCH_CLOSED"
        for row in rows["zero_switch_gate"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["qbar_source_template"]) and all(
        row["runner_status"] == "REJECTED_MISSING_SOURCE_TEST_CHARGE_INPUTS" for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2663_4_verdict" and row["current_status"] == "CLAIM_BLOCKED"
        for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2664-Y5-R2FR-source-current-zero" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2663_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2663_01_charge_contract", derivation_ok, "source/test charge normalization contract is written and nonclaim"),
        ("VAL2663_02_qbar_template", qbar_ok, "Qbar/KX/qbar/tau/alpha templates are staged as nonclaim rows"),
        ("VAL2663_03_kx_gate", kx_ok, "K_X normalization gate blocks claim promotion"),
        ("VAL2663_04_zero_switch_gate", zero_ok, "no source/test zero switch is closed"),
        ("VAL2663_05_runner_refuses", runner_ok, "charge runner refuses all missing inputs"),
        ("VAL2663_06_claim_gates_blocked", claim_ok, "R10/local claim gates remain blocked"),
        ("VAL2663_07_next_target", next_ok, "2664 source-current zero or Qbar row target selected"),
        ("VAL2663_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2663_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2663_10_formalization_untouched", formal_ok, "no 2663 outputs are written under formalization-workbench"),
        ("VAL2663_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2663_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2663 derives the R10 source/test charge normalization contract, blocks all claim routes, and selects source-current zero or first Qbar_XH row next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2663 - R10 Source-Test Charge Normalization Or QbarXH Source Row

## Purpose

This checkpoint turns the R10 coupling gap into an exact source/test charge contract. It does not claim a pass. It says precisely what must be filled before the R10 alpha(lambda) lane can score.

## Result

- The MTS-side R10 strength is decomposed as `alpha_R10(lambda)=K_X Qbar_XH qbar_XT tau_R10 + alpha_tail_abs`.
- `Qbar_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/M_H_ref` is the first source-side object to derive or source.
- `K_X=s_X/(4*pi*Z_X*G_obs)` is conditionally exact, but blocked by missing parent normalization.
- `qbar_XT=0` and `Qbar_XH=0` remain conditional zero switches, not active theorem closures.
- The next best target is the source-current zero theorem or the first explicit `Qbar_XH` source row.

## Source Register

{markdown_table(rows["source_register"])}

## Charge Normalization Derivation

{markdown_table(rows["charge_derivation"])}

## Qbar Source Row Template

{markdown_table(rows["qbar_source_template"])}

## KX Normalization Gate

{markdown_table(rows["kx_normalization_gate"])}

## Zero Switch Gate

{markdown_table(rows["zero_switch_gate"])}

## Charge Runner Results

{markdown_table(rows["runner_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "charge_derivation": charge_derivation_rows(),
        "qbar_source_template": qbar_source_template_rows(),
        "kx_normalization_gate": kx_normalization_gate_rows(),
        "zero_switch_gate": zero_switch_gate_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["qbar_source_template"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
