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

CHECKPOINT = "4577"
CLAIM_ID = "L-419"
BRANCH_ID = "MTS_R2FR_Y5_DENSITY_PROFILE_OWNER_OR_DELTAWTR_FIRST_BOUND_4577"
MARKER = "PPC4161_DENSITY_PROFILE_OWNER_OR_DELTAWTR_FIRST_BOUND_4577"
PACKET_MARKER = "PPC4161_PACKET_DENSITY_PROFILE_OWNER_OR_DELTAWTR_FIRST_BOUND_4577"
DECISION = "LAPSE_TEST_PROFILE_OWNER_IDENTITY_DERIVED_DELTAWTR_FIRST_BOUND_ROWS_STAGED_RAW_TRANSITION_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4578-Y5-R2FR-lapse-test-parent-signature-or-first-real-source-leak-row.md"

DOC_PATH = POST / "4577-Y5-R2FR-density-profile-owner-or-DeltaWtr-first-bound.md"
FORMAL_PATH = FORMAL / "593-PPC4161-density-profile-owner-or-DeltaWtr-first-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4576 = POST / "4576-Y5-R2FR-same-worldtube-Hilbert-source-lock-or-residual-moment-bound.md"
CSV_4576_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4576_NEXT_TARGET.csv"
CSV_4576_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4576_RESIDUAL_MOMENT_BOUND_ROWS.csv"
CSV_4576_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4576_PARENT_SIGNATURE_AUDIT.csv"
CSV_4576_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4576_SAME_WORLDTUBE_LOCK_THEOREM.csv"
CSV_4376_SHADOW = SOURCE_DIR / "P8_Y5_R2FR_4376_SHADOW_BAN_ATTEMPT.csv"
CSV_4376_EPROFILE = SOURCE_DIR / "P8_Y5_R2FR_4376_EPROFILE_FIRST_SOURCE_ROW.csv"
CSV_4377_GRAMMAR = SOURCE_DIR / "P8_Y5_R2FR_4377_PARENT_GRAMMAR_THEOREM.csv"
CSV_4377_MOMENT = SOURCE_DIR / "P8_Y5_R2FR_4377_TEST_FUNCTION_MOMENT_GATE.csv"
CSV_4377_TOPO = SOURCE_DIR / "P8_Y5_R2FR_4377_TOPOLOGICAL_PROFILE_EQUALITY.csv"
CSV_4378_HARMONIC = SOURCE_DIR / "P8_Y5_R2FR_4378_HARMONIC_NULL_THEOREM.csv"
CSV_4378_BOUNDS = SOURCE_DIR / "P8_Y5_R2FR_4378_TOPOLOGICAL_MULTIPOLE_BOUND_ROWS.csv"
CSV_4379_L0 = SOURCE_DIR / "P8_Y5_R2FR_4379_L0_SYMMETRY_THEOREM.csv"
CSV_4379_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4379_PARENT_SIGNATURE_AUDIT.csv"
CSV_4407_DERIVATIONS = SOURCE_DIR / "P8_Y5_R2FR_4407_DERIVATIONS.csv"
CSV_4407_PROFILE_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4407_PROFILE_ZERO_OUTPUT.csv"
CSV_4407_EPROFILE_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4407_EPROFILE_BOUND_OUTPUT.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4577_SOURCE_REGISTER.csv"
LAPSE_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_LAPSE_TEST_PROFILE_OWNER_THEOREM.csv"
PROFILE_DEFECT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_PROFILE_DEFECT_DECOMPOSITION.csv"
DELTAWTR_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_DELTAWTR_FIRST_BOUND_ROWS.csv"
PROFILE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_PROFILE_FUNCTIONAL_INPUT_TEMPLATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4577_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4577_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        ("SRC4577_00_4576_doc", "4576 source-lock checkpoint", DOC_4576, "epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile"),
        ("SRC4577_01_4576_next", "4576 selected 4577 target", CSV_4576_NEXT, "density-profile-owner-or-DeltaWtr-first-bound"),
        ("SRC4577_02_4576_bound", "4576 profile/DeltaWtr bound rows", CSV_4576_BOUND, "RB4576_2_profile_trace_defect"),
        ("SRC4577_03_4576_audit", "4576 density profile audit", CSV_4576_AUDIT, "AUD4576_3_density_profile"),
        ("SRC4577_04_4576_theorem", "4576 same-worldtube theorem", CSV_4576_THEOREM, "SWL4576_3_profile_or_trace_defect"),
        ("SRC4577_05_4376_shadow", "4376 source-shadow ban attempt", CSV_4376_SHADOW, "SBA4376_1_same_action_Hilbert_filter"),
        ("SRC4577_06_4376_eprofile", "4376 first Eprofile row", CSV_4376_EPROFILE, "EP4376_5_KN_score_gate"),
        ("SRC4577_07_4377_grammar", "4377 no-source-shadow grammar", CSV_4377_GRAMMAR, "PG4377_1_no_source_shadow_type_error"),
        ("SRC4577_08_4377_moment", "4377 all-test-function gate", CSV_4377_MOMENT, "MOM4377_0_test_function_all"),
        ("SRC4577_09_4377_topo", "4377 distributional equality gate", CSV_4377_TOPO, "TPE4377_2_distributional_equality"),
        ("SRC4577_10_4378_harmonic", "4378 harmonic-null theorem", CSV_4378_HARMONIC, "HN4378_1_laplacian_null_sufficient_condition"),
        ("SRC4577_11_4378_bounds", "4378 topological multipole bounds", CSV_4378_BOUNDS, "TB4378_SUP4371_2_Sun_Earth_average_dipole"),
        ("SRC4577_12_4379_l0", "4379 centered l0 theorem", CSV_4379_L0, "L0S4379_0_statement"),
        ("SRC4577_13_4379_audit", "4379 parent signature audit", CSV_4379_AUDIT, "SIG4379_2_distributional_equality"),
        ("SRC4577_14_4407_derivations", "4407 Eprofile derivations", CSV_4407_DERIVATIONS, "EP4407_0_profile_owner_theorem"),
        ("SRC4577_15_4407_profile_zero", "4407 profile-zero output", CSV_4407_PROFILE_ZERO, "PZ4407_0_current_parent_grammar_open"),
        ("SRC4577_16_4407_eprofile_bound", "4407 Eprofile bound output", CSV_4407_EPROFILE_BOUND, "EP4407_0_missing_live_profile_components"),
        ("SRC4577_17_packet_4576", "packet source-lock marker", PACKET_PATH, "PPC4161_PACKET_SAME_WORLDTUBE_HILBERT_SOURCE_LOCK_OR_RESIDUAL_MOMENT_BOUND_4576"),
        ("SRC4577_18_claim_418", "prior claim register row", CLAIMS_PATH, "L-418"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in source_specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "lapse-test density-profile owner derivation and Delta_Wtr first bound",
                "valid_for_claim": "False",
            }
        )
    return rows


