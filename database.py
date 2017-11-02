#coding=utf-8
import sys, shelve

dbfilename = 'people-file'
ENDDB = 'enddb.'
ENDREC = 'endrec.'
RECSEP = '=>'

def store_person(db):
    pid = raw_input('Enter unique ID number:')
    person = {}
    person['name'] = raw_input('Enter namme:')
    person['age'] = raw_input('Enter age:')
    person['phone'] = raw_input('Enter phone number:')

    db[pid] = person

def lookup_person(db):
    pid = raw_input('Enter ID number:')
    field = raw_input('What would you like to know?(name, age, phone)')
    field = field.strip().lower()
    print(field.capitalize() + ':', db[pid][field])

def print_help():
    print('The available  commands are:')
    print('store : Stores information about a person')
    print('lookup :  Looks up a person from ID number')
    print('quit : Save changes and exit')
    print('? : Prints this message')

def enter_command():
    cmd = raw_input('Enter command (? for help): ')
    cmd = cmd.strip().lower()
    return cmd


def storeDbase(db, dbfilename=dbfilename):
    dbfile = open(dbfilename, 'w')
    for (key, value) in db.items():
        #print(key, file=dbfilename)
        dbfile.write(key)
        dbfile.write("\n")
        for (name, value_attr) in value.items():
            #print(name + RECSEP + repr(value), file=dbfile)
            dbfile.write(name+RECSEP + repr(value_attr))
            dbfile.write("\n")
        #print(ENDREC, file=dbfile)
        dbfile.write(ENDREC)
        dbfile.write("\n")
    #print(ENDDB, file=dbfile)
    dbfile.write(ENDDB)
    dbfile.close()


def loadDbase(dbfilename=dbfilename):
    dbfile = open(dbfilename)
    import sys
    sys.stdin = dbfile
    db = {}
    while key != ENDDB:
        rec = {}
        field = input()
        while field != field.split(RECSEP):
            name, value = field.split(RECSEP)
            rec[name] = eval(value)
            field = input()
        db[key] = rec
        key = input()
    return db



def main():
    database = shelve.open('database.dat')
    try:
        while True:
            cmd = enter_command()
            if cmd == 'store':
                store_person(database)
            elif cmd == 'lookup':
                lookup_person(database)
            elif cmd == '?':
                print_help()
            elif cmd == 'quit':
                return
    finally:
        database.close()

def execute():
    from initdata import db
    storeDbase(db)

if __name__ == '__main__':
    execute()

