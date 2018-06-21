from pyg import twod as pyg2d


def test_add_line():
    """Test that add_line returns the correct json."""
    plot = pyg2d.pyg2d()
    plot.add_line([0., 0.], [0., 1.])
    plot.save()
    assert
