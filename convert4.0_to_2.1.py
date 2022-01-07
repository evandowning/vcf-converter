#!/usr/bin/env python3

import sys

class Contact:
    def __init__(self):
        self.name = ''
        self.phone = list()
        self.email = list()
        self.addr = ''

def usage():
    sys.stdout.write('usage: python convert.py input.vcf output.vcf\n')
    sys.exit(2)

def _main():
    if len(sys.argv) != 3:
        usage()

    inFN = sys.argv[1]
    outFN = sys.argv[2]

    # List of contacts
    contacts = list()

    read = 0
    c = Contact()

    # Read in VCF 4.0 file
    with open(inFN,'r') as fr:
        for line in fr:
            line = line.strip('\n\r')

            # Initialize new contact
            if line == 'BEGIN:VCARD':
                read = 1
                c = Contact()
                continue

            # End new contact
            if line == 'END:VCARD':
                read = 0
                contacts.append(c)
                continue

            # Read content into contact
            if read == 1:
                key = 'FN;'
                if line[:len(key)] == key:
                    c.name = line[len(key):]
                    c.name = c.name.split(':',1)[1]

                key = 'TEL;'
                if line[:len(key)] == key:
                    pn = line[len(key):]
                    pn = pn.split(':',1)[1]
                    c.phone.append(pn)

                key = 'EMAIL'
                if key in line:
                    pos = line.rfind(':')
                    e = line[pos+1:]
                    c.email.append(e)

                key = 'ADR;'
                if line[:len(key)] == key:
                    _,street,city,state,zipcode = line.rsplit(';', 4)
                    c.addr = '{0}, {1}, {2} {3}'.format(street,city,state,zipcode)

    sys.stdout.write('{0} Contacts read\n'.format(len(contacts)))

    # Write to VCF 2.1 file
    with open(outFN,'w') as fw:
        for c in contacts:
            fw.write('BEGIN:VCARD\n')
            fw.write('VERSION:2.1\n')

            if len(c.name.split(' ')) > 1:
                firstname = c.name.split(' ',1)[0]
                lastname = c.name.split(' ',1)[1]

                fw.write('N:{0};{1};;;\n'.format(lastname, firstname))
                fw.write('FN:{0} {1}\n'.format(firstname, lastname))
            else:
                fw.write('N:{0};;;;\n'.format(c.name))
                fw.write('FN:{0}\n'.format(c.name))

            for i,pn in enumerate(c.phone):
                fw.write('TEL;X-{0}:{1}\n'.format(i,pn))

            for i,e in enumerate(c.email):
                fw.write('EMAIL;X-{0}:{1}\n'.format(i,e))

            if len(c.addr) > 0:
                addr = '='.join([hex(ord(c)).replace('0x','').upper() for c in c.addr])
                fw.write('ADR;X-0;ENCODING=QUOTED-PRINTABLE:;;{0};;;;\n'.format(addr))

            fw.write('END:VCARD\n')

if __name__ == '__main__':
    _main()
