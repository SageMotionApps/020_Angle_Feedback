import logging
from sage.base_app import BaseApp
if __name__ == '__main__':
    import AngleCalculation
else:
    from . import AngleCalculation

class Core(BaseApp):
    ###########################################################
    # INITIALIZE APP
    ###########################################################
    def __init__(self, my_sage):
        BaseApp.__init__(self, my_sage, __file__)
        
        # The prefix "self" denotes global variables 
        self.iteration = 0
        
        # Define the node number for sensing this_angle
        self.sensor_node = self.info["sensors"].index("sensor")
        self.max_feedback_node = self.info["feedback"].index("max feedback")  
        self.min_feedback_node = self.info["feedback"].index("min feedback")  
                
        # self.config values are set in the App Configuration panel of the SageMotion Graphical Interface
        self.this_angle_min = self.config['angle_min'] #  minimum angle with no feedback
        self.this_angle_max = self.config['angle_max'] #  maximum angle with no feedback
        


    ###########################################################
    # CHECK NODE CONNECTIONS
    # Make sure all the nodes needed for sensing and feedback
    # are present before starting the app.
    ###########################################################
    def check_status(self):
        sensors_count = self.get_sensors_count()
        feedback_count = self.get_feedback_count()
        logging.debug("config pulse length {}".format(self.info["pulse_length"]))
        err_msg = ""
        if sensors_count < len(self.info['sensors']):
            err_msg += "App requires {} sensors but only {} are connected".format(
                    len(self.info['sensors']), sensors_count)
        if self.config['feedback_enabled'] and feedback_count < len(self.info['feedback']):
            err_msg += "App require {} feedback but only {} are connected".format(
                    len(self.info['feedback']), feedback_count)
        if err_msg != "":
            return False, err_msg
        return True, "Now running Angle Feedback Test App"
    
    #############################################################
    # UPON STARTING THE APP
    # If you have anything that needs to happen before the app starts 
    # collecting data, you can uncomment the following lines
    # and add the code in there. This function will be called before the
    # run_in_loop() function below. 
    #############################################################
    # def on_start_event(self, start_time):
    #     print(f"In On Start Event: {start_time}")

    #############################################################
    # RUN APP IN LOOP
    ############################################################# 
    def run_in_loop(self):
        # Get next data packet
        data = self.my_sage.get_next_data()

        # Calculate angle
        this_angle = AngleCalculation.calculate_angle(self.sensor_node,data)

        # Turn feedback nodes on/off
        if self.config['feedback_enabled']:
            min_feedback_state = int(this_angle < self.this_angle_min)
            max_feedback_state = int(this_angle > self.this_angle_max)
            
            self.toggle_feedback(self.min_feedback_node,self.info["pulse_length"],feedback_state=min_feedback_state)
            self.toggle_feedback(self.max_feedback_node,self.info["pulse_length"],feedback_state=max_feedback_state)
        else:
            min_feedback_state = 0
            max_feedback_state = 0
            
        # To save data, add it to the my_data structure and update the user_fields in info.json accordingly 
        my_data = {'time': [self.iteration/self.info["datarate"]],
                   'angle': [this_angle],
                   'angle_min': [self.this_angle_min],
                   'angle_max': [self.this_angle_max],
                   'min_feedback_state': [min_feedback_state],
                   'max_feedback_state': [max_feedback_state]}

        self.my_sage.save_data(data, my_data)
        self.my_sage.send_stream_data(data, my_data)
        
        # Increment for next loop
        self.iteration += 1
        
        return True

    def toggle_feedback(self, feedbackNode=0, duration = 1, feedback_state = False):
            if feedback_state:
                self.my_sage.feedback_on(feedbackNode, duration)
            else:
                self.my_sage.feedback_off(feedbackNode)
        
    #############################################################
    # UPON STOPPING THE APP
    # If you have anything that needs to happen after the app stops, 
    # you can uncomment the following lines and add the code in there.
    # This function will be called after the data file is saved and 
    # can be read back in for reporting purposes if needed.
    #############################################################
    # def on_stop_event(self, stop_time):
    #     print(f"In On Stop Event: {stop_time}")
