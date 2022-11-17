import sys  # sys нужен для передачи argv в QApplication
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QFileDialog, QMessageBox
from qgis.PyQt.QtCore import QSize, Qt, QModelIndex

import ui_Converter_dialog_base
import os
import pandas as pd
import numpy as np
import lasio
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as Soup
import xmltodict
import geojson



class XMLConverter(QtWidgets.QMainWindow, Converter_dialog_base.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btnLoadXML.clicked.connect(self.get_folder)
        self.btnConvert.clicked.connect(self.convert_xml)

        self.xml_file = 'rf_map.xml'

    def load_xml(self):
        central_widget = self.tableWidget  # Create a central widget

        grid_layout = QGridLayout(self)  # Create QGridLayout
        central_widget.setLayout(grid_layout)  # Set this layout in central widget
        table = self.tableWidget  # Create a table
        table.setColumnCount(5)  # Set columns
        table.setRowCount(82)  # and rows
        table.setHorizontalHeaderLabels(["region_id", "region_name", "value", "use_hand_cursor","kp"])

        # Set the tooltips to headings
        table.horizontalHeaderItem(0).setToolTip("region_id")
        table.horizontalHeaderItem(1).setToolTip("region_name")
        table.horizontalHeaderItem(2).setToolTip("value")
        table.horizontalHeaderItem(3).setToolTip("use_hand_cursor")
        table.horizontalHeaderItem(4).setToolTip("kp")

        with open(self.xml_file, 'r', encoding='utf-8') as xml:
            soup = Soup(xml.read(), 'lxml')
        i = 0
        for event, elem in ET.iterparse("rf_map.xml"):
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
                i+=1

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
        with open(name+".geojson", "w", encoding='utf-8') as json_file:
            json_file.write(json_data)
        print(json_data)

        json_file.close()

        QMessageBox.about(self, "Сообщение", "Успешно сформирован GeoJSON файл "+ json_file.name)

    def get_folder(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'E:\Work\QGISProject\XML2GeoJSONConverter')[0]
        self.xml_file = fname
        self.load_xml()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = XMLConverter()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()