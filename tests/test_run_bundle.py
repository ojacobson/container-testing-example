def test_runs_bundle(bundles, containers):
    bundles.make_bundle_with_output("canned output bundle", stdout="example output")
    containers.run_bundle("container 1", bundle="canned output bundle")
    containers.wait_for("container 1")
    assert containers.output_of("container 1") == "example output"
    assert containers.exit_status_of("container 1") == 0

def test_no_sensitive_info(bundles, containers, environment_probe):
    bundles.make_bundle_with_program("environment probe", program=environment_probe)
    containers.run_bundle("container 2", bundle="environment probe")
    containers.wait_for("container 2")
    assert containers.exit_status_of("container 2") == 0
