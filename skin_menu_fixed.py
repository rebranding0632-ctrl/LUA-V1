
def add_skin_ids(file_path):
    clear_screen()
    print(f"{Colors.LCYAN}Enter IDs in format: NEW_ID,OLD_ID{Colors.NC}")
    print(f"{Colors.YELLOW}Type 'save' to finish.{Colors.NC}")

    with open(file_path, "a") as f:
        while True:
            user_input = input("ID > ").strip()
            if user_input.lower() == "save":
                break
            if "," in user_input:
                f.write(user_input + "\n")
                print(f"{Colors.LGREEN}Added:{Colors.NC} {user_input}")
            else:
                print(f"{Colors.LRED}Invalid format! Use NEW_ID,OLD_ID{Colors.NC}")


import os
import sys
import time
import re
import subprocess
import shutil
import glob
import time
import sys
import colorsys

def rainbow_print(text: str, speed: float = 0.01):
    """
    Print text with typing rainbow color effect on each line.
    """
    # Reset color at the end
    reset_color = "\033[0m"
    
    for line in text.splitlines():
        for i, char in enumerate(line):
            # Calculate color based on character position
            hue = i / (len(line) + 1)
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            r, g, b = [int(c * 255) for c in rgb]
            
            # Create 24-bit ANSI color code
            color_code = f"\033[38;2;{r};{g};{b}m"
            
            # Print colored character with typing delay
            sys.stdout.write(f"{color_code}{char}")
            sys.stdout.flush()
            time.sleep(speed)
        print(reset_color) # In ký tự xuống dòng và reset màu

def rainbow_prompt(text: str, speed: float = 0.01):
    """
    Display a prompt with typing rainbow color effect,
    without moving to a new line so the user can input data.
    """
    reset_color = "\033[0m"
    
    for i, char in enumerate(text):
        hue = i / (len(text) + 1)
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        r, g, b = [int(c * 255) for c in rgb]
        
        color_code = f"\033[38;2;{r};{g};{b}m"
        
        sys.stdout.write(f"{color_code}{char}")
        sys.stdout.flush()
        time.sleep(speed)
        
    sys.stdout.write(f"{reset_color} ") # Only reset color and add a space without newline
    sys.stdout.flush()

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

class Colors:
    NC = "\033[0m"
    LRED = "\033[1;31m"
    LGREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    PURPLE = "\033[1;35m"
    LCYAN = "\033[1;36m"
    LBLUE = "\033[1;36m"
    WHITE = "\033[1;37m"

# --- HELPER FUNCTIONS ---

def execute_command(command):
    """
    Execute shell command and return output.
    Use errors='replace' to handle binary output.
    """
    full_command = command + " 2>/dev/null"
    try:
        result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8', errors='replace').strip()
    except Exception as e:
        print(f"Error executing command: {command}, {e}")
        return ""


def safe_hex_to_bytes(hex_string):
    """
    Convert hex string safely to bytes.
    """
    hex_string = hex_string.replace(" ", "").replace("\\x", "")
    try:
        return bytes.fromhex(hex_string)
    except Exception:
        return b""


def binary_patch(file_path, offset, hex_data):
    """
    Reliable binary patch writer for repack fixes.
    """
    try:
        data = safe_hex_to_bytes(hex_data)
        with open(file_path, "r+b") as f:
            f.seek(offset)
            f.write(data)
        return True
    except Exception as e:
        print(f"Patch Error: {e}")
        return False


def validate_offsets(offsets):
    """
    Remove invalid/duplicate offsets.
    """
    valid = []
    for off in offsets:
        try:
            off = int(off)
            if off >= 0 and off not in valid:
                valid.append(off)
        except:
            pass
    return valid


# --- PATH CONFIGURATION ---
UNZIPOBB = "/storage/emulated/0/AKMOD_SKIN_OBB/OBB/"
REPACK_DIR = "/storage/emulated/0/AKMOD_SKIN_OBB/OBB/REPACK/"
SKIN_INGAME = REPACK_DIR + "SKIN_INGAME/"
SKIN_LOBBY = REPACK_DIR + "SKIN_LOBBY/"
DEADBOX = REPACK_DIR + "DEADBOX/"
HIT_EFFECT = REPACK_DIR + "HIT_EFFECT/"
TEMP_DIR = "/data/user/0/com.termux/files/home/AKMOD_SKIN_OBB/"

source_file = "/sdcard/AKMOD_SKIN_OBB/SOURCE_FILE/"
source_skin_ingame  = source_file + "SKIN_INGAME/"
source_skin_lobby  = source_file + "SKIN_LOBBY/"
source_accessories = source_file + "GUN_ACCESSORIES/"
source_effect = source_file + "HIT_EFFECT/"
source_deadbox_weapon = source_file + "DEADBOX_WEAPON/"
source_deadbox = source_file + "DEADBOX/"

cache_obb = "/sdcard/AKMOD_SKIN_OBB/CACHE/"
result_obb = "/sdcard/AKMOD_SKIN_OBB/RESULT/"
id_item = "/sdcard/AKMOD_SKIN_OBB/ID_ITEM/"

id_skin_ingame = id_item + "SKIN_INGAME.txt"
id_skin_lobby = id_item + "SKIN_LOBBY.txt"
id_accessories = id_item + "GUN_ACCESSORIES.txt"
id_effect = id_item + "HIT_EFFECT.txt"
id_deadbox_weapon = id_item + "DEADBOX_WEAPON.txt"
id_deadbox = id_item + "DEADBOX.txt"

