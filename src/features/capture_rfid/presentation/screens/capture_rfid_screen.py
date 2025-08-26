from PyQt6.QtWidgets import  QWidget,QLabel
from PyQt6.QtCore import QTimer,Qt
from features.shared.presentation.layouts.app_layout import AppLayout
from features.capture_rfid.presentation.partials.list_scaneos import ListScaneos
from features.capture_rfid.presentation.partials.panels_video import PanelsVideo
from features.capture_rfid.domain.usecases.impinj_gpos_usecase import ImpinjGposWoker
from features.capture_rfid.infrastructure.models.gpo_configuration_model import GpoConfigurationModel
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.infrastructure.constants.constants import COLORS_LED



import numpy as np
from features.capture_rfid.domain.workers.cdh_tarimas_worker import CdhTarimasWorker
from features.database.models.tarima import Tarima
from features.capture_rfid.presentation.widgets.scaneo_item import ScaneoItem
from features.shared.utils.wokers.frame_direccion_cv2 import StateDirection




class CaptureRfidScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.list_scaneos_panel = ListScaneos(
            get_images=lambda: self.get_images(),
            on_add_scaneo=self.on_add_scaneo,
            # send_scaneo=self.send_scaneo
        )
        self.panels_videos = PanelsVideo(
            on_change_direction=self.on_change_direction
        )
        self.resp_colors = set()

        app_layout = AppLayout(
            header=self.message_label,
            sidebar=self.list_scaneos_panel,
            content=self.panels_videos,
        )

        self.setLayout(app_layout)

        self.cdh_worker = CdhTarimasWorker()
        
        self.cdh_worker.task_complete.connect(self._result_worker_cdh)

        self.debounce_gpo_timer = QTimer()
        self.debounce_gpo_timer.setInterval(700)
        self.debounce_gpo_timer.setSingleShot(True)
        self.debounce_gpo_timer.timeout.connect(self.update_geos_leds)

        self.gpos_worker = ImpinjGposWoker()
        self.gpos_worker.task_complete.connect(self._result_worker_gpos)


    def _result_worker_cdh(self, color:str, must_change:bool):
        if len(self.resp_colors) > 0:
            QTimer.singleShot(1000, lambda: self.off_leds())
        if must_change:
            self.check_change_color(color)


    def check_change_color(self,color:str):
        # if self.times_led_changed > 10:
        #     return
        if color not in self.resp_colors:
            if color == 'red' or ((color == 'yellow' or color == 'blue')and 'red' not in self.resp_colors) or (color == 'green' and len(self.resp_colors) == 0):
                self.change_color_timer_geo(color)
            
            self.resp_colors.add(color)


    def _result_worker_gpos(self):
        print(self.gpos_worker.error)
        self.message_label.setText("")    

        # self.message_label.setText('')

    def on_change_direction(self,direction: StateDirection):
        self.message_label.setText("Detectando imagen...")
        if len(self.list_scaneos_panel.list_scaneos) > 0:
            scaneoItem = self.list_scaneos_panel.list_scaneos[0]
            scaneo = scaneoItem.scaneo
            scaneo.images = self.panels_videos.save_frames()
            scaneo.direction = direction.value

            self.send_scaneo(scaneoItem.scaneo)

    def send_scaneo(self, scaneo:ScaneoModel):
        self.cdh_worker.scaneo = scaneo
        self.cdh_worker.start()

    def on_add_scaneo(self,scaneoItem:ScaneoItem):
            self.message_label.setText("Guardando...")
            tarima = Tarima.select('*').firstWhere('token_tag', 'like', f'%{scaneoItem.scaneo.tag_inventory_event.epc}%')

            if tarima is not None:
                # print(f"Encontro la tarima {tarima}")
                # self.cdh_worker.must_change = False
                color = 'green' if tarima.switch else 'red'
                
            else:
                color = 'blue'
                # self.cdh_worker.must_change = True
            # print(f"color:{color}___________________________")
            scaneoItem.updateColor(color)
            self.check_change_color(color)

            # self.cdh_worker.start()

    def get_images(self)->np.ndarray:
        return self.panels_videos.save_frames()
    
    # apagado de los leds y reincio de los scaneos, respuesta de colores
    def off_leds(self):
        self.change_color_timer_geo('off')
        self.list_scaneos_panel.clear_scaneos()
        self.resp_colors.clear()
    
    #actualiza el color de los geos para el worker
    # y reinicia el timer
    def change_color_timer_geo(self, color:str):
        # print(f"cambiando color: {color}___________")
        self.gpos_worker.color = color
        self.debounce_gpo_timer.start()
        

    # se ejecuta una vez terminado el timer
    # el worker se encarga de hacer la peticion a la api deñ worker
    def update_geos_leds(self):
        self.message_label.setText("Respondiendo...")
        self.gpos_worker.start()

        

    

    



         














