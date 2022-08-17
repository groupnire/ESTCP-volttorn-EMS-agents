"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC
import json
_log = logging.getLogger(__name__)
utils.setup_logging()
__version__ = "0.1"


def dataConcentrator(config_path, **kwargs):
    """Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.

    :type config_path: str
    :returns: Dataconcentrator
    :rtype: Dataconcentrator
    """
    try:
        config = utils.load_config(config_path)
    except StandardError:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Dataconcentrator(setting1,
                          setting2,
                          **kwargs)


class Dataconcentrator(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic",
                 **kwargs):
        super(Dataconcentrator, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}


        #Set a default configuration to ensure that self.configure is called immediately to setup
        #the agent.

        self.vip.config.set_default("config", self.default_config)
        #Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")
        self.core.periodic(10,self.BEMS_rpc)
    def configure(self, config_name, action, contents):
        """
        Called after the Agent has connected to the message bus. If a configuration exists at startup
        this will be called before onstart.

        Is called every time the configuration in the store changes.
        """
        config = self.default_config.copy()
        config.update(contents)

        _log.debug("Configuring Agent")

        try:
            setting1 = int(config["setting1"])
            setting2 = str(config["setting2"])
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        self.setting1 = setting1
        self.setting2 = setting2

        self._create_subscriptions(self.setting2)

    def _create_subscriptions(self, topic):
        #Unsubscribe from everything.
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix='devices/Campus1/',
                                  callback=self._handle_publish,all_platforms=True,)

    def _handle_publish(self, peer, sender, bus, topic, headers,
                                Message):
        x=topic.find('Campus1')
        if x>0:
          temp1=topic.split("devices")
          topic2="devices/dataconcentrator/Monitor"+temp1[1]
        else:
          topic2='dataconcentrator/'+topic
        self.vip.pubsub.publish('pubsub',topic2, message=Message)
        print("ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss",topic2)


    def BEMS_rpc(self):
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
     #   result=self.vip.rpc.call('platform.driver','set_point','fake-campus/fake-building/fake-device','ValveState',30,external_platform='BEMS_4').get(timeout=10)
#        try:
 #         result=self.vip.rpc.call('bEmsControlMonitoragent-0.1_1','rpc_method',1,430,external_platform='BEMS_4')
 #       except :
  #        pass


    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        #Example publish to pubsub
        #self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        #Exmaple RPC call
        #self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        pass

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_BEMS_Control(self,Agent,Topic,Point,Message,BEMS, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call """
        ##result=self.vip.rpc.call('platform.driver','set_point',Topic,Point,Message,external_platform=BEMS)
#        result=self.vip.rpc.call('platform.driver','set_point','fake-campus/fake-building/fake-device','SampleWritableShort1',30,external_platform='BEMS_4').get(timeout=10)
       # self.BEMS_rpc() 
        result=4
        print('##############################################',result)
     #   'BEMS_4' 'dataConcentratoragent-0.1_1'
        return result
    @RPC.export
    def rpc_NIRE_control(self,control,message, kwarg1=None, kwarg2=None):
        command=message
#        message1=json.loads(command)
        """
        RPC method

        May be called from another agent via self.core.rpc.call """
        ##result=self.vip.rpc.call('platform.driver','set_point',Topic,Point,Message,external_platform=BEMS)
#        result=self.vip.rpc.call('platform.driver','set_point','fake-campus/fake-building/fake-device','SampleWritableShort1',30,exter$
       # self.BEMS_rpc()
       # print('##########################################################',message1['BEMS_1'])
     #   'BEMS_4' 'dataConcentratoragent-0.1_1'
        if  control=='SupervisoryLPC':
           for key,value in command.items():
                   Message= [{"Threashhold":  value},{"Unit": 'kw'}]
                   print(key,value,'&&&&&&&&&&&&&&&&&&&&&&&&&&kkkkkkkkkkkkkpppppppppppppppp')
                   topic3='dataconcentrator/devices/control/'+str(key).split('_')[0]+str(key).split('_')[1]+'/PeakShaver'
                   self.vip.pubsub.publish('pubsub',topic3, message=Message)
                   print(topic3,'######################################')
        if control=='HMIcontrol':
#           print(json.loads(message))
           Message= [{"Threashhold":  10000},{"Threashhold": 'kw'}]
           for i in range(1,19):
                    BEMS='BEMS'+str(i)
                    result = self.vip.pubsub.publish(peer='pubsub',topic= 'dataconcentrator/devices/control/'+BEMS+'/PeakShaver', message=Message)
           for i in range(1,19):
                    message1=json.loads(command)
                   # Message=[1,1,1,1,1,1,1,1,1,1]
                    BEMS='BEMS_'+str(i)
                    Message=message1[BEMS]
                    result=self.vip.rpc.call('platform.driver','set_multiple_points', 'Campus1/Benshee1/'+BEMS,[('CMDC_G1',Message[0]),('CMDC_G2',Message[1]),('CMDC_G3',Message[2]),('CMDC_G4',Message[3]),('CMDC_G5',Message[4]),('CMDC_G6',Message[5]),('CMDC_G7',Message[6]),('CMDC_G9',Message[8]),('CMDC_G10',Message[9])],external_platform=BEMS).get(timeout=20)                   
        return  message

def main():
    """Main method called to start the agent."""
    utils.vip_main(dataConcentrator, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
