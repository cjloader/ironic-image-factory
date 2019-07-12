import os
import sys
import urllib3
from keystoneauth1.identity import v3
from keystoneauth1 import session as keystone_session
from keystoneclient.v3 import client as keystone_client
from ironicclient import client as ironic_client
from novaclient import client as nova_client
import glanceclient
import wget
import tempfile
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CLIENTS = {}


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

    url = ('http://84101b01061cb1b0b6e9-f697b3e19d8f61d62243203199cd335f'
           '.r43.cf5.rackcdn.com/Alpine/3.9/'
           '2019-07-08/alpine-3.9-2019-07-08.qcow2')
    
    glance = CLIENTS['glance']

    images = glance.images.list()

    with tempfile.TemporaryDirectory() as tempdir:
         image_download = wget.download(url, tempdir)
         print(image_download)

    if head.headers[‘ETag’] not in[image.checksum for image in images]:
        
        glance_image = glance.images.create(name="alpine-3.9-2019-07-08", is_public="True", disk_format="qcow2",
                        container_format="bare", tags=["RackspaceManaged"])
    print('')
    print("Uploading images to Glance")
    
    glance.images.upload(glance_image.id, open('alpine-3.9-2019-07-08.qcow2', 'rb'))

    
def main():
    load_auth_clients()
    upload_new_images()

    print("Image Updates are Complete")


if __name__ == "__main__":
    main()
