from src.smartsave import scenefile


def main():
    scene_file = scenefile.SceneFile("D:\\sandbox\\test_folder\\test_folder_deeper\\mayatest_tankmdl_v001.ma")
    print(scene_file.folder_path)
    print(scene_file.descriptor)
    print(scene_file.task)
    print(scene_file.version)
    print(scene_file.extension)
    print(scene_file.file_name)


if __name__ == '__main__':
    main()

