from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4124-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_NO_MARKER_SOURCE_THEOREM_CURRENT_SPINE_4124"
CHECKPOINT_ID = "4124"
DECISION = "NO_MARKER_THEOREM_UNSIGNED_BETAXZ_COMPONENT_PACK_FILLED_ABSOLUTE_ENVELOPE_ACTIVE"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4124_00_4123_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4123_NEXT_TARGET.csv",
        "4124-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md",
        "4123 selected no-marker/source-blind theorem or beta component pack.",
    ),
    "SRC4124_01_4123_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4123_STATUS.csv",
        "SPECIES_BLIND_THEOREM_CONDITIONAL_BETAXZ_DIFFERENCE_ROW_FILLED_COMMON_MODE_GUARD_ACTIVE",
        "Current-chain species-blind beta-difference handoff.",
    ),
    "SRC4124_02_4123_decomp": (
        SOURCE_DIR / "P8_Y5_R2FR_4123_BETAXZ_SPECIES_DECOMPOSITION.csv",
        "BXD4123_5_marker_EM_clock",
        "Current-chain marker/EM/clock beta decomposition.",
    ),
    "SRC4124_03_4123_eta": (
        SOURCE_DIR / "P8_Y5_R2FR_4123_ETA_SOURCE_AB_BETAXZ_ROWS.csv",
        "ETA4123_1_betaZ_species_difference",
        "Current-chain betaX/betaZ eta rows.",
    ),
    "SRC4124_04_4123_guard": (
        SOURCE_DIR / "P8_Y5_R2FR_4123_COMMON_MODE_GUARD.csv",
        "CMG4123_3_EM_common_mode",
        "Current-chain common-mode/EM guard.",
    ),
    "SRC4124_05_3638_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3638_STATUS.csv",
        "NO_MARKER_THEOREM_UNSIGNED_BETA_COMPONENT_PACK_FILLED_ABSOLUTE_ENVELOPE_ACTIVE",
        "Older no-marker beta component checkpoint.",
    ),
    "SRC4124_06_3638_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3638_NO_MARKER_SOURCE_THEOREM_AUDIT.csv",
        "NMS3638_5_verdict",
        "Older no-marker theorem audit.",
    ),
    "SRC4124_07_3638_pack": (
        SOURCE_DIR / "P8_Y5_R2FR_3638_BETAX_COMPONENT_PACK.csv",
        "BETA3638_9_b_support",
        "Older beta_X component pack.",
    ),
    "SRC4124_08_3638_envelope": (
        SOURCE_DIR / "P8_Y5_R2FR_3638_BETAX_ABSOLUTE_ENVELOPE.csv",
        "ENV3638_2_eta_bound_rule",
        "Older absolute-envelope rule.",
    ),
    "SRC4124_09_3638_eta_update": (
        SOURCE_DIR / "P8_Y5_R2FR_3638_ETA_SOURCE_AB_COMPONENT_UPDATE.csv",
        "ETA3638_0_componentized_beta_source_charge",
        "Older componentized eta update.",
    ),
    "SRC4124_10_3638_next": (
        SOURCE_DIR / "P8_Y5_R2FR_3638_NEXT_TARGET.csv",
        "3639-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md",
        "Older next target selecting common beta.",
    ),
    "SRC4124_11_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4124_no_marker_source_theorem_or_beta_component_pack.py",
        "Reproducible generator for this 4124 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def no_marker_audit_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "NMS4124_0_parent_q_kernel",
            "X_N and Z_N are vertical to the parent quotient before matter/source variation",
            "v_A in ker(Dq), A in {X,Z}, with boundary/proper gauge silence",
            "4123 keeps q-kernel/no-marker ownership unsigned",
            "UNSIGNED",
            "X/Z may be physical/source-coupled fields, so beta components remain active",
        ),
        (
            "NMS4124_1_matter_functor",
            "ordinary matter/source action factors through q-owned public structures only",
            "S_matter=sum_m S_m[Psi_m,Qvis(q),theta_m(q)] with no source-only slot",
            "conditional normal form exists but matter-interface restriction is not parent-signed",
            "CONDITIONAL_NOT_PARENT_SIGNED",
            "source prefactors, action weights, or non-terminal labels can carry beta",
        ),
        (
            "NMS4124_2_marker_constants",
            "masses, material constants, EM constants, and clock/readout markers are q-owned or superselected",
            "Lie_A m_m=Lie_A alpha_EM=Lie_A theta_m=Lie_A tau_clock=0 for A in {X_N,Z_N}",
            "4123 retains marker/EM/clock failure modes",
            "MISSING_NO_MARKER_THEOREM",
            "b_mass, b_alpha, b_clock, and material sensitivity rows remain active",
        ),
        (
            "NMS4124_3_species_action_weight",
            "species action weights, hbar_m, source weights, and Jacobians are not legal parent symbols",
            "w_m=hbar_m=J_m=0 as independent species/source residuals",
            "object-language route sharpens target but is not signed",
            "TARGET_SHARPENED_NOT_SIGNED",
            "b_source_weight and b_measure_weight remain in beta component pack",
        ),
        (
            "NMS4124_4_hidden_source_tail",
            "non-Hilbert, boundary, projector, support-shift, and readout tails are zero or separately scored",
            "q_nonH=0, Delta_W_support=0, Delta_PiM=0, or all enter absolute envelope",
            "charge-current residual ledgers keep hidden tails active",
            "HIDDEN_TAILS_RETAINED",
            "b_nonH and b_support enter beta envelope and common-mode source normalization",
        ),
        (
            "NMS4124_5_verdict",
            "no-marker/source-blind theorem for current MTS corpus",
            "all clauses NMS4124_0..4 parent-signed together",
            "conditional theorem exists but parent signature is missing in multiple independent clauses",
            "NO_MARKER_THEOREM_NOT_PARENT_SIGNED_BETAXZ_COMPONENT_PACK_REQUIRED",
            "build beta component rows and absolute envelopes for X and Z",
        ),
    ]
    for audit_id, clause, form, evidence, status, if_unsigned in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "theorem_clause": clause,
                "mathematical_form": form,
                "current_evidence": evidence,
                "status": status,
                "if_unsigned": if_unsigned,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def beta_component_rows() -> List[dict]:
    components = [
        ("beta_common", "common species-blind source charge shared by ordinary source/test bodies", "beta_A^m=beta_A_common+delta beta_A^m", "R10;Gdot;radial_source_hair;source_normalization;clock_common_mode;EM_common_mode", "COMMON_MODE_ACTIVE_NOT_WEP_ERASED"),
        ("b_Geff_species", "species/source-label derivative of G_eff/kappa_eff", "Delta_mn partial_AN ln G_eff", "R1;R9;R10;R11", "OPEN_NOT_PARENT_DERIVED"),
        ("b_Meff_species", "species/material derivative of projected source mass M_eff", "Delta_mn partial_AN ln M_eff", "R1;R4;R9;R11", "OPEN_NOT_PARENT_DERIVED"),
        ("b_epsilon_mu_species", "species/material derivative of extra measured-GM contribution epsilon_mu", "Delta_mn partial_AN ln(1+epsilon_mu)", "R1;R3;R4;R7;R8;R9;R11", "FAILED_MISSING_COEFFICIENT_VECTOR"),
        ("b_mass_marker", "vertical derivative of material mass/species constants", "Delta beta_mass_mn=sum_i(s_i^m-s_i^n)b_mass_i", "WEP;clock;composition;R10", "MISSING_CONSTANT_DESCENT_OR_NUMERIC_BMASS"),
        ("b_alpha_EM", "vertical derivative of EM/fine-structure/electromagnetic binding marker", "Delta beta_EM_mn=(s_alpha^m-s_alpha^n)b_alpha", "clock;EM;WEP;composition", "MISSING_EM_CONSTANT_DESCENT_OR_NUMERIC_BOUND"),
        ("b_clock", "clock/readout marker derivative changing measured source/frequency standards", "Delta beta_clock_mn=(s_clock^m-s_clock^n)b_clock", "clock;R2;WEP;source_normalization", "MISSING_CLOCK_MARKER_DESCENT"),
        ("b_source_weight", "species/action/source prefactor derivative w_m, hbar_m, source Jacobian", "Delta beta_weight_mn=Delta_mn partial_AN ln w_m", "R1;R4;R9;R11", "NO_SPECIES_ACTION_WEIGHT_NOT_DERIVED"),
        ("b_nonH", "non-Hilbert/boundary/projector/domain source tail contribution", "Delta beta_nonH_mn from q_nonH, Delta_PiM, boundary/domain/source-tail pieces", "R1;R7;R8;R10;R11", "HIDDEN_SOURCE_TAIL_RETAINED"),
        ("b_support", "source/worldtube support shift contribution under observed-frame/source support changes", "Delta beta_support_mn from Delta_W_support and support-rule variation", "orbital;source_normalization;local_GR", "SUPPORT_SHIFT_RETAINED"),
    ]
    rows: List[dict] = []
    for axis in ("X", "Z"):
        for index, (symbol, definition, formula_slot, links, status) in enumerate(components):
            row = row_base()
            row.update(
                {
                    "component_id": f"BETA4124_{axis}_{index}_{symbol}",
                    "axis": axis,
                    "symbol": f"{symbol}_{axis}",
                    "definition": definition,
                    "formula_slot": formula_slot.replace("partial_AN", f"partial_{axis}N").replace("beta_A", f"beta_{axis}"),
                    "units": "dimensionless or source-current normalized",
                    "observable_links": links,
                    "zero_or_score_requirement": "parent theorem-zero or sourced component value with units/sensitivities/observable link",
                    "status": status,
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            rows.append(row)
    return rows


def envelope_rows() -> List[dict]:
    rows: List[dict] = []
    for axis in ("X", "Z"):
        data = [
            (
                f"ENV4124_{axis}_0_delta_beta_abs",
                f"abs_Delta_beta_{axis}_mn_envelope",
                f"|Delta beta_{axis}_mn| <= |Delta b_Geff|+|Delta b_Meff|+|Delta b_epsilon_mu|+|Delta beta_marker|+|Delta beta_weight|+|Delta beta_nonH|+|Delta beta_support|",
                "component cancellation is forbidden unless a parent identity proves it for all allowed material pairs",
                "eta_source_AB small-charge limit; R1 source WEP",
                "ABSOLUTE_ENVELOPE_READY_VALUES_MISSING",
            ),
            (
                f"ENV4124_{axis}_1_marker_abs",
                f"abs_Delta_beta_marker_{axis}_mn",
                f"|Delta beta_marker_{axis}_mn| <= sum_i |s_i^m-s_i^n||b_mass_i| + |s_alpha^m-s_alpha^n||b_alpha| + |s_clock^m-s_clock^n||b_clock|",
                "material/EM/clock components add by absolute envelope without sign tuning",
                "WEP;clock;EM;composition",
                "SENSITIVITY_ROWS_MISSING",
            ),
            (
                f"ENV4124_{axis}_2_eta_bound_rule",
                f"eta_source_mn_bound_rule_{axis}",
                f"eta_source_mn <= 2 abs_Delta_beta_{axis}_mn_envelope/|2+beta_{axis}^m+beta_{axis}^n|, approx abs_Delta_beta_{axis}_mn_envelope for small beta",
                "a one-pair material cancellation cannot certify theory zero",
                "2.8e-15 source-charge WEP target",
                "BOUND_RULE_READY_NUMERIC_VALUES_MISSING",
            ),
        ]
        for envelope_id, quantity, formula, rule, feeds, status in data:
            row = row_base()
            row.update(
                {
                    "envelope_id": envelope_id,
                    "quantity": quantity,
                    "formula": formula,
                    "no_cancellation_rule": rule,
                    "feeds": feeds,
                    "status": status,
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
            rows.append(row)
    return rows


def eta_update_rows() -> List[dict]:
    rows: List[dict] = []
    for axis in ("X", "Z"):
        row = row_base()
        row.update(
            {
                "row_id": f"ETA4124_{axis}_0_componentized_beta_source_charge",
                "axis": axis,
                "observable": "eta_source_AB;eta_WEP_source_charge",
                "componentized_prediction": f"eta_source_AB=2|Delta b_Geff+Delta b_Meff+Delta b_epsilon_mu+Delta beta_marker+Delta beta_weight+Delta beta_nonH+Delta beta_support|/|2+beta_{axis}^A+beta_{axis}^B|",
                "absolute_envelope": f"abs_Delta_beta_{axis}_AB_envelope from ENV4124_{axis}_0_delta_beta_abs",
                "small_charge_scoring": f"eta_source_AB ~= abs_Delta_beta_{axis}_AB_envelope only after component values or theorem zeros exist",
                "bound_or_target": "2.8e-15",
                "score_status": "not_scoreable_until_component_values_or_parent_zero",
                "common_mode_guard": f"beta_common_{axis} still bypasses eta_source_AB and remains active for R10/Gdot/radial/source-normalization/EM",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4124_0_no_marker_theorem",
            "The no-marker/source-blind theorem is still conditional; it is not parent-signed for current MTS.",
            "NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            "use beta component pack rather than claiming source-charge zero.",
        ),
        (
            "DEC4124_1_component_pack",
            "The beta source-charge row now has X and Z component placeholders: b_mass, b_alpha, b_clock, b_source_weight, b_nonH, b_support, and beta_common.",
            "BETAXZ_COMPONENT_PACK_FILLED",
            "derive or source components one by one with units, sensitivities, and observable links.",
        ),
        (
            "DEC4124_2_no_cancellation",
            "eta_source_AB must use an absolute-sum envelope until a parent identity proves cancellation.",
            "ABSOLUTE_ENVELOPE_REQUIRED",
            "do not use material-pair cancellation as a theory result.",
        ),
        (
            "DEC4124_3_next_focus",
            "The next highest-value fork is common-mode beta because WEP can pass while a universal source force survives.",
            "COMMON_BETA_NEXT",
            "try beta_common_X/Z=0 or map beta_common into R10/Gdot/radial/source-normalization/EM rows.",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4124_0",
            "target_doc": "4125-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md",
            "target_script": "scripts/Y5_R2FR_4125_common_beta_zero_or_source_normalization_runner.py",
            "objective": "try to derive beta_common_X=beta_common_Z=0 from parent quotient/source action; if not, map common beta into R10, Gdot, radial source hair, source-normalization, and EM common-mode residual rows without relying on WEP",
            "success_gate": "common beta is theorem-zero from parent q-data, or beta_common_X/Z gains nonclaim rows for R10/Gdot/radial/source-normalization/EM with units, observable links, and required bound inputs",
            "reason": "4124 shows differential WEP can miss common source coupling; common beta is the next highest-pressure source-coupling target.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4124_0",
            "result": DECISION,
            "summary": (
                "4124 audits the no-marker/source-blind theorem and keeps it conditional. It converts beta_X and beta_Z "
                "source-charge rows into a component pack: beta_common, b_Geff, b_Meff, b_epsilon_mu, b_mass, b_alpha, "
                "b_clock, b_source_weight, b_nonH, and b_support. It also installs an absolute-sum envelope so unknown "
                "marker/source components cannot cancel into a fake eta_source_AB pass. Common-mode beta is the next priority."
            ),
            "no_marker_theorem_signed": "False",
            "betaxz_component_pack_written": "True",
            "absolute_envelope_active": "True",
            "score_ready": "False",
            "claim_state": "no source_WEP, Newton, R10, R11, local_GR, PPN, clock, EM, or source_zero claim",
            "next_target": "4125 common beta zero or source-normalization runner",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4124_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4124_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4124_NO_MARKER_SOURCE_THEOREM_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4124_NO_MARKER_SOURCE_THEOREM_AUDIT.csv",
        "P8_Y5_R2FR_4124_BETAXZ_COMPONENT_PACK": SOURCE_DIR / "P8_Y5_R2FR_4124_BETAXZ_COMPONENT_PACK.csv",
        "P8_Y5_R2FR_4124_BETAXZ_ABSOLUTE_ENVELOPE": SOURCE_DIR / "P8_Y5_R2FR_4124_BETAXZ_ABSOLUTE_ENVELOPE.csv",
        "P8_Y5_R2FR_4124_ETA_SOURCE_AB_COMPONENT_UPDATE": SOURCE_DIR / "P8_Y5_R2FR_4124_ETA_SOURCE_AB_COMPONENT_UPDATE.csv",
        "P8_Y5_R2FR_4124_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4124_DECISION_GATES.csv",
        "P8_Y5_R2FR_4124_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4124_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4124_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4124_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4124 - No-Marker Source Theorem or Beta Component Pack",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- No-marker/source-blind theorem remains conditional, not claim-live.",
        "- `beta_X` and `beta_Z` are now componentized into common beta, coupling/mass/EM/clock/source/support pieces.",
        "- Absolute-sum envelope is active: unknown pieces cannot cancel into a fake `eta_source_AB` pass.",
        "- Next pressure point is common-mode beta, because WEP can pass while universal source coupling survives.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## No-Marker Audit", "", "| audit_id | status | if_unsigned |", "|---|---|---|"])
    for row in no_marker_audit_rows():
        sections.append(f"| {row['audit_id']} | {row['status']} | {row['if_unsigned']} |")
    sections.extend(["", "## Beta Component Pack", "", "| component_id | symbol | status |", "|---|---|---|"])
    for row in beta_component_rows():
        sections.append(f"| {row['component_id']} | {row['symbol']} | {row['status']} |")
    sections.extend(["", "## Absolute Envelope", "", "| envelope_id | quantity | status |", "|---|---|---|"])
    for row in envelope_rows():
        sections.append(f"| {row['envelope_id']} | {row['quantity']} | {row['status']} |")
    sections.extend(["", "## Next Target", "", "- `4125-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md`", "- Try to prove common beta is zero; otherwise route it into R10, Gdot, radial/source-normalization, and EM common-mode rows.", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4124_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4124_NO_MARKER_SOURCE_THEOREM_AUDIT": no_marker_audit_rows,
        "P8_Y5_R2FR_4124_BETAXZ_COMPONENT_PACK": beta_component_rows,
        "P8_Y5_R2FR_4124_BETAXZ_ABSOLUTE_ENVELOPE": envelope_rows,
        "P8_Y5_R2FR_4124_ETA_SOURCE_AB_COMPONENT_UPDATE": eta_update_rows,
        "P8_Y5_R2FR_4124_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4124_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4124_STATUS": status_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4124_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4124_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4124_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4124_NO_MARKER_SOURCE_THEOREM_AUDIT"]])
    audit_ok = all(token in audit_text for token in ["NO_MARKER_THEOREM_NOT_PARENT_SIGNED", "MISSING_NO_MARKER_THEOREM", "HIDDEN_TAILS_RETAINED"])
    add("VAL4124_3_audit", "no-marker audit blocks claim and retains marker/hidden-tail rows", audit_ok, "audit tokens checked")

    pack_text = flatten_rows([outputs["P8_Y5_R2FR_4124_BETAXZ_COMPONENT_PACK"]])
    pack_ok = all(token in pack_text for token in ["beta_common_X", "beta_common_Z", "b_alpha_EM", "b_clock", "b_support"])
    add("VAL4124_4_component_pack", "component pack includes X/Z common, EM, clock, and support components", pack_ok, "component tokens checked")

    envelope_text = flatten_rows([outputs["P8_Y5_R2FR_4124_BETAXZ_ABSOLUTE_ENVELOPE"]])
    envelope_ok = all(token in envelope_text for token in ["ENV4124_X_0", "ENV4124_Z_0", "2.8e-15", "component cancellation is forbidden"])
    add("VAL4124_5_envelope", "absolute envelope exists for X and Z and forbids cancellation", envelope_ok, "envelope tokens checked")

    eta_text = flatten_rows([outputs["P8_Y5_R2FR_4124_ETA_SOURCE_AB_COMPONENT_UPDATE"]])
    eta_ok = all(token in eta_text for token in ["ETA4124_X_0", "ETA4124_Z_0", "not_scoreable_until_component_values_or_parent_zero", "beta_common"])
    add("VAL4124_6_eta_update", "eta source update includes X/Z componentized rows and common-mode guard", eta_ok, "eta tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4124_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4125-Y5-R2FR-common-beta-zero-or-source-normalization-runner.md"
    add("VAL4124_7_next_target", "next target is 4125 common beta route", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4124_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no source_WEP" in status_rows_local[0].get("claim_state", "")
    add("VAL4124_8_status", "status records beta component pack and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4124_9_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4124*")) or any(FORMALIZATION.rglob("4124-Y5-R2FR*"))
    add("VAL4124_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4124_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4124_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
