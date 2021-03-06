# GoDaddyDNSUpdater
If you want to be able to access your home network remotely but your ISP uses dynamic IP addresses, then this utility is for you.

Using this, you can update your GoDaddy DNS records to your current IP.  Useful as a dynamic DNS update tool if you don't want to use
freedns.afraid.org or dyndns.org etc.  I run it from a Raspberry PI.

This program will update your main domain name to point to your local IP address.
The default name for your domain record is '@'.
If you have a subdomain, you can change the 'RECORD' field in your .env file or environment variables from '@' to your subdomain name.

Note that if an IP update is not necessary, the utility will not perform it.

## Installation

(This utility should be compatible with Python2 and Python3 - let's please not use python2 though, OK?)
* Though instructions are taylored toward Linux, this utility should work fine in Windows as well.
* Please consider using a virtual environment to isolate requirements: https://docs.python-guide.org/dev/virtualenvs/

```
python3 -m virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## USAGE
1) Fill out the relevant fields in the .env file or environment variables.

    # Your GoDaddy API key
    KEY = "<key>"

    # Your GoDaddy API secret key"
    SECRET = "<secret>"

    # Your domain name - ex: example.com"
    DOMAIN = "example.com"

   You can obtain the secret and key from
   https://developer.godaddy.com/

2) Run the utility on your local system to update the DNS record for GoDaddy.
  ```
  > source .venv/bin/activate
  > python set_ip.py
  ```
   
It's recommended that you set up a cron job to execute periodically
