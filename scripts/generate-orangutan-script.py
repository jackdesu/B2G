import argparse, sys
from itertools import *
from random import *

def print_device_home(device):
  if device == 'unagi':
    print 'tap 44 515 1 2000' # long home key for unagi
  elif device == 'aries':
    print 'tap 360 1240 1 2000' # also a long software home press
  else:
    # 102 corresponds to the home button key (at least on flame devices)
    print 'keydown 102'
    print 'sleep 5'
    print 'keyup 102'

def main():
  parser = argparse.ArgumentParser(description="Generate automated test script for orangutan")
  parser.add_argument("-s", "--steps", help="Number of steps")
  parser.add_argument("-d", "--device", help="Optional device name for defaults")
  parser.add_argument("--width", help="Device width in pixels")
  parser.add_argument("--height", help="Device height in pixels")

  args = parser.parse_args(sys.argv[1:])

  rndSeed = random()
  fuzzSeed = str(rndSeed)  # replace rndSeed here with the required seed
  #print 'Current seed is: ' + fuzzSeed
  rnd = Random(fuzzSeed)

  if (args.steps):
    steps = int(args.steps)
  else:
    steps = 10000

  if args.device:
    device = args.device
  else:
    device = 'flame'

  if device == 'unagi':
    maxX = 320
    # The home key is around (44, 515) on unagi.
    # Filed a followup bug (838267) for better key support.
    maxY = 520
  elif device == 'flame':
    maxX = 480
    maxY = 854
  elif device == 'aries':
    maxX = 720
    maxY = 1280
  else:
    maxX = 320
    maxY = 520
    if args.width:
      maxX = int(args.width)
    if args.height:
      maxY = int(args.height)

  count = 1
  sleepAllowed = 1
  while (count <= steps):
    if count % 1000 == 0:
      print_device_home(device)
      count = count + 1
      sleepAllowed = 1
      continue

    x = rnd.choice(['tap', 'sleep', 'drag'])
    if x == 'tap':
      # tap [x] [y] [num times] [duration of each tap in msec]
      print 'tap ', rnd.randint(1, maxX), ' ', rnd.randint(1, maxY), ' ', rnd.randint(1,3), rnd.randint(50, 1000)
      sleepAllowed = 1
      count = count + 1
    elif x == 'sleep':
      # sleep [duration in msec]
      if (sleepAllowed):
        print 'sleep', rnd.randint(100, 3000)
        count = count + 1
        sleepAllowed = 0
    else:
      # drag [start x] [start y] [end x] [end y] [num steps] [duration in msec]
      print 'drag',rnd.randint(1, maxX), ' ', rnd.randint(1, maxY), ' ' , rnd.randint(1, maxX), ' ', rnd.randint(1, maxY), ' ', rnd.randint(10, 20), ' ', rnd.randint(10, 350)
      sleepAllowed = 1
      count = count + 1

if __name__ == "__main__":
  main()
