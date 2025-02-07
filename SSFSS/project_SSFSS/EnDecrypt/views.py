# EnDecrypt
# views.py
from django.http import JsonResponse
from .models import EncryptedFile
from django.core.files.base import ContentFile
from uuid import UUID
from django.http import HttpResponseBadRequest, HttpResponseServerError, FileResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .decryptor import Decryptor
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import EncryptedFile, DecryptedFile
from django.conf import settings
from base64 import b64encode, b64decode
from .encryptor import Encryptor
from django.contrib.auth import get_user_model
import os
import binascii

import uuid

import tempfile

from registration.models import User


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        user_id = request.POST.get('user_id')
        if not uploaded_file:
            return HttpResponseBadRequest('No file provided')

        if uploaded_file:
            # Generate a random encryption key (you may change this as needed)
            key_u = os.urandom(16)
            key = b64encode(key_u).decode('utf-8')
            # Convert bytes to hexadecimal string
            key_hex = binascii.hexlify(key_u).decode('utf-8')
            print(f"geenrated key:{key}")
            print(f"geenrated key_hex:{key_hex}")
            print(f"geenrated ultimate key:{key_u}")
            try:
                # Initialize the Encryptor with the key
                print('sa')
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)

                enc = Encryptor(key)

                encrypted_file_id = uuid.uuid4()
                # Encrypt the uploaded file and get the path to the encrypted file
                encrypted_file_path = enc.encrypt_file(
                    temp_file.name, encrypted_file_id.hex)
                # Generate a unique ID for the encrypted file
                encrypted_data = encrypted_file_path[0]
                encrypted_file_path = encrypted_file_path[1]
                print(f"get path:{encrypted_file_path}")

                print(f"get data:{encrypted_data}")
                os.remove(temp_file.name)

                # Debugging: Print the user_id
                print(f"Received user_id: {user_id}")

                try:
                    user = User.objects.get(user_id=user_id)
                    print(f"Found user: {user.user_id}")
                except User.DoesNotExist:
                    return HttpResponseBadRequest('User not found')

               # user = get_user_model().objects.get(id=user_id)
                encrypted_file = EncryptedFile.objects.create(
                    user=user,
                    encrypted_file=encrypted_file_path,
                    original_file_name=uploaded_file.name,
                    encryption_key=key,
                    # Set the unique ID
                    encrypted_file_id=encrypted_file_id.hex
                )
                print(f"hahah:{encrypted_file.encrypted_file.url}")
                # Return the path to the encrypted file as a response
                encrypted_file_url = encrypted_file.encrypted_file.url  # Get the URL

                encrypted_file_url = encrypted_file_url.replace(
                    '/media/', '/', 1)

                encrypted_datas = b64encode(encrypted_data).decode('utf-8')
                encrypted_data = binascii.hexlify(
                    encrypted_data).decode('utf-8')
                response_data = {
                    'encrypted_file': encrypted_file_url,

                    #        'encryption_key': key  # Include the key in the response
                    'encryption_key': key,  # Include the hexadecimal key in the response
                    'encrypted_file_id': encrypted_file_id.hex  # Include the unique ID
                    , 'encrypted_datas': encrypted_datas,
                    'encrypted_data_hex': encrypted_data
                }
                # response_data.write(encrypted_data)
                return JsonResponse(response_data)

                # response = FileResponse(open(encrypted_file_path, 'rb'))
                # response['Content-Disposition'] = f'attachment; filename="{encrypted_file.original_file_name}.enc"'

                # return response
            except Exception as e:
                return HttpResponseBadRequest('Error during encryption: {}'.format(str(e)))
    return JsonResponse({'error': 'Invalid request'})


@csrf_exempt
def decrypt_file(request):
    if request.method == 'POST':
        encryption_key = request.POST.get('encryption_key')
        encrypted_file_id = request.POST.get('encrypted_file_id')

        # Check if encryption_key and encrypted_file_id are not empty or None
        if not encryption_key or not encrypted_file_id:
            return HttpResponseBadRequest('Missing encryption key or encrypted file ID')

        try:
            # Convert the received encrypted_file_id to a UUID object
            decrypted_file_uuid = UUID(encrypted_file_id)

            # Fetch the encrypted file from the database
            try:
                encrypted_file = EncryptedFile.objects.get(
                    encrypted_file_id=decrypted_file_uuid)
            except ObjectDoesNotExist:
                return HttpResponseBadRequest('Encrypted file not found')

            # Check if the encrypted file exists at the expected path
            # expected_encryption_path = os.path.join(
            #    settings.MEDIA_ROOT, encrypted_file.encrypted_file.name)
            # print(f"expected {expected_encryption_path}")
            # if not os.path.exists(expected_encryption_path):
            #    return HttpResponseBadRequest('EnScrypted file not found')

            # Key is used correctly as a string
            key = encryption_key
            decryptor = Decryptor(key)

            print(f"hello:{encrypted_file.encrypted_file.path}")
            encrypted_file_url = encrypted_file.encrypted_file.path  # Get the URL

            encrypted_file_url = encrypted_file_url.replace(
                '/media/', '/', 1)

            decrypted_data = decryptor.decrypt_file(
                encrypted_file_url)

            # Check if decryption was successful
            if decrypted_data is None:
                return HttpResponseServerError('Decryption failed')

            # Prepare the response with the decrypted file for download
            response = HttpResponse(content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{encrypted_file.original_file_name}"'

            # Write the decrypted data to the response
            response.write(decrypted_data)

            return response
        except Exception as e:
            print(f"Error during decryption: {str(e)}")
            return HttpResponseServerError(f'Error during decryption: {str(e)}')

    return HttpResponseBadRequest('Invalid request')


@csrf_exempt
def download_encrypted_file(request, encrypted_file_id):
    try:
        encrypted_file = EncryptedFile.objects.get(
            encrypted_file_id=encrypted_file_id)

        # Specify the path to the encrypted file on the server
        encrypted_file_path = encrypted_file.encrypted_file.path
       # encrypted_file_url = encrypted_file.encrypted_file.url  # Get the URL

        # Remove one "media" from the URL
       # encrypted_file_path = encrypted_file_url.replace('/media/', '/', 1)

        # Prepare the response with the encrypted file for download
        response = FileResponse(open(encrypted_file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{encrypted_file.original_file_name}.enc"'

        return response
    except Exception as e:
        return HttpResponseBadRequest('Error during download: {}'.format(str(e)))


@csrf_exempt
def get_user_encrypted_files(request):
    try:
        # Get the user_id from the JSON request body
        data = json.loads(request.body)
        user_id = data.get('user_id')
        if user_id is not None:
            # Add this line for debugging
            print(f"Received user_id: {user_id}")

            encrypted_files = EncryptedFile.objects.filter(user=user_id)
            data = [{
                'original_file_name': file.original_file_name,
                'encrypted_file_id': str(file.encrypted_file_id),
                'user_id': user_id,
            } for file in encrypted_files]
            return JsonResponse({'encrypted_files': data})
        else:
            return HttpResponseBadRequest('Missing user_id')
    except User.DoesNotExist:
        return HttpResponseBadRequest('User not found')
