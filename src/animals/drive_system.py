from src import config
import numpy as np


class DriveSystem:
    ############################################################################################################
    def __init__(self, animal):
        self.animal = animal
        self.num_drives = None
        self.drive_list = None
        self.drive_index_dict = None
        self.drive_value_array = None
        self.last_drive_value_array = None

        self.drive_init_dict = config.Animal.drive_init_dict
        self.action_drive_change_dict = config.Animal.action_drive_change_dict

        self.init_drives()

    ############################################################################################################
    def __repr__(self):
        output_string = "Drive System: {} Drives\n".format(self.num_drives)
        for i in range(self.num_drives):
            output_string += "    {:8s}: {:0.4f}\n".format(self.drive_list[i], self.drive_value_array[i])
        return output_string

    ############################################################################################################
    def init_drives(self):
        self.num_drives = len(self.drive_init_dict)

        self.drive_list = []
        self.drive_index_dict = {}

        self.drive_value_array = np.ones([self.num_drives], float)
        self.last_drive_value_array = np.ones([self.num_drives], float)

        i = 0
        for drive in self.drive_init_dict:
            self.drive_list.append(drive)
            self.drive_index_dict[drive] = i
            self.drive_value_array[i] = self.drive_init_dict[drive]
            self.last_drive_value_array[i] = self.drive_init_dict[drive]
            i += 1

    ############################################################################################################
    def update_drives(self, action_choice, debug=False):

        self.last_drive_value_array = np.copy(self.drive_value_array)

        # the action taken, so we can enact its effects
        action_effect_dict = self.action_drive_change_dict[action_choice]

        # update the drives
        for i in range(self.num_drives):
            drive = self.drive_list[i]

            if drive == 'Energy':
                # metabolism and size effect how much energy things take
                energy_cost = (self.animal.current_size * action_effect_dict[drive] * self.animal.metabolism)/100
                self.drive_value_array[i] += energy_cost
            else:
                self.drive_value_array[i] += action_effect_dict[drive]/100

        # drop health by the starvation rate
        if self.drive_value_array[self.drive_index_dict['Energy']] <= 0:
            self.drive_value_array[self.drive_index_dict['Health']] -= config.Animal.starvation_rate/100

        # raise arousal by the genetically determined arousal growth rate
        self.drive_value_array[self.drive_index_dict['Arousal']] += self.animal.phenotype.trait_value_dict['Arousal Growth']

        # cap all drives between 0 and 1
        for i in range(self.num_drives):
            if self.drive_value_array[i] < 0:
                self.drive_value_array[i] = 0
            if self.drive_value_array[i] > 1:
                self.drive_value_array[i] = 1

        if config.Debug.drive_system:
            print("\nUpdate Drives")
            print("    Start Drives", self.last_drive_value_array)
            print("    Action Choice & Effect", action_choice, action_effect_dict)
            print("    End Drives", self.drive_value_array, '\n')



