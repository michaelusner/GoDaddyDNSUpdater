# GoDaddyDNSUpdater
Updates GoDaddy DNS records to your current IP.  Useful as a dynamic DNS update tool if you don't want to use
freedns.afraid.org or dyndns.org etc.

This program will update your main domain name to point to your local IP address.
The default name for your domain record is '@'.
If you have a subdomain, you can change the 'record' field in data.py from '@' to your subdomain name.

USAGE:
1) Fill out the relevant fields in the data.py file.  You can obtain the secret and key from
   https://developer.godaddy.com/
2) Run the utility on your local system to update the DNS record for GoDaddy.
