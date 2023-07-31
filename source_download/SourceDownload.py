import gdown


class SourceDownload:
    pass


def download_file(url):
    gdown.download_folder(url)
