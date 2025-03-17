from django.utils.encoding import force_str
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Fingerprint
from django.core.files.storage import default_storage
from django.utils.encoding import force_bytes
from .fingerprint_scanner import read_file, handle_verification,delete_fingerprint_file, THRESHOLD_RATE, handle_create_enrollement, \
                handle_start_enrollment, handle_add_to_enrollment, DPFJ_E_MORE_DATA, handle_generate_finger_print_template, generate_random_filename
import ctypes


@api_view(['POST'])
def enroll_fingerprint(request):
    user_id = request.data.get('user_id')
    finger_print_file = request.data.get('finger_print_file')
    
    if not user_id or not finger_print_file:
        return Response({"detail": "user_id and finger_print_file are required"}, status=400)

    try:
        # Save uploaded file temporarily
        random_filename = generate_random_filename('bin')
        file_path = default_storage.save(f"{random_filename}", finger_print_file)
        
        full_path = default_storage.path(file_path) 
        data, size = read_file(full_path)

        # Start the enrollment process
        result = handle_start_enrollment()

        while True:
            result = handle_add_to_enrollment(data, size)
            if result != DPFJ_E_MORE_DATA:
                print("Enrollment is done")
                break
            print("==================More==============data===============required===========")
            
            response = {
                "detail": "More fingerprint data required", 
                'is_more_data': True
                }
            
            # Delete the saved fingerprint file
            delete_fingerprint_file(file_path)
            
            return Response({"response":response}, status=200)

        # Generate fingerprint template
        size2 = ctypes.c_uint()
        result = handle_generate_finger_print_template(size2)
        
        data2 = (ctypes.c_ubyte * size2.value)()
        result = handle_create_enrollement(data2, size2)

        if result != 0:
            # Delete the saved fingerprint file
            delete_fingerprint_file(file_path)
            return Response({"detail": "Failed to create enrollment template"}, status=400)

        # Store the fingerprint in the database
        fingerprint_instance, created = Fingerprint.objects.update_or_create(
            user_id=user_id, defaults={"template": bytes(data2)}
        )
        res_data = {
            "message": "Fingerprint enrolled successfully",
            'is_more_data': False,
            "user_id": user_id,
            "fingerprint_id": fingerprint_instance.id
            }
        
        # Delete the saved fingerprint file
        delete_fingerprint_file(file_path)
        return Response({"response": res_data}, status=201)

    except Exception as e:
        # Delete the saved fingerprint file
        delete_fingerprint_file(file_path)
        
        print(f"Enrollment failed: {str(e)}")
        return Response({"detail": "Internal server error"}, status=500)
    

@api_view(['POST'])
def verify_fingerprint(request):
    """
    Verifies the fingerprint against the stored template.
    """
    try:
        user_id = request.data.get('user_id')
        finger_print_file = request.data.get('finger_print_file')  # Expecting file upload

        if not user_id or not finger_print_file:
            return Response({"error": "user_id and fingerprint file are required"}, status=400)

        # Save file temporarily
        random_filename = generate_random_filename('bin')
        file_path = default_storage.save(f"{random_filename}", finger_print_file)
        full_path = default_storage.path(file_path) 

        # Read the uploaded fingerprint data
        data1, size1 = read_file(full_path)

        # Retrieve stored fingerprint from database
        fingerprint_instance = Fingerprint.objects.get(user_id=user_id)
        stored_template = fingerprint_instance.template  # Stored as binary data
        size2 = len(stored_template)

        # Convert stored template back to ctypes array
        data2 = (ctypes.c_ubyte * size2).from_buffer_copy(stored_template)
        
        # Perform fingerprint comparison
        falsematch_rate = ctypes.c_uint(0)
        result = handle_verification(data1, size1, data2, size2, falsematch_rate)

        verified = result == 0 and falsematch_rate.value < THRESHOLD_RATE

        response_data = {
            "verified": verified,
            "result": result,
            "falsematch_rate": falsematch_rate.value,
            "user_id": user_id,
        }

        # Delete the saved fingerprint file
        delete_fingerprint_file(file_path)
        return Response({"response": response_data}, status=200)

    except Fingerprint.DoesNotExist:
        # Delete the saved fingerprint file
        delete_fingerprint_file(file_path)
        
        return Response({"detail": "No fingerprint found for this user"}, status=404)

    except Exception as e:
        # Delete the saved fingerprint file
        delete_fingerprint_file(file_path)
        
        print(f"Fingerprint verification failed: {str(e)}")
        return Response({"detail": "Internal server error"}, status=500)