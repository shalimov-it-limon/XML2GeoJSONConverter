def classFactory(iface):  # pylint: disable=invalid-name
    """Load Converter class from file Converter.
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Converter import XMLConverter
    return XMLConverter(iface)