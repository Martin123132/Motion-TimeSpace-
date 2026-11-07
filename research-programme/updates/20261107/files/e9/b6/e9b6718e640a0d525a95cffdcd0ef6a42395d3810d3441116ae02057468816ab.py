from source_tangent import *
import argparse


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["stencil", "target"])
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--stop-at", default="2026-10-19T21:50:00+00:00")
    args = parser.parse_args()
    config = json.loads((ROOT / "configuration.json").read_text())
    assert verify(ROOT / "results/preparation")["all_checks_passed"]
    if args.phase == "target":
        frozen = verify(ROOT / "results/frozen")
        assert frozen["all_predictions_written"] and frozen["target_source_evaluated"] is False
        offsets = {"target": config["delta_log_temperature"]}
    else:
        offsets = OFFSETS
    stop_at = datetime.fromisoformat(args.stop_at)
    anchor, unused = context(START)
    for tag, offset in offsets.items():
        folder = ROOT / "events" / tag
        folder.mkdir(parents=True, exist_ok=True)
        if (folder / "COMPLETE").exists():
            verify(folder)
            continue
        fraction = START-offset/config["expansion_span"]
        bundle, theta = context(fraction)
        paired = PairedHistory(bundle, anchor)
        moving = models(paired)
        by_order = {order: {node["index"]: node for node in physics.integration_nodes(theta, order)} for order in [6, 7, 8]}
        paths = [ROOT / "configuration.json", *bundle.inputs, *anchor.inputs]
        checks = []
        began = time.monotonic()
        for record in config["selected"][:args.limit]:
            ordinal = record["ordinal"]
            path = folder / f"event-{ordinal:03d}.npz"
            if datetime.now(timezone.utc) >= stop_at:
                write_json(folder / "progress.json", dict(state="paused_at_event", next_event=ordinal, phase=tag))
                return
            if not path.exists():
                node = by_order[record["order"]][record["node"]["index"]]
                assert node["frequency"] == record["node"]["frequency"] and node["cosine"] == record["node"]["cosine"]
                parameters, weight = physics.parameters_and_weight(theta, node)
                scalar, loop_path, reused = virtual(parameters)
                combined_high, combined_low, diagnostics = evaluate(parameters, paired, moving, scalar)
                dynamic_high, fixed_high = combined_high[..., :4], combined_high[..., 4:]
                dynamic_low, fixed_low = combined_low[..., :4], combined_low[..., 4:]
                dynamic_checks, fixed_checks = diagnostics, diagnostics
                weighted_high, weighted_low = precise_combine(
                    [(np.stack([dynamic_high, fixed_high]), np.stack([dynamic_low, fixed_low]))], [-weight])
                temporary = path.with_suffix(".tmp")
                with temporary.open("wb") as handle:
                    np.savez_compressed(handle, high=weighted_high,
                                        low=weighted_low,
                                        weight=weight, node=json.dumps(node, sort_keys=True), theta=theta,
                                        offset=offset, loop_path=str(loop_path), loop_reused=reused,
                                        diagnostics=json.dumps([dynamic_checks, fixed_checks]),
                                        finished_utc=datetime.now(timezone.utc).isoformat())
                temporary.replace(path)
            with np.load(path) as saved:
                assert float(saved["offset"]) == offset and float(saved["theta"]) == theta
                assert np.isfinite(saved["high"]).all() and np.isfinite(saved["low"]).all()
                diagnostics = json.loads(str(saved["diagnostics"]))
                for branch, values in enumerate(diagnostics):
                    for name, value in values.items():
                        check(checks, f"{ordinal}:{branch}:{name}", value, 1e-10)
                paths.extend([path, Path(str(saved["loop_path"]))])
            write_json(folder / "progress.json", dict(state="running", completed_events=ordinal+1, total_events=len(config["selected"]),
                                                       phase=tag, elapsed_seconds=time.monotonic()-began, pid=os.getpid()))
            print(json.dumps(dict(phase=tag, event=ordinal+1, seconds=time.monotonic()-began)), flush=True)
        if args.limit < len(config["selected"]):
            return
        finish(folder, checks, paths, phase=tag, theta=theta, fraction=fraction, event_count=len(config["selected"]),
               target_source_evaluated=args.phase == "target", source_curve_used=False)
    print("Completed " + args.phase, flush=True)


if __name__ == "__main__":
    main()