def create_folder_skin():
    directories = [
        UNZIPOBB, REPACK_DIR, SKIN_INGAME, SKIN_LOBBY, DEADBOX, HIT_EFFECT,cache_obb, result_obb, source_skin_ingame, source_skin_lobby, 
        source_accessories, source_effect, source_deadbox, id_item
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def create_folder_id():
    files = [
        id_skin_ingame, id_skin_lobby, id_accessories, id_effect, id_deadbox
    ]
    for file_path in files:
        if not os.path.exists(file_path):
            open(file_path, 'a').close()

# --- LOGIC FUNCTIONS ---

def find_file_patch(formatted_hex, search_path):
    cmd = f'LANG=C grep -robUaP "{formatted_hex}" "{search_path}" | tr -d \'\\0\''
    search_result = execute_command(cmd)
    
    if not search_result:
        return ""

    lines = search_result.split('\n')
    file_paths = []
    for line in lines:
        colon_pos = line.find(":")
        if colon_pos != -1:
            file_paths.append(line[:colon_pos])

    similar_files = {}
    for fp in file_paths:
        base_name = os.path.basename(fp)
        if base_name in similar_files:
            return similar_files[base_name] + " " + fp
        else:
            similar_files[base_name] = fp

    result = " ".join(file_paths)
    return result

def clean_cache():
    for filename in os.listdir(cache_obb):
        file_path = os.path.join(cache_obb, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception:
            pass

def clean_result():
    if os.path.exists(result_obb):
        for filename in os.listdir(result_obb):
            file_path = os.path.join(result_obb, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                pass

# --- MAIN SKIN INGAME ---
def main_skin_ingame(original_value, expected_value):
    if not str(original_value).isdigit(): return False
    if not str(expected_value).isdigit(): return False

    if not os.path.exists(source_skin_ingame) or not os.listdir(source_skin_ingame):
        print(f"{Colors.LRED}No resources found !{Colors.NC}")
        return False

    # 1. Original Value Logic
    original_hex_value = f"{original_value:08X}"
    original_reversed_hex = execute_command(f'echo "{original_hex_value}" | sed \'s/../& /g\' | awk \'{{for(i=NF;i>0;i--) printf $i; print ""}}\'')
    original_formatted_hex = execute_command(f'echo "{original_reversed_hex}" | sed \'s/../\\\\x&/g\'')

    original_search_result_str = find_file_patch(original_formatted_hex, source_skin_ingame)
    tokens = original_search_result_str.split()
    if not tokens:
        print(f"No results found for SKIN ID: {original_value}")
        return False
    original_found_file = tokens[0]

    cache_file_path = os.path.join(cache_obb, os.path.basename(original_found_file))
    if not os.path.exists(cache_file_path):
        execute_command(f'cp "{original_found_file}" "{cache_obb}"')

    find_offset = execute_command(f'LANG=C grep -robUaP "{original_formatted_hex}" "{cache_obb}" | tr -d \'\\0\'')
    offsets = []
    for line in find_offset.split('\n'):
        if ':' in line:
            try: offsets.append(int(line.split(':')[1]))
            except ValueError: pass

    offsets = validate_offsets(offsets)
    original_first_found_offset = offsets[0] if offsets else 0

    special_hex_0 = execute_command('echo "FFFFFF" | sed \'s/../\\\\x&/g\'')
    lower_bound = original_first_found_offset - 20
    special_match_1 = execute_command(f'LANG=C grep -robUaP "{special_hex_0}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lower_bound}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

    special_hex_6 = execute_command('echo "506C61795F576561706F6E735F5069636B5570" | sed \'s/../\\\\x&/g\'')
    lower_bound_6 = original_first_found_offset - 42
    special_match_7 = execute_command(f'LANG=C grep -robUaP "{special_hex_6}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lower_bound_6}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

    original_two_byte_offset = 0
    if 101001 <= original_value <= 105010:
        special_hex_1 = execute_command('echo "9A000000" | sed \'s/../\\\\x&/g\'')
        lb1 = original_first_found_offset - 120
        special_match_2 = execute_command(f'LANG=C grep -robUaP "{special_hex_1}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb1}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_2 = execute_command('echo "9B000000" | sed \'s/../\\\\x&/g\'')
        lb2 = original_first_found_offset - 120
        special_match_3 = execute_command(f'LANG=C grep -robUaP "{special_hex_2}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb2}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_3 = execute_command('echo "9D000000" | sed \'s/../\\\\x&/g\'')
        lb3 = original_first_found_offset - 120
        special_match_4 = execute_command(f'LANG=C grep -robUaP "{special_hex_3}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb3}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_4 = execute_command('echo "A0000000" | sed \'s/../\\\\x&/g\'')
        lb4 = original_first_found_offset - 120
        special_match_5 = execute_command(f'LANG=C grep -robUaP "{special_hex_4}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb4}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_5 = execute_command('echo "9E000000" | sed \'s/../\\\\x&/g\'')
        lb5 = original_first_found_offset - 120
        special_match_6 = execute_command(f'LANG=C grep -robUaP "{special_hex_5}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb5}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        if special_match_2: original_two_byte_offset = int(special_match_2.split(':')[1]) - 18
        elif special_match_3: original_two_byte_offset = int(special_match_3.split(':')[1]) - 18
        elif special_match_4: original_two_byte_offset = int(special_match_4.split(':')[1]) - 18
        elif special_match_5: original_two_byte_offset = int(special_match_5.split(':')[1]) - 18
        elif special_match_6: original_two_byte_offset = int(special_match_6.split(':')[1]) - 18
        elif special_match_1: original_two_byte_offset = int(special_match_1.split(':')[1]) - 13
        else: original_two_byte_offset = original_first_found_offset - 16
    elif special_match_1:
        original_two_byte_offset = int(special_match_1.split(':')[1]) - 13
    elif special_match_7:
        original_two_byte_offset = int(special_match_7.split(':')[1]) - 16
    else:
        original_two_byte_offset = original_first_found_offset - 16

    # ADD .upper() here
    original_extracted_bytes = execute_command(f'dd if="{original_found_file}" bs=1 skip="{original_two_byte_offset}" count=2 2>/dev/null | xxd -p').upper()

    print(f"{Colors.LRED}OFFSET: {Colors.LBLUE}{original_reversed_hex}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}INDEX: {Colors.LBLUE}{original_extracted_bytes}{Colors.NC}")
    clean_cache()

    # 2. Expected Value Logic
    expected_hex_value = f"{expected_value:08X}"
    expected_reversed_hex = execute_command(f'echo "{expected_hex_value}" | sed \'s/../& /g\' | awk \'{{for(i=NF;i>0;i--) printf $i; print ""}}\'')
    expected_formatted_hex = execute_command(f'echo "{expected_reversed_hex}" | sed \'s/../\\\\x&/g\'')

    expected_search_result_str = find_file_patch(expected_formatted_hex, source_skin_ingame)
    tokens_new = expected_search_result_str.split()
    if not tokens_new:
        print(f"No results found for new SKIN ID: {expected_value}")
        return False
    expected_found_file = tokens_new[0]

    found_file = os.path.join(cache_obb, os.path.basename(expected_found_file))
    result_file_path = os.path.join(result_obb, os.path.basename(expected_found_file))

    if not os.path.exists(found_file):
        execute_command(f'cp "{expected_found_file}" "{cache_obb}"')
    if not os.path.exists(result_file_path):
        execute_command(f'cp "{expected_found_file}" "{result_obb}"')

    find_offset = execute_command(f'LANG=C grep -robUaP "{expected_formatted_hex}" "{cache_obb}" | tr -d \'\\0\'')
    offsets1 = []
    for line in find_offset.split('\n'):
        if ':' in line:
            try: offsets1.append(int(line.split(':')[1]))
            except ValueError: pass
    
    offsets1 = validate_offsets(offsets1)
    expected_first_found_offset = offsets1[0] if offsets1 else 0
    expected_second_found_offset = offsets1[1] if len(offsets1) > 1 else 0

    special_hex_00 = execute_command('echo "FFFFFF" | sed \'s/../\\\\x&/g\'')
    lower_bound_00 = expected_first_found_offset - 50
    special_match_11 = execute_command(f'LANG=C grep -robUaP "{special_hex_00}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lower_bound_00}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

    special_hex_66 = execute_command('echo "506C61795F576561706F6E735F5069636B5570" | sed \'s/../\\\\x&/g\'')
    lower_bound_66 = expected_first_found_offset - 42
    special_match_77 = execute_command(f'LANG=C grep -robUaP "{special_hex_66}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lower_bound_66}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

    two_byte_offset = 0

    if 101001 <= expected_value <= 105010:
        special_hex_11 = execute_command('echo "9A000000" | sed \'s/../\\\\x&/g\'')
        lb11 = expected_first_found_offset - 120
        special_match_22 = execute_command(f'LANG=C grep -robUaP "{special_hex_11}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb11}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_22 = execute_command('echo "9B000000" | sed \'s/../\\\\x&/g\'')
        lb22 = expected_first_found_offset - 120
        special_match_33 = execute_command(f'LANG=C grep -robUaP "{special_hex_22}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb22}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_33 = execute_command('echo "9D000000" | sed \'s/../\\\\x&/g\'')
        lb33 = expected_first_found_offset - 120
        special_match_44 = execute_command(f'LANG=C grep -robUaP "{special_hex_33}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb33}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_44 = execute_command('echo "A0000000" | sed \'s/../\\\\x&/g\'')
        lb44 = expected_first_found_offset - 120
        special_match_55 = execute_command(f'LANG=C grep -robUaP "{special_hex_44}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb44}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        special_hex_55 = execute_command('echo "9E000000" | sed \'s/../\\\\x&/g\'')
        lb55 = expected_first_found_offset - 120
        special_match_66 = execute_command(f'LANG=C grep -robUaP "{special_hex_55}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lb55}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

        if special_match_22: two_byte_offset = int(special_match_22.split(':')[1]) - 18
        elif special_match_33: two_byte_offset = int(special_match_33.split(':')[1]) - 18
        elif special_match_44: two_byte_offset = int(special_match_44.split(':')[1]) - 18
        elif special_match_55: two_byte_offset = int(special_match_55.split(':')[1]) - 18
        elif special_match_66: two_byte_offset = int(special_match_66.split(':')[1]) - 18
        elif special_match_11: two_byte_offset = int(special_match_11.split(':')[1]) - 13
        else: two_byte_offset = expected_first_found_offset - 16
    elif special_match_11:
         two_byte_offset = int(special_match_11.split(':')[1]) - 13
    elif special_match_77:
         two_byte_offset = int(special_match_77.split(':')[1]) - 16
    else:
        two_byte_offset = expected_first_found_offset - 16

    # ADD .upper() here
    expected_extracted_bytes = execute_command(f'dd if="{expected_found_file}" bs=1 skip="{two_byte_offset}" count=2 2>/dev/null | xxd -p').upper()
    
    print(f"{Colors.LRED}OFFSET: {Colors.YELLOW}{expected_reversed_hex}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}INDEX: {Colors.YELLOW}{expected_extracted_bytes}{Colors.NC}")

    # --- PATCHING (FIXED WITH xxd -r -p) ---
    byte1 = original_extracted_bytes[0:2]
    byte2 = original_extracted_bytes[2:4] if len(original_extracted_bytes) >= 4 else "00"
    
    # FIX: Use xxd -r -p to convert hex string to binary, avoiding echo -e / sed issues
    binary_patch(result_file_path, two_byte_offset, f"{byte1}{byte2}")

    # FIX: original_reversed_hex has spaces, xxd handles them automatically
    binary_patch(result_file_path, expected_second_found_offset, original_reversed_hex)

    print(f"{Colors.LGREEN}CHANGED INDEX {Colors.LBLUE}{original_extracted_bytes}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{expected_extracted_bytes}{Colors.NC}")
    print(f"{Colors.LGREEN}CHANGED OFFSET {Colors.LBLUE}{original_reversed_hex}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{expected_reversed_hex}{Colors.NC}")
    print(f"{Colors.LRED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")

    clean_cache()
    return True

# --- MAIN SKIN LOBBY ---
def main_skin_lobby(original_value, expected_value):
    if not str(original_value).isdigit(): return False
    if not str(expected_value).isdigit(): return False

    if not os.path.exists(source_skin_lobby) or not os.listdir(source_skin_lobby):
        print(f"{Colors.LRED}No resources found !{Colors.NC}")
        return False

    original_hex_value = f"{original_value:08X}"
    original_reversed_hex = execute_command(f'echo "{original_hex_value}" | sed \'s/../& /g\' | awk \'{{for(i=NF;i>0;i--) printf $i; print ""}}\'')
    original_formatted_hex = execute_command(f'echo "{original_reversed_hex}" | sed \'s/../\\\\x&/g\'')

    original_search_result_str = find_file_patch(original_formatted_hex, source_skin_lobby)
    tokens = original_search_result_str.split()
    if not tokens:
        print(f"No results found for SKIN ID: {original_value}")
        return False
    original_found_file = tokens[0]

    cache_file_path = os.path.join(cache_obb, os.path.basename(original_found_file))
    if not os.path.exists(cache_file_path):
        execute_command(f'cp "{original_found_file}" "{cache_obb}"')

    find_offset = execute_command(f'LANG=C grep -robUaP "{original_formatted_hex}" "{cache_obb}" | tr -d \'\\0\'')
    offsets = []
    for line in find_offset.split('\n'):
        if ':' in line:
            try: offsets.append(int(line.split(':')[1]))
            except ValueError: pass
    offsets = validate_offsets(offsets)
    original_first_found_offset = offsets[0] if offsets else 0

    special_hex_0 = execute_command('echo "FFFFFF" | sed \'s/../\\\\x&/g\'')
    lower_bound = original_first_found_offset - 50
    special_match_1 = execute_command(f'LANG=C grep -robUaP "{special_hex_0}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{lower_bound}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    
    # ... (keep original offset check logic) ...
    special_match_2 = execute_command(f'LANG=C grep -robUaP "$(echo "0100000000000000" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{original_first_found_offset-50}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_4 = execute_command(f'LANG=C grep -robUaP "$(echo "00000000000006" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{original_first_found_offset-20}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_5 = execute_command(f'LANG=C grep -robUaP "$(echo "9F860100" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{original_first_found_offset-100}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_6 = execute_command(f'LANG=C grep -robUaP "$(echo "0000000000000000000064" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{original_first_found_offset-20}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_7 = execute_command(f'LANG=C grep -robUaP "$(echo "05000000" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{original_first_found_offset-20}" -v upper="{original_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

    original_two_byte_offset = 0
    if special_match_1: original_two_byte_offset = int(special_match_1.split(':')[1]) - 13
    elif special_match_2: original_two_byte_offset = int(special_match_2.split(':')[1]) + 8
    elif special_match_4: original_two_byte_offset = int(special_match_4.split(':')[1]) - 2
    elif special_match_5: original_two_byte_offset = int(special_match_5.split(':')[1]) - 13
    elif special_match_6: original_two_byte_offset = int(special_match_6.split(':')[1]) - 2
    elif special_match_7: original_two_byte_offset = original_first_found_offset - 21
    else: original_two_byte_offset = original_first_found_offset - 22

    # ADD .upper() here
    original_extracted_bytes = execute_command(f'dd if="{original_found_file}" bs=1 skip="{original_two_byte_offset}" count=2 2>/dev/null | xxd -p').upper()
    print(f"{Colors.LRED}OFFSET: {Colors.LBLUE}{original_reversed_hex}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}INDEX: {Colors.LBLUE}{original_extracted_bytes}{Colors.NC}")
    clean_cache()

    # Expected Value
    expected_hex_value = f"{expected_value:08X}"
    expected_reversed_hex = execute_command(f'echo "{expected_hex_value}" | sed \'s/../& /g\' | awk \'{{for(i=NF;i>0;i--) printf $i; print ""}}\'')
    expected_formatted_hex = execute_command(f'echo "{expected_reversed_hex}" | sed \'s/../\\\\x&/g\'')

    expected_search_result_str = find_file_patch(expected_formatted_hex, source_skin_lobby)
    tokens_new = expected_search_result_str.split()
    if not tokens_new:
        print(f"No results found for new SKIN ID: {expected_value}")
        return False
    expected_found_file = tokens_new[0]

    found_file = os.path.join(cache_obb, os.path.basename(expected_found_file))
    result_file_path = os.path.join(result_obb, os.path.basename(expected_found_file))

    if not os.path.exists(found_file): execute_command(f'cp "{expected_found_file}" "{cache_obb}"')
    if not os.path.exists(result_file_path): execute_command(f'cp "{expected_found_file}" "{result_obb}"')

    find_offset = execute_command(f'LANG=C grep -robUaP "{expected_formatted_hex}" "{cache_obb}" | tr -d \'\\0\'')
    offsets1 = []
    for line in find_offset.split('\n'):
        if ':' in line:
            try: offsets1.append(int(line.split(':')[1]))
            except ValueError: pass
    offsets1 = validate_offsets(offsets1)
    expected_first_found_offset = offsets1[0] if offsets1 else 0
    expected_second_found_offset = offsets1[1] if len(offsets1) > 1 else 0

    special_match_11 = execute_command(f'LANG=C grep -robUaP "{special_hex_0}" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{expected_first_found_offset-50}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_22 = execute_command(f'LANG=C grep -robUaP "$(echo "0100000000000000" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{expected_first_found_offset-50}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_44 = execute_command(f'LANG=C grep -robUaP "$(echo "00000000000006" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{expected_first_found_offset-20}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_55 = execute_command(f'LANG=C grep -robUaP "$(echo "9F860100" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{expected_first_found_offset-100}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_66 = execute_command(f'LANG=C grep -robUaP "$(echo "0000000000000000000064" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{expected_first_found_offset-20}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')
    special_match_77 = execute_command(f'LANG=C grep -robUaP "$(echo "05000000" | sed \'s/../\\\\x&/g\')" "{cache_obb}" | tr -d \'\\0\' | awk -v lower="{expected_first_found_offset-20}" -v upper="{expected_first_found_offset}" -F: \'$2 >= lower && $2 <= upper\' | tail -n 1')

    two_byte_offset = 0
    if special_match_11: two_byte_offset = int(special_match_11.split(':')[1]) - 13
    elif special_match_22: two_byte_offset = int(special_match_22.split(':')[1]) + 8
    elif special_match_44: two_byte_offset = int(special_match_44.split(':')[1]) - 2
    elif special_match_55: two_byte_offset = int(special_match_55.split(':')[1]) - 13
    elif special_match_66: two_byte_offset = int(special_match_66.split(':')[1]) - 2
    elif special_match_77: two_byte_offset = expected_first_found_offset - 21
    else: two_byte_offset = expected_first_found_offset - 22

    # ADD .upper() here
    expected_extracted_bytes = execute_command(f'dd if="{expected_found_file}" bs=1 skip="{two_byte_offset}" count=2 2>/dev/null | xxd -p').upper()
    print(f"{Colors.LRED}OFFSET: {Colors.YELLOW}{expected_reversed_hex}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}INDEX: {Colors.YELLOW}{expected_extracted_bytes}{Colors.NC}")

    byte1 = original_extracted_bytes[0:2]
    byte2 = original_extracted_bytes[2:4] if len(original_extracted_bytes) >= 4 else "00"

    # FIX: Use xxd -r -p
    binary_patch(result_file_path, two_byte_offset, f"{byte1}{byte2}")

    # FIX: Use xxd -r -p
    change_offset_command = f'echo "{original_reversed_hex}" | xxd -r -p | dd of="{result_file_path}" bs=1 seek="{expected_second_found_offset}" count=4 conv=notrunc 2>/dev/null'
    execute_command(change_offset_command)

    print(f"{Colors.LGREEN}CHANGED INDEX {Colors.LBLUE}{original_extracted_bytes}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{expected_extracted_bytes}{Colors.NC}")
    print(f"{Colors.LGREEN}CHANGED OFFSET {Colors.LBLUE}{original_reversed_hex}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{expected_reversed_hex}{Colors.NC}")
    print(f"{Colors.LRED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")
    clean_cache()
    return True

# --- GENERIC FUNCTION FIXES ---

def main_skin_accessories(decimal_value, new_decimal_value):
    hex_value = f"{decimal_value:08X}"
    reversed_hex_list = [hex_value[i:i+2] for i in range(len(hex_value)-2, -1, -2)]
    formatted_hex = "".join([f"\\x{b}" for b in reversed_hex_list])

    if not os.path.exists(source_accessories) or not os.listdir(source_accessories):
        print(f"{Colors.LRED}No source file found!{Colors.NC}")
        sys.exit(1)

    search_result = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{source_accessories}" | tr -d \'\\0\' | head -n 1')
    if not search_result:
        print(f"No results found for SKIN ID: {decimal_value}")
        return False

    file_path = search_result.split(':')[0]
    user_hex_offset = int("".join(filter(str.isdigit, search_result.split(':')[1])))

    cache_file = os.path.join(cache_obb, os.path.basename(file_path))
    result_file = os.path.join(result_obb, os.path.basename(file_path))

    execute_command(f'cp "{file_path}" "{cache_obb}"')
    if not os.path.exists(result_file):
        execute_command(f'cp "{file_path}" "{result_obb}"')

    last_match = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{user_hex_offset}" -F: \'$2 <= max_offset\' | tail -n 1')
    
    new_offset = 0
    if last_match:
        last_offset = int("".join(filter(str.isdigit, last_match.split(':')[1])))
        new_offset = last_offset - 16
        # ADD .upper() here
        extracted_bytes = execute_command(f'dd if="{file_path}" bs=1 skip="{new_offset}" count=2 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}OFFSET: {Colors.NC}{Colors.LBLUE}{hex_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}INDEX: {Colors.NC}{Colors.LBLUE}{extracted_bytes}{Colors.NC}")

    clean_cache()

    # New Value
    new_hex_value = f"{new_decimal_value:08X}"
    new_reversed_hex_list = [new_hex_value[i:i+2] for i in range(len(new_hex_value)-2, -1, -2)]
    new_formatted_hex = "".join([f"\\x{b}" for b in new_reversed_hex_list])

    new_search_result = execute_command(f'LANG=C grep -robUaP "{new_formatted_hex}" "{source_accessories}" | tr -d \'\\0\' | head -n 1')
    if not new_search_result:
        print(f"No results found for new SKIN ID: {new_decimal_value}")
        return False
    
    new_file_path = new_search_result.split(':')[0]
    new_user_hex_offset = int("".join(filter(str.isdigit, new_search_result.split(':')[1])))

    new_pattern_hex = "\\x00\\x00\\x00\\x00\\x00\\x00\\x01\\x00"
    execute_command(f'cp "{new_file_path}" "{cache_obb}"')
    
    new_last_match = execute_command(f'LANG=C grep -robUaP "{new_pattern_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{new_user_hex_offset}" -F: \'$2 <= max_offset\' | tail -n 1')
    
    if new_last_match:
        new_last_offset = int("".join(filter(str.isdigit, new_last_match.split(':')[1])))
        new_new_offset = new_last_offset - 2
        # ADD .upper() here
        new_extracted_bytes = execute_command(f'dd if="{new_file_path}" bs=1 skip="{new_new_offset}" count=2 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}OFFSET: {Colors.NC}{Colors.YELLOW}{new_hex_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}INDEX: {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")
        
        # FIX: Replace shell sed hex construction with xxd -r -p
        cmd_final = f'echo "{new_extracted_bytes}" | xxd -r -p | dd of="{result_file}" bs=1 seek="{new_offset}" conv=notrunc 2>/dev/null'
        execute_command(cmd_final)

        print(f"{Colors.LGREEN}CHANGED INDEX {Colors.LBLUE}{hex_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")
        print(f"{Colors.LRED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")
        clean_cache()
        return True
    
    clean_cache()
    return False

def main_hit_effect(decimal_value, new_decimal_value):
    hex_value = f"{decimal_value:08X}"
    reversed_hex_list = [hex_value[i:i+2] for i in range(len(hex_value)-2, -1, -2)]
    formatted_hex = "".join([f"\\x{b}" for b in reversed_hex_list])

    if not os.path.exists(source_effect) or not os.listdir(source_effect):
        print(f"{Colors.LRED}No source file found!{Colors.NC}")
        sys.exit(1)

    search_result = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{source_effect}" | tr -d \'\\0\' | head -n 1')
    if not search_result:
        print(f"No results found for SKIN ID: {decimal_value}")
        return False
    
    file_path = search_result.split(':')[0]
    user_hex_offset = int("".join(filter(str.isdigit, search_result.split(':')[1])))

    result_file = os.path.join(result_obb, os.path.basename(file_path))
    execute_command(f'cp "{file_path}" "{cache_obb}"')
    if not os.path.exists(result_file):
        execute_command(f'cp "{file_path}" "{result_obb}"')

    last_match = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{user_hex_offset}" -F: \'$2 <= max_offset\' | tail -n 1')
    
    new_offset = 0
    if last_match:
        last_offset = int("".join(filter(str.isdigit, last_match.split(':')[1])))
        new_offset = last_offset
        # ADD .upper() here
        extracted_bytes = execute_command(f'dd if="{file_path}" bs=1 skip="{new_offset}" count=4 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}ID SKIN{Colors.NC} {Colors.LBLUE}{decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}OFFSET {Colors.NC}{Colors.LBLUE}{extracted_bytes}{Colors.NC}")
    
    clean_cache()

    new_hex_value = f"{new_decimal_value:08X}"
    new_reversed_hex_list = [new_hex_value[i:i+2] for i in range(len(new_hex_value)-2, -1, -2)]
    new_formatted_hex = "".join([f"\\x{b}" for b in new_reversed_hex_list])

    new_search_result = execute_command(f'LANG=C grep -robUaP "{new_formatted_hex}" "{source_effect}" | tr -d \'\\0\' | head -n 1')
    if not new_search_result:
        print(f"No results found for new SKIN ID: {new_decimal_value}")
        return False
    
    new_file_path = new_search_result.split(':')[0]
    new_user_hex_offset = int("".join(filter(str.isdigit, new_search_result.split(':')[1])))

    execute_command(f'cp "{new_file_path}" "{cache_obb}"')
    new_last_match = execute_command(f'LANG=C grep -robUaP "{new_formatted_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{new_user_hex_offset}" -F: \'$2 <= max_offset\' | tail -n 1')

    if new_last_match:
        new_last_offset = int("".join(filter(str.isdigit, new_last_match.split(':')[1])))
        new_new_offset = new_last_offset
        # ADD .upper() here
        new_extracted_bytes = execute_command(f'dd if="{new_file_path}" bs=1 skip="{new_new_offset}" count=4 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}ID SKIN{Colors.NC} {Colors.YELLOW}{new_decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}OFFSET {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")

        # FIX: Use xxd -r -p
        cmd_final = f'echo "{new_extracted_bytes}" | xxd -r -p | dd of="{result_file}" bs=1 seek="{new_offset}" conv=notrunc 2>/dev/null'
        execute_command(cmd_final)
        
        print(f"{Colors.LGREEN}CHANGED OFFSET {Colors.LBLUE}{decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")
        print(f"{Colors.LRED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")
        clean_cache()
        return True
    
    clean_cache()
    return False

def main_deadbox_weapon(decimal_value, new_decimal_value):
    hex_value = f"{decimal_value:08X}"
    reversed_hex_list = [hex_value[i:i+2] for i in range(len(hex_value)-2, -1, -2)]
    formatted_hex = "".join([f"\\x{b}" for b in reversed_hex_list])

    if not os.path.exists(source_deadbox_weapon) or not os.listdir(source_deadbox_weapon):
        print(f"{Colors.LRED}No source file found!{Colors.NC}")
        sys.exit(1)

    search_result = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{source_deadbox_weapon}" | tr -d \'\\0\' | head -n 1')
    if not search_result:
        print(f"No results found for SKIN ID: {decimal_value}")
        return False
    
    file_path = search_result.split(':')[0]
    user_hex_offset = int("".join(filter(str.isdigit, search_result.split(':')[1])))
    result_file = os.path.join(result_obb, os.path.basename(file_path))

    execute_command(f'cp "{file_path}" "{cache_obb}"')
    if not os.path.exists(result_file):
        execute_command(f'cp "{file_path}" "{result_obb}"')

    last_match = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{user_hex_offset}" -F: \'$2 <= max_offset\' | head -n 1')

    new_offset = 0
    if last_match:
        last_offset = int("".join(filter(str.isdigit, last_match.split(':')[1])))
        new_offset = last_offset - 5
        # ADD .upper() here
        extracted_bytes = execute_command(f'dd if="{file_path}" bs=1 skip="{new_offset}" count=9 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}ID SKIN{Colors.NC} {Colors.LBLUE}{decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}OFFSET {Colors.NC}{Colors.LBLUE}{extracted_bytes}{Colors.NC}")
    
    clean_cache()

    new_hex_value = f"{new_decimal_value:08X}"
    new_reversed_hex_list = [new_hex_value[i:i+2] for i in range(len(new_hex_value)-2, -1, -2)]
    new_formatted_hex = "".join([f"\\x{b}" for b in new_reversed_hex_list])

    new_search_result = execute_command(f'LANG=C grep -robUaP "{new_formatted_hex}" "{source_deadbox_weapon}" | tr -d \'\\0\' | head -n 1')
    if not new_search_result:
        print(f"No results found for new SKIN ID: {new_decimal_value}")
        return False
    
    new_file_path = new_search_result.split(':')[0]
    new_user_hex_offset = int("".join(filter(str.isdigit, new_search_result.split(':')[1])))

    execute_command(f'cp "{new_file_path}" "{cache_obb}"')
    new_last_match = execute_command(f'LANG=C grep -robUaP "{new_formatted_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{new_user_hex_offset}" -F: \'$2 <= max_offset\' | tail -n 1')

    if new_last_match:
        new_last_offset = int("".join(filter(str.isdigit, new_last_match.split(':')[1])))
        new_new_offset = new_last_offset - 5
        # ADD .upper() here
        new_extracted_bytes = execute_command(f'dd if="{new_file_path}" bs=1 skip="{new_new_offset}" count=9 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}ID SKIN{Colors.NC} {Colors.YELLOW}{new_decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}OFFSET {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")

        # FIX: Use xxd -r -p
        cmd_final = f'echo "{new_extracted_bytes}" | xxd -r -p | dd of="{result_file}" bs=1 seek="{new_offset}" conv=notrunc 2>/dev/null'
        execute_command(cmd_final)
        
        print(f"{Colors.LGREEN}CHANGED OFFSET {Colors.LBLUE}{decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")
        print(f"{Colors.LRED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")
        clean_cache()
        return True
    
    clean_cache()
    return False

def main_skin_deadbox(decimal_value, new_decimal_value):
    hex_value = f"{decimal_value:08X}"
    reversed_hex_list = [hex_value[i:i+2] for i in range(len(hex_value)-2, -1, -2)]
    formatted_hex = "".join([f"\\x{b}" for b in reversed_hex_list])

    if not os.path.exists(source_deadbox) or not os.listdir(source_deadbox):
        print(f"{Colors.LRED}No source file found!{Colors.NC}")
        sys.exit(1)

    search_result = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{source_deadbox}" | tr -d \'\\0\' | head -n 1')
    if not search_result:
        print(f"No results found for SKIN ID: {decimal_value}")
        return False
    
    file_path = search_result.split(':')[0]
    user_hex_offset = int("".join(filter(str.isdigit, search_result.split(':')[1])))
    result_file = os.path.join(result_obb, os.path.basename(file_path))

    execute_command(f'cp "{file_path}" "{cache_obb}"')
    if not os.path.exists(result_file):
        execute_command(f'cp "{file_path}" "{result_obb}"')

    last_match = execute_command(f'LANG=C grep -robUaP "{formatted_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{user_hex_offset}" -F: \'$2 <= max_offset\' | tail -n 1')
    
    new_offset = 0
    if last_match:
        last_offset = int("".join(filter(str.isdigit, last_match.split(':')[1])))
        new_offset = last_offset
        # ADD .upper() here
        extracted_bytes = execute_command(f'dd if="{file_path}" bs=1 skip="{new_offset}" count=4 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}ID SKIN{Colors.NC} {Colors.LBLUE}{decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}OFFSET {Colors.NC}{Colors.LBLUE}{extracted_bytes}{Colors.NC}")
    
    clean_cache()

    new_hex_value = f"{new_decimal_value:08X}"
    new_reversed_hex_list = [new_hex_value[i:i+2] for i in range(len(new_hex_value)-2, -1, -2)]
    new_formatted_hex = "".join([f"\\x{b}" for b in new_reversed_hex_list])

    new_search_result = execute_command(f'LANG=C grep -robUaP "{new_formatted_hex}" "{source_deadbox}" | tr -d \'\\0\' | head -n 1')
    if not new_search_result:
        print(f"No results found for new SKIN ID: {new_decimal_value}")
        return False
    
    new_file_path = new_search_result.split(':')[0]
    new_user_hex_offset = int("".join(filter(str.isdigit, new_search_result.split(':')[1])))

    execute_command(f'cp "{new_file_path}" "{cache_obb}"')
    new_last_match = execute_command(f'LANG=C grep -robUaP "{new_formatted_hex}" "{cache_obb}" | tr -d \'\\0\' | awk -v max_offset="{new_user_hex_offset}" -F: \'$2 <= max_offset\' | tail -n 1')

    if new_last_match:
        new_last_offset = int("".join(filter(str.isdigit, new_last_match.split(':')[1])))
        new_new_offset = new_last_offset
        # ADD .upper() here
        new_extracted_bytes = execute_command(f'dd if="{new_file_path}" bs=1 skip="{new_new_offset}" count=4 2>/dev/null | xxd -p').upper()
        print(f"{Colors.LRED}ID SKIN{Colors.NC} {Colors.YELLOW}{new_decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.LRED}OFFSET {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")

        # FIX: Use xxd -r -p
        cmd_final = f'echo "{new_extracted_bytes}" | xxd -r -p | dd of="{result_file}" bs=1 seek="{new_offset}" conv=notrunc 2>/dev/null'
        execute_command(cmd_final)
        
        print(f"{Colors.LGREEN}CHANGED OFFSET {Colors.LBLUE}{decimal_value}{Colors.NC}{Colors.LGREEN} ≫ {Colors.NC}{Colors.YELLOW}{new_extracted_bytes}{Colors.NC}")
        print(f"{Colors.LRED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}")
        clean_cache()
        return True

    clean_cache()
    return False

# --- RUN MENU FUNCTIONS (UNCHANGED) ---

def run_skin_ingame():
    os.system("toilet \"   STARTING MOD SKIN INGAME  \" -f term -F border --gay  | pv -qL 3000")
    clean_result()

    if not os.path.exists(id_skin_ingame) or os.stat(id_skin_ingame).st_size == 0:
        print(f"{Colors.LRED}File SKIN_INGAME.txt has no data! Please enter skin code{Colors.NC}")
        return

    total_count = 0
    success_count = 0
    failure_count = 0

    with open(id_skin_ingame, 'r') as f:
        for line in f:
            line = re.sub(r'[\[\]\r\n\s]', '', line)
            if not line: continue
            total_count += 1
            parts = line.split(',')
            if len(parts) >= 2:
                try:
                    expected = int(parts[0])
                    original = int(parts[1])
                    result = main_skin_ingame(original, expected)
                    if result is True:
                        success_count += 1
                    else:
                        failure_count += 1
                except ValueError:
                    print(f"{Colors.LRED}Error: Invalid value{Colors.NC}")
                    failure_count += 1
    
    time.sleep(2)
    print(f"{Colors.YELLOW}MOD SKIN INGAME SUCCESSFUL!{Colors.NC}")
    print(f"{Colors.LGREEN}Total ID: {total_count}{Colors.NC}")
    print(f"{Colors.LGREEN}Success ID: {success_count}{Colors.NC}")
    print(f"{Colors.LRED}Failed ID: {failure_count}{Colors.NC}\n")
    input(f"\n{Colors.YELLOW}Press Enter to return to Menu...{Colors.NC}")
    return

def run_skin_lobby():
    os.system("toilet \"   STARTING MOD SKIN LOBBY  \" -f term -F border --gay  | pv -qL 3000")
    clean_result()

    if not os.path.exists(id_skin_lobby) or os.stat(id_skin_lobby).st_size == 0:
        print(f"{Colors.LRED}File SKIN_LOBBY.txt has no data! Please enter skin code{Colors.NC}")
        return

    total_count = 0
    success_count = 0
    failure_count = 0

    with open(id_skin_lobby, 'r') as f:
        for line in f:
            line = re.sub(r'[\[\]\r\n\s]', '', line)
            if not line: continue
            total_count += 1
            parts = line.split(',')
            if len(parts) >= 2:
                try:
                    expected = int(parts[0])
                    original = int(parts[1])
                    result = main_skin_lobby(original, expected)
                    if result is True:
                        success_count += 1
                    else:
                        failure_count += 1
                except ValueError:
                    print(f"{Colors.LRED}Error: Invalid value{Colors.NC}")
                    failure_count += 1
    
    time.sleep(2)
    print(f"{Colors.YELLOW}MOD SKIN LOBBY SUCCESSFUL!{Colors.NC}")
    print(f"{Colors.LGREEN}Total ID: {total_count}{Colors.NC}")
    print(f"{Colors.LGREEN}Success ID: {success_count}{Colors.NC}")
    print(f"{Colors.LRED}Failed ID: {failure_count}{Colors.NC}\n")
    input(f"\n{Colors.YELLOW}Press Enter to return to Menu...{Colors.NC}")
    return

def run_skin_accessories():
    os.system("toilet \"   STARTING MOD ACCESSORIES  \" -f term -F border --gay  | pv -qL 3000")
    clean_result()

    if not os.path.exists(id_accessories) or os.stat(id_accessories).st_size == 0:
        print(f"{Colors.LRED}File ACCESSORIES.txt has no data! Please enter skin code{Colors.NC}")
        return

    total_count = 0
    success_count = 0
    failure_count = 0

    with open(id_accessories, 'r') as f:
        for line in f:
            line = re.sub(r'[\[\]\r\n\s]', '', line)
            if not line: continue
            total_count += 1
            parts = line.split(',')
            if len(parts) >= 2:
                try:
                    val = int(parts[0])
                    new_val = int(parts[1])
                    if main_skin_accessories(val, new_val):
                        success_count += 1
                    else:
                        failure_count += 1
                except ValueError:
                    print(f"{Colors.LRED}Invalid input in ACCESSORIES.txt{Colors.NC}")
                    failure_count += 1
    
    time.sleep(1)
    print(f"{Colors.YELLOW}MOD ACCESSORIES SUCCESSFUL!{Colors.NC}")
    print(f"{Colors.LGREEN}Total ID: {total_count}{Colors.NC}")
    print(f"{Colors.LGREEN}Success ID: {success_count}{Colors.NC}")
    print(f"{Colors.LRED}Failed ID: {failure_count}{Colors.NC}\n")
    input(f"\n{Colors.YELLOW}Press Enter to return to Menu...{Colors.NC}")
    return

def run_skin_hit_effect():
    os.system("toilet \"   STARTING MOD HIT EFFECT  \" -f term -F border --gay  | pv -qL 3000")
    clean_result()

    if not os.path.exists(id_effect) or os.stat(id_effect).st_size == 0:
        print(f"{Colors.LRED}File HIT_EFFECT.txt has no data! Please enter skin code{Colors.NC}")
        return

    total_count = 0
    success_count = 0
    failure_count = 0

    with open(id_effect, 'r') as f:
        for line in f:
            line = re.sub(r'[\[\]\r\n\s]', '', line)
            if not line: continue
            total_count += 1
            parts = line.split(',')
            if len(parts) >= 2:
                try:
                    val = int(parts[0])
                    new_val = int(parts[1])
                    if main_hit_effect(val, new_val):
                        success_count += 1
                    else:
                        failure_count += 1
                except ValueError:
                    print(f"{Colors.LRED}Invalid input in HIT_EFFECT.txt{Colors.NC}")
                    failure_count += 1

    time.sleep(1)
    print(f"{Colors.YELLOW}MOD HIT EFFECT SUCCESSFUL!{Colors.NC}")
    print(f"{Colors.LGREEN}Total ID: {total_count}{Colors.NC}")
    print(f"{Colors.LGREEN}Success ID: {success_count}{Colors.NC}")
    print(f"{Colors.LRED}Failed ID: {failure_count}{Colors.NC}\n")
    input(f"\n{Colors.YELLOW}Press Enter to return to Menu...{Colors.NC}")
    return

def run_skin_deadbox_weapon():
    os.system("toilet \"  STARTING MOD DEADBOX WEAPON \" -f term -F border --gay  | pv -qL 3000")
    clean_result()

    if not os.path.exists(id_deadbox_weapon) or os.stat(id_deadbox_weapon).st_size == 0:
        print(f"{Colors.LRED}File DEADBOX_WEAPON.txt has no data! Please enter skin code{Colors.NC}")
        return

    total_count = 0
    success_count = 0
    failure_count = 0

    with open(id_deadbox_weapon, 'r') as f:
        for line in f:
            line = re.sub(r'[\[\]\r\n\s]', '', line)
            if not line: continue
            total_count += 1
            parts = line.split(',')
            if len(parts) >= 2:
                try:
                    val = int(parts[0])
                    new_val = int(parts[1])
                    if main_deadbox_weapon(val, new_val):
                        success_count += 1
                    else:
                        failure_count += 1
                except ValueError:
                    print(f"{Colors.LRED}Invalid input in DEADBOX_WEAPON.txt{Colors.NC}")
                    failure_count += 1

    time.sleep(1)
    print(f"{Colors.YELLOW}MOD WEAPON DEADBOX SUCCESSFUL!{Colors.NC}")
    print(f"{Colors.LGREEN}Total ID: {total_count}{Colors.NC}")
    print(f"{Colors.LGREEN}Success ID: {success_count}{Colors.NC}")
    print(f"{Colors.LRED}Failed ID: {failure_count}{Colors.NC}\n")
    input(f"\n{Colors.YELLOW}Press Enter to return to Menu...{Colors.NC}")
    return

def run_skin_deadbox():
    os.system("toilet \"   STARTING MOD DEADBOX  \" -f term -F border --gay  | pv -qL 3000")
    clean_result()

    if not os.path.exists(id_deadbox) or os.stat(id_deadbox).st_size == 0:
        print(f"{Colors.LRED}File DEADBOX.txt has no data! Please enter skin code{Colors.NC}")
        return

    total_count = 0
    success_count = 0
    failure_count = 0

    with open(id_deadbox, 'r') as f:
        for line in f:
            line = re.sub(r'[\[\]\r\n\s]', '', line)
            if not line: continue
            total_count += 1
            parts = line.split(',')
            if len(parts) >= 2:
                try:
                    val = int(parts[0])
                    new_val = int(parts[1])
                    if main_skin_deadbox(val, new_val):
                        success_count += 1
                    else:
                        failure_count += 1
                except ValueError:
                    print(f"{Colors.LRED}Invalid input in DEADBOX.txt{Colors.NC}")
                    failure_count += 1

    time.sleep(1)
    print(f"{Colors.YELLOW}MOD DEADBOX SUCCESSFUL!{Colors.NC}")
    print(f"{Colors.LGREEN}Total ID: {total_count}{Colors.NC}")
    print(f"{Colors.LGREEN}Success ID: {success_count}{Colors.NC}")
    print(f"{Colors.LRED}Failed ID: {failure_count}{Colors.NC}\n")
    input(f"\n{Colors.YELLOW}Press Enter to return to Menu...{Colors.NC}")
    return


# MAIN FUNCTION REPACK

import os
import subprocess
import ssl
import urllib.request
import datetime
import itertools as it
import math
import struct
import zlib
import socket
from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePath, Path
import shutil
import getpass
import base64
import glob
from typing import List
import gmalg
from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_CBC
from Crypto.Hash import SHA1
from Crypto.Util.Padding import pad, unpad

# MAIN TOOL
try:
    from gmalg.base import BlockCipher
    from gmalg.errors import IncorrectLengthError
    from gmalg.utils import ROL32
except ImportError:
    # Provide fallback classes/functions if gmalg is not installed or has a different structure
    print("Cảnh báo: Library not found 'gmalg'. Sử dụng các định nghĩa giữ chỗ.")
    class BlockCipher:
        pass
    class IncorrectLengthError(Exception):
        def __init__(self, name, expected, actual):
            super().__init__(f"Incorrect length for {name}: expected {expected}, got {actual}")
    def ROL32(x, n):
        return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))
        
from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict, DICT_TYPE_AUTO

ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')

RSA_MOD_1 = bytes.fromhex(
    'CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex(
    '7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')

SIMPLE1_DECRYPT_KEY = 0x79

SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16

SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = [
    'xG2qW5lP7lV2iN5fN5pG',
    'xT1cJ6dL5wC0kK1rB4dK',
    'qC4jS5bZ6fL5xE6nD4zA',
    'gD4jQ2aL3bS3lC3xT0iW',
    'xU1yQ8wE9zY3gZ3bT5aE'
]

EM_SIMPLE1 = 1
EM_SIMPLE2 = 16
EM_SM4_2 = 2
EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31
EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE

CM_NONE = 0
CM_ZLIB = 1
CM_ZSTD = 6
CM_ZSTD_DICT = 8
CM_MASK = 15


# ----------------- SM4 MODULE CONTENT -----------------
"""SM4 Algorithm Implementation Module."""
# tencent is using custom S-BOX, FK and CK

_S_BOX = bytes([
    0x34, 0x66, 0x25, 0x74, 0x89, 0x78, 0xE4, 0xA9, 0x5A, 0x41, 0xBC, 0x7A, 0xD6, 0x16, 0x21, 0x23,
    0x4D, 0x61, 0xDA, 0x94, 0x9B, 0xDF, 0x13, 0x3C, 0x69, 0x3A, 0x31, 0x0A, 0x5F, 0xD7, 0x99, 0x95,
    0xF1, 0xAE, 0x72, 0x3D, 0x07, 0x60, 0x24, 0xB6, 0x98, 0xEE, 0xC4, 0xA2, 0x2D, 0x88, 0xDD, 0x8D,
    0x04, 0xEA, 0xBB, 0x11, 0xCA, 0x3E, 0x5D, 0xA1, 0xF6, 0x3F, 0xB0, 0x97, 0x80, 0x47, 0x2B, 0xA6,
    0xE6, 0xF7, 0xD9, 0xB1, 0x59, 0xC0, 0x7C, 0xBE, 0x54, 0x28, 0xB7, 0x7E, 0x4F, 0xF8, 0x43, 0x6E,
    0xA0, 0x50, 0x0E, 0xF5, 0x90, 0xB8, 0xFB, 0xA3, 0x7B, 0x62, 0x19, 0x46, 0x03, 0x2A, 0xB9, 0x8F,
    0x9F, 0x77, 0xB4, 0x5B, 0x83, 0x87, 0x08, 0xEB, 0xE2, 0x1E, 0x42, 0xF0, 0x0F, 0xE8, 0x71, 0x6A,
    0x75, 0xAD, 0x55, 0x1F, 0xB5, 0xAB, 0x33, 0xFA, 0x7F, 0x15, 0xBD, 0x85, 0xD8, 0x06, 0x68, 0xB3,
    0x52, 0x30, 0x48, 0x0B, 0x00, 0xED, 0xEF, 0xB2, 0x57, 0x8E, 0xE7, 0x6C, 0xD5, 0xE5, 0x2E, 0x53,
    0x82, 0x05, 0xF9, 0x81, 0xF4, 0x56, 0xBF, 0x8C, 0x4B, 0xE3, 0xDB, 0x4A, 0x91, 0x4C, 0x2C, 0xD3,
    0x40, 0x29, 0x4E, 0x20, 0x14, 0x36, 0x79, 0x09, 0x6F, 0xD1, 0x37, 0xE0, 0x39, 0x0C, 0x8A, 0x92,
    0x38, 0x12, 0x35, 0x6D, 0xE1, 0xFD, 0x93, 0x9A, 0x17, 0xD4, 0xC9, 0x9C, 0x6B, 0x84, 0x26, 0x9D,
    0xAF, 0x76, 0xC1, 0x9E, 0xD0, 0x96, 0xC5, 0xCB, 0xE9, 0x73, 0x49, 0xD2, 0xCD, 0x64, 0xC3, 0xC7,
    0x01, 0x7D, 0xF3, 0xAC, 0xFC, 0xDE, 0xA4, 0x44, 0x32, 0x1B, 0xC2, 0xBA, 0x1C, 0x02, 0xC6, 0x27,
    0x45, 0x8B, 0xF2, 0x18, 0xA7, 0x10, 0x51, 0x1D, 0xC8, 0xCF, 0x63, 0xFF, 0x2F, 0x0D, 0x58, 0xCE,
    0x65, 0xA5, 0xDC, 0x1A, 0x3B, 0x86, 0xFE, 0x22, 0x5C, 0xA8, 0x5E, 0x67, 0xAA, 0xEC, 0x70, 0xCC
])

_FK = [
    0x46970E9C, 0x4BC0685E, 0x59056186, 0xBCA2491E
]

_CK = [
    0x000EB92B, 0x3A0AE783, 0x9E3B5C67, 0xADDBDABF, 0x7B7484CB, 0x49156C63, 0xC79AB5E7, 0x79EC9CFF,
    0x1725BEAB, 0x2FB89CA3, 0x24808AD7, 0xDDD28B1F, 0x4740DA4B, 0xBBC3EA73, 0x247B30E7, 0x91BE385F,
    0x0401248B, 0x45FCD3A3, 0x530B4CE7, 0xC68DD35F, 0xE3D16C2B, 0x4F698C13, 0x6B92C747, 0x769EFB1F,
    0x4C73BE9B, 0xC942B193, 0xAD80D827, 0x372FB33F, 0x13CB6AAB, 0x2BDC0AA3, 0x17A4A247, 0xD5E96CAF
]

def _BS(X):
    return ((_S_BOX[(X >> 24) & 0xff] << 24) |
            (_S_BOX[(X >> 16) & 0xff] << 16) |
            (_S_BOX[(X >> 8) & 0xff] << 8) |
            (_S_BOX[X & 0xff]))


def _T0(X):
    X = _BS(X)
    return X ^ ROL32(X, 2) ^ ROL32(X, 10) ^ ROL32(X, 18) ^ ROL32(X, 24)


def _T1(X):
    X = _BS(X)
    return X ^ ROL32(X, 13) ^ ROL32(X, 23)


def _key_expand(key: bytes, rkey: List[int]):
    """Key expansion."""

    K0 = int.from_bytes(key[0:4], "big") ^ _FK[0]
    K1 = int.from_bytes(key[4:8], "big") ^ _FK[1]
    K2 = int.from_bytes(key[8:12], "big") ^ _FK[2]
    K3 = int.from_bytes(key[12:16], "big") ^ _FK[3]

    for i in range(0, 32, 4):
        K0 = K0 ^ _T1(K1 ^ K2 ^ K3 ^ _CK[i])
        rkey[i] = K0
        K1 = K1 ^ _T1(K2 ^ K3 ^ K0 ^ _CK[i + 1])
        rkey[i + 1] = K1
        K2 = K2 ^ _T1(K3 ^ K0 ^ K1 ^ _CK[i + 2])
        rkey[i + 2] = K2
        K3 = K3 ^ _T1(K0 ^ K1 ^ K2 ^ _CK[i + 3])
        rkey[i + 3] = K3


class SM4(BlockCipher):
    """SM4 Algorithm."""

    @classmethod
    def key_length(self) -> int:
        """Get key length in bytes."""

        return 16

    @classmethod
    def block_length(self) -> int:
        """Get block length in bytes."""

        return 16

    def __init__(self, key: bytes) -> None:
        """SM4 Algorithm.

        Args:
            key: 16 bytes key.

        Raises:
            IncorrectLengthError: Incorrect key length.
        """

        if len(key) != self.key_length():
            raise IncorrectLengthError("Key", f"{self.key_length()} bytes", f"{len(key)} bytes")

        self._key: bytes = key
        self._rkey: List[int] = [0] * 32
        _key_expand(self._key, self._rkey)

        self._block_buffer = bytearray()

    def encrypt(self, block: bytes) -> bytes:
        """Encrypt.

        Args:
            block: Plain block to encrypt, must be 16 bytes.

        Returns:
            bytes: 16 bytes cipher block.

        Raises:
            IncorrectLengthError: Incorrect block length.
        """

        if len(block) != self.block_length():
            raise IncorrectLengthError("Block", f"{self.block_length()} bytes", f"{len(block)} bytes")

        RK = self._rkey

        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")

        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[i])
            X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[i + 1])
            X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[i + 2])
            X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[i + 3])

        BUFFER = self._block_buffer
        BUFFER.clear()
        BUFFER.extend(X3.to_bytes(4, "big"))
        BUFFER.extend(X2.to_bytes(4, "big"))
        BUFFER.extend(X1.to_bytes(4, "big"))
        BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)

    def decrypt(self, block: bytes) -> bytes:
        """Decrypt.

        Args:
            block: cipher block to decrypt, must be 16 bytes.

        Returns:
            bytes: 16 bytes plain block.

        Raises:
            IncorrectLengthError: Incorrect block length.
        """

        if len(block) != self.block_length():
            raise IncorrectLengthError("Block", f"{self.block_length()} bytes", f"{len(block)} bytes")

        RK = self._rkey

        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")

        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[31 - i])
            X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
            X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[29 - i])
            X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[28 - i])

        BUFFER = self._block_buffer
        BUFFER.clear()
        BUFFER.extend(X3.to_bytes(4, "big"))
        BUFFER.extend(X2.to_bytes(4, "big"))
        BUFFER.extend(X1.to_bytes(4, "big"))
        BUFFER.extend(X0.to_bytes(4, "big"))
        return bytes(BUFFER)

# ... (Các lớp Misc, Reader, PakInfo, TencentPakInfo, PakCompressedBlock, TencentPakEntry không thay đổi) ...
class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        assert n > 0
        padding = n - (len(data) % n)
        if padding == n:
            return data
        return data + b'\x00' * padding

    @staticmethod
    def align_up(x: int, n: int) -> int:
        return ((x + n - 1) // n) * n


class Reader:
    def __init__(self, buffer, cursor=0):
        self._buffer = buffer
        self._cursor = cursor

    def u1(self, move_cursor=True) -> int:
        return self.unpack('B', move_cursor=move_cursor)[0]

    def u4(self, move_cursor=True) -> int:
        return self.unpack('<I', move_cursor=move_cursor)[0]

    def u8(self, move_cursor=True) -> int:
        return self.unpack('<Q', move_cursor=move_cursor)[0]

    def i1(self, move_cursor=True) -> int:
        return self.unpack('b', move_cursor=move_cursor)[0]

    def i4(self, move_cursor=True) -> int:
        return self.unpack('<i', move_cursor=move_cursor)[0]

    def i8(self, move_cursor=True) -> int:
        return self.unpack('<q', move_cursor=move_cursor)[0]

    def s(self, n: int, move_cursor=True) -> bytes:
        return self.unpack(f'{n}s', move_cursor=move_cursor)[0]

    def unpack(self, f: str | bytes, offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor:
            self._cursor += struct.calcsize(f)
        return x

    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0:
            return str()
        # TODO
        assert length > 0
        offset = 0 if move_cursor else 4
        return self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00').decode()


class PakInfo:
    def __init__(self, buffer, keystream: list[int]):
        def decrypt_index_encrypted(x: int) -> int:
            MASK_8 = 0xFF
            return (x ^ keystream[3]) & MASK_8

        def decrypt_magic(x: int) -> int:
            return x ^ keystream[2]

        def decrypt_index_hash(x: bytes) -> bytes:
            key = struct.pack('<5I', *keystream[4:][:5])
            assert len(x) == len(key)
            return bytes(a ^ b for a, b in zip(x, key))

        def decrypt_index_size(x: int) -> int:
            return x ^ ((keystream[10] << 32) | keystream[11])

        def decrypt_index_offset(x: int) -> int:
            return x ^ ((keystream[0] << 32) | keystream[1])

        reader = Reader(buffer[-PakInfo._mem_size(-1):])

        self.index_encrypted: bool = decrypt_index_encrypted(reader.u1()) == 1
        self.magic: int = decrypt_magic(reader.u4())
        self.version: int = reader.u4()
        self.index_hash: bytes = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size: int = decrypt_index_size(reader.u8())
        self.index_offset: int = decrypt_index_offset(reader.u8())
        if self.version <= 3:
            self.index_encrypted = False

    @staticmethod
    def _mem_size(_: int) -> int:
        return 1 + 4 + 4 + 20 + 8 + 8


class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: list[int]):
        def decrypt_unk(x: bytes) -> bytes:
            key = struct.pack('<8I', *keystream[7:][:8])
            assert len(x) == len(key)
            return bytes(a ^ b for a, b in zip(x, key))

        def decrypt_stem_hash(x: int) -> int:
            return x ^ keystream[8]

        def decrypt_unk_hash(x: int) -> int:
            return x ^ keystream[9]

        super().__init__(buffer, keystream)

        reader = Reader(buffer[-TencentPakInfo._mem_size(self.version):])

        self.unk1: bytes = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash: bytes = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash: int = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
        self.unk2: int = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash: bytes = reader.s(20) if self.version >= 12 else bytes()

    @staticmethod
    def _mem_size(version: int) -> int:
        size_for_7 = 32 if version >= 7 else 0
        size_for_8 = 256 * 3 if version >= 8 else 0
        size_for_9 = 4 * 2 if version >= 9 else 0
        size_for_12 = 20 if version >= 12 else 0
        return PakInfo._mem_size(version) + size_for_7 + size_for_8 + size_for_9 + size_for_12


class PakCompressedBlock:
    def __init__(self, reader: Reader):
        self.start: int = reader.u8()
        self.end: int = reader.u8()
        
@dataclass
class TencentPakEntry:
    def __init__(self, reader: Reader, version: int):
        self.content_hash: bytes = reader.s(20)
        if version <= 1:
            _ = reader.u8()
        self.offset: int = reader.u8()
        self.uncompressed_size: int = reader.u8()
        self.compression_method: int = reader.u4() & CM_MASK
        self.size: int = reader.u8()
        self.unk1: int = reader.u1() if version >= 5 else 0
        self.unk2: bytes = reader.s(20) if version >= 5 else bytes()
        self.compressed_blocks: list[PakCompressedBlock] = [PakCompressedBlock(reader) for _ in range(
            reader.u4())] if self.compression_method != 0 and version >= 3 else []
        self.compression_block_size: int = reader.u4() if version >= 4 else 0
        self.encrypted: bool = reader.u1() == 1 if version >= 4 else False
        self.encryption_method: int = reader.u4() if version >= 12 else 0
        self.index_new_sep: int = reader.u4() if version >= 12 else 0 # <<< DÒNG MỚI ĐƯỢC THÊM VÀO

    def _mem_size(self, version: int) -> int:
        size_for_123 = 20 + 8 + 8 + 4 + 8 + (8 if version == 1 else 0)
        size_for_4 = 4 + 1 if version >= 4 else 0
        size_for_compressed_blocks = 4 + len(self.compressed_blocks) * 16 if self.compressed_blocks else 0
        size_for_5 = 1 + 20 if version >= 5 else 0
        # Cập nhật size_for_12 để tính cả trường mới
        size_for_12 = 8 if version >= 12 else 0 # <<< DÒNG NÀY CŨNG NÊN ĐƯỢC SỬA LẠI (từ 4 thành 8)
        return size_for_123 + size_for_4 + size_for_5 + size_for_12 + size_for_compressed_blocks


class PakCrypto:
    # ... (LCG class không thay đổi) ...
    class _LCG:
        def __init__(self, seed: int):
            self.state = seed

        def next(self) -> int:
            MASK_32 = 0xFFFFFFFF
            MSB_1 = 1 << 31

            def wrap(x: int) -> int:
                x &= MASK_32
                if not x & MSB_1:
                    return x
                else:
                    return ((x + MSB_1) & MASK_32) - MSB_1

            x1 = wrap(0x41C64E6D * self.state)
            self.state = wrap(x1 + 12345)
            x2 = wrap(x1 + 0x13038) if self.state < 0 else self.state
            return ((x2 >> 16) & MASK_32) % 0x7FFF

    @staticmethod
    def zuc_keystream() -> list[int]:
        zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]

    # ... (Các hàm _xorxor, _hashhash, _meowmeow, rsa_extract không thay đổi) ...
    @staticmethod
    def _xorxor(buffer, x) -> bytes:
        return bytes(buffer[i] ^ x[i % len(x)] for i in range(len(buffer)))

    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        result = bytes()
        for i in range(math.ceil(n / SHA1.digest_size)):
            result += SHA1.new(buffer).digest()
        if len(result) >= n:
            result = result[:n]
        else:
            result += b'\x00' * (n - len(result))
        return result

    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]

        if len(buffer) < 43:
            return bytes()

        x1 = buffer[1:][:SHA1.digest_size]
        x2 = buffer[SHA1.digest_size + 1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))

        part1, m = (x2[:SHA1.digest_size], x2[SHA1.digest_size:])
        if part1 != SHA1.new(b'\x00' * SHA1.digest_size).digest():
            return bytes()

        return unpad(m)

    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature, 'little')
        n = int.from_bytes(modulus, 'little')
        e = 0x10001
        m = pow(c, e, n).to_bytes(256, 'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))

    # --- THÊM HÀM MÃ HÓA ---
    @staticmethod
    def _encrypt_simple1(plaintext) -> bytes:
        # XOR là đối xứng, nên hàm mã hóa và giải mã giống nhau
        return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in plaintext)

    @staticmethod
    def _decrypt_simple1(ciphertext) -> bytes:
        return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in ciphertext)
    
    @staticmethod
    def _encrypt_simple2(plaintext) -> bytes:
        class RollingKey:
            def __init__(self, initial_value: int):
                self._value = initial_value

            def update(self, x: int) -> int:
                original_value = self._value
                self._value = x
                return original_value ^ x
        
        assert len(plaintext) % SIMPLE2_BLOCK_SIZE == 0
        
        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rolling_key = RollingKey(initial_key)
        ciphertext = (
            struct.pack('<I', rolling_key.update(x)) for x in struct.unpack(f'<{len(plaintext) // 4}I', plaintext)
        )
        return bytes(it.chain.from_iterable(ciphertext))


    @staticmethod
    def _decrypt_simple2(ciphertext) -> bytes:
        class RollingKey:
            def __init__(self, initial_value: int):
                self._value = initial_value

            def update(self, x: int) -> int:
                self._value ^= x
                return self._value

        assert len(ciphertext) % SIMPLE2_BLOCK_SIZE == 0

        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rolling_key = RollingKey(initial_key)
        plaintext = (
            struct.pack('<I', rolling_key.update(x)) for x in struct.unpack(f'<{len(ciphertext) // 4}I', ciphertext)
        )
        return bytes(it.chain.from_iterable(plaintext))

    # ... (Các hàm _derive_sm4_key, _sm4_context_for_key không thay đổi) ...
    @staticmethod
    @lru_cache(maxsize=1)
    def _derive_sm4_key(file_path: PurePath, encryption_method: int) -> bytes:
        part1 = file_path.stem.lower()
        if encryption_method == EM_SM4_2:
            secret = SM4_SECRET_2
        elif encryption_method == EM_SM4_4:
            secret = SM4_SECRET_4
        else:
            index = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
            secret = f'{SM4_SECRET_NEW[index]}{encryption_method}'
        return SHA1.new(str(part1 + secret).encode()).digest()[:SM4.key_length()]

    @staticmethod
    @lru_cache(maxsize=1)
    def _sm4_context_for_key(key: bytes) -> SM4:
        return SM4(key)

    # --- THÊM HÀM MÃ HÓA ---
    @staticmethod
    def _encrypt_sm4(plaintext, file_path: PurePath, encryption_method: int) -> bytes:
        padded_plaintext = pad(plaintext, SM4.block_length())
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        # SỬA LỖI: Thêm bytes(x) để chuyển tuple thành bytes trước khi đưa vào encrypt
        return bytes(it.chain.from_iterable(sm4.encrypt(bytes(x)) for x in it.batched(padded_plaintext, SM4.block_length())))

    @staticmethod
    def _decrypt_sm4(ciphertext, file_path: PurePath, encryption_method: int) -> bytes:
        assert len(ciphertext) % SM4.block_length() == 0
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        # SỬA LỖI: Thêm bytes(x) để chuyển tuple thành bytes trước khi đưa vào decrypt
        return bytes(it.chain.from_iterable(sm4.decrypt(bytes(x)) for x in it.batched(ciphertext, SM4.block_length())))


    @staticmethod
    def decrypt_index(ciphertext, pak_info: TencentPakInfo) -> bytes:
        # ... (Không thay đổi) ...
        if pak_info.version > 7:
            key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
            iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
            assert len(key) == 32 and len(iv) == 32

            aes = AES.new(key, MODE_CBC, iv[:16])
            return unpad(aes.decrypt(ciphertext), AES.block_size)
        else:
            return bytes(PakCrypto._decrypt_simple1(ciphertext))


    @staticmethod
    def _is_simple1_method(encryption_method: int) -> bool:
        return encryption_method == EM_SIMPLE1

    @staticmethod
    def _is_simple2_method(encryption_method: int) -> bool:
        return encryption_method == EM_SIMPLE2

    @staticmethod
    def _is_sm4_method(encryption_method: int) -> bool:
        return (encryption_method == EM_SM4_2
                or encryption_method == EM_SM4_4
                or encryption_method & EM_SM4_NEW_MASK != 0)

    @staticmethod
    def align_encrypted_content_size(n: int, encryption_method: int) -> int:
        if PakCrypto._is_simple2_method(encryption_method):
            return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        elif PakCrypto._is_sm4_method(encryption_method):
            return Misc.align_up(n, SM4.block_length())
        else:
            return n
            
    # --- THÊM HÀM MÃ HÓA CHUNG ---
    @staticmethod
    def encrypt_block(plaintext, file: PurePath, encryption_method: int) -> bytes:
        if PakCrypto._is_simple1_method(encryption_method):
            return PakCrypto._encrypt_simple1(plaintext)
        elif PakCrypto._is_simple2_method(encryption_method):
            # Cần padding cho simple2
            padded_plaintext = pad(plaintext, SIMPLE2_BLOCK_SIZE)
            return PakCrypto._encrypt_simple2(padded_plaintext)
        elif PakCrypto._is_sm4_method(encryption_method):
            # Hàm _encrypt_sm4 đã tự xử lý padding
            return PakCrypto._encrypt_sm4(plaintext, file, encryption_method)
        else:
            assert False, f"Phương thức mã hóa không xác định: {encryption_method}"


    @staticmethod
    def decrypt_block(ciphertext, file: PurePath, encryption_method: int) -> bytes:
        if PakCrypto._is_simple1_method(encryption_method):
            return PakCrypto._decrypt_simple1(ciphertext)
        elif PakCrypto._is_simple2_method(encryption_method):
            return PakCrypto._decrypt_simple2(ciphertext)
        elif PakCrypto._is_sm4_method(encryption_method):
            return PakCrypto._decrypt_sm4(ciphertext, file, encryption_method)
        else:
            if encryption_method == 0:
                 return ciphertext
            assert False, f"Phương thức mã hóa không xác định: {encryption_method}"
            
    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, encryption_method: int) -> list[int]:
        if not PakCrypto._is_sm4_method(encryption_method):
            return list(range(n))

        permutation = []
        lcg = PakCrypto._LCG(n)
        while len(permutation) != n:
            x = lcg.next() % n
            if x not in permutation:
                permutation.append(x)

        inverse = [0] * len(permutation)
        for i, x in enumerate(permutation):
            inverse[x] = i

        return inverse

    @staticmethod
    def stat():
        print(PakCrypto._derive_sm4_key.cache_info())
        print(PakCrypto._sm4_context_for_key.cache_info())

 
class PakCompression:
    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_decompressor(dict_data: bytes | None) -> ZstdDecompressor:
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        return ZstdDecompressor(dict_obj)

    @staticmethod
    @lru_cache(maxsize=128) 
    def _zstd_compressor(dict_data: bytes | None, level: int) -> ZstdCompressor:
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        
        # --- [QUAN TRỌNG] TẮT TOÀN BỘ METADATA ĐỂ TIẾT KIỆM BYTES ---
        return ZstdCompressor(
            level=level, 
            dict_data=dict_obj,
            write_checksum=False,      # Không ghi Checksum (Tiết kiệm 4 bytes)
            write_content_size=False,  # Không ghi kích thước file (Tiết kiệm bytes)
            write_dict_id=False        # Không ghi ID từ điển (Tiết kiệm 4 bytes)
        )

    @staticmethod
    def decompress_block(block, dict_data: bytes | None, compression_method: int) -> bytes:
        if compression_method == CM_ZLIB:
            return zlib.decompress(block)
        elif compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
            if compression_method != CM_ZSTD_DICT:
                dict_data = None
            return PakCompression._zstd_decompressor(dict_data).decompress(block)
        else:
            assert False, f"Unknown decompression method: {compression_method}"

    @staticmethod
    def compress_block(block, dict_data: bytes | None, compression_method: int, level: int | None = None) -> bytes:
        if compression_method == CM_ZLIB:
            use_level = level if level is not None else 9
            # Thử nén Zlib thông thường
            compressed = zlib.compress(block, level=use_level)
            return compressed
            
        elif compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
            use_level = level if level is not None else 22
            if compression_method != CM_ZSTD_DICT:
                dict_data = None
            return PakCompression._zstd_compressor(dict_data, use_level).compress(block)
        else:
            assert False, f"Unknown compression method: {compression_method}"

# --- LỚP COMPRESSIONFINDER MỚI ---
class CompressionFinder:
    """
    Lớp thông minh để tìm mức nén tốt nhất cho một khối dữ liệu
    để vừa với không gian lưu trữ gốc.
    """
    ZLIB_LEVELS_TO_TRY = list(range(9, 0, -1))
    # Bao gồm cả các mức nén "ultra" của Zstandard (số âm)
    ZSTD_LEVELS_TO_TRY = list(range(22, 0, -1)) + list(range(-1, -8, -1))

    @staticmethod
    def find_best_level(
        uncompressed_chunk: bytes, 
        original_compressed_size: int, 
        dict_data: bytes | None, 
        compression_method: int
    ) -> (int | None, int):
        
        levels_to_try = []
        default_level = 9
        if compression_method == CM_ZLIB:
            levels_to_try = CompressionFinder.ZLIB_LEVELS_TO_TRY
            default_level = 9
        elif compression_method in [CM_ZSTD, CM_ZSTD_DICT]:
            levels_to_try = CompressionFinder.ZSTD_LEVELS_TO_TRY
            default_level = 22
        else:
            # Không nén
            return None, len(uncompressed_chunk)

        best_fit_level = None
        closest_size_so_far = -1 # Kích thước vừa vặn nhất tìm được

        for level in levels_to_try:
            compressed_data = PakCompression.compress_block(uncompressed_chunk, dict_data, compression_method, level=level)
            current_size = len(compressed_data)

            # Nếu kích thước nén vừa vặn và lớn hơn kích thước tốt nhất đã tìm thấy
            if original_compressed_size >= current_size > closest_size_so_far:
                closest_size_so_far = current_size
                best_fit_level = level
                # Nếu khớp hoàn hảo, không cần tìm nữa
                if current_size == original_compressed_size:
                    break
        
        # Nếu đã tìm thấy một level phù hợp
        if best_fit_level is not None:
            return best_fit_level, closest_size_so_far

        # Nếu không có level nào tạo ra tệp nhỏ hơn bản gốc, trả về level cao nhất
        # và kích thước của nó để hàm gọi có thể báo lỗi.
        final_compressed = PakCompression.compress_block(uncompressed_chunk, dict_data, compression_method, level=default_level)
        return default_level, len(final_compressed)

class TencentPakFile:
    def __init__(self, file_path: PurePath, is_od=False):
        self._file_path = file_path
        with open(file_path, 'rb') as file:
            self._file_content = memoryview(file.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._files: list[TencentPakEntry] = []
        self._index: dict[PurePath, dict[str, TencentPakEntry]] = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())

        self._verify_stem_hash()
        self._tencent_load_index()

    def _verify_stem_hash(self) -> None:
        if not self._is_od and self._pak_info.version >= 9:
            assert self._pak_info.stem_hash == zlib.crc32(self._file_path.stem.encode('utf-32le'))

    def _tencent_load_index(self) -> None:
        index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]

        if self._pak_info.index_encrypted:
            index_data = PakCrypto.decrypt_index(index_data, self._pak_info)
        else:
            index_data = index_data

        self._verify_index_hash(index_data)
        self._load_index(index_data)

    def _verify_index_hash(self, index_data) -> None:
        expected_hash = self._pak_info.index_hash
        if not self._is_od and self._pak_info.version >= 8:
            assert expected_hash == PakCrypto.rsa_extract(self._pak_info.packed_index_hash, RSA_MOD_2)
        assert expected_hash == SHA1.new(index_data).digest()

    @staticmethod
    def _construct_mount_point(mount_point: str) -> PurePath:
        result = PurePath()
        for part in PurePath(mount_point).parts:
            if part != '..':
                result /= part
        return result

    def _peek_content(self, offset: int, size: int, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(size, encryption_method)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block: PakCompressedBlock, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, encryption_method)
        return self._file_content[block.start:][:size]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry) -> None:
        assert not self._zstd_dict
        assert not dict_entry.encrypted
        assert dict_entry.compression_method == CM_NONE

        # --- [THÊM] HIỂN THỊ THÔNG BÁO TẢI TỪ ĐIỂN ---
        print(f"{Colors.PURPLE}► ĐANG TẢI TỪ ĐIỂN ZSTD (Dictionary)...{Colors.NC}")
        print(f"► Kích thước dữ liệu: {dict_entry.size} bytes")
        
        # Giả lập thanh loading nhỏ (nếu file lớn sẽ thấy tác dụng, file nhỏ thì lướt qua nhanh)
        # Thực hiện đọc dữ liệu
        reader = Reader(self._peek_content(dict_entry.offset, dict_entry.size, 0))

        dict_size = reader.u8()
        _ = reader.u4()
        
        # Kiểm tra kích thước thực tế
        real_dict_size = reader.u4()
        assert dict_size == real_dict_size
        
        # Đọc nội dung từ điển
        dict_data = reader.s(dict_size)
        self._zstd_dict = dict_data

        # --- [THÊM] THÔNG BÁO HOÀN TẤT ---
        print(f"{Colors.LGREEN}► ĐÃ TẢI TỪ ĐIỂN THÀNH CÔNG!{Colors.NC}")
        rainbow_print("━" * 54, speed=0.005)
        time.sleep(2)

    def _load_index(self, index_data) -> None:
        if self._pak_info.version <= 10:
            print(f"{Colors.LRED}Cảnh báo: Phiên bản Pak quá cũ, có thể không được hỗ trợ đầy đủ{Colors.NC}")

        reader = Reader(index_data)
        self._mount_point = self._construct_mount_point(reader.string())
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(reader.u4())]

        try:
            num_dirs = reader.u8()
            for _ in range(num_dirs):
                dir_path = PurePath(reader.string())
                num_files_in_dir = reader.u8()
                
                # Tạo dictionary chứa các file trong thư mục này
                e = {reader.string(): self._files[~reader.i4()] for _ in range(num_files_in_dir)}
                
                # --- [SỬA ĐỔI] KIỂM TRA ZSTDDIC VÀ IN THÔNG BÁO ---
                if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                    print(f"\n{Colors.YELLOW}► PHÁT HIỆN CẤU TRÚC ZSTD DICTIONARY{Colors.NC}")
                    assert len(e) == 1
                    # Gọi hàm tải từ điển (đã sửa ở trên)
                    self._construct_zstd_dict(e[[*e.keys()][0]])
                    continue
                
                self._index.update({PurePath(dir_path): e})
                
        except struct.error:
            print("Lưu ý: Đã kết thúc việc đọc chỉ mục, có thể do định dạng pak cũ hơn.")
    
    def _get_method_str(self, method_int, is_encryption):
        if is_encryption:
            if PakCrypto._is_simple1_method(method_int): return "SIMPLE1"
            if PakCrypto._is_simple2_method(method_int): return "SIMPLE2"
            if PakCrypto._is_sm4_method(method_int): return f"SM4 (Type {method_int})"
            return "NONE" if method_int == 0 else "UNKNOWN"
        else:
            if method_int == CM_NONE: return "NONE"
            if method_int == CM_ZLIB: return "ZLIB"
            if method_int == CM_ZSTD: return "ZSTD"
            if method_int == CM_ZSTD_DICT: return "ZSTD_DICT"
            return "UNKNOWN"

    def _write_to_disk(self, file_path: PurePath, entry: TencentPakEntry) -> None:
        encryption_method = entry.encryption_method
        compression_method = entry.compression_method

        # Lấy tên phương thức dưới dạng chuỗi
        enc_str = self._get_method_str(encryption_method, True)
        comp_str = self._get_method_str(compression_method, False)
        
        # [MODIFIED] Hiển thị thông tin chi tiết: TÊN ► MÃ HÓA ► NÉN
        print(f"► UNPACK: {Colors.LGREEN}{file_path.name}{Colors.NC} ► {Colors.PURPLE}{enc_str}{Colors.NC} ► {Colors.YELLOW}{comp_str}{Colors.NC}")

        with open(file_path, 'wb') as file:
            if compression_method == CM_NONE:
                data = self._peek_content(entry.offset, entry.size, encryption_method)
                if entry.encrypted:
                    data = PakCrypto.decrypt_block(bytes(data), file_path, encryption_method)
                file.write(data)
                return

            decrypted_uncompressed_data = bytearray()
            for x in PakCrypto.generate_block_indices(len(entry.compressed_blocks), encryption_method):
                data = self._peek_block_content(entry.compressed_blocks[x], encryption_method)
                if entry.encrypted:
                    data = PakCrypto.decrypt_block(bytes(data), file_path, encryption_method)
                
                if not data:
                    continue
                
                # Sửa đổi: truyền dict dưới dạng bytes
                decompressed_data = PakCompression.decompress_block(bytes(data), self._zstd_dict, compression_method)
                decrypted_uncompressed_data.extend(decompressed_data)
            
            file.write(decrypted_uncompressed_data[:entry.uncompressed_size])


    def dump(self, out_path: PurePath) -> None:
        out_path /= self._mount_point

        for dir_path, dir_content in self._index.items():
            current_out_path = Path(out_path / dir_path)
            if not current_out_path.exists():
                current_out_path.mkdir(parents=True, exist_ok=True)
            for file_name, entry in dir_content.items():
                self._write_to_disk(current_out_path / file_name, entry)
    

    def repack(self, repack_dir: PurePath, target_pak_path: Path):
        
        # --- CẤU HÌNH TỰ ĐỘNG ---
        is_auto_scan = True        # Tự động quét file trong folder REPACK
        mode_choice = '3'          # '3' = AUTO (Chunk Mode cho file > 64KB)
        
        print(f"{Colors.LGREEN}KHỞI TẠO DỮ LIỆU REPACK CHO:{Colors.NC}{Colors.YELLOW} {target_pak_path.name}{Colors.NC}")
        
        p_repack_dir = Path(repack_dir)
        if not p_repack_dir.exists():
             print(f"{Colors.LRED}LỖI: Thư mục REPACK không tồn tại!{Colors.NC}")
             return False 

        # --- LOGIC AUTO SCAN ---
        user_files_map = {} 
        
        print(f"{Colors.YELLOW}► Kích hoạt: AUTO SCAN FILE REPACK...{Colors.NC}")
        count_scan = 0
        for file_path in p_repack_dir.rglob('*'):
            if file_path.is_file():
                f_name = file_path.name
                f_size = file_path.stat().st_size
                if f_name not in user_files_map: user_files_map[f_name] = []
                user_files_map[f_name].append((file_path, f_size))
                count_scan += 1
        print(f"► Đã tìm thấy {count_scan} tệp trong thư mục REPACK.")

        # ======================= CORE REPACK LOOP =======================
        repacked_success_list = [] 
        files_processed_count = 0

        with open(target_pak_path, 'r+b') as target_file:
            for dir_path, dir_content in self._index.items():
                for file_name, entry in dir_content.items():
                    
                    selected_path = None
                    target_uncompressed_size = entry.uncompressed_size
                    
                    # ---------------- LOGIC TÌM FILE (AUTO SCAN) ----------------
                    candidates = user_files_map.get(file_name)
                    if not candidates: continue
                    
                    best_candidate = None
                    min_diff = float('inf')
                    MAX_ALLOWED_DIFF = 50 

                    for path, size in candidates:
                        diff = abs(size - target_uncompressed_size)
                        if diff <= MAX_ALLOWED_DIFF:
                            if diff < min_diff:
                                min_diff = diff
                                best_candidate = path
                    
                    if not best_candidate: continue
                    selected_path = best_candidate

                    # ---------------- BẮT ĐẦU XỬ LÝ FILE ----------------
                    files_processed_count += 1
                    internal_pak_path = dir_path / file_name
                    
                    # Lấy thông tin hiển thị
                    enc_str = self._get_method_str(entry.encryption_method, True)
                    comp_str = self._get_method_str(entry.compression_method, False)

                    print(f"")
                    print(f"► REPACKING: {Colors.LGREEN}{file_name}{Colors.NC} ► {Colors.PURPLE}{enc_str}{Colors.NC} ► {Colors.YELLOW}{comp_str}{Colors.NC}")
                    
                    try:
                        with open(selected_path, 'rb') as f_modified:
                            modified_data = f_modified.read()

                        is_success = False
                        
                        # === TRƯỜNG HỢP 1: KHÔNG NÉN (CM_NONE) ===
                        if entry.compression_method == CM_NONE:
                            data_to_write = modified_data
                            if entry.encrypted:
                                data_to_write = PakCrypto.encrypt_block(modified_data, selected_path, entry.encryption_method)
                            
                            original_size = entry.size
                            if len(data_to_write) > original_size:
                                print(f"{Colors.LRED}    LỖI: Kích thước mới lớn hơn gốc. BỎ QUA.{Colors.NC}")
                                continue

                            target_file.seek(entry.offset)
                            target_file.write(data_to_write)
                            if len(data_to_write) < original_size:
                                target_file.write(b'\x00' * (original_size - len(data_to_write)))
                                
                            print(f"{Colors.LGREEN}    HOÀN TẤT REPACK{Colors.NC} {Colors.YELLOW}{file_name} {Colors.NC}")
                            is_success = True
                             
                        # === TRƯỜNG HỢP 2: CÓ NÉN (ZSTD/ZLIB) ===
                        else: 
                            repack_done = False
                            SIZE_64KB = 65536
                            original_block_count = len(entry.compressed_blocks)
                            
                            run_direct = False
                            # Nếu file nhỏ và block gốc ít, ưu tiên Direct
                            if len(modified_data) <= SIZE_64KB and original_block_count == 1:
                                run_direct = True

                            # --- DIRECT REPACK ---
                            if run_direct:
                                if len(entry.compressed_blocks) > 0:
                                    first_block = entry.compressed_blocks[0]
                                    original_compressed_space = first_block.end - first_block.start
                                    
                                    # Tìm level tốt nhất
                                    best_level, _ = CompressionFinder.find_best_level(
                                        modified_data, original_compressed_space, self._zstd_dict, entry.compression_method
                                    )

                                    compressed_chunk = PakCompression.compress_block(
                                        modified_data, self._zstd_dict, entry.compression_method, level=best_level
                                    )
                                    
                                    data_to_write = compressed_chunk
                                    if entry.encrypted:
                                        data_to_write = PakCrypto.encrypt_block(data_to_write, selected_path, entry.encryption_method)
                                    
                                    final_target_space = PakCrypto.align_encrypted_content_size(original_compressed_space, entry.encryption_method)
                                    
                                    if len(data_to_write) <= final_target_space:
                                        target_file.seek(first_block.start)
                                        target_file.write(data_to_write)
                                        target_file.write(b'\x00' * (final_target_space - len(data_to_write)))
                                        print(f"{Colors.LGREEN}    HOÀN TẤT REPACK{Colors.NC} {Colors.YELLOW}{file_name} {Colors.NC}")
                                        is_success = True
                                        repack_done = True

                            # --- CHUNK MODE (ZSTD) ---
                            if not repack_done:
                                block_indices = PakCrypto.generate_block_indices(len(entry.compressed_blocks), entry.encryption_method)
                                uncompressed_offset = 0
                                skipped_chunk_indices = [] 
                                
                                for i, block_index in enumerate(block_indices):
                                    block_info = entry.compressed_blocks[block_index]
                                    chunk_size = entry.compression_block_size
                                    
                                    uncompressed_chunk = modified_data[uncompressed_offset : uncompressed_offset + chunk_size]
                                    uncompressed_offset += chunk_size
                                    
                                    if not uncompressed_chunk: break
                                    
                                    original_compressed_space = block_info.end - block_info.start
                                    
                                    best_level, _ = CompressionFinder.find_best_level(
                                        uncompressed_chunk, original_compressed_space, self._zstd_dict, entry.compression_method
                                    )
                                    
                                    print(f"    ► CHUNK [{i}] ► {best_level}", end=" ► ")
                                    
                                    compressed_chunk = PakCompression.compress_block(
                                        uncompressed_chunk, self._zstd_dict, entry.compression_method, level=best_level
                                    )
                                    
                                    data_to_write = compressed_chunk
                                    if entry.encrypted:
                                        data_to_write = PakCrypto.encrypt_block(data_to_write, selected_path, entry.encryption_method)
                                    
                                    final_target_space = PakCrypto.align_encrypted_content_size(original_compressed_space, entry.encryption_method)
                                    
                                    if len(data_to_write) > final_target_space:
                                        print(f"{Colors.LRED}FAIL{Colors.NC}")
                                        skipped_chunk_indices.append(i)
                                        continue 
                                    
                                    print(f"{Colors.LGREEN}OK{Colors.NC}")
                                    target_file.seek(block_info.start)
                                    target_file.write(data_to_write)
                                    if len(data_to_write) < final_target_space:
                                        target_file.write(b'\x00' * (final_target_space - len(data_to_write)))
                            
                                if not skipped_chunk_indices:
                                    print(f"{Colors.LGREEN}    HOÀN TẤT REPACK{Colors.NC} {Colors.YELLOW}{file_name} {Colors.NC}")
                                    is_success = True
                                else:
                                    # SỬA ĐỔI: Vẫn báo thành công nhưng hiện cảnh báo màu vàng
                                    fail_count = len(skipped_chunk_indices)
                                    print(f"{Colors.YELLOW}    CẢNH BÁO: {fail_count} Chunk bị tràn (Skip), các phần khác OK.{Colors.NC}")
                                    print(f"{Colors.LGREEN}    HOÀN TẤT REPACK{Colors.NC} {Colors.YELLOW}{file_name} {Colors.NC}")
                                    is_success = True # <--- Đánh dấu là thành công để hiện trong danh sách cuối cùng

                        if is_success:
                            repacked_success_list.append(f"{file_name}")

                    except Exception as e:
                        print(f"{Colors.LRED}    LỖI: {file_name}: {e}{Colors.NC}")

        # --- TỔNG KẾT ---
        rainbow_print("━" * 54, speed=0.005)
        print(f"{Colors.YELLOW}Tổng số tệp đã xử lý:{Colors.NC} {files_processed_count}")
        print(f"{Colors.LGREEN}Tổng số tệp thành công:{Colors.NC} {len(repacked_success_list)}")
        
        if repacked_success_list:
            print(f"\n{Colors.LCYAN}Danh sách tệp thành công:{Colors.NC}")
            for item in repacked_success_list:
                parts = item.split(": ", 1)
                print(f"  - {Colors.LGREEN}{parts[0]}{Colors.NC}")
        else:
            print(f"\n{Colors.LRED}Không có tệp nào được repack.{Colors.NC}")
        rainbow_print("━" * 54, speed=0.005)
        
        return True



# --- Logic xử lý kích thước file (Size Adjustment) ---
def run_system_cmd(cmd):
    """Chạy lệnh hệ thống (tương đương system() trong C++)"""
    os.system(cmd)


# --- SỬA HÀM get_zip_size_bytes ---
def get_zip_size_bytes():
    """Lấy kích thước file zip hiện tại bằng lệnh du"""
    # SỬA: Chuyển string sang Path trước khi dùng glob
    zip_files = list(Path(UNZIPOBB).glob("*.zip"))
    if not zip_files:
        return None
    
    try:
        # Cách giả lập lệnh gốc
        res = execute_command(f"du -b \"{zip_files[0]}\" | awk '{{print $1}}'")
        return int(res) if res else 0
    except ValueError:
        return 0
def truncate_zip(operator, amount):
    """Thay đổi kích thước file zip (+ hoặc - byte)"""
    # C++ dùng system("truncate ... *.zip"), khá nguy hiểm nếu có nhiều file
    # Ta sẽ áp dụng cho tất cả file .zip trong folder hiện tại
    cmd = f"truncate -s{operator}{amount} *.zip"
    run_system_cmd(cmd)

# --- SỬA HÀM sizeupdown ---
def sizeupdown():
    os.chdir(UNZIPOBB)
    
    # SỬA: Chuyển string sang Path
    ini_path = Path(TEMP_DIR) / "size_obb.ini"
    if not ini_path.exists():
        print(f"{Colors.LRED}Error: Could not open size_obb.ini{Colors.NC}")
        return

    with open(ini_path, "r") as f:
        try:
            obb_size = int(f.read().strip())
        except ValueError:
            return

    current_size = get_zip_size_bytes()
    if current_size is None:
        print(f"{Colors.LRED}Error: No zip files found.{Colors.NC}")
        return

    if current_size < obb_size:
        while current_size < obb_size:
            truncate_zip("+", 1)
            current_size = get_zip_size_bytes()
            print(" ", end="", flush=True)
    elif current_size > obb_size:
        while current_size > obb_size:
            truncate_zip("-", 1)
            current_size = get_zip_size_bytes()
            print("", end="", flush=True)

# --- SỬA HÀM fnsh ---
def fnsh():
    os.chdir(UNZIPOBB)
    
    # SỬA: Chuyển string sang Path
    ini_path = Path(TEMP_DIR) / "size_obb.ini"
    if not ini_path.exists():
        print(f"{Colors.LRED}Error: Could not open size_obb.ini{Colors.NC}")
        return

    with open(ini_path, "r") as f:
        try:
            obb_size = int(f.read().strip())
        except ValueError:
            return

    current_size = get_zip_size_bytes()
    if current_size is None:
        print(f"{Colors.LRED}Error: No zip files found.{Colors.NC}")
        return

    if current_size < obb_size:
        while current_size < obb_size:
            truncate_zip("+", 100)
            current_size = get_zip_size_bytes()
            print("", end="", flush=True)
        sizeupdown()
    elif current_size > obb_size:
        while current_size > obb_size:
            truncate_zip("-", 100)
            current_size = get_zip_size_bytes()
            print("", end="", flush=True)
        sizeupdown()

# --- SỬA HÀM rezipobb ---
def rezipobb():
    print()
    print(f"{Colors.YELLOW}► STARTING COMPRESS OBB...{Colors.NC}")
    print()

    os.chdir(UNZIPOBB)
    
    # SỬA: Tạo đối tượng Path
    p_unzip = Path(UNZIPOBB)
    p_temp = Path(TEMP_DIR)

    # Di chuyển file zip từ TEMP về UNZIPOBB
    try:
        for item in p_temp.glob("*.zip"):
            shutil.move(str(item), str(p_unzip / item.name))
    except Exception as e:
        print(f"{Colors.LRED}Error moving zip file: {e}{Colors.NC}")
        return

    obb_name = execute_command("find *.zip")
    if not obb_name:
        print(f"{Colors.LRED}No zip file found to compress.{Colors.NC}")
        return

    zip_command = f"zip -u -0 \"{obb_name}\""
    run_system_cmd(zip_command)
    
    fnsh()

    ini_path = p_temp / "size_obb.ini"
    if ini_path.exists():
        with open(ini_path, 'r') as f:
            try:
                obb_size = int(f.read().strip())
                current_zip_size = get_zip_size_bytes()
            except:
                pass

    for zip_file in p_unzip.glob("*.zip"):
        new_name = zip_file.name.replace(".obb.zip", ".obb")
        
        if new_name == zip_file.name: 
            new_name = zip_file.stem + ".obb"
            
        try:
            os.rename(zip_file, p_unzip / new_name)
        except OSError as e:
            print(f"Error renaming: {e}")

    if ini_path.exists():
        os.remove(ini_path)

    # --- [SỬA ĐỔI] DỌN DẸP THƯ MỤC NHƯNG GIỮ LẠI REPACK ---
    for item in p_unzip.iterdir():
        if item.is_dir():
            # Nếu tên thư mục là REPACK thì bỏ qua, không xóa
            if item.name == "REPACK":
                continue
            try:
                shutil.rmtree(item)
            except Exception as e:
                print(f"Warning: Cannot delete {item}: {e}")
    # ------------------------------------------------------

    found_obb = list(p_unzip.glob("*.obb"))
    if found_obb:
        print()
        print(f"{Colors.LGREEN}► COMPRESS OBB SUCCESSFUL{Colors.NC}")
        print()
    else:
        print()
        print(f"{Colors.LRED}► COMPRESS OBB FAILED{Colors.NC}")
        print()

# --- SỬA HÀM unzipobb (Đây là hàm gây ra lỗi bạn gặp) ---
def unzipobb():
    print()
    print(f"{Colors.YELLOW}► STARTING UN-COMPRESS OBB...{Colors.NC}")
    print()

    try:
        os.chdir(UNZIPOBB)
    except OSError:
        print(f"{Colors.LRED}LỖI: Không thể truy cập thư mục OBB: {UNZIPOBB}{Colors.NC}")
        return False

    # SỬA: Tạo đối tượng Path
    p_unzip = Path(UNZIPOBB)
    p_temp = Path(TEMP_DIR)

    # --- [MỚI] KIỂM TRA FILE OBB ---
    obb_files = list(p_unzip.glob("*.obb"))
    if not obb_files:
        print(f"{Colors.LRED}LỖI: Không tìm thấy file .obb nào trong thư mục:{Colors.NC}")
        print(f"{Colors.YELLOW}{UNZIPOBB}{Colors.NC}")
        print(f"{Colors.LCYAN}Vui lòng copy file OBB vào thư mục trên và thử lại.{Colors.NC}")
        return False
    # -------------------------------

    # Đổi tên .obb -> .obb.zip
    for f in obb_files:
        new_name = str(f) + ".zip"
        try:
            os.rename(f, new_name)
        except OSError as e:
            print(f"{Colors.LRED}Lỗi khi đổi tên file: {e}{Colors.NC}")
            return False

    obb_size_str = execute_command("du -b *.obb.zip | awk '{print $1}'")
    if not obb_size_str:
        print(f"{Colors.LRED}Error: No OBB zip files found.{Colors.NC}")
        return False

    try:
        obb_size = int(obb_size_str)
        # Đảm bảo thư mục temp tồn tại
        if not p_temp.exists():
            p_temp.mkdir(parents=True, exist_ok=True)
            
        with open(p_temp / "size_obb.ini", "w") as f:
            f.write(str(obb_size))
    except ValueError:
        print(f"{Colors.LRED}Error: Invalid OBB zip file size.{Colors.NC}")
        return False

    unzip_result = os.system("unzip *.obb.zip")
    time.sleep(1)

    for item in p_unzip.glob("*.zip"):
        if ".obb" in item.name:
            try:
                shutil.move(str(item), str(p_temp / item.name))
            except Exception as e:
                print(f"Error moving to temp: {e}")

    if unzip_result == 0:
        print()
        print(f"{Colors.LGREEN}► UN-COMPRESS OBB SUCCESSFUL{Colors.NC}")
        print()
        return True
    else:
        print()
        print(f"{Colors.LRED}► UN-COMPRESS OBB FAILED{Colors.NC}")
        print()
        return False
 
# ==========================================
# CÁC CHẾ ĐỘ (MODES)
# ==========================================

# Đảm bảo bạn đã import Path ở đầu file (nếu chưa có thì thêm vào):
from pathlib import Path, PurePath

def run_repack_skin_logic():
    clear_screen()
    rainbow_print(">>> REPACK SKIN <<<", speed=0.005)
    
    # 1. GIẢI NÉN
    rainbow_print("\n[1/3] GIẢI NÉN OBB...", speed=0.005)
    unzipobb()
    
    # 2. TÌM VÀ REPACK
     
    rainbow_print("\n[2/3] REPACK SKIN...", speed=0.005)
    
    # --- SỬA LỖI Ở ĐÂY: Dùng Path(UNZIPOBB) ---
    found_paks = list(Path(UNZIPOBB).rglob("mini_obb.pak"))
    
    if not found_paks:
        print(f"{Colors.LRED}LỖI: Không tìm thấy 'mini_obb.pak' trong OBB.{Colors.NC}")
        input("Nhấn Enter để quay lại...")
        return

    target_pak_path = found_paks[0]
    print(f"► PAK TARGET: {Colors.LCYAN}{target_pak_path}{Colors.NC}")

    # --- SỬA LỖI Ở ĐÂY: Dùng Path(REPACK_DIR) ---
    if not Path(REPACK_DIR).exists():
        print(f"{Colors.LRED}LỖI: Thư mục REPACK chưa được tạo.{Colors.NC}")
        input("Nhấn Enter để quay lại...")
        return

    try:
        pak_file = TencentPakFile(PurePath(target_pak_path))
        pak_file.repack(REPACK_DIR, target_pak_path) # Gọi hàm tự động ở trên
    except Exception as e:
        print(f"{Colors.LRED}Lỗi: {e}{Colors.NC}")
        return

    # 3. NÉN LẠI
     
    rainbow_print("\n[3/3] NÉN LẠI OBB...", speed=0.005)
    rezipobb()
    
    rainbow_print("\n>>> XONG! SKIN ĐÃ ĐƯỢC REPACK THÀNH CÔNG <<<", speed=0.005)
    print(f"{Colors.LGREEN}Vào game và thưởng thức!{Colors.NC}")
    rainbow_print("━"*54, speed=0.005)
    input(f"{Colors.YELLOW}Nhấn Enter để quay lại menu...{Colors.NC}")
    
def modskin():    

    while True:
        clear_screen()
        
    
        
        menu_text = (
            "\n" + "━"*6 + " MAIN MENU SKIN TOOL " + "━"*6 + "\n"
            "[1] SKIN LOBBY\n"
            "[2] SKIN INGAME\n"
            "[3] GUN ACCESSORIES\n"
            "[4] HIT EFFECT\n"
            "[5] DEADBOX\n"
            "[6] EXIT\n"
            + "━"*33
        )
        
        rainbow_print(menu_text, speed=0.005)
        rainbow_prompt("Nhập lựa chọn : ", speed=0.01)
        choice = input()
        
        if choice == '1':
            run_skin_lobby()
        elif choice == '2':
            run_skin_ingame()
        elif choice == '3':
            run_skin_accessories()
        elif choice == '4':
            run_skin_hit_effect()
        elif choice == '5':
            run_skin_deadbox()
        elif choice == '6':        
            rainbow_print("Thoát", speed=0.005)
            return 
        else:
            rainbow_print("Đầu vào không hợp lệ. Vui lòng thử lại.", speed=0.005)
            time.sleep(1)


def main():
    clear_screen()
    create_folder_skin()
    create_folder_id()    
    

    while True:
        clear_screen()
        
        
        menu_text = (
            "\n" + "━"*6 + " MAIN MENU SKIN TOOL " + "━"*6 + "\n"
            "[1] MOD SKIN\n"
            "[2] REPACK SKIN\n"
            "[3] EXIT\n"
            + "━"*33
        )
        
        rainbow_print(menu_text, speed=0.005)
        rainbow_prompt("Nhập lựa chọn : ", speed=0.01)
        choice = input()
        
        if choice == '1':
            modskin()
        elif choice == '2':
            run_repack_skin_logic()
        elif choice == '3':             
            rainbow_print("Thoát", speed=0.005)
            sys.exit()
        else:
            rainbow_print("Đầu vào không hợp lệ. Vui lòng thử lại.", speed=0.005)
            time.sleep(1)

if __name__ == "__main__":
    main()


elif option == "7":
    add_skin_ids(id_skin_lobby)

elif option == "8":
    add_skin_ids(id_skin_ingame)
