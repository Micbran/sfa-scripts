from src.SceneFile.SceneFile import SceneFile


def main():
    scene_file_test = SceneFile("D:/", "test_file", "testing1", 1, "ma")
    print(scene_file_test.file_name, scene_file_test.path, sep="\n")


if __name__ == '__main__':
    main()
