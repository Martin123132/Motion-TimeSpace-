from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4731"
CLAIM_ID = "L-573"
MARKER = "PPC4161_COEFFR826_TYPED_TARGET_OWNER_OR_HHIDDEN_VALUE_SOURCE_4731"
PACKET_MARKER = "PPC4161_PACKET_COEFFR826_TYPED_TARGET_OWNER_OR_HHIDDEN_VALUE_SOURCE_4731"
DECISION = "COEFFR826_PARENT_OWNER_THEOREM_EXACT_CONDITIONAL_ACTUAL_R826_CONSTRUCTOR_UNSIGNED_FIRST_HHIDDEN_VALUE_SOURCE_ROW_STAGED"
NEXT_TARGET = "4732-Y5-R2FR-R826-parent-constructor-list-from-action-density-or-CI826-VI-source-row.md"

DOC_PATH = POST / "4731-Y5-R2FR-CoeffR826-typed-target-owner-from-parent-action-or-Hhidden-value-source.md"
FORMAL_PATH = FORMAL / "747-PPC4161-CoeffR826-typed-target-owner-from-parent-action-or-Hhidden-value-source.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_SOURCE_REGISTER.csv"
OWNER_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_COEFFR826_PARENT_OWNER_THEOREM.csv"
OWNER_CERTIFICATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_COEFFR826_OWNER_CERTIFICATE_AUDIT.csv"
VALUE_SOURCE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_FIRST_HHIDDEN_VALUE_SOURCE_ROW.csv"
PROPAGATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_CI826_VI_TO_B826_PROPAGATION.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4731_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4731_VALIDATION.csv"


