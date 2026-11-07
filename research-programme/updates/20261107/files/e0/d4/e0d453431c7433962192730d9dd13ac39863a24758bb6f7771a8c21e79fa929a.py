from source_tangent import *


def main():
    modest()
    config = json.loads((ROOT / "configuration.json").read_text())
    bundle, theta = context(START)
    record = config["selected"][0]
    parameters, weight = physics.parameters_and_weight(theta, record["node"])
    started = time.monotonic()
    scalar, path, reused = virtual(parameters)
    high, low, checks = evaluate(parameters, bundle, models(bundle), scalar)
    print(json.dumps(dict(seconds=time.monotonic()-started, shape=high.shape,
                          finite=bool(np.isfinite(high).all()), diagnostics=checks,
                          virtual_reused=reused)), flush=True)


if __name__ == "__main__":
    main()
