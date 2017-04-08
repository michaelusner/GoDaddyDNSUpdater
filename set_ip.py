'''
******************************************************************************
MIT License

Copyright (c) 2017 Michael Usner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
******************************************************************************

This program uses the GoDaddy API to set your DNS name to point to
your home IP address.
It is intended to be used in a cron job or run with a scheduler.

This utility is compatible with Python2/3.

Package requirements: requests>=2.4.3
Install with "pip install requests"

You need to create a 'data.py' file with the following information
obtained from GoDaddy:
key = '<your API key>'
secret = '<your secret key>'
domain = 'your domain name (i.e. example.com)'

See https://developer.godaddy.com/ for more information.
'''
import json
import requests
import data


class ApiException(Exception):
    ''' Generic exception class '''
    pass


def get_godaddy_record_ip(domain, record, key, secret):
    '''
    Get the IP associated with the domain DNS record.
    Arguments:
    domain: The domain need
    record: The DNS record.  Note that the main domain record is '@'
    key: Your API key
    secret: Your API secret
    '''
    response = requests.get(
        'https://api.godaddy.com/v1/domains/{}/records/A/{}'.
        format(domain, record),
        headers={'Authorization': 'sso-key {}:{}'.format(key, secret)})
    if response.status_code != 200:
        raise ApiException('Failed to retrieve DNS record for {}/{}'.format(domain, record))
    return json.loads(response.text)[0]['data'].strip()


def get_current_ip():
    ''' Get the current IP of your internet connection. '''
    return json.loads(requests.get('http://ipinfo.io/json').text)['ip'].strip()


def set_godaddy_dns_ip(domain=None, record='@', key=None, secret=None, ip_address=None):
    '''
    Update a GoDaddy DNS record

    Arguments:
    domain: The domain need
    record: The DNS record.  Note that the main domain record is '@'
    key: Your API key
    secret: Your API secret
    '''
    # make sure the data is valid
    if domain is None:
        print("No domain name provided")
    if key is None:
        print("No API key provided")
        return False
    if secret is None:
        print("No secret key provided")
        return False
    if ip_address is None:
        print("No IP address provided")

    # make the API request to GoDaddy to set the IP
    response = requests.put(
        'https://api.godaddy.com/v1/domains/{}/records/A/{}'.format(domain, record),
        headers={
            'Authorization': 'sso-key {}:{}'.format(key, secret),
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'ttl': 3600,
            'data': ip_address
        })
    )
    # handle any issues
    if response.status_code != 200:
        raise ApiException(
            'Failed to set IP.  Status code was {}.  Error was: {}'.format(
                response.status_code,
                response.text))
    return True


def update_godaddy_record(domain, record, key, secret):
    ''' Update a DNS record for a GoDaddy domain '''
    # get the GoDaddy record IP and the current IP
    godaddy_ip = get_godaddy_record_ip(domain, record, key, secret)
    current_ip = get_current_ip()
    print('Current DNS IP Address: {}'.format(godaddy_ip))
    print('Current IP Address:     {}'.format(current_ip))

    # if they're different, update the GoDaddy record
    if godaddy_ip == current_ip:
        print('No update necessary.')
        return current_ip
    else:
        print('\nUpdating DNS IP to {}'.format(current_ip))
        if not set_godaddy_dns_ip(domain, record, key, secret, current_ip):
            return None
        if get_godaddy_record_ip(domain, record, key, secret) == current_ip:
            print("Successfully set {}/{} to {}".format(domain, record, current_ip))
            return current_ip


if __name__ == '__main__':
    if update_godaddy_record(data.DOMAIN, data.RECORD, data.KEY, data.SECRET) is not None:
        exit(0)
    else:
        print("Failed to set GoDaddy DNS record IP")
        exit(-1)
