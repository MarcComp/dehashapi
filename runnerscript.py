import subprocess
import re
import sys

from hash_table import get_hash_name

def run_hashcat(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True, check=False)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running hashcat: {e}")
        return None

def run_hashcat_show(hash_text):
    command = f"hashcat --show '{hash_text}'"
    return run_hashcat(command)

def run_hashcat_lookup(hash_text, hash_number):
    command = f"hashcat -a 0 -m {hash_number} '{hash_text}' /usr/share/wordlists/rockyou.txt --potfile-disable"
    return run_hashcat(command)

def extract_numbers_from_output(output):
    numbers = re.findall(r'\b(\d+) \|', output)
    return sorted(map(int, numbers))

def process_output_show(output):
    lines = output.split('\n')
    for line in lines:
        print(f"{line}")

def process_output_run(output, hash_text):
    lines = output.split('\n')
    for line in lines:
        print(f"{line}")
    pattern = re.compile(fr'{hash_text}:\s*(.+)$', re.MULTILINE | re.IGNORECASE)
    matches = pattern.findall(output)

    # If the hashtext is found adjacent to the ':'
    if matches:
        # Found it
        return matches[0]
    else:  
        return False

# def escape_dollar_signs(input_str):
#     return input_str.replace('$', r'\$')


def run_hashcat_operations(hash_text):
    # if not hash_text:
    #     sys.exit("Missing required argument 'hash_text'. Please provide the hash text.")
    

    print(hash_text)

    output_show = run_hashcat_show(hash_text)

    if output_show:
        process_output_show(output_show)
        numbers = extract_numbers_from_output(output_show)
        print(numbers)

        tester = 0
        for number in numbers:
            output_lookup = run_hashcat_lookup(hash_text, number)

            if output_lookup:
                result = process_output_run(output_lookup, hash_text)
                print(result)


                # If found the hash already, do not search anymore
                if result:
                    return {
                        "hash": hash_text,
                        "hashName": get_hash_name(number),
                        "hashResult": result
                    }
                else:
                    hash_name = get_hash_name(number)
                    print(f"{number} --> {hash_name} --> FAIL")
            tester += 1