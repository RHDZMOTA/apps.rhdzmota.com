from rhdzmota.apps.hello_world_version import version


def test_hello_world_version_components():
    components = version.split(".")
    assert len(components) == 3
    for component in components:
        assert component.isdigit()
