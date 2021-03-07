def main():
    import scenefile
    reload(scenefile)

    scene_file = scenefile.SceneFile("D:\\sandbox\\test_folder\\test_folder_deeper\\mayatest_tankmdl_v001.ma")
    print(scene_file.path)
    print(scene_file.save_file())
    print(scene_file.increment_save_file())


if __name__ == '__main__':
    main()