SOURCE_SPECS = [
    ("SRC4731_0_resume", POST / "CURRENT_LOCAL_RESUME.md", "4731-Y5-R2FR-CoeffR826-typed-target-owner-from-parent-action-or-Hhidden-value-source.md", "current local handoff into 4731"),
    ("SRC4731_1_4730_doc", POST / "4730-Y5-R2FR-HR826-hidden-scalar-target-exclusion-or-first-bound-input-pack.md", "D_v R826_hidden", "4730 derivative law and hidden scalar handoff"),
    ("SRC4731_2_4730_next", SOURCE_DIR / "P8_Y5_R2FR_4730_NEXT_TARGET.csv", "4731-Y5-R2FR-CoeffR826-typed-target-owner-from-parent-action-or-Hhidden-value-source.md", "machine handoff into 4731"),
    ("SRC4731_3_4730_zero", SOURCE_DIR / "P8_Y5_R2FR_4730_HIDDEN_SCALAR_R826_ZERO_THEOREM.csv", "HSZ4730_2_typed_no_target", "typed no-target branch for Hhidden"),
    ("SRC4731_4_4730_bound", SOURCE_DIR / "P8_Y5_R2FR_4730_FIRST_HIDDEN_SCALAR_BOUND_INPUT_PACK.csv", "HIN4730_1_value_scalar", "C_I826 V_I source row demand"),
    ("SRC4731_5_4729_inventory", SOURCE_DIR / "P8_Y5_R2FR_4729_R826_PARENT_OBJECT_INVENTORY.csv", "INV4729_3_hidden_scalar_target", "R826 object inventory hidden target"),
    ("SRC4731_6_4729_exhaustion", SOURCE_DIR / "P8_Y5_R2FR_4729_R826_EXHAUSTION_THEOREM.csv", "EXH4729_0_exact_statement", "R826 allowed/forbidden exact conditional statement"),
    ("SRC4731_7_1055_contract", SOURCE_DIR / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_6_single_parent_action", "single parent action contract candidate"),
    ("SRC4731_8_1236_certificate", SOURCE_DIR / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv", "CERT1236_1_visible_coefficient_domain", "typed visible coefficient domain certificate"),
    ("SRC4731_9_1236_meta", SOURCE_DIR / "P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv", "META1236_0_statement", "no-hidden-visible coefficient meta-theorem"),
    ("SRC4731_10_2659_operator", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv", "ODT2659_1_exact_typed_theorem", "R2FR typed operator-domain theorem"),
    ("SRC4731_11_2659_counter", SOURCE_DIR / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_COUNTERMODEL_LEDGER.csv", "CM2659_2_constant_marker_leak", "constant marker leak countermodel"),
    ("SRC4731_12_4704_object", SOURCE_DIR / "P8_Y5_R2FR_4704_PARENT_GENERATOR_OBJECT_LANGUAGE.csv", "OBJ4704_0_parent_Maxwell_norm", "parent generator object-language pattern"),
    ("SRC4731_13_1219_noarg", SOURCE_DIR / "P8_Y5_R10_1219_NO_HIDDEN_ARGUMENT_CONDITIONAL_THEOREM.csv", "NHA1219_0_type_rule", "no hidden argument conditional theorem"),
    ("SRC4731_14_1219_hsc", SOURCE_DIR / "P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv", "HSC1219_0_generic_scalar", "hidden scalar counterexample lock"),
    ("SRC4731_15_1092_triviality", SOURCE_DIR / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv", "HIT1092_5_verdict", "hidden invariant triviality not derived"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def owner_theorem_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("OWN4731_0_target", "Coeff_R826 parent target owner", "Identify the parent constructor for Coeff_R826 and prove Arg(Coeff_R826) subset Q_obs x Theta_fixed x Branch_fixed, with no C_hid argument.", "This is the exact owner theorem needed to set C_I826=0.", "TARGET_SHARP", "SRC4731_3_4730_zero"),
        ("OWN4731_1_variational_form", "parent action density route", "If S_parent contains R826 only through int mu(q,theta) Rbar826(q,theta) O826(q,Psi,theta), then vertical v in ker(Dq) cap ker(Dtheta) gives D_v Coeff_R826=0.", "Direct chain rule from the action density kills hidden scalar target dependence.", "EXACT_CONDITIONAL_THEOREM", "SRC4731_7_1055_contract"),
        ("OWN4731_2_constructor_exclusion", "no hidden constructor", "No constructor h:C_hid -> Coeff_R826, no hidden marker retyped as theta_fixed, and no readout-generated coefficient may exist before variation.", "Without this, rho_826(I_hid) is legal and Hhidden survives.", "REQUIRED_OWNER_CLAUSE", "SRC4731_8_1236_certificate"),
        ("OWN4731_3_CI826_zero_corollary", "C_I826 zero", "If OWN4731_1 and OWN4731_2 are parent-signed, C_I826=sup|partial R826_hidden/partial I_hid|=0.", "The value-scalar part C_I826 V_I drops out without fitting or cancellation.", "EXACT_CONDITIONAL_COROLLARY", "SRC4731_13_1219_noarg"),
        ("OWN4731_4_VI_zero_alternative", "V_I zero", "If hidden invariant triviality or local nohair signs D_v I_hid=0, then C_I826 V_I=0 even if a formal coefficient map could be written.", "This is an alternative zero path but current corpus does not prove it.", "EXACT_IF_TRIVIALITY_SIGNED_NOT_DERIVED", "SRC4731_15_1092_triviality"),
        ("OWN4731_5_actual_R826_constructor", "current corpus ownership", "The current corpus has typed visible coefficient templates and a parent action contract, but not an explicit R826 constructor list sourced from the parent action density.", "The exact theorem cannot be promoted until R826 itself is classified by the parent action grammar.", "ACTUAL_CONSTRUCTOR_UNSIGNED", "SRC4731_6_4729_exhaustion"),
        ("OWN4731_6_verdict", "4731 owner theorem verdict", "Coeff_R826 hidden-target exclusion is exact if the parent action constructor list signs it; present evidence is still a contract/template, not a derived R826 owner row.", "Stage first Hhidden value source row and make 4732 target the constructor list.", "ZERO_NOT_PROMOTED_VALUE_ROW_STAGED", "SRC4731_10_2659_operator"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "target": target,
            "statement": statement,
            "derivation_or_effect": effect,
            "status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for theorem_id, target, statement, effect, status, source_id in specs
    ]


def owner_certificate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("CERT8264731_0_parent_sort", "Parent sort declaration", "Coeff_R826 is a visible/reduced response coefficient sort, not a hidden observable sort.", "MISSING_R826_SORT_DECLARATION", "SRC4731_8_1236_certificate"),
        ("CERT8264731_1_allowed_arguments", "Allowed argument list", "Arg(Coeff_R826) subset {q_obs, theta_fixed, branch_fixed, common_measure_after_variation}.", "MISSING_EXPLICIT_ALLOWED_ARG_ROW", "SRC4731_6_4729_exhaustion"),
        ("CERT8264731_2_forbidden_arguments", "Forbidden hidden target list", "C_hid, I_hid, Xhat, memory scalar, gradient norm, marker/domain label and readout selector cannot target Coeff_R826.", "MISSING_PARENT_FORBIDDEN_ARG_SIGNATURE", "SRC4731_5_4729_inventory"),
        ("CERT8264731_3_action_density_owner", "Action-density owner", "R826 must be generated by a parent local density before variation, not by post-fit response notation.", "MISSING_ACTION_DENSITY_ROW", "SRC4731_7_1055_contract"),
        ("CERT8264731_4_no_extension_marker", "No hidden-to-fixed retyping", "Hidden branch/domain markers cannot be renamed fixed representation data unless discrete, fixed and parent-owned.", "MISSING_NO_EXTENSION_PROOF", "SRC4731_11_2659_counter"),
        ("CERT8264731_5_readout_stability", "Readout/radiative stability", "Effective/readout maps must preserve the same Coeff_R826 target domain.", "MISSING_RADIOUT_STABILITY", "SRC4731_9_1236_meta"),
        ("CERT8264731_6_current_verdict", "Owner certificate status", "The certificate is now explicit but not parent-signed for R826.", "CERTIFICATE_EXPLICIT_UNSIGNED", "SRC4731_12_4704_object"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": certificate_id,
            "clause": clause,
            "required_content": required,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for certificate_id, clause, required, status, source_id in specs
    ]


def value_source_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("HVAL4731_0_value_product", "C_I826_V_I", "value-scalar hidden contribution", "C_I826 * V_I", "C_I826:=sup|partial Coeff_R826/partial I_hid|; V_I:=sup_{B_loc,||v||=1}|D_v I_hid|", "R826 derivative norm", "MISSING_COEFFICIENT_AND_AMPLITUDE_VALUES", "SRC4731_4_4730_bound"),
        ("HVAL4731_1_CI826", "C_I826", "hidden coefficient Lipschitz/sensitivity constant", "sup_{local branch}|partial Coeff_R826/partial I_hid|", "zero if owner certificate signs; otherwise needs parent coefficient source or finite prior with units", "R826 per hidden-scalar unit", "MISSING_CI826_SOURCE", "SRC4731_1_4730_doc"),
        ("HVAL4731_2_VI", "V_I", "vertical hidden scalar amplitude", "sup_{B_loc,||v||=1}|D_v I_hid|", "zero if local invariant triviality/nohair signs; otherwise needs branch amplitude source", "hidden-scalar vertical unit", "MISSING_VI_SOURCE", "SRC4731_15_1092_triviality"),
        ("HVAL4731_3_domain", "local branch domain", "domain over which suprema are taken", "B_loc; weak-field/local-vacuum/source worldtube branch; fixed q_obs and theta_fixed", "must be named before numeric row can score", "domain descriptor", "MISSING_DOMAIN_SPECIFICATION", "SRC4731_2_4730_next"),
        ("HVAL4731_4_units", "unit bridge", "unit convention for I_hid and R826", "dimensionless I_hid or explicit scale; R826 derivative norm compatible with B826 formula", "prevents hidden unit rescaling from faking smallness", "unit contract", "MISSING_UNIT_NORMALIZATION", "SRC4731_4_4730_bound"),
        ("HVAL4731_5_source_path", "source-backed value row", "real source for C_I826 and V_I", "local derivation file, empirical bound, or parent-action coefficient table", "not allowed to use MISSING, unity by convention, or threshold as prediction", "path/provenance", "MISSING_SOURCE_PATH", "SRC4731_14_1219_hsc"),
        ("HVAL4731_6_acceptance", "valid_for_claim switch", "claim eligibility", "true only if certificate signs C_I826=0, or both C_I826 and V_I have source-backed units and domain", "currently false", "boolean", "FALSE_NOW", "SRC4731_4_4730_bound"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "role": role,
            "formula": formula,
            "definition": definition,
            "units": units,
            "current_status": status,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, quantity, role, formula, definition, units, status, source_id in specs
    ]


def propagation_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("CIPROP4731_0_Hhidden_value", "H_hidden_R826_value", "H_hidden_R826_value <= C_I826 V_I", "the first value-scalar part of the hidden bound is isolated", "SRC4731_4_4730_bound"),
        ("CIPROP4731_1_Hhidden_total", "H_hidden_R826", "H_hidden_R826 <= C_I826 V_I + H_gradI + H_marker + H_rad + H_boundary", "4731 closes or bounds only the value-scalar slot; other slots remain live", "SRC4731_1_4730_doc"),
        ("CIPROP4731_2_B826", "B_826", "|B_826| <= |a_F| L_cg^-2 [C_I826 V_I + H_gradI + H_marker + H_rad + H_boundary + H_rest_R826 + C_root tail]", "finite value row propagates to B826 but is not claim-grade yet", "SRC4731_4_4730_bound"),
        ("CIPROP4731_3_zero_case", "zero branch", "If Coeff_R826 owner certificate signs, C_I826=0 and the value-scalar slot is removed exactly.", "this is the cleanest derivation route into 4732", "SRC4731_3_4730_zero"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "propagation_id": propagation_id,
            "target": target,
            "formula": formula,
            "meaning": meaning,
            "source_path": source_path(source_id),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for propagation_id, target, formula, meaning, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4731_0_sources_verified", "All 4731 source paths exist and needles are found.", True, "NONE"),
        ("GATE4731_1_owner_theorem_shape", "Parent action owner theorem for Coeff_R826 is written.", True, "THEOREM_SHAPE_ONLY_NOT_CLAIM"),
        ("GATE4731_2_actual_R826_constructor_signed", "Actual R826 constructor list is extracted from parent action density.", False, "R826_CONSTRUCTOR_UNSIGNED"),
        ("GATE4731_3_no_hidden_target_signed", "Coeff_R826 no-C_hid target is parent-signed.", False, "COEFFR826_NO_HIDDEN_TARGET_UNSIGNED"),
        ("GATE4731_4_no_extension_readout_signed", "No hidden marker retyping and readout/radiative stability are signed.", False, "EXTENSION_RADIOUT_UNSIGNED"),
        ("GATE4731_5_CI826_zero_or_value", "C_I826 is theorem-zero or source-backed with units.", False, "CI826_VALUE_MISSING"),
        ("GATE4731_6_VI_zero_or_value", "V_I is theorem-zero or source-backed with units.", False, "VI_VALUE_MISSING"),
        ("GATE4731_7_B826_claim_ready", "B826 hidden value slot is claim-grade and propagated.", False, "B826_VALUE_SLOT_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "condition": condition,
            "passed": passed,
            "blocker": blocker,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, condition, passed, blocker in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4731_0_template_not_owner", "A typed certificate template is not an actual R826 parent constructor list."),
        ("FW4731_1_no_unit_rescale", "Do not make C_I826 or V_I small by redefining the hidden scalar unit."),
        ("FW4731_2_no_silent_marker", "Do not retype hidden branch/domain markers as fixed constants without a parent no-extension proof."),
        ("FW4731_3_no_readout_escape", "Tree-level target exclusion is not enough if readout/EFT can generate rho_eff(I_hid)."),
        ("FW4731_4_no_component_victory", "Closing C_I826 V_I does not close gradient, marker, readout, boundary, or other H_R826 components."),
        ("FW4731_5_local_only", "No GitHub action or public claim from this checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derivation_result": "If R826 is generated only by a q_obs/fixed-data parent action density, then D_v Coeff_R826=0 and C_I826=0 exactly",
            "nonclaim_result": "the actual R826 constructor list is not yet sourced from the parent action, so Coeff_R826 hidden target exclusion remains unsigned",
            "finite_row_result": "first C_I826 V_I value-source row is staged with domain, units and provenance requirements",
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4731_0_local_only",
            "status": "local_files_only_no_github_action",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4731_1_science_verdict",
            "status": "CoeffR826_owner_exact_conditional_value_row_staged",
            "detail": "The owner theorem is exact if the actual R826 constructor is q_obs/fixed-data only; the constructor list is the next derivation target.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "4731 proves the owner theorem shape but cannot promote it without an actual R826 constructor list from the parent action density.",
            "first_task": "Extract or derive the R826 constructor list from the parent action density and classify every allowed/forbidden target.",
            "fallback_task": "If the constructor list is not recoverable, fill C_I826 and V_I as the first Hhidden source row with units, domain and provenance.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    theorem: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    values: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4731 - CoeffR826 Typed Target Owner From Parent Action or Hhidden Value Source

Generated: `{ts}`

## Purpose

4731 attacks the coefficient-owner route left by 4730. The question is now precise: does the parent action actually type `Coeff_R826` so it cannot take a hidden scalar argument?

## What Actually Moved

- The exact theorem shape is now written: if `R826` appears in the parent action only as a `q_obs`/fixed-data local density, then `D_v Coeff_R826=0` for vertical `v`, so `C_I826=0`.
- This is a real derivation route, not a smallness assumption.
- It is not promoted because the actual `R826` constructor list is not yet extracted from the parent action density.
- The first value-source fallback row now exists: `H_hidden_R826_value <= C_I826 V_I`, with explicit requirements for coefficient, amplitude, domain, units and provenance.

## Owner Theorem Rows

{bullets(theorem, "theorem_id", "status")}

## Owner Certificate Audit

{bullets(certificate, "certificate_id", "current_status")}

## First Value Source Row

{bullets(values, "row_id", "current_status")}

## Gates

{bullets(gates, "gate_id", "blocker")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 747 - CoeffR826 Typed Target Owner From Parent Action or Hhidden Value Source

Generated: `{ts}`

## Result

If the parent action contains the `826` response only through a local density of the form

`int mu(q,theta) Rbar826(q,theta) O826(q,Psi,theta)`,

and the local vertical vector satisfies `Dq[v]=0` and `Dtheta[v]=0`, then

`D_v Coeff_R826 = 0`,

so the value-scalar hidden contribution has `C_I826=0`.

## Current Status

The theorem is exact, but the corpus has not yet supplied the actual `R826` constructor list from the parent action density. Therefore `C_I826=0` is not claimed.

## Fallback Contract

`H_hidden_R826_value <= C_I826 V_I`.

Both `C_I826` and `V_I` need either a parent zero theorem or source-backed values with units and a local branch domain.

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: the `Coeff_R826` owner theorem is exact if the actual `R826` constructor comes only from `q_obs` and fixed parent data.
- Zero gate: `C_I826=0` follows from the parent action density chain rule, but the actual `R826` constructor list is still unsigned.
- Finite row: `H_hidden_R826_value <= C_I826 V_I` is staged with coefficient, amplitude, units, domain and source-path requirements.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: moves the hidden scalar branch from general target exclusion into a concrete parent-action constructor-list requirement, with a first value-source fallback row.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`{DOC_PATH.name}`

## Decision

`{DECISION}`

## What moved forward

- The `Coeff_R826` parent-owner theorem is exact as a chain-rule result from a q_obs/fixed-data parent action density.
- The actual `R826` constructor list remains unsigned, so `C_I826=0` is not claimed.
- The first value fallback row is now concrete: `H_hidden_R826_value <= C_I826 V_I`.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4731 writes the exact Coeff_R826 parent-owner theorem and stages the first C_I826 V_I value-source row; the actual R826 constructor remains unsigned.",
        "current_evidence": "Generated source register, owner theorem rows, owner certificate audit, value source row, propagation, gates, firewalls, decision, status, next target and validation.",
        "status": "CoeffR826_owner_theorem_exact_conditional_value_row_staged_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using a generic typed certificate as if it were the actual R826 parent constructor list.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "R826 constructor list, C_I826, V_I, units and local domain remain unsourced.",
        "title": "CoeffR826 typed target owner from parent action or Hhidden value source",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    certificate: list[dict[str, Any]],
    values: list[dict[str, Any]],
    propagation: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    csv_paths = [
        SOURCE_REGISTER_CSV,
        OWNER_THEOREM_CSV,
        OWNER_CERTIFICATE_CSV,
        VALUE_SOURCE_CSV,
        PROPAGATION_CSV,
        GATES_CSV,
        FIREWALL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_TARGET_CSV,
    ]
    theorem_status = ";".join(row["status"] for row in theorem)
    certificate_status = ";".join(row["current_status"] for row in certificate)
    value_status = ";".join(row["current_status"] for row in values)
    formula_text = ";".join(row["formula"] for row in propagation)
    checks = [
        ("VAL4731_0_sources_exist", all(bool(row["exists"]) for row in sources), "all cited 4731 source paths exist"),
        ("VAL4731_1_needles_found", all(bool(row["needle_found"]) for row in sources), "all cited 4731 source needles found"),
        ("VAL4731_2_owner_theorem_written", "EXACT_CONDITIONAL_THEOREM" in theorem_status and "C_I826=0" in read_text(DOC_PATH), "Coeff_R826 owner theorem shape is written"),
        ("VAL4731_3_actual_constructor_unsigned", "ACTUAL_CONSTRUCTOR_UNSIGNED" in theorem_status and "ZERO_NOT_PROMOTED_VALUE_ROW_STAGED" in theorem_status, "actual R826 constructor remains unsigned and zero is not promoted"),
        ("VAL4731_4_certificate_audit_written", "MISSING_ACTION_DENSITY_ROW" in certificate_status and "CERTIFICATE_EXPLICIT_UNSIGNED" in certificate_status, "owner certificate audit is explicit"),
        ("VAL4731_5_value_row_created", "MISSING_CI826_SOURCE" in value_status and "MISSING_VI_SOURCE" in value_status, "first C_I826 V_I source row is created"),
        ("VAL4731_6_propagation_written", "C_I826 V_I" in formula_text and "|B_826|" in formula_text, "C_I826 V_I propagates into B826 bound"),
        ("VAL4731_7_claim_gates_closed", all(not bool(row["claim_allowed"]) for row in gates) and not any(row["passed"] for row in gates if row["gate_id"] not in {"GATE4731_0_sources_verified", "GATE4731_1_owner_theorem_shape"}), "all claim gates remain closed except structural nonclaim gates"),
        ("VAL4731_8_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4731_9_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4731_10_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-573"),
        ("VAL4731_11_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4732 next target"),
        ("VAL4731_12_csv_parse", all(parse_csv(path) for path in csv_paths), "all generated 4731 CSV files parse cleanly"),
        ("VAL4731_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    overall = all(result for _check_id, result, _detail in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4731_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "4731 CoeffR826 typed target owner or Hhidden value-source validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    cleanup_pycache()
    sources = source_register(ts)
    theorem = owner_theorem_rows(ts)
    certificate = owner_certificate_rows(ts)
    values = value_source_rows(ts)
    propagation = propagation_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(OWNER_THEOREM_CSV, theorem)
    write_csv(OWNER_CERTIFICATE_CSV, certificate)
    write_csv(VALUE_SOURCE_CSV, values)
    write_csv(PROPAGATION_CSV, propagation)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, theorem, certificate, values, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, certificate, values, propagation, gates, ts))


if __name__ == "__main__":
    main()
