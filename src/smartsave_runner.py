from SceneFile.SceneFile import SceneFile


def main():
    scene_file_test = SceneFile("D:/testfile_testing1_v001.ma")
    print(scene_file_test.file_name, scene_file_test.path)


if __name__ == '__main__':
    main()
