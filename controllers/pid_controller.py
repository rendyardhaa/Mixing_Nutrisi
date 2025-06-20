class PIDController:
    def __init__(self, Kp, Ki, Kd, name="PID"):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.name = name
        self.prev_error = 0
        self.integral = 0

    def calculate(self, setpoint, current_value):
        error = setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        output = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
        return max(0, min(255, int(output)))
