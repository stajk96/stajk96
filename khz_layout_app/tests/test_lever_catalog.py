from core.lever_catalog import lever_default_inputs, lever_intensity, load_lever_catalog


def test_lever_catalog_parsing():
    catalog = load_lever_catalog("data/layout_lever_catalog.yaml")
    assert len(catalog) >= 40


def test_lever_parameter_validation_and_intensity_bounds():
    catalog = load_lever_catalog("data/layout_lever_catalog.yaml")
    lever = catalog[0]
    values = lever_default_inputs(lever)
    intensity = lever_intensity(lever, values)
    assert 0 <= intensity <= 1
