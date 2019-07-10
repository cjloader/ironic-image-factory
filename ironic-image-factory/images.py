
import os
import sys
import urllib3
from keystoneauth1.identity import v3
from keystoneauth1 import session as keystone_session
from keystoneclient.v3 import client as keystone_client
from ironicclient import client as ironic_client
from novaclient import client as nova_client
import glanceclient
import argparse


CLIENTS = {}

def load_args():
    return parser.parse_args()


def load_auth_clients():
    auth_fields = {
        'auth_url': os.environ['OS_AUTH_URL'],
        'username': os.environ['OS_USERNAME'],
        'password': os.environ['OS_PASSWORD'],
        'project_name': os.environ['OS_PROJECT_NAME'],
        'user_domain_name': os.environ['OS_USER_DOMAIN_NAME'],
        'project_domain_name': os.environ['OS_PROJECT_DOMAIN_NAME']
    }

    v3_auth = v3.Password(**auth_fields)
    ks_sess = keystone_session.Session(auth=v3_auth, verify=False)
    ks_client = keystone_client.Client(session=ks_sess)
    CLIENTS['keystone'] = ks_client

    gl_client = glanceclient.Client('2', session=ks_sess)
    CLIENTS['glance'] = gl_client

    nv_client = nova_client.Client(2, session=ks_sess)
    CLIENTS['nova'] = nv_client

def upload_new_images():
    print("Downloading new images...")
    urllib.request.urlretrieve("https://c8dbf21d7d7507d989c7-f697b3e19d8f61d62243203199cd335f.ssl.cf5.rackcdn.com","test-image.qcow2")

    glance = CLIENTS['glance']
    glance.images.create(name="ubuntu-test", is_public=True, disk_format="qcow2",
                        container_format=“bare”, data="test-image.qcow2")

def delete_old_images():
    nova = CLIENTS['nova']
    glance = CLIENTS['glance']
    instances = nova.servers.list()
    images = glance.images.list()
    for image in images:
        for instance in instances:
            if images[image] != instance['image']:
                glance.images.delete(image)

def main():
    args = load_args()
    load_auth_clients()

    delete_old_images()
    upload_new_images()

    print("Image Updates are Complete")