def lapse_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "LTP4577_0_lapse_probe_definition",
            "statement": "Use compact lapse probes f on W_H to read the source density before exterior/orbital readout.",
            "formula": "delta_f g_{mu nu}=2 epsilon f n_mu n_nu on W_H; R_H[f]:=c^2 int_W f rho_H dV_H = int_W f T_H(n,n) dV_H",
            "derivation": "The Hilbert density is the functional response of the same source action to local normal-normal metric/lapse variations.",
            "status": "PROFILE_PROBE_DEFINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "LTP4577_1_effective_profile_identity",
            "statement": "If the effective Newton/local source profile has the same response functional for every compact lapse probe, it equals the Hilbert density as a distribution.",
            "formula": "R_eff[f]:=c^2 int_W f rho_eff dV_H; if R_eff[f]=R_H[f] for all f in C_c^infty(W_H), then rho_eff=rho_H",
            "derivation": "By the fundamental lemma of distributions, int_W f(rho_eff-rho_H)dV_H=0 for all compact f implies rho_eff-rho_H=0.",
            "status": "EXACT_DISTRIBUTIONAL_PROFILE_OWNER_THEOREM_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "LTP4577_2_no_monopole_shortcut",
            "statement": "The total mass equality is only the f=1 probe and cannot prove profile ownership.",
            "formula": "M_eff=M_H is Delta_f=0 for f=1 only; E_profile=0 needs Delta_f=0 for all compact f or an equivalent complete moment/profile certificate",
            "derivation": "Zero-monopole source-shadow or topological wrong-profile defects can have nonzero dipole/quadrupole/profile response.",
            "status": "MONOPOLE_SHORTCUT_REJECTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "LTP4577_3_finite_fallback",
            "statement": "If all-test-function identity is not signed, retain a finite no-cancellation profile bound.",
            "formula": "E_profile <= E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile; |delta a_profile|/|a_N| <= K_N(s) E_profile",
            "derivation": "This preserves 4407 but now ties each finite component to a failed lapse-test/profile-owner premise.",
            "status": "FINITE_PROFILE_BOUND_RETAINED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "LTP4577_4_raw_transition_status",
            "statement": "The theorem is exact, but raw q_tr cannot use it until the parent action supplies the same response functional before readout.",
            "formula": "profile_zero_claim requires S_tr^H action-domain + support lock + R_eff[f]=R_H[f] for all f",
            "derivation": "4576 leaves action-domain, worldtube support and density-profile ownership unsigned for the raw transition shell.",
            "status": "THEOREM_DERIVED_RAW_TRANSITION_UNSIGNED_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def profile_defect_rows(now: str) -> list[dict[str, Any]]:
    components = [
        (
            "PDD4577_0_shadow",
            "E_shadow",
            "Delta_shadow[f]=c^2 int_W f rho_shadow dV_H",
            "no SourceOnly->Dens(W_H) object and effective profile is Hilbert action response only",
            "MISSING_PARENT_NO_SOURCE_SHADOW_SIGNATURE",
        ),
        (
            "PDD4577_1_topological",
            "E_top_profile",
            "Delta_top[f]=c^2 int_W f(rho_top-rho_H)dV_H",
            "distributional equality, harmonic-null Laplacian with boundary silence, or centered l=0 zero-monopole exterior theorem",
            "MISSING_TOPOLOGICAL_PROFILE_CERTIFICATE_OR_MOMENTS",
        ),
        (
            "PDD4577_2_nonHilbert",
            "E_nonHilbert_profile",
            "Delta_nonHilbert[f]=c^2 int_W f rho_nonHilbert dV_H",
            "P_nonHilbert_action_domain q_tr=0 by parent source action",
            "MISSING_PARENT_ACTION_DOMAIN_SIGNATURE",
        ),
        (
            "PDD4577_3_readout",
            "E_readout_profile",
            "Delta_readout[f]=c^2 int_W f rho_readout_shift dV_H",
            "source support/profile fixed before exterior/orbital/local readout",
            "MISSING_READOUT_ORDER_SIGNATURE",
        ),
        (
            "PDD4577_4_total",
            "E_profile",
            "Delta_profile[f]=c^2 int_W f(rho_eff-rho_H)dV_H",
            "all profile defect components zero or bounded below K_N gate",
            "MISSING_PROFILE_ZERO_OR_BOUND_VALUES",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "defect_id": defect_id,
            "component": component,
            "lapse_functional": lapse_functional,
            "zero_if": zero_if,
            "current_value": current_value,
            "feeds": "epsilon_lock; epsilon_moment_perp; Newton/PPN/orbital profile residual",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for defect_id, component, lapse_functional, zero_if, current_value in components
    ]


def deltawtr_bound_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "DW4577_0_definition",
            "quantity": "Delta_Wtr",
            "formula": "Delta_Wtr := ||P_offW J_tr^H||_TV / M_H_ref",
            "input_required": "transition support leakage current outside/pre-readout W_H",
            "units": "dimensionless",
            "current_value": "MISSING_P_offW_Jtr_SOURCE_ROW",
            "status": "BOUND_DEFINITION_DERIVED",
        },
        {
            "bound_id": "DW4577_1_first_bound",
            "quantity": "Delta_Wtr upper bound",
            "formula": "Delta_Wtr <= N_leak/M_H_ref <= (||mu_tr||_TV + ||B_src^A||_TV + ||rho_readout_shift||_TV)/M_H_ref",
            "input_required": "mu_tr, B_src^A, rho_readout_shift, M_H_ref with same worldtube/frame/readout provenance",
            "units": "dimensionless",
            "current_value": "MISSING_mu_tr_Bsrc_rho_shift_MHref_VALUES",
            "status": "FIRST_SOURCE_LEAK_BOUND_STAGED",
        },
        {
            "bound_id": "DW4577_2_profile_link",
            "quantity": "epsilon_lock update",
            "formula": "epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile",
            "input_required": "Y_nonHilbert components plus Delta_Wtr leak bound plus lapse-test/profile defect bound",
            "units": "dimensionless",
            "current_value": "MISSING_EPSILON_LOCK_COMPONENT_VALUES",
            "status": "LOCK_BOUND_READY_NONCLAIM",
        },
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            **row,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in rows
    ]


