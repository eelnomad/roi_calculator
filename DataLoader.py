
def savefile(file, result, loading, src):
    original_name = file['filename']
    output_file = open("data/" + original_name, 'wb')
    output_file.write(file['body'])
    output_file.close()
    result[0] = True
    loading[0] = False
    src[0] = "data/" + original_name
