""" Python motion data export from Choregraph.
Includes some Python code to run outside Choregraph.
Mike added code to stand robot up.
10-03-14: This appears to be a simple but effective way to control individual joints.
Will also allow multiple body parts to be combined into a single motion.angleInterpolation(names, keys, times, True)
commands ie chose from each Markov matrix, then append to the motion list.


@author: Aldebaran Robotics Python export, Mike McFarlane

"""


# Choregraphe simplified export in Python.
from naoqi import ALProxy

names = list()
times = list()
keys = list()


##############################################################

# Move left arm left right.

names.append("LElbowRoll")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([-0.335904, -0.308292, -0.269942, -0.283748, -0.19631, -0.1733, -0.079726])

names.append("LElbowYaw")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([-1.19963, -1.20116, -1.18736, -1.08305, -1.12293, -1.11219, -1.11833])

names.append("LHand")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([0.2952, 0.2952, 0.2952, 0.2952, 0.2952, 0.2952, 0.2952])

names.append("LShoulderPitch")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([0.892746, 0.87127, 1.00933, 1.01393, 1.02927, 1.04615, 1.14125])

names.append("LShoulderRoll")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([0.110406, 0.478566, -0.0629361, -0.30991, 0.082794, 0.41107, -0.0798099])

names.append("LWristYaw")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([-0.377406, -1.30241, 0.191708, 0.960242, -0.599836, 0.582878, -0.314512])

names.append("RElbowRoll")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([0.40962, 0.40962, 0.40962, 0.40962, 0.40962, 0.40962, 0.40962])

names.append("RElbowYaw")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([1.20568, 1.20568, 1.20568, 1.20568, 1.20568, 1.20568, 1.20568])

names.append("RHand")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([0.2936, 0.2936, 0.2936, 0.2936, 0.2936, 0.2936, 0.2936])

names.append("RShoulderPitch")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([1.45888, 1.45888, 1.45888, 1.45888, 1.45888, 1.45888, 1.45888])

names.append("RShoulderRoll")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([-0.16418, -0.16418, -0.16418, -0.16418, -0.16418, -0.16418, -0.16418])

names.append("RWristYaw")
times.append([0.88, 1.28, 1.68, 2.04, 2.44, 2.84, 3.2])
keys.append([0.0643861, 0.0643861, 0.0643861, 0.0628521, 0.0643861, 0.0643861, 0.0628521])

##############################################################

# Move left arm forward and back.

# names.append("LElbowRoll")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([-0.194776, -0.0873961, -0.237728, -0.049046, -0.0628521, -0.0352399, -0.222388, -0.10427])

# names.append("LElbowYaw")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([-1.11986, -1.11833, -1.12293, -1.11219, -1.12293, -1.12293, -1.11986, -1.11986])

# names.append("LHand")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([0.2948, 0.2948, 0.2944, 0.2944, 0.2948, 0.2948, 0.2944, 0.2944])

# names.append("LShoulderPitch")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([0.753152, 1.01393, 0.605888, 1.13052, 0.705598, 1.17193, 0.766958, 1.19648])

# names.append("LShoulderRoll")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([0.0352399, 0.030638, 0.0413761, 0.00149202, 0.032172, 0.024502, 0.0597839, 0.049046])

# names.append("LWristYaw")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([-0.483252, -0.452572, -0.48632, -0.446436, -0.538476, -0.504728, -0.513932, -0.452572])

# names.append("RElbowRoll")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([0.403484, 0.403484, 0.40195, 0.40195, 0.403484, 0.403484, 0.403484, 0.40195])

# names.append("RElbowYaw")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([1.19801, 1.19801, 1.19801, 1.19801, 1.19801, 1.19801, 1.19801, 1.19801])

# names.append("RHand")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([0.3056, 0.3056, 0.3056, 0.3056, 0.3056, 0.3056, 0.3056, 0.3056])

# names.append("RShoulderPitch")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([1.46501, 1.46501, 1.46808, 1.46808, 1.46961, 1.46961, 1.47422, 1.47422])

# names.append("RShoulderRoll")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([-0.182588, -0.182588, -0.0890141, -0.0859461, -0.0859461, -0.0859461, -0.0752079, -0.0752079])

# names.append("RWristYaw")
# times.append([0.76, 1.12, 1.48, 1.84, 2.16, 2.52, 2.88, 3.24])
# keys.append([0.102736, 0.102736, 0.102736, 0.102736, 0.102736, 0.102736, 0.102736, 0.102736])

##############################################################

# Shake left arm in front, then open close hand.

# names.append("LElbowRoll")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([-0.0613179, -0.076658, -0.0429101, -0.08126, -0.08126, -0.079726, -0.08126, -0.0429101])

# names.append("LElbowYaw")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([-1.07998, -1.26713, -1.23338, -1.28707, -1.28707, -1.28707, -1.28707, -1.25025])

