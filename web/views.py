from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage

import os

from web.detectionSNP import detection, getCharacteristic

class Test(APIView):
    def get(self, request):
        return Response({
            "Response" : "success"
        })

class Result(APIView):
    def get(self, request):

        user_id = request.data.get('user_id')

        csv_filename = user_id + ".csv"
        directory_name = 'genome_file'

        current_directory = os.getcwd()
        csv_path = os.path.join(current_directory, directory_name)
        csv_path = os.path.join(csv_path, csv_filename)

        if os.path.isfile(csv_path):
            find_snp_list = detection(csv_path)
            result = getCharacteristic(find_snp_list)
            print(result)
        else:
            error_message = "CSV 파일 " + csv_filename + "가 존재하지 않습니다."
            return HttpResponseNotFound(error_message)

        return Response(result)
        
class Upload(APIView):
    def get(self, request):
        user_id = request.data.get('user_id') #사용자 아이디 6자리
        genome_file = request.FILES['genome_file'] #게놈 데이터 파일

        file_storage = FileSystemStorage()
        filename = file_storage.save(user_id + ".csv", genome_file)

        if filename:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
