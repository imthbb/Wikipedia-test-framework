import unittest as ut
from configparser import ConfigParser
import wiki_tests

settings_file = 'settings.ini'
cf_sett_f = ConfigParser()
cf_sett_f.read(settings_file)
line = '-----------------------------------------------'


def display_choices(choices: {}, spaces_frmt=1, val_max_len=17) -> str:
    val2_max_len = val_max_len * 2 + spaces_frmt + 6
    ordered_items = ''
    val_column = 0  # value column 0 | value column 1 | value column 2

    for key, val in choices.items():
        val_len = len(val)
        ordered_items += f'''{key:>{spaces_frmt}} — {val}'''
        if val_len < val_max_len + 1 and (val_column == 0 or val_column == 1):
            ordered_items += f'''{' ' * (val_max_len - val_len)} | '''
            val_column += 1
        elif val_column == 0 and val_len < val2_max_len + 1:
            ordered_items += f'''{' ' * (val2_max_len - val_len)} | '''
            val_column += 2
        else:
            ordered_items += f'''\n'''
            val_column = 0
    return ordered_items.rstrip().rstrip('|').rstrip()


def save_choices(choices: {}, file_section: str, file_key: str) -> []:
    global settings_file
    global cf_sett_f
    user_inputs = input(': ').split()
    temp_default_values = ''

    if len(user_inputs) != 0:
        correct_input = False
        for user_input in user_inputs:
            if choices.get(user_input):
                correct_input = True
                temp_default_values += str(user_input) + ' '
        if correct_input:
            cf_sett_f[file_section][file_key] = temp_default_values
    else:
        for i in cf_sett_f[file_section][file_key].split():
            if choices.get(i):
                temp_default_values += i + ' '
        cf_sett_f[file_section][file_key] = temp_default_values

    with open(settings_file, 'w') as file:
        cf_sett_f.write(file)
    return [choices[i] for i in cf_sett_f[file_section][file_key].replace(' ', '')]


def run_tests(test_names: []):
    loaded_tests = []
    for test_name in test_names:
        loaded_tests.append(ut.TestLoader().loadTestsFromName(test_name))
    test_suite = ut.TestSuite(loaded_tests)
    ut.TextTestRunner().run(test_suite)


# Prompt for tests:
class_of_tests = wiki_tests.TestingVarious
name_of_class = str(class_of_tests)[8:-2]  # a string version of the name of the class
test_choices_to_display = {}
actual_test_choices = {}
choice_key = 0
for choice_value in dir(class_of_tests):
    if choice_value.startswith('test'):
        choice_key += 1
        test_choices_to_display[str(choice_key)] = choice_value[5:]
        actual_test_choices[str(choice_key)] = name_of_class + '.' + choice_value

test_choices_to_display.update({'a': 'All', 'Nothing': 'Last used'})
spaces_formatting_lol = len(str(len(test_choices_to_display)))
print(display_choices(test_choices_to_display, spaces_formatting_lol))

actual_test_choices.update({'a': name_of_class, 'A': name_of_class})
tests_to_run = save_choices(actual_test_choices, 'presets', 'tests')

print('\n' + line)


# Prompt for divers:
print('1 - Firefox  | 2 - Chrome   | Nothing - Last used')
driver_to_use = input(': ').strip()
driver_choices = {'1': cf_sett_f['private_data']['firefox_driver'],
                  '2': cf_sett_f['private_data']['chrome_driver']}
if driver_to_use in driver_choices:
    cf_sett_f['presets']['driver'] = driver_choices[driver_to_use]
    with open(settings_file, 'w') as file:
        cf_sett_f.write(file)

print('\n' + line)


# Prompt for url:
print(f'''Enter URL  | Nothing - Last used''')
chosen_url = input(': ').strip()
if chosen_url != '':
    cf_sett_f['presets']['url'] = chosen_url
    with open(settings_file, 'w') as file:
        cf_sett_f.write(file)


run_tests(tests_to_run)









