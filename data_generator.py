from os import listdir
from os.path import join, isfile

import numpy as np


class DataGenerator(object):
    def __init__(self, data_directory, output_data_directory):
        self.items = None
        self._data = None
        self._row = 0

        for file_name in (f for f in listdir(data_directory) if isfile(join(data_directory, f))):
            local_file = join(data_directory, file_name)
            with open(local_file, 'r') as f:
                print('reading file {file_name}'.format(file_name=file_name))
                play_date = f.readline().split()[0]
                f.readline()
                self.define_items(f.readline())
                lines = f.readlines()
                self._data = np.zeros((len(lines), 15), dtype=np.float32)
                self._row = 0
                for line in lines:
                    self.add_info(line)
                print('saving file {file_name}'.format(file_name=file_name))
                np.save(output_data_directory + play_date + "_" + file_name[:-4], self._data)

    def add_gripper_info(self, entries):
        self._data[self._row][0] = entries['gripper_center_p_x']
        self._data[self._row][1] = entries['gripper_center_p_y']
        self._data[self._row][2] = entries['gripper_center_p_z']
        self._data[self._row][3] = entries['gripper_center_r_x']
        self._data[self._row][4] = entries['gripper_center_r_y']
        self._data[self._row][5] = entries['gripper_center_r_z']
        self._data[self._row][6] = entries['gripper_center_r_w']
        self._data[self._row][7] = entries['gripper']

    def add_box_info(self, entries):
        self._data[self._row][8] = entries['box_put_p_x']
        self._data[self._row][9] = entries['box_put_p_y']
        self._data[self._row][10] = entries['box_put_p_z']
        self._data[self._row][11] = entries['box_put_r_x']
        self._data[self._row][12] = entries['box_put_r_y']
        self._data[self._row][13] = entries['box_put_r_z']
        self._data[self._row][14] = entries['box_put_r_w']

    def add_info(self, line):
        entries = {i[0]: i[1] for i in zip(self.items, line.split(','))}
        self.add_gripper_info(entries)
        self.add_box_info(entries)
        self._row += 1

    def define_items(self, line):
        self.items = line.split(',')


if __name__ == "__main__":
    data_directory = "data/level1/"
    generated_data_directory = "data/level1/numpy/"
    dg = DataGenerator(data_directory, generated_data_directory)
    print(dg.items)
