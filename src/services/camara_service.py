
from pygrabber.dshow_graph import FilterGraph

#en lista las resoluciones estandar de una camara

RESOLUTION_ACCEPT_CV2 = [
    (320,240),
    (640,480),
    (1280,720),
    (1920,1080),
    (2560,1440)
]

class ResolutionInfo: 
    def __init__(self,index:int, width:int, height:int):
        self.index = index
        self.width = width
        self.height = height

    def __str__(self):
        return f"ResolutionInfo(width={self.width}, height={self.height})"




class CamaraInfo:
    def __init__(self, camera_index:int=0, name:str="", resolutions:list[ResolutionInfo]=[]):
        self.camera_index = camera_index
        self.name = name
        self.resolutions = resolutions

    def __str__(self):
        return f"CamaraInfo(camera_index={self.camera_index}, name={self.name}, resolution={self.resolutions})"
    
    def __eq__(self, value):
        if isinstance(value, CamaraInfo):
            return self.camera_index == value.camera_index and self.name == value.name
        return False




def get_camera_info()->list[CamaraInfo]:
    """Returns a list of available cameras with their device paths."""
    cameras:list[CamaraInfo] = []

    graph = FilterGraph()
    list_devices = (graph.get_input_devices())# list of camera device 
    for i, name_device in enumerate(list_devices):
        if "virtual" in name_device.lower():
            continue
        try:
            
            graph.add_video_input_device(i)
            device = graph.get_input_device()
            resolutions = device.get_formats()
            resolutions = [ ResolutionInfo(r['index'],r['width'] , r['height'])  for r in resolutions if (r['width'], r['height']) in RESOLUTION_ACCEPT_CV2 ]
            #filtra las resoluciones estantar para que solo tenga las mas importantes
            resolutions = [ r for r in resolutions if not exist_resolution(resolutions,r)]
            resolutions.sort(key=lambda r: r.width*r.height)
            cameras.append(CamaraInfo(i,name_device,resolutions=resolutions))
            graph.stop()
            graph.remove_filters()
        except Exception as e:
            print(str(e))
    return cameras


def exist_resolution(resolutions:list[ResolutionInfo], resolution:ResolutionInfo)->bool:
    exit_r = False
    for r in resolutions:
        if  resolution.index > r.index and r.width  == resolution.width and r.height == resolution.height:
            exit_r = True
            break
    return exit_r



