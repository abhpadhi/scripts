print('Imported the pre-defined custom module for image-id storing...')

def imageid_store(file_name, lines_to_append):
    with open(file_name, "a+") as file_object:
        file_object.truncate(0)
        appendEOL = False
        file_object.seek(0)
        data= file_object.read(100)
        if len(data) > 0:
            appendEOL = True
        else:
            file_object.seek(0)

        for line in lines_to_append:
            file_object.write(line)
            file_object.write("\n")

    return -1
