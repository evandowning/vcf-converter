import sys
import re

class Contact:
    def __init__(self):
        self.name = ''
        self.phone = list()
        self.email = list()
        self.addr = ''

def usage():
    print 'usage: python convert.py input.vcf output.vcf'
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
                key = 'FN:'
                if line[:len(key)] == key:
                    c.name = line[len(key):]

                key = 'TEL;TYPE='
                if line[:len(key)] == key:
                    pn = line[len(key):]
                    c.phone.append(pn)

                key = 'EMAIL'
                if key in line:
                    pos = line.rfind(':')
                    e = line[pos+1:]
                    c.email.append(e)

                key = 'ADR'
                if line[:len(key)] == key:
                    f = re.findall(r'\d+',line)
                    pos = line.find(f[0])
                    addr = line[pos:]
                    c.addr = addr

    print '{0} Contacts read'.format(len(contacts))

    # Write to VCF 2.1 file
    with open(outFN,'w') as fw:
        for c in contacts:
            fw.write('BEGIN:VCARD\n')
            fw.write('VERSION:2.1\n')
            fw.write('FN:{0}\n'.format(c.name))

            for pn in c.phone:
                fw.write('TEL;{0}\n'.format(pn))

            for i,e in enumerate(c.email):
                fw.write('EMAIL;{0}:{1}\n'.format(i,e))

            fw.write('ADR;HOME:;;{0}\n'.format(c.addr))

            fw.write('END:VCARD\n')

if __name__ == '__main__':
    _main()
