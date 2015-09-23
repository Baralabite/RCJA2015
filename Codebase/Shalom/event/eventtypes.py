class EventTypes:
    #Data: (message)
    TEST = "TEST"

    #Data: (legName, angle)
    JOINT_ANGLE_CHANGE = "JOINT_ANGLE_CHANGE"
    #Data: (legName, signal)
    JOINT_SERVO_SIGNAL_CHANGE = "JOINT_SERVO_SIGNAL_CHANGE"
    #Data: {legName, signal, time}
    JOINT_ANGLE_CHANGE_TIME = "JOINT_ANGLE_CHANGE_TIME"

    #Called by /types/Position
    #Data: {newPosition}
    POSITION_CHANGED = "POSITION_CHANGED"