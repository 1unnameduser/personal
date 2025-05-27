from instagrapi import Client # type: ignore
import os, var

os.chdir(os.path.dirname(os.path.realpath(__file__)))
account = {'username': var.instUSERNAME, 'password': var.instPASSWORD}

cl = Client()
cl.set_proxy("socks5://127.0.0.1:1080")
cl.login(account['username'], account['password'])
cl.dump_settings("instagram_session.json")