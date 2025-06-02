from typing import Callable, Union
import config.constants.enviroments as Enviroments
from pysher.channel import Channel
import pysher

class PusherService(pysher.Pusher): 

  _pusher_server = None
  _pusher_client = None

  def __init__(self, 
                connect_handler: Callable,
                app_id=Enviroments.pusherAppId,
                key=Enviroments.pusherAppkey,
                secret=Enviroments.pusherSecret,
                cluster=Enviroments.pusherCluster,
                show_logging=True
                ):
      self.connect_handler = connect_handler
      self.app_id=app_id
      self.key=key
      self.secret=secret
      self.cluster=cluster
      import pusher
      import sys

      # Add a logging handler so we can see the raw communication data
      import logging



    
      pysher.Pusher.__init__(self,key=self.key, 
                              cluster=self.cluster, 
                              secret=self.secret
                                          )
      self._pusher_client = pusher.Pusher(app_id=self.app_id,
                                          key=self.key,
                                          secret=self.secret,
                                          cluster=self.cluster)

      self.connection.bind('pusher:connection_established', self.connect_handler)
      if show_logging:
          root = logging.getLogger()
          root.setLevel(logging.INFO)
          ch = logging.StreamHandler(sys.stdout)
          root.addHandler(ch)
      
      # self._pusher_server.connect()

  # We can't subscribe until we've connected, so we use a callback handler
  # to subscribe when able
  

  def listen(self, channel_name:str)->Union[Channel, None]:
    channel = self.subscribe(channel_name)
    return channel



  def trigger(self, channelName:str, event:str, data:Union[dict,str]):
    
    self._pusher_client.trigger(channelName, event, data)


