from source_download import SourceDownload


def print_hi(name):
    print(f'Hi, {name}')
    SourceDownload.download_file("https://drive.google.com/drive/folders/1bGbVRol7v_biZ6k1_GCwHbte9J8E1q8o")


if __name__ == '__main__':
    print_hi('PyCharm')
