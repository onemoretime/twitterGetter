TwitterGetter v1.0

Prerequisites :
mysql 5+
python 2.7
twitter-1.9.2 (python module)
MySQL-python-1.2.3 (python module)

twitterGetter - my twitter-log implementation (from twitter module) for TwitterManager

reference: twitter-log - Twitter Logger/Archiver

PREREQUISITES INSTALLATION:

INSTALLATION:

USAGE:

    Main.py {(-t|--token <token> -ts|--token-secret <token secret>) | -tcfg } [-m|--max-id=<max_id>] [--quiet] <screen_name>

DESCRIPTION:

    --t|--token <token> -ts|--token-secret <token secret> are mandatory since the forced usage of API 1.1
    -tcfg indicates that token informations are in cfg file (twitter_credentials section)

    insert <screen_name>'s tweets into a database for TwitterManager frontend.
    
    -m|--max_id is optional and may be provided to ignore previously downloaded tweets 
and avoid multiple downloads.
    --quiet indicates very few output
    
WARNING:

     a massive usage of Twitter API (more than 300 downloads / 15 min / API user) implicates a ban of your account.
     a downloads limit will be add in TwitterGetter v1.1