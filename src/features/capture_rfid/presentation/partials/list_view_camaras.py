
from PyQt6.QtWidgets import QWidget,QVBoxLayout,QScrollArea,QSizePolicy
from PyQt6.QtCore import Qt
from services.camara_service import CamaraInfo
from features.capture_rfid.presentation.widgets.view_camara_item import ViewCamaraItem



class ListViewCamaras(QWidget):
    def __init__(self, 
                 camaras: list[CamaraInfo]= [],
                 on_click=lambda x:None,
                 ):
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)
        self._camaras = camaras
        self.on_click = on_click
        
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
    
        self.scroll_area.setProperty("class", "bg_dark")
        # Cea un widget contenedor para el QScrollArea
        scroll_content = QWidget()
        
        scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_content.setContentsMargins(0, 0, 0, 0)
        
        scroll_content.setProperty("class", "bg_dark")

        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        
        self.scroll_area.setWidget(scroll_content)

        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

        self.update_camaras()
    
    @property
    def camaras(self):
        return self._camaras
    
    @camaras.setter
    def camaras(self, camaras:list[CamaraInfo]):
        self._camaras = camaras
        self.update_camaras()

    

    



    def descative_other_menus(self,view_camara_item:ViewCamaraItem):
        for index in  range(len(self._camaras)):
            if index != view_camara_item.index:
                camara_item:ViewCamaraItem = self.scroll_layout.itemAt(index).widget()
                camara_item.is_active = False

    def update_camaras(self):
        self.remove_camaras()
        for index, camara in  enumerate(self._camaras):
            carama_item = ViewCamaraItem(
                index = index,
                camara = camara,
                on_click = self.on_click,
            )
            self.scroll_layout.addWidget(carama_item)

    def remove_camaras(self):
        for index in range(self.scroll_layout.count()):
            self.scroll_layout.itemAt(index).widget().deleteLater()

    def clear_layout(self):
        for index in range(self.main_layout.count()):
            self.main_layout.removeItem(self.main_layout.itemAt(index))



