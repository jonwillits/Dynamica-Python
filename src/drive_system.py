from src import config
import numpy as np


############################################################################################################
############################################################################################################
class DriveSystem:
    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal
        self.num_drives = None
        self.drive_list = None
        self.drive_index_dict = None
        self.drive_direction_array = None
        self.drive_value_array = None
        self.last_drive_value_array = None
        self.drive_value_change_array = None

        self.action_drive_change_dict = config.Animal.action_drive_change_dict

        self.init_drives()

    ############################################################################################################
    def __repr__(self):
        return "Drive System: {} Drives\n".format(self.num_drives)

    ############################################################################################################
    def init_drives(self):

        drive_direction_list = []
        for action in self.action_drive_change_dict:
            drive_direction_list = []
            self.num_drives = 0
            self.drive_list = []
            self.drive_index_dict = {}
            for drive in self.action_drive_change_dict[action]:
                self.drive_list.append(drive)
                self.drive_index_dict[drive] = self.num_drives
                self.num_drives += 1

                trait_string = drive + ' Value Direction'
                drive_direction_list.append(self.animal.phenotype.trait_value_dict[trait_string])
            break

        self.drive_value_array = np.ones([self.num_drives], float)
        self.last_drive_value_array = np.ones([self.num_drives], float)
        self.drive_value_change_array = np.zeros([self.num_drives], float)
        self.drive_direction_array = np.array(drive_direction_list)

    ############################################################################################################
    def update_drives(self, action_choice):

        # the action taken, so we can enact its effects
        action_effect_dict = self.action_drive_change_dict[action_choice]

        # make a copy of the drives before we started
        self.last_drive_value_array = np.copy(self.drive_value_array)

        # update the drives
        for i in range(self.num_drives):
            drive = self.drive_list[i]

            if drive == 'Energy':
                # metabolism and size effect how much energy things take
                self.drive_value_array[i] += self.animal.current_size * action_effect_dict[drive] * self.animal.metabolism
            else:
                self.drive_value_array[i] += action_effect_dict[drive]

        # drop health by the starvation rate
        if self.drive_value_array[self.drive_index_dict['Energy']] <= 0:
            self.drive_value_array[self.drive_index_dict['Health']] -= config.Animal.starvation_rate

        # cap all drives between 0 and 100
        for i in range(self.num_drives):
            if self.drive_value_array[i] < 0:
                self.drive_value_array[i] = 0
            if self.drive_value_array[i] > 100:
                self.drive_value_array[i] = 100

        # make a list of the drive changes for the current turn
        self.drive_value_change_array = self.drive_value_array - self.last_drive_value_array

    ############################################################################################################
    def print_drive_system(self):
        print(self, end='')
        for i in range(self.num_drives):
            print("     ", self.drive_list[i], self.drive_direction_array[i],
                  self.drive_value_array[i], self.drive_value_change_array[i])
