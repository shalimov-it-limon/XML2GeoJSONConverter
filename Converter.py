from qgis.PyQt.QtCore import QSettings, QTranslator
from qgis.core import QgsProject
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (
    QGridLayout,
    QWidget,
    QTableWidgetItem,
    QFileDialog,
    QMessageBox,
    QAction)
from qgis.PyQt.QtCore import Qt

import os
import xml.etree.ElementTree as ET
import xmltodict
import geojson
from ConverterDockwidget import ConverterDockWidget


# from .resources import *


# class XMLConverter(QtWidgets.QMainWindow, Converter_dialog_base.Ui_MainWindow):
class XMLConverter:
    def __init__(self, iface):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        """Constructor.
           :param iface: An interface instance that will be passed to this class
               which provides the hook by which you can manipulate the QGIS
               application at run time.
           :type iface: QgsInterface
           """
        self.iface = iface
        self.actions = []
        self.menu = self.tr(u'&Converter')
        self.toolbar = self.iface.addToolBar(u'Converter')
        self.toolbar.setObjectName(u'Converter')

        self.xml_file = 'rf_map.xml'

        self.project = QgsProject.instance()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Selector_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.work_dir = os.path.dirname(os.path.realpath(__file__))
        self.pluginIsActive = False
        self.dockwidget = None

    @staticmethod
    def tr(message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Converter', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.
        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str
        :param text: Text that should be shown in menu items for this action.
        :type text: str
        :param callback: Function to be called when the action is triggered.
        :type callback: function
        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool
        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool
        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool
        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str
        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget
        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.
        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/XML2GeoJSONConverter/XML2JSON.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        print("** CLOSING Converter")

        self.dockwidget.clean()

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crash
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        print("** UNLOAD Converter")

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Converter'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            print("** STARTING Converter")

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget is None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = ConverterDockWidget()

            # show the widget
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.dockwidget)

            # self.project = QgsProject.instance()
            # self.layers = self.project.mapLayers()
            # self.layer_names = [layer.name() for layer in self.layers.values()]
            # self.selected_layer = None

            # self.dockwidget.comboBox.addItems([''] + self.layer_names)
            # self.dockwidget.pushButton.clicked.connect(self.do_query)
            #
            # self.dockwidget.btnLoadProject.clicked.connect(self.load_project)
            # self.dockwidget.btnCheckPlacement.clicked.connect(self.check_lot)
            # self.dockwidget.btnPlaceLot.clicked.connect(self.draw_rectangle)
            # self.dockwidget.btnExport.clicked.connect(self.export_map)
            self.dockwidget.setupUi(self)  # Это нужно для инициализации нашего дизайна
            self.dockwidget.btnLoadXML.clicked.connect(self.get_folder)
            self.dockwidget.btnConvert.clicked.connect(self.convert_xml)

            self.dockwidget.show()
            # app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
            # window = XMLConverter(self.iface)  # Создаём объект класса XMLConverter
            # window.show()  # Показываем окно
            # app.exec_()  # и запускаем приложение

    def load_xml(self):
        central_widget = self.dockwidget.tableWidget  # Create a central widget

        grid_layout = QGridLayout(self.dockwidget)  # Create QGridLayout
        central_widget.setLayout(grid_layout)  # Set this layout in central widget
        table = self.dockwidget.tableWidget  # Create a table
        table.setColumnCount(5)  # Set columns
        table.setRowCount(82)  # and rows
        table.setHorizontalHeaderLabels(["region_id", "region_name", "value", "use_hand_cursor", "kp"])

        # Set the tooltips to headings
        table.horizontalHeaderItem(0).setToolTip("region_id")
        table.horizontalHeaderItem(1).setToolTip("region_name")
        table.horizontalHeaderItem(2).setToolTip("value")
        table.horizontalHeaderItem(3).setToolTip("use_hand_cursor")
        table.horizontalHeaderItem(4).setToolTip("kp")

        with open(self.xml_file, 'r', encoding='utf-8') as xml:
            i = 0
            for event, elem in ET.iterparse(self.xml_file):
                if elem.tag == "region" and event == "end":
                    table.setItem(i, 0, QTableWidgetItem(str(elem.attrib['id'])))
                    table.setItem(i, 1, QTableWidgetItem(str(elem.attrib['name'])))
                    if elem.attrib.__contains__('value'):
                        table.setItem(i, 2, QTableWidgetItem(str(elem.attrib['value'])))
                    if elem.attrib.__contains__('useHandCursor'):
                        table.setItem(i, 3, QTableWidgetItem(str(elem.attrib['useHandCursor'])))
                    if elem.attrib.__contains__('kp'):
                        table.setItem(i, 4, QTableWidgetItem(str(elem.attrib['kp'])))
                    elem.clear()
                    i += 1

        # Do the resize of the columns by content
        table.resizeColumnsToContents()

        grid_layout.addWidget(table, 0, 0)  # Adding the table to the grid


    def convert_xml(self):
        # переводжим XML в словарь
        with open(self.xml_file, encoding='utf-8') as xml_file:
            data_dict = xmltodict.parse(xml_file.read())
        xml_file.close()
        print(data_dict)

        # переводим словарь в geoJSON
        json_data = geojson.dumps(data_dict)

        # сохораняем результат в файл
        name = self.xml_file.title()[:-4]
        with open(name + ".geojson", "w", encoding='utf-8') as json_file:
            json_file.write(json_data)
        print(json_data)

        json_file.close()

        QMessageBox.about(self.dockwidget, "Сообщение", "Успешно сформирован GeoJSON файл " + json_file.name)
    

    def get_folder(self):
        fname = QFileDialog.getOpenFileName(self.dockwidget, 'Open file', 'E:\Work\QGISProject\XML2GeoJSONConverter')[0]
        self.xml_file = fname
        self.load_xml()


"""def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = XMLConverter()  # Создаём объект класса XMLConverter
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()"""
