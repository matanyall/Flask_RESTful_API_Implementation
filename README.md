# User Game Scores REST API
Flask is configured in pyarcade_rest/__init__.py is configured to use an in-memory sqlite database if FLASK_ENV=test and to use a MySQL database if FLASK_ENV=production. You can configure FLASK_ENV in PyCharm by editing the run configurations (usually a dropdown in the top right with an option called edit configurations) and changing the Environment Variables to be FLASK_ENV=test

Instance link: ec2-18-144-7-192.us-west-1.compute.amazonaws.com

IMPORTANT: I think there was a typo in the instructions for the run.sh script, and this only works if run as `./run.sh [domain name]:80` instead of `./run.sh [domain name]/5000`. I think the reason for this is because the port was forwarded from 5000 to 80, and because the way to specify a port in a URL is with `:`, not `/`.