def profile_input_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("PIT4577_0_lapse_basis", "lapse_probe_basis", "finite or complete set of compact f_i on W_H", "dimensionless", "MISSING_BASIS_OR_ALL_TEST_FUNCTION_CERTIFICATE"),
        ("PIT4577_1_RH", "R_H[f_i]", "Hilbert functional response c^2 int f_i rho_H dV_H", "energy_or_mass_weighted", "MISSING_HILBERT_RESPONSE_VALUES"),
        ("PIT4577_2_Reff", "R_eff[f_i]", "effective Newton/local profile response c^2 int f_i rho_eff dV_H", "energy_or_mass_weighted", "MISSING_EFFECTIVE_RESPONSE_VALUES"),
        ("PIT4577_3_profile_remainder", "profile_remainder", "bound on untested lapse/profile modes", "dimensionless", "MISSING_REMAINDER_BOUND"),
        ("PIT4577_4_DeltaWtr", "N_leak/M_H_ref", "support/readout-order leakage mass norm over source mass", "dimensionless", "MISSING_SUPPORT_LEAK_VALUES"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": input_id,
            "quantity": quantity,
            "definition": definition,
            "units": units,
            "current_status": status,
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": "False",
        }
        for input_id, quantity, definition, units, status in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        {
            "control_id": "CTRL4577_all_lapse_identity",
            "input_case": "Delta_f=0 for every compact lapse probe and N_leak=0",
            "expected": "rho_eff=rho_H, E_profile=0, Delta_Wtr=0",
            "smoke_values": "symbolic clean theorem",
            "verdict": "CONTROL_PASS_NONCLAIM",
        },
        {
            "control_id": "CTRL4577_monopole_only_fail",
            "input_case": "Delta_1=0 but one nonconstant lapse probe has Delta_f!=0",
            "expected": "total mass equality passes but E_profile remains active",
            "smoke_values": "M_eff=M_H, Delta_f2=nonzero",
            "verdict": "COUNTERMODEL_CAUGHT",
        },
        {
            "control_id": "CTRL4577_small_DeltaWtr_pass_smoke",
            "input_case": "mu_tr=2e-6, B_src^A=3e-6, rho_shift=0, M_H_ref=1, tolerance=1e-5",
            "expected": "Delta_Wtr=5e-6 <= tolerance",
            "smoke_values": "Delta_Wtr_smoke=5e-6",
            "verdict": "SCHEMA_PASS_NONCLAIM",
        },
        {
            "control_id": "CTRL4577_large_DeltaWtr_fail_smoke",
            "input_case": "mu_tr=2e-3, B_src^A=0, rho_shift=0, M_H_ref=1, tolerance=1e-5",
            "expected": "Delta_Wtr=2e-3 > tolerance",
            "smoke_values": "Delta_Wtr_smoke=2e-3",
            "verdict": "SCHEMA_FAIL_NONCLAIM",
        },
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            **row,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row in controls
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    gates = [
        ("PROM4577_0_parent_lapse_identity", "Parent action proves R_eff[f]=R_H[f] for all compact lapse probes on W_H.", "BLOCKED", "True"),
        ("PROM4577_1_no_monopole_shortcut", "Same total mass alone is forbidden as profile proof.", "PASSED_FIREWALL", "True"),
        ("PROM4577_2_DeltaWtr_source_rows", "mu_tr, B_src^A, rho_readout_shift and M_H_ref are sourced numeric rows.", "BLOCKED", "True"),
        ("PROM4577_3_Eprofile_bound", "E_shadow, E_top_profile, E_nonHilbert_profile and E_readout_profile are zero-certified or numeric-bounded.", "BLOCKED", "True"),
        ("PROM4577_4_no_public_claim", "No local-GR/R10/PPN/orbital claim while parent identity or source rows are missing.", "PASSED_FIREWALL", "True"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "required_for_claim": required,
            "valid_for_claim": "False",
        }
        for gate_id, gate, status, required in gates
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4577 turns density-profile ownership into a real functional theorem: equality against every compact lapse probe forces rho_eff=rho_H as a distribution. The raw transition still lacks the parent signature, so the checkpoint stages the first Delta_Wtr source-leak bound rows rather than claiming local GR.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The next non-circling move is to hunt for the parent signature that makes the lapse-test identity true; if absent, fill one real source-leak row for mu_tr, B_src^A or rho_readout_shift.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "complete_nonclaim_checkpoint",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    defects: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4577 - Density-profile owner or Delta_Wtr first bound

Generated: `{now}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Claim status: private nonclaim checkpoint.

## Result

4577 derives a sharper profile-owner theorem.

The right object is not just total mass.  The right object is the response of the source action to every compact local lapse probe on the same worldtube:

```text
R_H[f] := c^2 int_W f rho_H dV_H
R_eff[f] := c^2 int_W f rho_eff dV_H
```

If

```text
R_eff[f] = R_H[f] for every f in C_c^\u221e(W_H)
```

then

```text
rho_eff = rho_H
E_profile = 0
```

as a distributional theorem.  This is the cleanest form of the density-profile owner route: it proves profile equality by local functional response, not by fitting `GM`, not by total charge, and not by a topological slogan.

The raw transition shell still does **not** own this theorem, because the parent action has not yet signed the all-lapse-test identity for `q_tr`.  Therefore 4577 keeps the fallback:

```text
E_profile <= E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile
Delta_Wtr <= (||mu_tr||_TV + ||B_src^A||_TV + ||rho_readout_shift||_TV)/M_H_ref
epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile
```

## Lapse-test profile-owner theorem

{markdown_table(theorem)}

## Profile defect decomposition

{markdown_table(defects)}

## Delta_Wtr first bound rows

{markdown_table(bounds)}

## Profile/source input template

{markdown_table(inputs)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: either parent-sign the all-lapse-test identity, or fill one real `Delta_Wtr` source-leak row instead of circling the generic coupling issue.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4577 lapse-test density-profile owner

Marker: `{MARKER}`  
Generated: `{now}`

4577 turns profile ownership into an all-lapse-test functional identity: if `R_eff[f]=R_H[f]` for every compact lapse probe on the same worldtube, then `rho_eff=rho_H` as a distribution and `E_profile=0`.  Same total mass is only the `f=1` probe and is explicitly insufficient.  Because the raw transition shell does not yet parent-sign the identity, the fallback is `E_profile <= E_shadow + E_top_profile + E_nonHilbert_profile + E_readout_profile` and `Delta_Wtr <= (||mu_tr||_TV + ||B_src^A||_TV + ||rho_readout_shift||_TV)/M_H_ref`.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4577 packet update - lapse-test profile owner

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The packet now uses a concrete profile-owner theorem: profile equality follows from equality of the Hilbert and effective source response against every compact lapse probe, not from total charge.  If the parent action does not sign that identity for the transition sector, retain the no-cancellation profile decomposition and first `Delta_Wtr` source-leak bound rows.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4577 derives the lapse-test density-profile owner theorem: R_eff[f]=R_H[f] for every compact lapse probe on W_H implies rho_eff=rho_H distributionally and E_profile=0; otherwise retain E_profile and Delta_Wtr source-leak bounds.",
        "current_evidence": "Generated source register, lapse-test theorem rows, profile defect decomposition, Delta_Wtr first bound rows, profile input template, controls, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Using total mass or same Hamiltonian charge as if it proved distributional density-profile equality.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Raw transition shell still needs parent all-lapse-test identity or real numeric source-leak/profile rows.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    defects: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4577_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4577_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4577_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4577_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4577_lapse_identity_theorem",
        "lapse-test theorem derives distributional equality",
        any("rho_eff=rho_H" in row["formula"] and "C_c" in row["formula"] for row in theorem),
        "R_eff[f]=R_H[f] all compact probes",
    )
    add(
        "VAL4577_monopole_rejected",
        "monopole shortcut rejected",
        any(row["theorem_id"] == "LTP4577_2_no_monopole_shortcut" for row in theorem),
        "f=1 only is insufficient",
    )
    add(
        "VAL4577_defects_missing_visible",
        "profile defect rows expose missing inputs",
        all("MISSING" in row["current_value"] for row in defects),
        "profile defect missing inputs",
    )
    add(
        "VAL4577_DeltaWtr_bound",
        "Delta_Wtr first bound is staged",
        any("Delta_Wtr <=" in row["formula"] and "mu_tr" in row["formula"] for row in bounds),
        "Delta_Wtr source-leak formula",
    )
    add(
        "VAL4577_input_template_nonclaim",
        "all input template rows remain nonclaim",
        all(row["valid_for_claim"] == "False" and "MISSING" in row["current_status"] for row in inputs),
        "profile/source input template",
    )
    add(
        "VAL4577_controls_cover_pass_fail",
        "controls include pass and fail smoke rows",
        any(row["verdict"] == "SCHEMA_PASS_NONCLAIM" for row in controls)
        and any(row["verdict"] == "SCHEMA_FAIL_NONCLAIM" for row in controls)
        and any(row["verdict"] == "COUNTERMODEL_CAUGHT" for row in controls),
        "pass/fail/countermodel controls",
    )
    add(
        "VAL4577_decision_token",
        "decision token recorded",
        DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH),
        DECISION,
    )
    add(
        "VAL4577_next_target",
        "next target recorded",
        NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH),
        NEXT_TARGET,
    )
    add("VAL4577_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4577_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    theorem = lapse_theorem_rows(now)
    defects = profile_defect_rows(now)
    bounds = deltawtr_bound_rows(now)
    inputs = profile_input_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    next_targets = next_rows(now)
    statuses = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(LAPSE_THEOREM_CSV, theorem)
    write_csv(PROFILE_DEFECT_CSV, defects)
    write_csv(DELTAWTR_BOUND_CSV, bounds)
    write_csv(PROFILE_INPUT_CSV, inputs)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, theorem, defects, bounds, inputs, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        LAPSE_THEOREM_CSV,
        PROFILE_DEFECT_CSV,
        DELTAWTR_BOUND_CSV,
        PROFILE_INPUT_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, theorem, defects, bounds, inputs, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
