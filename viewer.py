# from OCC.Display.qtDisplay import QtCore
import os.path

from PyQt5.QtGui import QIcon, QImage, QPixmap
from ifcopenshell.geom.app import application
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolBar, QVBoxLayout, QScrollArea, QLabel, QGroupBox, \
    QFormLayout, QAction
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
#from pyparsing import unicode

import LBD_Query





class my_app(application):
    class window(application.window):
        def __init__(self):
            application.window.__init__(self)
            self.TITLE = "My proprietary money cow"
            self.setWindowTitle(self.TITLE)

    class toolbar(QToolBar):
        def __init__(self):
            QToolBar.__init__(self)

    class property_table(QWidget):
        instanceSelected = pyqtSignal([object])

        def __init__(self):
            QWidget.__init__(self)
            self.layout = QVBoxLayout(self)
            self.setLayout(self.layout)

            self.scroll = QScrollArea(self)
            self.layout.addWidget(self.scroll)
            self.scroll.setWidgetResizable(True)

            self.scrollContent = QWidget(self.scroll)
            self.scrollLayout = QVBoxLayout(self.scrollContent)
            self.scrollContent.setLayout(self.scrollLayout)
            self.scroll.setWidget(self.scrollContent)

            self.prop_dict = {}

        def select(self, product):

            while self.scrollLayout.count():
                child = self.scrollLayout.takeAt(0)
                if child is not None:
                    if child.widget() is not None:
                        child.widget().deleteLater()

            self.scroll = QScrollArea()
            self.scroll.setWidgetResizable(True)

            scrollContent = QWidget(self.scroll)
            print("properties for selection {}".format(self.prop_dict.get(str(product))))
            prop_sets = self.prop_dict.get(str(product))
            if prop_sets is not None:
                for k, v in prop_sets.items():
                    group_box = QGroupBox()

                    group_box.setTitle(k)
                    group_layout = QVBoxLayout()

                    group_box.setLayout(group_layout)
                    for name, value in v.items():
                        prop_name = str(name)
                        value_str = value.wrappedValue
                        if isinstance(value_str, str):
                            value_str = value_str.encode('utf-8')
                        if isinstance(value_str, float) or isinstance(value_str, bool):
                            value_str = str(value_str)
                        # print (value_str, type(value_str))
                        type_str = value.is_a()
                        label = QLabel(prop_name + " : " + str(value_str) + " : " + str(type_str))
                        group_layout.addWidget(label)
                    group_layout.addStretch()
                    self.scrollLayout.addWidget(group_box)
                self.scrollLayout.addStretch()
                # for props in k.values():
                #    print(props)
            else:

                label = QLabel("No IfcPropertySets asscociated with selected entity instance")
                self.scrollLayout.addWidget(label)

            res = self.links.getLD(product.GlobalId)
            group_box = QGroupBox()

            group_box.setTitle('Linked Information')
            group_layout = QVBoxLayout()
            form_layout = QFormLayout()
            group_box.setLayout(form_layout)
            # group_box.setLayout(group_layout)
            # top_labels = []

            if res is not None:
                for row in res:
                    row = row.replace("http://example.org/sibbw7936662#", "sib:")
                    row = row.replace("https://w3id.org/asbingowl/keys#", "asbkey:")
                    olabel = QLabel(str(row))
                    olabel.setWordWrap(True)
                    olabel.setStyleSheet("font-weight: bold; font-size: 10pt")
                    plabel = QLabel("propertyPlaceholderName:")
                    label.setMaximumWidth(300)
                    form_layout.addRow(plabel, olabel)
                    if "JPG" in row:
                        # print(row)
                        picpath = os.path.join(r"ICCD_TwinGenDemo\Payload documents", row)
                        # print(picpath)
                        image = QPixmap(picpath)
                        #image.scaled(20,20)

                        label = QLabel(self)
                        label.setPixmap(QPixmap(image).scaled(200,200,Qt.KeepAspectRatio))
                        group_layout.addWidget(label)
                        form_layout.addRow(label)
            else:
                label = QLabel("No Linked Information available")
                self.scrollLayout.addWidget(label)


            self.scrollLayout.addWidget(group_box)
            self.scrollLayout.addStretch()

        def load_file(self, f, **kwargs):
            # self.otl_dict {}
            print("construct property tables")
            products = list(f.by_type("IfcBuildingelementProxy"))
            for p in products:
                propset_dict = {}
                try:
                    for is_def_by in p.IsDefinedBy:
                        if is_def_by.RelatingPropertyDefinition is not None:
                            prop_def = is_def_by.RelatingPropertyDefinition
                            prop_set_name = prop_def.Name
                            props = {}
                            # props= {Name:NominalValue for (Name, NominalValue)in is_def.RelatingPropertyDefinition.HasProperties}
                            for rel in prop_def.HasProperties:
                                props[rel.Name] = rel.NominalValue

                                # print(rel)
                            propset_dict[prop_set_name] = props

                except:
                    print("failed to load properties")

                self.prop_dict[str(p)] = propset_dict

                print("property set dictionary has {} entries".format(len(propset_dict)))

            self.links = LBD_Query


    def __init__(self):
        application.__init__(self)
        # self.window = my_app.window()
        self.window.setWindowTitle("Linked Data Container Browser for Infra Objects [Demonstrator] ")
        tb = self.window.addToolBar("File")

        loadButton = QAction("new", self)
        loadButton.triggered.connect(self.loadExampleFile)
        tb.addAction(loadButton)
        zoomAllButton = QAction("newZoom", self)
        zoomAllButton.triggered.connect(self.zoomAll)
        tb.addAction(zoomAllButton)
        self.propview = self.property_table()
        self.tabs.addTab(self.propview, "Properties")
        self.tabs.setCurrentWidget(self.propview)

        self.components.append(self.propview)
        # connect properties tab selection
        self.propview.instanceSelected.connect(self.makeSelectionHandler(self.propview))


    def loadExampleFile(self):
        self.load(r"C:\Users\Anne\Desktop\TwinGenViewer\BW45-2_ohneGel_try3.ifc")

    def zoomAll(self):
        self.canvas._display.FitAll()


app = application()
my_app().start()
