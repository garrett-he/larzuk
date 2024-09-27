target = 'armor.txt'


def migrate(txt_file):
    for row in txt_file:
        row['minac'] = row['maxac']
