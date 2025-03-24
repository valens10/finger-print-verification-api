import ctypes
import random
import string, time
from django.core.files.storage import default_storage

# Constants (replace these with actual values)
DPFJ_FMD_DP_REG_FEATURES = 1  # Example value
DPFJ_FMD_DP_VER_FEATURES = 2  # Example value
DPFJ_FMD_DP_PRE_REG_FEATURES = 0  # Example value
DPFJ_E_MORE_DATA = 96075789  # Example value
THRESHOLD_RATE = 0.5

#Load the library (update path if needed)
dpfj_lib = ctypes.CDLL("/usr/lib64/libdpfj.so")
dpfjdd_lib = ctypes.CDLL("/usr/lib64/libdpfpdd.so")

# dpfj_lib = ctypes.CDLL("dpfj.dll")
# dpfjdd_lib = ctypes.CDLL("dpfpdd.dll")

# Function to read a file as bytes
def read_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return (ctypes.c_ubyte * len(data))(*data), len(data)

def handle_start_enrollment():
    dpfjdd_lib.dpfpdd_init()
    result = dpfj_lib.dpfj_start_enrollment(ctypes.c_uint(DPFJ_FMD_DP_REG_FEATURES))
    return result

def handle_add_to_enrollment(data, size):
    result = dpfj_lib.dpfj_add_to_enrollment(ctypes.c_uint(DPFJ_FMD_DP_PRE_REG_FEATURES), data, ctypes.c_uint(size), 0)
    return result

def handle_generate_finger_print_template(size2):
    result = dpfj_lib.dpfj_create_enrollment_fmd(None, ctypes.byref(size2))
    return result

def handle_create_enrollement(data2, size2):
    result = dpfj_lib.dpfj_create_enrollment_fmd(data2, ctypes.byref(size2))
    return result

def handle_finish_enrollement():
    result = dpfj_lib.dpfj_finish_enrollment()
    return result

def handle_verification(data1, size1, data2, size2,falsematch_rate):
    result = dpfj_lib.dpfj_compare(
            ctypes.c_uint(DPFJ_FMD_DP_VER_FEATURES), data1, size1, ctypes.c_uint(0),
            ctypes.c_uint(DPFJ_FMD_DP_REG_FEATURES), data2, size2, ctypes.c_uint(0),
            ctypes.byref(falsematch_rate)
        )
    return result


def generate_random_filename(extension: str = 'bin') -> str:
    """Generate a random filename using timestamp and random characters."""
    timestamp = str(int(time.time()))  # Get current timestamp
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Random alphanumeric string
    return f"FeatureSet_{timestamp}_{random_string}.{extension}"

# Function to delete the saved fingerprint file
def delete_fingerprint_file(file_path):
    try:
        default_storage.delete(file_path)
    except Exception as e:
        print(f"Failed to delete file {file_path}: {str(e)}")