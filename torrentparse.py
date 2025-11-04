import libtorrent, os

Dir      = 'FOLDER PATH'
dirList  = []
file     = '.torrent file path'
fileList = []

info = libtorrent.torrent_info(file) # получаем список файлов из .torrent

for f in info.files():
    torDir = f.path.split('\\')[0]
    #print(torDir)
    break # получаем имя папки загрузки файлов из .torrent

for f in info.files():
    fileList.append(Dir + '\\' + str(f.path)) # список полных путей файлов из .torrent

for root, dirs, files in os.walk(Dir + '\\' + torDir):
    for file in files:
        dirList.append(os.path.join(root, file)) # список полных путей из папки

print(set(dirList) - set(fileList))
