import io

import cv2
import numpy as np
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.baseconv import base64
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from . import stickerGen


@require_http_methods(["POST"])
@csrf_exempt
def getSticks(request):
    back= 'createFace/resource/'+request.POST.get('name', '')+'.jpg'
    #print(back)
    file=request.FILES['image']
    #print(type(file))
    #print(file.read())
    bytesfile=file.read()
    image=Image.open(io.BytesIO(bytesfile))
    pil_image = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    sticker=stickerGen.create_expression(pil_image, back)
    result=Image.fromarray(sticker)

    result.save('./temp.jpg', 'jpeg')
    # 从内存中取出bytes类型的图片
    f = io.FileIO('./temp.jpg')
    data = f.read()
    # 将bytes转成base64
    #data = base64.b64encode(data).decode()
    #return data
    return HttpResponse(data, content_type='image/jpeg')
