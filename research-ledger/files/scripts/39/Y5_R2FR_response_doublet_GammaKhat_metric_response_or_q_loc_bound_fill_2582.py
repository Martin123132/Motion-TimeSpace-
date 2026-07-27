from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_RESPONSE_DOUBLET_GAMMAKHAT_QLOC_2582"
CHECKPOINT_ID = "2582"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2582-Y5-R2FR-response-doublet-GammaKhat-metric-response-or-q_loc-bound-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_SOURCE_REGISTER.csv",
    "doublet_gate": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_DOUBLET_GATE.csv",
    "obstruction_ledger": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_OBSTRUCTION_LEDGER.csv",
    "q_loc_bound_rows": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_QLOC_BOUND_FILL_ROWS.csv",
    "claim_gates": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2582_VALIDATION.csv",
}

COPY_TARGETS = {
    "doublet_gate": QUEUE / "JR2582_RESPONSE_DOUBLET_GK_METRIC_RESPONSE_GATE_NONCLAIM.csv",
    "obstruction_ledger": QUEUE / "JR2582_RESPONSE_DOUBLET_Y5_Y6_PPN_OBSTRUCTION_LEDGER_NONCLAIM.csv",
    "q_loc_bound_rows": LOCAL_BOUNDS / "Response_doublet_q_loc_bound_fill_rows_2582_NONCLAIM.csv",
    "next_target": QUEUE / "JR2582_Y5_SOURCE_NORMALIZATION_OR_QLOC_BOUND_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2582_00_2581_handoff",
        "source_path": ROOT / "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
        "needles": ["NEXT2581_0_selected", "GK2581_7_verdict", "VAL2581_OVERALL"],
        "role": "active handoff selecting response doublet or q_loc bound fill",
    },
    {
        "source_id": "SRC2582_01_1011_response",
        "source_path": ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
        "needles": ["RDT1011_7_verdict", "QBF1011_0_compact_shell_budget", "V1011_SUMMARY"],
        "role": "prior response-doublet proof-or-bound gate",
    },
    {
        "source_id": "SRC2582_02_doublet_contract",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "needles": ["RD516_1_even_scalar_density", "RD516_5_PPN_lock", "RD516_6_boundary_no_flux"],
        "role": "response doublet action contract",
    },
    {
        "source_id": "SRC2582_03_doublet_variation",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        "needles": ["AV517_3_double_zero", "AV517_4_Euler_equation", "AV517_5_positive_theorem"],
        "role": "doublet first variation and positive theorem candidate",
    },
    {
        "source_id": "SRC2582_04_euler_source",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
        "needles": ["Y5_source_normalization", "Y6_stress_Bianchi"],
        "role": "Euler source blockers, especially Y5/Y6",
    },
    {
        "source_id": "SRC2582_05_metric_response",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv",
        "needles": ["MR517_2_Z_metric_lock", "MR517_3_boundary_terms", "MR517_4_fixed_point_stress"],
        "role": "metric response leakage and boundary terms",
    },
    {
        "source_id": "SRC2582_06_obstruction",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv",
        "needles": ["OB517_0_Y5_even_scalar", "OB517_2_PPN_lock", "OB517_3_boundary_metric_response"],
        "role": "hard obstructions for promotion",
    },
    {
        "source_id": "SRC2582_07_gate_tests",
        "source_path": OUT / "P8_RESPONSE_DOUBLET_VARIATION_GATE_TESTS.csv",
        "needles": ["G517_1_formal_double_zero", "G517_2_current_MTS_derivation", "G517_4_local_GR_claim"],
        "role": "prior response variation gate tests",
    },
    {
        "source_id": "SRC2582_08_bound_spec",
        "source_path": OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "needles": ["QB516_0_compact_shell_budget", "QB516_1_alpha3_pressure", "QB516_4_R11_operator"],
        "role": "q_loc bound runner specification",
    },
    {
        "source_id": "SRC2582_09_bound_triggers",
        "source_path": OUT / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
        "needles": ["BT517_0_owner_match_fails", "BT517_1_Y5_unsolved", "BT517_4_PPN_lock_missing"],
        "role": "bound branch trigger ledger",
    },
    {
        "source_id": "SRC2582_10_2581_validation",
        "source_path": OUT / "P8_Y5_BRR545_2581_VALIDATION.csv",
        "needles": ["VAL2581_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def doublet_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("RDG2582_0_doublet_variables", "parent exchange doublets exist for every physical residual channel", "Z^A=(R_+^A-R_-^A)/2 and R_even^A=(R_+^A+R_-^A)/2", "PARTIAL_ONLY", "only some component maps are conditional; not every q_loc/PPN/source residual is mapped"),
        ("RDG2582_1_exchange_symmetry", "exchange is exact parent symmetry", "E:R_+^A <-> R_-^A forbids linear Z source terms", "CONDITIONAL_TEMPLATE", "no full parent source signs exact exchange symmetry"),
        ("RDG2582_2_even_Gamma", "Gamma_eff is even scalar density in Z", "Gamma_eff=Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)", "CANDIDATE_WRITTEN_NOT_MATCHED", "Gamma0/background subtraction and physical component map remain unsigned"),
        ("RDG2582_3_metric_response", "K_hat is metric response of sqrt(-g) Gamma_eff", "K_hat = K_metric[Gamma_eff] including volume, delta_g Z, derivative and boundary terms", "NOT_CHECKED_CURRENT_MTS", "metric response can reintroduce linear/boundary leakage"),
        ("RDG2582_4_positive_operator", "Z operator is positive after gauge/constraint removal", "integral_A Z^A L_AB Z^B >= 0 with gap/coercivity on compact local collars", "FORMAL_CANDIDATE_ONLY", "cannot activate without zero source and boundary work"),
        ("RDG2582_5_zero_odd_source", "odd source current vanishes", "J_Z=0 including matter, source-normalization and boundary channels", "NOT_DERIVED_HARD_BLOCK", "Y5 source normalization is exchange-even and not killed by odd symmetry"),
        ("RDG2582_6_boundary_no_flux", "odd/boundary response flux vanishes", "B_Z=0 and no metric-response boundary/collar/domain leakage", "OPEN", "bulk double-zero can still leak through boundary/source mass"),
        ("RDG2582_7_PPN_lock", "Z equals physical q_loc/PPN residual vector", "Z^A=Y_loc^A through beta/gamma/alpha_i/xi/Gdot/R11 order", "NOT_DERIVED", "the theorem may zero an auxiliary shadow, not the physical residual"),
        ("RDG2582_8_verdict", "response doublet parent-signs Gamma/Khat/q_loc route", "RDG2582_0 through RDG2582_7 all pass with source/equation paths", "RESPONSE_DOUBLET_GK_ROUTE_NOT_DERIVED_CURRENT_CORPUS", "formal F1=0 survives only as conditional theorem; q_loc residual remains active"),
    ]
    return [
        stamp(
            {
                "gate_id": gate_id,
                "required_clause": clause,
                "mathematical_form": form,
                "current_status": status,
                "failure_if_missing": failure,
                "valid_for_claim": False,
            }
        )
        for gate_id, clause, form, status, failure in rows
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS2582_0_Y5_even_scalar", "Y5 source normalization is exchange-even", "odd doublet symmetry does not automatically erase measured-GM/source normalization", "Newton/source-normalized GR remains blocked", "derive mass/source-normalization owner theorem or fill measured-GM/R11 coefficients"),
        ("OBS2582_1_Y6_even_stress", "Y6 extra stress may be exchange-even and conserved", "Ward/Bianchi plus doublet parity does not erase conserved nonzero stress", "EH-only local exterior remains blocked", "topological/invisible stress theorem or residual score"),
        ("OBS2582_2_PPN_lock", "Z=0 must equal the physical residual vector being zero", "auxiliary doublet variables must map to beta/gamma/alpha_i/xi/Gdot/R11 components", "the theorem may zero a bookkeeping shadow", "component lock ledger through PPN/source-normalization order"),
        ("OBS2582_3_metric_response_boundary", "delta_g Z, domain/projector and boundary terms can enter K_hat", "metric response can generate local force or mass flux even if Gamma_eff is even", "q_loc bulk silence may not imply source-measure closure", "boundary no-flux theorem or q_loc bound row"),
        ("OBS2582_4_operator_positive_but_sourced", "positive operator does not imply Z=0 if source/boundary work survives", "integral Z L Z = source_work + boundary_flux", "formal coercivity cannot close local GR", "prove J_Z=B_Z=0 or bound residual"),
    ]
    return [
        stamp(
            {
                "obstruction_id": obstruction_id,
                "obstruction": obstruction,
                "reason": reason,
                "effect": effect,
                "next_action": next_action,
                "valid_for_claim": False,
            }
        )
        for obstruction_id, obstruction, reason, effect, next_action in rows
    ]


def q_loc_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("QBF2582_0_compact_shell_budget", "max |P_loc d_rel J_rel| or equivalent q_loc leakage", "7.432631961576971e-06", "dimensionless_proxy", "anchor_proxy_not_claim_curve", "map this proxy into PPN/source-normalization units"),
        ("QBF2582_1_alpha3_pressure", "alpha3-equivalent q_loc channel", "MISSING_QLOC_TO_ALPHA3_COEFFICIENT", "dimensionless", "mapping_missing", "coefficient normalization from q_loc to alpha3"),
        ("QBF2582_2_Gdot_GMdot", "dln_mu_obs_dt or dln_Meff_dt", "MISSING_TIME_COMPONENT_AND_UNITS", "yr^-1", "time_projection_missing", "time component and source-normalization units"),
        ("QBF2582_3_PPN_metric_tail", "Delta_PPN from q_loc", "MISSING_WEAK_FIELD_METRIC_SOLUTION", "dimensionless_vector", "PPN_mapping_missing", "weak-field metric solution sourced by q_loc"),
        ("QBF2582_4_R11_operator", "c_GK_operator_vector", "MISSING_OPERATOR_FAMILY_UNITS", "operator_units", "R11_operator_mapping_missing", "operator family, units, normalization and bound comparison"),
        ("QBF2582_5_Y5_source_normalization", "c_domain_source_normalization_operator or measured-GM residual", "MISSING_Y5_OWNER_OR_NUMERIC_COEFFICIENT", "dimensionless_or_operator_units", "Y5_hard_fail_current", "derive Y5 owner theorem or fill measured-GM/R11 coefficients"),
        ("QBF2582_6_boundary_flux", "B_Z/B_GK compact boundary flux", "MISSING_BOUNDARY_FLUX_VALUE", "GM_flux_or_dimensionless", "boundary_projection_missing", "fixed-reference boundary map and local bound"),
    ]
    return [
        stamp(
            {
                "bound_id": bound_id,
                "quantity": quantity,
                "current_value": value,
                "units": units,
                "status": status,
                "needed_before_claim": needed,
                "score_ready": bound_id == "QBF2582_0_compact_shell_budget",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for bound_id, quantity, value, units, status, needed in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2582_0_formal_double_zero", "response doublet gives formal F1=0 at Z=0", "PASS_CONDITIONAL", "quadratic/even Gamma_eff route remains mathematically useful", True),
        ("CG2582_1_parent_doublet", "parent doublets exist for every physical residual channel", "BLOCKED_NONCLAIM", "component map is partial and not parent-signed", False),
        ("CG2582_2_metric_response", "K_hat metric-response equality is proved", "BLOCKED_NONCLAIM", "delta_g Z and boundary/domain terms remain open", False),
        ("CG2582_3_source_boundary", "J_Z=0 and B_Z=0 are proved", "BLOCKED_NONCLAIM", "Y5/Y6 and boundary terms remain unsigned", False),
        ("CG2582_4_PPN_lock", "Z=0 implies physical q_loc/PPN/R11 residual vector is zero", "BLOCKED_NONCLAIM", "physical lock is not derived", False),
        ("CG2582_5_q_loc_bound_claim", "q_loc bound rows are claim-ready", "BLOCKED_NONCLAIM", "only compact-shell proxy is staged; mappings/units missing", False),
        ("CG2582_6_local_GR", "local GR/Newton reduction can be claimed", "BLOCKED_NONCLAIM", "response route and q_loc bound branch are nonclaim", False),
        ("CG2582_7_guardrail", "response proof-or-bound guardrail is installed", "PASS_GUARDRAIL", "doublet theorem is not promoted and bound rows stay nonclaim", True),
    ]
    return [
        stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2582_0_formal_route_survives",
            "decision": "RESPONSE_DOUBLET_REMAINS_CONDITIONAL_ROUTE",
            "reason": "an even quadratic Gamma_eff can give F1=0 if Z is physical and source/boundary work vanish",
            "effect": "do not discard it",
        },
        {
            "decision_id": "DEC2582_1_current_fail",
            "decision": "CURRENT_MTS_DOES_NOT_PARENT_SIGN_RESPONSE_ROUTE",
            "reason": "J_Z, B_Z, metric response, PPN lock, Y5 source normalization and Y6 extra stress are open",
            "effect": "q_loc remains residual",
        },
        {
            "decision_id": "DEC2582_2_y5_pressure",
            "decision": "Y5_SOURCE_NORMALIZATION_IS_NEXT_PRESSURE",
            "reason": "source normalization is exchange-even and directly affects Newton/GR recovery",
            "effect": "next target should derive the Y5 source owner or implement q_loc/R11 coefficients",
        },
        {
            "decision_id": "DEC2582_3_bound_branch",
            "decision": "QLOC_BOUND_BRANCH_STAGED_NOT_READY",
            "reason": "compact-shell proxy exists, but alpha3, PPN, Gdot, R11 and Y5 coefficient maps are missing",
            "effect": "future testing can proceed once units/projections/source paths are filled",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2582_0_selected",
            "selection_status": "selected",
            "target_file": "2583-Y5-R2FR-Y5-source-normalization-owner-or-q_loc-R11-bound-implementation.md",
            "target_script": "scripts/Y5_R2FR_Y5_source_normalization_owner_or_q_loc_R11_bound_implementation_2583.py",
            "task": "derive whether measured-GM/source normalization is owned by the parent current chain and zero/topological locally; if not, implement numeric q_loc/R11/source-normalization bound rows with units, projections, and source paths",
            "acceptance_target": "Y5 source-normalization owner theorem passes, or q_loc/R11/Y5 residual rows become source-backed nonclaim test inputs",
            "guardrails": "no odd-symmetry overclaim; no plateau axiom; no fitted cancellation; no H_tau/M_H_ref/local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "doublet_gate": OUTPUTS["doublet_gate"],
        "obstruction_ledger": OUTPUTS["obstruction_ledger"],
        "q_loc_bound_rows": OUTPUTS["q_loc_bound_rows"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2582_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2582_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2582_01_doublet_verdict_nonclaim",
        any(row["gate_id"] == "RDG2582_8_verdict" and row["current_status"] == "RESPONSE_DOUBLET_GK_ROUTE_NOT_DERIVED_CURRENT_CORPUS" for row in data["doublet_gate"]),
        "response-doublet GK route remains blocked",
    )
    add(
        "VAL2582_02_y5_y6_obstructions",
        any(row["obstruction_id"] == "OBS2582_0_Y5_even_scalar" for row in data["obstructions"]) and any(row["obstruction_id"] == "OBS2582_1_Y6_even_stress" for row in data["obstructions"]),
        "Y5/Y6 obstructions are explicit",
    )
    add(
        "VAL2582_03_bound_rows_nonclaim",
        len(data["q_loc_bounds"]) >= 7 and all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["q_loc_bounds"]),
        "q_loc bound rows are staged but nonclaim",
    )
    add(
        "VAL2582_04_compact_proxy_retained",
        any(row["bound_id"] == "QBF2582_0_compact_shell_budget" and row["current_value"] == "7.432631961576971e-06" for row in data["q_loc_bounds"]),
        "compact-shell proxy retained as nonclaim anchor",
    )
    add(
        "VAL2582_05_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows response-doublet, q_loc-bound, Newton or local-GR claim",
    )
    add(
        "VAL2582_06_next_target_written",
        any(row["route_id"] == "NEXT2582_0_selected" for row in data["next"]),
        "2583 Y5 source-normalization/q_loc-R11 bound target selected",
    )
    add(
        "VAL2582_07_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2582*", "*P8_Y5_RESPONSE_DOUBLET_QLOC_2582*", "*JR2582*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2582_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2582 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2582_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2582_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2582_OVERALL",
        overall,
        "2582 keeps response-doublet GK route conditional/nonclaim, stages q_loc bound rows, and selects Y5 source-normalization owner or q_loc-R11 bound implementation next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2582 Y5 R2FR Response Doublet GammaKhat Metric Response Or q_loc Bound Fill",
        "",
        "**Status:** private nonclaim derivation checkpoint. The response-doublet route remains a serious conditional mechanism, but it does not currently parent-sign the `Gamma/Khat/q_loc` zero theorem.",
        "",
        "**Main result:** an even quadratic `Gamma_eff` can give formal `F1=0` at `Z=0`, but current MTS has not proved that `Z` is the physical q_loc/PPN/R11 residual vector, nor that `K_hat` is the full metric response, nor that `J_Z=0`, `B_Z=0`, Y5 source-normalization silence, Y6 stress invisibility, PPN lock, and boundary no-flux hold. Therefore the doublet is not promoted. The q_loc bound branch is staged, with the compact-shell proxy retained as nonclaim, but claim-ready PPN/R11/alpha3/Gdot/Y5 coefficient maps are still missing.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Response-Doublet Gate",
        markdown_table(data["doublet_gate"], ["gate_id", "required_clause", "mathematical_form", "current_status", "failure_if_missing", "valid_for_claim"]),
        "",
        "## Obstruction Ledger",
        markdown_table(data["obstructions"], ["obstruction_id", "obstruction", "reason", "effect", "next_action", "valid_for_claim"]),
        "",
        "## q_loc Bound Fill Rows",
        markdown_table(data["q_loc_bounds"], ["bound_id", "quantity", "current_value", "units", "status", "needed_before_claim", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "doublet_gate": doublet_gate_rows(),
        "obstructions": obstruction_rows(),
        "q_loc_bounds": q_loc_bound_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["doublet_gate"], data["doublet_gate"])
    write_csv(OUTPUTS["obstruction_ledger"], data["obstructions"])
    write_csv(OUTPUTS["q_loc_bound_rows"], data["q_loc_bounds"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2582_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
