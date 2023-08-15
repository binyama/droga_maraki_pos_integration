import os
import time
import xml.etree.ElementTree as ET
import helper
from bs4 import BeautifulSoup
from datetime import datetime


def update_invoice_with_pos_data():
    for filename in os.listdir(helper.pos_url):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(helper.pos_url, filename)
        # tree = ET.parse(fullname)

        # Reading the data inside the xml
        # file to a variable under the name
        # data
        with open(fullname, 'r') as f:
            data = f.read()

        # Passing the stored data inside
        # the beautifulsoup parser, storing
        # the returned object
        Bs_data = BeautifulSoup(data, "xml")

        # Using find() to extract attributes
        # of the first instance of the tag
        invoice_status = Bs_data.find_all('Invoice_Response')

        for inv_status in invoice_status:
            # printed = inv_status.find_all('printed')[0].text
            reference_number = inv_status.find_all('Reference_Number')[0].text
            # print_date = inv_status.find_all('print_date')[0].text
            fs_no = inv_status.find_all('FS_Number')[0].text

            # search invoice number
            # check existing attendance
            account_move = helper.models.execute_kw(helper.odoo_db, helper.uid, helper.odoo_password, 'account.move',
                                                    'search_read',
                                                    [[['name', '=', reference_number], ['company_id', '=', 2]]],
                                                    {'fields': ['id', 'name'], 'limit': 5})
            if account_move is not None:
                # update the record
                dt = datetime.utcnow()
                today = dt.strftime("%Y-%m-%d %H:%M:%S")
                status = helper.models.execute_kw(helper.odoo_db, helper.uid, helper.odoo_password, 'account.move',
                                                  'write', [[account_move[0]['id']], {'FSInvoiceNumber': fs_no,
                                                                                      'FTimeStamp': today,
                                                                                      'FPMachineID': 'BEB0049492'}])

                if status:
                    # delete file
                    os.remove(path=fullname)


def main():
    while True:
        update_invoice_with_pos_data()
        time.sleep(int(helper.service_run_time))


if __name__ == "__main__":
    main()
