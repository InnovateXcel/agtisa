class GearTransmissionECU:
    def __init__(self):
        # Initialize variables and parameters
        self.current_gear = 1
        self.target_speed = 0.0
        self.gear_ratios = [3.5, 2.5, 1.8, 1.2, 0.9]  # Example gear ratios for a 5-speed transmission
        self.shift_speed_thresholds = [20.0, 40.0, 60.0, 80.0]  # Example speed thresholds for gear shifting

    def update_target_speed(self, speed):
        # Update the target speed based on the user input or sensor data
        self.target_speed = speed

    def control_logic(self, current_speed):
        # Implement the control logic for gear shifting based on current speed and target speed
        # Find the appropriate target gear based on the current speed and target speed
        if current_speed < self.target_speed and self.current_gear < len(self.gear_ratios):
            # Shift to a higher gear if the current speed is below the target speed and there is a higher gear available
            self.current_gear += 1
        elif current_speed > self.target_speed and self.current_gear > 1:
            # Shift to a lower gear if the current speed is above the target speed and there is a lower gear available
            self.current_gear -= 1

        # Additional logic to handle gear shifting based on specific speed thresholds
        for i in range(len(self.shift_speed_thresholds)):
            if current_speed > self.shift_speed_thresholds[i] and self.current_gear == i + 1:
                self.current_gear += 1
            elif i > 0 and current_speed < self.shift_speed_thresholds[i - 1] and self.current_gear == i + 2:
                self.current_gear -= 1

    def run(self, current_speed):
        # Execute the ECU control loop
        print("Before control logic - Current Gear:", self.current_gear)
        self.control_logic(current_speed)
        print("After control logic - Current Gear:", self.current_gear)

        # Perform other ECU tasks such as actuator control, data logging, etc.

        # Return the current gear value
        return self.current_gear


# Create an instance of the GearTransmissionECU
ecu = GearTransmissionECU()

# Simulate the operation of the ECU
current_speed = 60.0
target_speed = 80.0
ecu.update_target_speed(target_speed)
current_gear = ecu.run(current_speed)
print("Final Current Gear:", current_gear)