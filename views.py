# -------------------------------------------------------------------------- #
# IMPORTAÇÕES


# os
from os import mkdir, chdir, remove, stat
from os.path import splitext

# shutil
from shutil import move

# glob
from glob import glob

# tarfile
import tarfile

# extensions
from extensions import extension_list


# -------------------------------------------------------------------------- #
# FUNÇÕES


def list_directory(directory):
    """Cuida de fazer a contagem das extensões."""
    chdir(directory)

    # Este é para a legenda do gráfico de pizza
    extension_dict = dict()

    # Este vai somando o tamanho de cada arquivo e depois
    # 'total_size' pega o tamanho total, para usar
    # no título do gráfico de pizza.
    extension_size = dict()

    for item in glob('*.*'):
        filename, ext = splitext(item)
        if ext in extension_list:
            extension_dict.setdefault(ext, 0)
            extension_size.setdefault(ext, 0)
            extension_dict[ext] += 1
            extension_size[ext] += stat(item).st_size / (1024 * 1024)

    total_size = sum([round(value, 2) for value in extension_size.values()])
    return total_size, extension_dict


def organize_files(directory):
    """Cuida de organizar os arquivos em pastas."""
    chdir(directory)
    for item in glob('*.*'):
        filename, ext = splitext(item)
        if ext in extension_list:
            new_directory = ext[1:]
            try:
                mkdir(new_directory)
            except FileExistsError:
                pass
            finally:
                move(item, new_directory)


def compress_files(directory, extension):
    """Cuida de compactar arquivos baseado na extensão."""
    chdir(directory)
    archive = 'archive.txz'

    with tarfile.open(archive, 'w:xz') as tar:
        [tar.add(item) for item in glob(f'*{extension}')]


def compress_all_files(directory):
    """Cuida de compactar TODOS os arquivos."""
    chdir(directory)
    archive = 'archive.txz'

    with tarfile.open(archive, 'w:xz') as tar:
        for item in glob('*.*'):
            filename, ext = splitext(item)
            if ext in extension_list:
                tar.add(item)


def delete_files(directory, extension):
    """Cuida de deletar arquivos baseado na extensão."""
    chdir(directory)
    [remove(item) for item in glob(f'*{extension}')]


def delete_all_files(directory):
    """Cuida de deletar TODOS os arquivos."""
    chdir(directory)
    for item in glob('*.*'):
        filename, ext = splitext(item)
        if ext in extension_list:
            remove(item)


# -------------------------------------------------------------------------- #
