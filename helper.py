import configparser
import xmlrpc.client

# CREATE OBJECT
config_file = configparser.ConfigParser()

# READ CONFIG FILE
config_file.read("setting.ini")

# odoo configuration
odoo_url = config_file['odoo']['odoo_url']
odoo_username = config_file['odoo']['odoo_username']
odoo_password = config_file['odoo']['odoo_password']
odoo_db = config_file['odoo']['odoo_db']

# pos configuration
pos_url = config_file['pos']['pos_url']

service_run_time=config_file['background']['service_run_time']

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))

uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})

