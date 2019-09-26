import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server

def reboot(unused_addr, args, reiniciar):
  command = "/usr/bin/sudo /sbin/reboot"
  import subprocess
  process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  output = process.communicate()[0]
  print (output)

def shutdown ( unused_addr, args, desligar):
  command = "/usr/bin/sudo /sbin/shutdown -h now"
  import subprocess
  process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  output = process.communicate()[0]
  print (output)



if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", 
      default='', help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5001, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/sons_de_silicio/reboot", reboot, "Reboot")
  dispatcher.map("/sons_de_silicio/shutdown", shutdown, "Shutdown")
  
  dispatcher.map("/buzu/reiniciar/tudo", reboot, "Reboot")
  dispatcher.map("/buzu/desligar/tudo", shutdown, "Shutdown")
  dispatcher.map("/buzu/reiniciar/buzuServidor", reboot, "Reboot")
  dispatcher.map("/buzu/desligar/buzuServidor", shutdown, "Shutdown")
  dispatcher.map("/buzu/reiniciar/buzuVideo", reboot, "Reboot")
  dispatcher.map("/buzu/desligar/buzuVideo", shutdown, "Shutdown")
  dispatcher.map("/buzu/reiniciar/buzuAudio_1-2", reboot, "Reboot")
  dispatcher.map("/buzu/desligar/buzuAudio_1-2", shutdown, "Shutdown")
  dispatcher.map("/buzu/reiniciar/buzuAudio_3-4", reboot, "Reboot")
  dispatcher.map("/buzu/desligar/buzuAudio_3-4", shutdown, "Shutdown")

  dispatcher.map("/tsf/reboot", reboot, "Reboot")
  dispatcher.map("/tsf/shutdown", shutdown, "Shutdown") 
  
  dispatcher.map("/sonhofonias/reboot", reboot, "Reboot")
  dispatcher.map("/sonhofonias/shutdown", shutdown, "Shutdown")

  dispatcher.map("/red_line/reboot", reboot, "Reboot")
  dispatcher.map("/red_line/shutdown", shutdown, "Shutdown")  
  
  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()
