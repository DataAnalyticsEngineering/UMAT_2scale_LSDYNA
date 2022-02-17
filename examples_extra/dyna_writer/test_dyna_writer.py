input_dictionary = {'*keyword': []}

mat_id = 1

input_dictionary[f'*MAT_elstic ${mat_id}'] = [[mat_id, 1.2, 1.3, 1.4, 1.5, 1], [0]]

input_dictionary['*end'] = []

def write_keyfile(input_dictionary, output_file):
    with open(output_file, 'w') as file:
        for key, val in input_dictionary.items():
            print(key)
            file.write(key + '\n')
            for line in val:
                # if key.startswith('*DEFINE_CURVE'):
                #     print(output_line := ''.join([f'{li:},' for li in line])[:-1])  #TODO better implementation
                #     file.write(output_line + '\n')
                output_line = ''.join([f'{li:},' for li in line])[:-1]
                print(output_line)
                file.write(output_line + '\n')

write_keyfile(input_dictionary, 'some_file.key')
