# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from handgesturerecognition.myapp.models import Image
from handgesturerecognition.myapp.forms import ImageForm
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib
import json
import cv2
import os
import cPickle
import pickle
import gzip
from skimage.feature import hog
from django.contrib import messages

letters = ["a", "b", "v", "g", "d", "gj", "e", "zh", "z", "dj", "i", "j", "k", "l", "lj", "m", "n", "nj", "o", "p", "r", "s", "t", "kj", "u", "f", "h", "c", "ch", "dz", "sh"]

def imageUpload(request):
    # File upload
    y = ''

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            
            y = predict(request)
            newImg = Image(image=request.FILES['image'])
            newImg.save()

            # Redirect to the document imageUpload after POST
            return HttpResponseRedirect(reverse('imageUpload'))
    else:
        form = ImageForm()  # An empty form


    # Load documents for the imageUpload page
    documents = Image.objects.all()
   
    # Render imageUpload page with the documents and the form
    return render(
        request,
        'imageUpload.html',
        {'documents': documents, 'form': form, 'output': y}
    )


@csrf_exempt
def predict(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    testing_set = []

    # check to see if this is a post request
    if request.method == "POST":

        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
          # grab the uploaded image
          image = _grab_image(stream=request.FILES["image"])

        # otherwise, assume that a URL was passed in
        else:
          # grab the URL from the request
          url = request.POST.get("url", None)

          # if the URL is None, then return an error
          if url is None:
              data["error"] = "No URL provided."
              return JsonResponse(data)

          # load the image and convert
          image = _grab_image(url=url)

        # convert the image to grayscale, load the face cascade detector,
        # and detect faces in the image
        hist = hog(image, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        testing_set.append(hist)
        clf = load_zipped_pickle('pickled_data')
        y = clf.predict(testing_set)
        output = letters[int(y)]

        # update the data dictionary with the faces detected
        data.update({"predicted output": output, "success": True})
        messages.info(request, 'Предвидениот знак е: %s. Пробајте одново:' %output)
        # jj_data = jsonify(data)

    # return a JSON response
    return output


def _grab_image(path=None, stream=None, url=None):
    # if the path is not None, then load the image from disk
    if path is not None:
        g_image = cv2.imread(path, 0)
        g_image = cv2.resize(g_image, (640, 480)) 

    # # otherwise, the image does not reside on disk
    # else: 
    #   # if the URL is not None, then download the image
    if url is not None:
        resp = urllib.urlopen(url)
        data = resp.read()
    
    #   # if the stream is not None, then the image has been uploaded
    elif stream is not None:
        data = stream.read()

    #   # convert the image to a NumPy array and then read it into
    #   # OpenCV format

    g_image = np.asarray(bytearray(data), dtype="uint8")
    g_image = cv2.imdecode(g_image, 0)
 
    # return the image
    return g_image


def jsonify(data):
    json_data = dict()
    for key, value in data.iteritems():
        if isinstance(value, imageUpload): # for imageUploads
            value = [ jsonify(item) if isinstance(item, dict) else item for item in value ]
        if isinstance(value, dict): # for nested imageUploads
            value = jsonify(value)
        if isinstance(key, int): # if key is integer: > to string
            key = str(key)
        if type(value).__module__=='numpy': # if value is numpy.*: > to python imageUpload
            value = value.toimageUpload()
        json_data[key] = value
    return json_data


def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = cPickle.load(f)
        return loaded_object
