import sys, os, collections

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
    
def saveThumbnail(skyrimSaveFilePath, skyrimImagePath):
    dimensions = getThumbnailDimensions(skyrimSaveFilePath)
    print(os.path.basename(skyrimImagePath))
    print(f'  -> Thumbnail-Width: {dimensions[0]}')
    print(f'  -> Thumbnail-Height: {dimensions[1]}')
    print()
    
    imageByteSize = 3 * dimensions[0] * dimensions[1]
    imageData = getImageData(skyrimSaveFilePath, dimensions)
    
    with open(skyrimImagePath, 'wb') as image:
        writeImageFileHeader(image, imageByteSize)
        writeImageHeader(image, dimensions)
        image.write(imageData)
    
def getImageData(skyrimSaveFilePath, dimensions):
    imageByteSize = 3 * dimensions[0] * dimensions[1]
    imageDeque = collections.deque([])
    
    with open(skyrimSaveFilePath, 'rb') as save:
        save.seek(13)
        headerSize = int.from_bytes(save.read(4), byteorder='little')
        imageLocation = headerSize + 17
        save.seek(imageLocation)
        
        for row in range(dimensions[1]):
            rowBytes = []
            for column in range(dimensions[0]):
                blue = save.read(1)
                green = save.read(1)
                red = save.read(1)
                rowBytes.append(bytearray(red))
                rowBytes.append(bytearray(green))
                rowBytes.append(bytearray(blue))
            imageDeque.appendleft(bytearray([readValue for barray in rowBytes for readValue in barray]))
    return bytearray([barray for sublist in imageDeque for barray in sublist])
    
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
    absolute_dir = os.path.abspath(directory)
    essFiles = [currFile for currFile in os.listdir(absolute_dir) if os.path.isfile(os.path.join(absolute_dir, currFile)) and currFile.endswith('.ess')]
    
    for essFile in essFiles:
        saveThumbnail(os.path.join(absolute_dir, essFile), os.path.join(absolute_dir, os.path.basename(essFile).replace('.ess', '.bmp')))
    
if __name__ == '__main__':
    arguments = getCommandArguments()
    skyrimSaveFilePath = arguments[0]
    skyrimImagePath = arguments[1]
    validatePaths(skyrimSaveFilePath, skyrimImagePath)
    
    saveThumbnail(skyrimSaveFilePath, skyrimImagePath)  

