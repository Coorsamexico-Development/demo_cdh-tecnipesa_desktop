from PyQt6.QtWidgets import  QWidget,QLabel,QMessageBox
from PyQt6.QtCore import  Qt
from features.shared.presentation.layouts.app_layout import AppLayout
from features.capture_rfid.presentation.partials.list_scaneos import ListScaneos
from features.capture_rfid.presentation.partials.panels_video import PanelsVideo
from features.capture_rfid.domain.usecases.impinj_gpos_usecase import ImpinjGposWoker
from features.capture_rfid.infrastructure.models.gpo_configuration_model import (
    GpoConfigurationModel)
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel
from features.capture_rfid.infrastructure.constants.constants import COLORS_LED



import numpy as np
from features.capture_rfid.domain.workers.cdh_tarimas_worker import CdhTarimasWorker



class CaptureRfidLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.list_scaneos = ListScaneos(
            get_image=lambda: self.get_image(),
            on_finish_scan=self.on_finish_scan
        )
        self.panels_videos = PanelsVideo()

        app_layout = AppLayout(
            header=self.message_label,
            sidebar=self.list_scaneos,
            content=self.panels_videos,
        )

        self.setLayout(app_layout)

        self.cdh_worker = CdhTarimasWorker()
        
        self.cdh_worker.task_complete.connect(self._result_worker_cdh)
        self.gpos_worker = ImpinjGposWoker()
        self.gpos_worker.task_complete.connect(self._result_worker_gpos)


    def _result_worker_cdh(self):
        if self.cdh_worker.has_error:
            error = self.cdh_worker.error
            self.message_label.setText(error.message)
            return
        currentType = self.cdh_worker.type

        if currentType == CdhTarimasWorker.Type.Store:
            self.message_label.setText("Guardado")
            

            # self.update_geos(gpo_configurations=self.colorsLeds(COLORS_LED['green']))
            # self.list_scaneos.captured_scaneos = True

        # self.message_label.setText('')


    def _result_worker_gpos(self):
        if self.gpos_worker.has_error:
            error = self.gpos_worker.error
            # QMessageBox.warning(self,error.title, error.message)
            self.message_label.setText(error.message)
            return
        currentType = self.gpos_worker.type

        if currentType == ImpinjGposWoker.Type.Update:
            self.message_label.setText(self.gpos_worker.resp)
            self.list_scaneos.captured_scaneos = True

        self.message_label.setText('')

    def on_finish_scan(self,scaneos: list[ScaneoModel]):
        if len(scaneos) > 0:
            self.message_label.setText("Guardando...")
            self.cdh_worker.type = CdhTarimasWorker.Type.Store
            self.cdh_worker.scaneos = scaneos
            self.cdh_worker.start()
        
        #self.update_geos(gpo_configurations=self.colorsLeds(COLORS_LED['red']))

    def get_image(self)->np.ndarray:
        images = self.panels_videos.save_frames()
        if len(images) == 0:
            return None
        
        return images[0][0]

    def colorsLeds(self, num_color:int):
       
        bin_numers = list(bin(num_color)[2:].rjust(3, '0'))
        leds = [GpoConfigurationModel(
                gpo=index+1,
                state=GpoConfigurationModel.StateGeo.HIGH if bin_numer == '1' else GpoConfigurationModel.StateGeo.LOW
            )  for index,bin_numer  in enumerate(bin_numers)]
        
        return leds

       



    def update_geos(self,gpo_configurations:list[GpoConfigurationModel]):

        self.message_label.setText("Actualizando...")
        self.gpos_worker.type = ImpinjGposWoker.Type.Update
        self.gpos_worker.params = {'gpo_configurations':gpo_configurations }
        self.gpos_worker.start()
       
       

    # def save_frame(self,frame:np.ndarray,image_time:str)->str:
    #     image_id = len(self.dataset_json['images']) + 100
    #     image_id = f"{image_id}{image_time}"
    #     image_path:str = os.path.join(self.record_path,  f"frame_{image_id}.jpg")
    #     relative_path = image_path.replace(self.db_rnn_datasets.base_path, "")[1:]
    #     cv2.imwrite(image_path, frame)
    #     height, width, _ = frame.shape

    #     self.dataset_json['images'].append({
    #         "id":image_id,
    #         "width": width,
    #         "height":height,
    #         "file_name":relative_path,
    #     })
        

    

    



         