# names.append("LHand")
# times.append([0.48, 0.92, 1.28, 1.64, 1.96, 2.2, 2.44, 2.68, 2.92, 3.12, 3.32])
# keys.append([0.2948, 0.2948, 0.2944, 0.2948, 0, 0.00559998, 1, 0.9648, 0.29, 0.2904, 0.2904])

# names.append("LShoulderPitch")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([1.21028, 1.20415, 1.21028, 1.1704, 1.1704, 1.17193, 1.17193, 1.20722])

# names.append("LShoulderRoll")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([0.0229681, 0.00149202, -0.0107799, 0.0214341, 0.0214341, 0.0214341, 0.0214341, 0.029104])

# names.append("LWristYaw")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([1.82387, -1.82387, 1.82387, -1.82387, -1.82387, -1.82387, -1.82387, -0.04146])

# names.append("RElbowRoll")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([0.391212, 0.391212, 0.391212, 0.392746, 0.391212, 0.391212, 0.392746, 0.391212])

# names.append("RElbowYaw")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([1.19801, 1.19801, 1.19801, 1.19801, 1.19801, 1.19801, 1.19801, 1.19801])

# names.append("RHand")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([0.3056, 0.3056, 0.3056, 0.3056, 0.3056, 0.3056, 0.3056, 0.3056])

# names.append("RShoulderPitch")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([1.48189, 1.48189, 1.48189, 1.48189, 1.48189, 1.48189, 1.48189, 1.48189])

# names.append("RShoulderRoll")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([-0.070606, -0.070606, -0.070606, -0.070606, -0.070606, -0.070606, -0.070606, -0.070606])

# names.append("RWristYaw")
# times.append([0.48, 0.92, 1.28, 1.64, 2.2, 2.68, 3.12, 3.32])
# keys.append([0.102736, 0.102736, 0.102736, 0.102736, 0.102736, 0.102736, 0.102736, 0.102736])

##############################################################

# Shake left hand behind back.

# names.append("LElbowRoll")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([-0.0674541, -0.05058, -0.0444441, -0.0444441, -0.0613179, -0.0643861, -0.05825, -0.049046, -0.049046, -0.401866])

# names.append("LElbowYaw")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([-1.18889, -1.18889, -1.17662, -1.17662, -1.16895, -1.18736, -1.17662, -1.18736, -1.18889, -1.18889])

# names.append("LHand")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([0.2944, 0.2944, 0.2948, 0.2944, 0.2944, 0.2948, 0.2944, 0.2944, 0.2944, 0.2944])

# names.append("LShoulderPitch")
# times.append([0.56, 0.96, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([2.07086, 2.06428, 2.05705, 2.05245, 2.07086, 2.04171, 2.06165, 2.01257, 2.01257, 1.50328])

# names.append("LShoulderRoll")
# times.append([0.56, 0.72, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.44, 2.72, 3, 3.32])
# keys.append([0.07359, 0.234641, 0.269336, -0.0844119, 0.167164, -0.122762, 0.174834, -0.185656, 0.10849, 0.168698, 0.168698, 0.11961])

# names.append("LWristYaw")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([-0.0813439, -0.0767419, 0.291418, -0.760906, 0.431012, -0.688808, 0.466294, -0.319114, -0.319114, -0.205598])

# names.append("RElbowRoll")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([0.400416, 0.400416, 0.400416, 0.400416, 0.400416, 0.400416, 0.400416, 0.400416, 0.400416, 0.400416])

# names.append("RElbowYaw")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([1.20568, 1.20568, 1.20568, 1.20568, 1.20568, 1.20568, 1.20568, 1.20568, 1.20568, 1.20568])

# names.append("RHand")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([0.2936, 0.2936, 0.2936, 0.2936, 0.2936, 0.2936, 0.2936, 0.2936, 0.2936, 0.2936])

# names.append("RShoulderPitch")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([1.46961, 1.46961, 1.46961, 1.46808, 1.46808, 1.46961, 1.46808, 1.46961, 1.46961, 1.46808])

# names.append("RShoulderRoll")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([-0.0859461, -0.0859461, -0.0844119, -0.0813439, -0.0752079, -0.070606, -0.070606, -0.069072, -0.069072, -0.067538])

# names.append("RWristYaw")
# times.append([0.56, 0.92, 1.24, 1.48, 1.72, 1.96, 2.2, 2.72, 3, 3.32])
# keys.append([0.0643861, 0.0643861, 0.0643861, 0.0643861, 0.0643861, 0.0643861, 0.0643861, 0.0643861, 0.0643861, 0.0643861])


##############################################################



try:
  # uncomment the following line and modify the IP if you use this script outside Choregraphe.
  IP = "mistcalf.local" # Mike
  motion = ALProxy("ALMotion", IP, 9559)
  posture = ALProxy("ALRobotPosture", IP, 9559)	# Mike
  motion.wakeUp()
  posture.goToPosture("StandInit", 0.8)
  # motion = ALProxy("ALMotion")
  motion.angleInterpolation(names, keys, times, True)
  posture.goToPosture("Crouch", 0.8)
  motion.rest()
except BaseException, err:
  print err
