#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib import request, error
import images
import json
import os


def gen_v1_list_tags_url(namespace, repository):
    return '/v1/repositories/' + namespace + '/' + repository + '/tags'


def gen_v2_list_tags_url(namespace, repository):
    return '/v2/' + namespace + '/' + repository + '/tags/list'


def get_tag_url(image_url):
    [domain, namespace, repository] = image_url.split('/')

    if domain == 'gcr.io':
        return 'https://gcr.io' + gen_v2_list_tags_url(namespace, repository)
    elif domain == 'quay.io':
        return 'https://quay.io' + gen_v1_list_tags_url(namespace, repository)


def to_kebab_case(str):
    return str.replace('/', '.')

for image_url, tags in images.IMAGES.items():
    print('dealing with ' + image_url)

    image_name = image_url.split('/')[-1]

    for tag in tags:
        cwd = os.getcwd()
        dir_name = to_kebab_case(image_url)
        filepath = os.path.join(cwd, dir_name, tag, 'Dockerfile')

        try:
            docker_file = open(filepath, 'w+')

        except IOError:
            os.makedirs(os.path.dirname(filepath))
            docker_file = open(filepath, 'w+')

        print('FROM ' + image_url + ':' + tag, file=docker_file)
