from typing import Union
from PyQt6.QtWidgets import  QWidget, QLabel, QHBoxLayout,QVBoxLayout, QSizePolicy

from PyQt6.QtCore import Qt




class AppLayout(QVBoxLayout):
    def __init__(self,sidebar:QWidget ,content:Union[QWidget, None] = None, footer:Union[QWidget, None]= None,):
        super().__init__()
        #add a vertial layout
        self.setContentsMargins(0, 0, 0, 0)
        #add a horizontal layout
        self.layout_body = QHBoxLayout()
        self.layout_body.setContentsMargins(0, 0, 0, 0)

        #add siderbar in horizontal layout
        self.sidebar = sidebar
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_body.addWidget(self.sidebar,3)

        #add content in horizontal layout
        self.content_section = content

        self.addLayout(self.layout_body)
        if footer is not None: 
            self.addWidget(footer)

    @property
    def content_section(self):
        return self.layout_body.itemAt(1).widget()


    @content_section.setter
    def content_section(self, content_section:Union[QWidget, None]):
        if content_section is None:
            content_section = QLabel("Content Section")
            content_section.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_content(content_section)




    def _update_content(self, content:QWidget):

        content_section = self.layout_body.itemAt(1)
        if content_section is not None:
            content_section = content_section.widget()
            content_section.deleteLater()
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout_body.addWidget(content, 7)
        



        
       



