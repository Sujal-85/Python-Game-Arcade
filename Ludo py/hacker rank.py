# Enter your code here. Read input from STDIN. Print output to STDOUT
def format_text(category , type_ , text):
    if category == 'S':
        if type_ in ['M' , 'V']:
            if text.endswith ( '()' ):
                text = text[:-2]
            return ''.join ( [' ' + i.lower ( ) if i.isupper ( ) else i for i in text] ).lstrip ( )
        elif type_ == 'C':
            return ''.join ( [' ' + i.lower ( ) if i.isupper ( ) else i for i in text] ).lstrip ( )
    elif category == 'C':
        if type_ == 'M':
            arr = []
            flag = 0
            for i in range(len(text)):
                if text[i] == " ":
                    flag = i
                    arr.append(text[flag+1].upper())

                elif text[flag + 1] and flag > 0:
                    flag = 0
                    continue
                else:
                    arr.append(text[i])
            arr.append("()")
            return "".join(arr)

        elif type_ == 'V':
            num = text.index ( " " )
            return text[0:num] + text[num + 1].upper ( ) + text[num + 2:].replace ( ' ' , '' )
        elif type_ == 'C':
            return ''.join ( [i.capitalize ( ) for i in text.split ( )] )


def process_input(input_text):
    lines = input_text.strip ( ).split ( '\n' )
    output = []
    for line in lines:
        parts = line.split ( ';' )
        if len ( parts ) == 3:
            category , type_ , text = parts
            formatted_text = format_text ( category , type_ , text )
            output.append ( formatted_text )
    return output


def main():
    # Get user input
    input_lines = []
    line = input ( )
    input_lines.append ( line )

    input_text = '\n'.join ( input_lines )

    # Process input
    output = process_input ( input_text )

    for item in output:
        print ( item )


if __name__ == "__main__":
    main ( )