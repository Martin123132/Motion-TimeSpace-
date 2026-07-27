from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "823-Y5-R10-C2A-boundary-current-representative-or-domain-demotion.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_823_SOURCE_REGISTER.csv"
TRANSPORT_IDENTITY_PATH = RESIDUALS / "P8_Y5_R10_823_TRANSPORT_IDENTITY.csv"
REPRESENTATIVE_TESTS_PATH = RESIDUALS / "P8_Y5_R10_823_REPRESENTATIVE_TESTS.csv"
BOUNDARY_STRESS_PATH = RESIDUALS / "P8_Y5_R10_823_BOUNDARY_STRESS_LEDGER.csv"
DEMOTION_GATE_PATH = RESIDUALS / "P8_Y5_R10_823_DEMOTION_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_823_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_823_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_823_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_823_VALIDATION.csv"

STATUS = "Y5_R10_823_Jrel_kinematic_representative_exists_Noether_stress_owner_missing_nonclaim"
CLAIM_CEILING = "kinematic_boundary_current_representative_only_no_parent_derivation_no_local_GR"
NEXT_TARGET = "824-Y5-R10-C2A-Noether-boundary-stress-owner-or-closure-demotion.md"

SOURCE_SPECS = [
    {
        "source_id": "822_doc",
        "path": POST_CHECKPOINT / "822-Y5-R10-C2A-coherent-load-tensor-parent-map-attempt.md",
        "needles": [
            "B822_1_boundary_current",
            "boundary-current/domain representative",
            "823-Y5-R10-C2A-boundary-current-representative-or-domain-demotion.md",
        ],
        "role": "immediate boundary-current handoff",
    },
    {
        "source_id": "822_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_822_VALIDATION.csv",
        "needles": [
            "V822_4_domain_boundary_failures_recorded,pass",
            "V822_7_next_target_selected,pass,823-Y5-R10-C2A-boundary-current-representative-or-domain-demotion.md",
            "V822_9_no_data_run_selected,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "138_pressure_kernel",
        "path": POST_CHECKPOINT / "138-coherent-volume-pressure-kernel-theorem.md",
        "needles": [
            "V_D = integral_D sqrt(h) d^3x.",
            "N_D = (1/3) ln(V_D0 / V_D).",
            "delta N_D = -(1/6)<h^ij delta h_ij>_D.",
            "boundary terms owned by `J_rel` | open",
        ],
        "role": "volume variable and boundary-term source",
    },
    {
        "source_id": "143_domain_selector",
        "path": POST_CHECKPOINT / "143-domain-selector-variational-action-attempt.md",
        "needles": [
            "boundary not hand tuned = fail open.",
            "the boundary current / representative is not owned.",
            "derive the J_rel representative / boundary exchange current.",
            "local stationary class is trivial,",
            "FLRW class is nontrivial,",
        ],
        "role": "boundary-current obstruction and desired local/FLRW behaviour",
    },
    {
        "source_id": "85_XB_firewall",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "transition shells remain local PPN obligations,",
            "not galaxy/cosmology sources.",
            "FLRW memory remains allowed only with:",
        ],
        "role": "firewall discipline for transition shells",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check_needles(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_path"
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def transport_identity_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "identity_id": "T823_0_volume_transport",
            "statement": "For a moving spatial domain D_tau, dV_D/dtau = integral_D theta dV + integral_boundary(D) v_rel dSigma.",
            "status": "kinematic_identity",
            "meaning": "bulk expansion plus relative boundary flux controls coherent-domain volume.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "identity_id": "T823_1_boundary_current_representative",
            "statement": "Define Phi_rel = integral_boundary(D) v_rel dSigma = integral_D div_D J_rel dV as a representative boundary flux.",
            "status": "representative_exists_kinematically",
            "meaning": "a current can represent boundary transport once D and boundary motion are supplied, but it is nonunique.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "identity_id": "T823_2_ND_evolution",
            "statement": "For N_D=(1/3)ln(V_D0/V_D), dN_D/dtau = -(1/3)(<theta>_D + Phi_rel/V_D).",
            "status": "derived_from_transport",
            "meaning": "local/FLRW behaviour can be tested by theta and boundary flux.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "identity_id": "T823_3_Noether_gap",
            "statement": "Kinematic J_rel does not imply a variational Noether current, conserved stress tensor, or bounded boundary energy.",
            "status": "parent_derivation_missing",
            "meaning": "this is the exact gap between bookkeeping and field theory.",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def representative_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "R823_0_local_stationary",
            "branch": "local stationary / frozen domain",
            "inputs": "<theta>_D=0 and Phi_rel=0",
            "result": "passes_kinematically",
            "consequence": "dN_D/dtau=0; local source remains silent only if the assumptions are parent-enforced.",
            "blocker": "does not prove every bound local system has theta=0 and Phi_rel=0 after perturbations/boundaries",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "R823_1_FLRW_comoving",
            "branch": "homogeneous FLRW comoving domain",
            "inputs": "<theta>_D=3H and Phi_rel=0",
            "result": "passes_kinematically",
            "consequence": "dN_D/dtau=-H, so N_D=-ln(a)+constant = ln(1+z) with present normalization.",
            "blocker": "does not derive why the cosmology domain is selected by parent action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "R823_2_transition_shell",
            "branch": "local-to-cosmology boundary / transition shell",
            "inputs": "Phi_rel nonzero or theta gradients nonzero",
            "result": "fails_for_promotion",
            "consequence": "boundary current can carry flux, but may also carry stress/hair unless a Noether owner bounds it.",
            "blocker": "PPN/R10 safety cannot be inferred from a representative current alone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "R823_3_dynamic_systems",
            "branch": "collapse / merger / virializing domain",
            "inputs": "time-dependent D, nonzero shear, nonzero boundary motion",
            "result": "open_risk",
            "consequence": "dynamic local activation may occur if boundary terms are not suppressed.",
            "blocker": "no parent theorem suppresses transition-shell source leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def boundary_stress_rows(generated_utc: str) -> list[dict[str, object]]:
    entries = [
        ("S823_0_nonunique_current", "J_rel is defined by its flux only; bulk representative is gauge/nonunique", "needs an action or equivalence class"),
        ("S823_1_Noether_missing", "no Noether identity ties J_rel to conservation of total stress", "needed for parent field theory"),
        ("S823_2_wall_stress_unbounded", "boundary flux may imply wall/surface stress in transition shells", "needed for local PPN/R10 safety"),
        ("S823_3_D_not_selected", "the physical domain D is still supplied, not selected", "needed to prevent hidden smoothing choices"),
        ("S823_4_XB_not_integrated", "J_rel/D behaviour is not yet routed through universal X_B gates", "needed to prevent sector retuning"),
        ("S823_5_perturbations_missing", "delta N_D and boundary perturbations lack a gauge-safe perturbation action", "needed for growth/CMB/lensing"),
    ]
    return [
        {
            "stress_id": stress_id,
            "issue": issue,
            "needed_fix": needed_fix,
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for stress_id, issue, needed_fix in entries
    ]


def demotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G823_0_kinematic_representative",
            "gate": "Can a J_rel representative be written?",
            "result": "pass_kinematic_only",
            "consequence": "domain transport is not nonsense; local/FLRW split has a clean bookkeeping identity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G823_1_dynamic_stress_owner",
            "gate": "Is J_rel derived from action/Noether conservation with bounded boundary stress?",
            "result": "fail",
            "consequence": "no parent-derived or local-GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G823_2_domain_demotion",
            "gate": "Must the entire domain route be demoted now?",
            "result": "partial_demote_to_kinematic_closure",
            "consequence": "retain as conditional closure skeleton; require Noether boundary owner next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G823_3_data_firewall",
            "gate": "Can data tests start from this?",
            "result": "fail",
            "consequence": "no SN/BAO/CMB/growth or local tests from this branch yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D823_0",
            "decision": "J_rel representative exists kinematically but not dynamically",
            "reason": "Reynolds/domain transport gives the local-trivial and FLRW-nontrivial bookkeeping split, but not a Noether/stress-safe parent current",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D823_1",
            "decision": "demote the domain route to kinematic closure until Noether boundary owner exists",
            "reason": "the transition shell remains the dangerous object for PPN/R10/local-GR safety",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to derive a Noether/boundary-stress owner for J_rel, or demote C2A domain mechanics to explicit closure-only",
            "allowed_work": "symbolic action variation, Bianchi/conservation audit, local boundary-stress bound contract",
            "forbidden_work": "SN/BAO/CMB/growth fitting, parent-derived claim, local-GR claim",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_survived": "domain transport gives a kinematic J_rel flux representative and local/FLRW split",
            "what_failed": "Noether/stress owner, unique current, domain selection, wall-stress bound, local-GR promotion",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    identity_rows: list[dict[str, object]],
    test_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V823_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_822, clean_822_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_822_VALIDATION.csv")
    add("V823_1_prior_822_clean", clean_822, clean_822_detail)
    add(
        "V823_2_transport_identity_present",
        {"T823_0_volume_transport", "T823_1_boundary_current_representative", "T823_2_ND_evolution"}.issubset({row["identity_id"] for row in identity_rows}),
        "volume, boundary-current, and N_D identities present",
    )
    add(
        "V823_3_local_FLRW_tests_present",
        {"R823_0_local_stationary", "R823_1_FLRW_comoving", "R823_2_transition_shell"}.issubset({row["test_id"] for row in test_rows}),
        "local, FLRW, and transition tests present",
    )
    add(
        "V823_4_Noether_stress_failure_recorded",
        {"S823_1_Noether_missing", "S823_2_wall_stress_unbounded"}.issubset({row["stress_id"] for row in stress_rows}),
        "Noether and wall-stress failures recorded",
    )
    add(
        "V823_5_domain_route_demoted_to_kinematic_closure",
        any(row["gate_id"] == "G823_2_domain_demotion" and row["result"] == "partial_demote_to_kinematic_closure" for row in demotion_rows),
        "domain route retained only as kinematic closure",
    )
    add(
        "V823_6_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "boundary-current branch remains non-runnable",
    )
    add(
        "V823_7_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + identity_rows + test_rows + stress_rows + demotion_rows + decisions + next_rows + summary
    add(
        "V823_8_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V823_9_no_data_or_local_GR_claim",
        all("fitting" in row["forbidden_work"] and "local-GR claim" in row["forbidden_work"] for row in next_rows),
        "no data or local-GR claim selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V823_10_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V823_11_validation_rows_ready", True, "validation table constructed")
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    identity_rows: list[dict[str, object]],
    test_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 823 - Y5 R10 C2A Boundary-Current Representative Or Domain Demotion",
            (
                "Current result: **a kinematic `J_rel` representative exists, but it is not a Noether/stress-safe parent current**. "
                "That is a useful half-win: the local-stationary/FLRW split can be written cleanly, but the route stays closure-only until boundary stress is owned."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim"]),
            "## Transport Identity\n\n" + markdown_table(identity_rows, ["identity_id", "statement", "status", "meaning", "valid_for_claim"]),
            "## Representative Tests\n\n" + markdown_table(test_rows, ["test_id", "branch", "inputs", "result", "consequence", "blocker", "valid_for_claim"]),
            "## Boundary Stress Ledger\n\n" + markdown_table(stress_rows, ["stress_id", "issue", "needed_fix", "status", "valid_for_claim"]),
            "## Demotion Gate\n\n" + markdown_table(demotion_rows, ["gate_id", "gate", "result", "consequence", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This improves the map without overclaiming it. The domain route is not dead, but it is demoted to kinematic closure until the Noether/boundary-stress owner is derived or explicitly rejected.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    identity_rows = transport_identity_rows(generated_utc)
    test_rows = representative_test_rows(generated_utc)
    stress_rows = boundary_stress_rows(generated_utc)
    demotion_rows = demotion_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, identity_rows, test_rows, stress_rows, demotion_rows, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(TRANSPORT_IDENTITY_PATH, identity_rows, ["identity_id", "statement", "status", "meaning", "valid_for_claim", "generated_utc"])
    write_csv(REPRESENTATIVE_TESTS_PATH, test_rows, ["test_id", "branch", "inputs", "result", "consequence", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(BOUNDARY_STRESS_PATH, stress_rows, ["stress_id", "issue", "needed_fix", "status", "valid_for_claim", "generated_utc"])
    write_csv(DEMOTION_GATE_PATH, demotion_rows, ["gate_id", "gate", "result", "consequence", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, identity_rows, test_rows, stress_rows, demotion_rows, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"823 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
