import sys, os

def getCommandArguments():
    if len(sys.argv) != 3:
        sys.exit('This module should be executed with the following form:\npython ess2bmp.py savefile.ess thumbnail.bmp')
        
    return (sys.argv[1], sys.argv[2])
    
def validatePaths(skyrimSavePath, skyrimImagePath):
    if not skyrimSavePath.endswith('.ess'):
        sys.exit('Skyrim saves must end with the ".ess" extension.')
    if not skyrimImagePath.endswith('.bmp'):
        sys.exit('The skyrim image file to produce must end with the ".bmp" extension.')
        
def getThumbnailDimensions(skyrimSaveFilePath):
    width = 0
    height = 0
    with open(skyrimSaveFilePath, 'rb') as save:
        save.seek(13)
        headerSize = int.from_bytes(save.read(4), byteorder='little')
        dimensionLocation = headerSize + 9
        save.seek(dimensionLocation)
        width = int.from_bytes(save.read(4), byteorder='little')
        height = int.from_bytes(save.read(4), byteorder='little')
    
    return (width, height)
    
def saveThumbnail(skyrimSaveFilePath, skyrimImagePath, dimensions):
    imageByteSize = 3 * dimensions[0] * dimensions[1]
    imageData = getImageData(skyrimSaveFilePath, imageByteSize)
    
    with open(skyrimImagePath, 'wb') as image:
        writeImageFileHeader(image, imageByteSize)
        writeImageHeader(image, dimensions)
        image.write(imageData)
    
def getImageData(skyrimSaveFilePath, imageByteSize):
    imageData = 0
    with open(skyrimSaveFilePath, 'rb') as save:
        save.seek(13)
        headerSize = int.from_bytes(save.read(4), byteorder='little')
        imageLocation = headerSize + 17
        save.seek(imageLocation)
        imageData = bytearray(save.read(imageByteSize))
        imageData.reverse()
    return imageData
    
def writeImageFileHeader(image, imageByteSize):
    image.write(b'BM')
    image.write((imageByteSize + 54).to_bytes(4, byteorder='little'))
    image.write((0).to_bytes(2, byteorder='little'))
    image.write((0).to_bytes(2, byteorder='little'))
    image.write((40).to_bytes(4, byteorder='little'))
    
def writeImageHeader(image, dimensions):
    image.write((40).to_bytes(4, byteorder='little'))
    image.write((dimensions[0]).to_bytes(4, byteorder='little'))
    image.write((dimensions[1]).to_bytes(4, byteorder='little'))
    image.write((1).to_bytes(2, byteorder='little'))
    image.write((24).to_bytes(2, byteorder='little'))
    image.write((0).to_bytes(4, byteorder='little'))
    image.write((0).to_bytes(4, byteorder='little'))
    image.write((0).to_bytes(4, byteorder='little'))
    image.write((0).to_bytes(4, byteorder='little'))
    image.write((0).to_bytes(4, byteorder='little'))
    image.write((0).to_bytes(4, byteorder='little'))
    
def saveAllThumbnails(directory):
    essFiles = [files for files in os.listdir(directory) if os.path.isfile(os.path.join(directory, files)) and files.name.endswith('.ess')]
    
    for essFile in essFiles:
        dimensions = getDimensions(os.path.abspath(essFile))
        saveThumbnail(os.path.abspath(essFile), os.path.join(directory, os.path.basename(essFile.name).replace('.ess', '.bmp')), dimensions)
    
if __name__ == '__main__':
    arguments = getCommandArguments()
    skyrimSaveFilePath = arguments[0]
    skyrimImagePath = arguments[1]
    validatePaths(skyrimSaveFilePath, skyrimImagePath)
    
    dimensions = getThumbnailDimensions(skyrimSaveFilePath)
    print(f'Thumbnail-Width: {dimensions[0]}')
    print(f'Thumbnail-Height: {dimensions[1]}')
    
    saveThumbnail(skyrimSaveFilePath, skyrimImagePath, dimensions)    

