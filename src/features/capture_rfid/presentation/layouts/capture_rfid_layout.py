import os
from typing import Union
from PyQt6.QtWidgets import  QWidget,QLabel,QMessageBox
from PyQt6.QtCore import  Qt
from features.shared.presentation.layouts.app_layout import AppLayout
from features.capture_rfid.presentation.partials.list_scaneos import ListScaneos
from features.capture_rfid.presentation.partials.panels_video import PanelsVideo
from features.capture_rfid.domain.usecases.impinj_gpos_usecase import ImpinjGposWoker
from features.capture_rfid.infrastructure.models.gpo_configuration_model import (
    GpoConfigurationModel)
from features.capture_rfid.infrastructure.models.scaneo_model import ScaneoModel





class CaptureRfidLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.message_label = QLabel("Camaras")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar = ListScaneos(
            on_finish_scan=self.on_finish_scan
        )
        self.panels_videos = PanelsVideo()

        app_layout = AppLayout(
            sidebar=sidebar,
            content=self.panels_videos,
            footer=self.message_label
        )

        self.setLayout(app_layout)

        self.gpos_worker = ImpinjGposWoker()
        self.gpos_worker.task_complete.connect(self._result_worker_gpos)


    def _result_worker_gpos(self):
        if self.gpos_worker.has_error:
            error = self.gpos_worker.error
            QMessageBox.warning(self,error.title, error.message)
            return
        currentType = self.gpos_worker.type

        if currentType == ImpinjGposWoker.Type.Update:
            self.message_label.setText(self.gpos_worker.resp)
       

        self.message_label.setText('')

    def on_finish_scan(self,scaneos: list[ScaneoModel]):
        
        # print(self.panels_videos.save_frames())
        self.update_geos(gpo_configurations=[
            GpoConfigurationModel(
                gpo=1,
                state=GpoConfigurationModel.StateGeo.HIGH
            ),
            GpoConfigurationModel(
                gpo=2,
                state=GpoConfigurationModel.StateGeo.LOW
            ),
        ])


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
        

    

    



         














