#menu principal para acceder a las configuracions y archivos
from PyQt6.QtWidgets import QMenuBar,QWidgetAction,QApplication


class MainMenu(QMenuBar):
    def __init__(self ):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create menu bar
        # Create File menu
        file_menu = self.addMenu("File")

        # Create Exit action
        exit_action = QWidgetAction( self)
        exit_action.setText("Exit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(QApplication.quit)
        file_menu.addAction( exit_action)


        # Create Draw Dataset menu
        # draw_dataset_menu = self.addMenu("Dibujar Dataset")

        # # Create Draw Dataset action
        # draw_dataset_action = QWidgetAction(self)
        # draw_dataset_action.setText("Dibujar Dataset")
        # draw_dataset_action.triggered.connect(self.open_draw_dataset_screen)
        # draw_dataset_menu.addAction(draw_dataset_action)

        # # Create Settings menu
        # settings_menu = self.addMenu("Configuraciones")

        # # Create Settings action
        # settings_action = QWidgetAction( self)
        # settings_action.setText("Configuraciones")
        # settings_action.triggered.connect(self.open_settings_screen)
        # settings_menu.addAction(settings_action)

        

    # funcion para abrir la pantalla de draw dataset
    def open_draw_dataset_screen(self):
       pass

    # funcion para abrir la pantalla de settings
    def open_settings_screen(self):
        pass


    def open_draw_dataset_screen(self):
        pass

   
   
        
        