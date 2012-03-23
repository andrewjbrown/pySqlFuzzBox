#! /usr/bin/env python

import re
import psycopg2
import sys


def main():
    if not sys.argv[1]:
        printHelp()
    elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
        printHelp()
    else:
        print 'Loading log file...\n'
        log = loadFile(sys.argv[1])
        print 'Parsing log file...\n'
        if len(sys.argv) > 2:
            pg_statments = mkSqlStatements(log, sys.argv[2])
        else:
            pg_statments = mkSqlStatements(log)
        print 'executing SQL statements...\n'
        executeSQL(pg_statments)


def printHelp():
    """
    Displays help informations for the command line

    """
    print """
    Usage: ./pg_fuzzer <postgresql log file> <SQL statement file>

    """


def loadFile(fileName):
    """
    Reads a file and returns it as an array.

    Keyword arguments:
    fileName -- the file name to open (default pgsql)

    """
    l = []
    fb = open(fileName)
    
    for line in fb:
        l.append(line)
    fb.close()
    
    return l


def mkSqlStatements(f, fileName = None):
    """
    Parses a postgresql log file and returns just the statments.

    f -- the array of the postgres log file
    fileName -- the file to write out (default = None)

    """
    p = re.compile("statement: ")
    q = re.compile("-\d\] ") 
    r = re.compile("prepare: ")
    pg = []

    if fileName: fb = open(fileName, 'w')
    
    for i in range(len(f)):
        s = ''
        if p.search(f[i]):
            s = f[i][p.search(f[i]).end(): ]
        elif r.search(f[i]):
            s = f[i][r.search(f[i]).end(): ]
        if s:
            try:
                while int(q.search(f[i + 1]).group()[1: 2]) != 1:
                    if not r.search(f[i + 1]):
                        i += 1
                        s += f[i][q.search(f[i]).end(): ]
                    elif r.search(f[i + 1]):
                        i += 1
                        s = f[i][r.search(f[i]).end(): ]
            except:
               pass
            
            pg.append(s)
            #print s
            if fileName: fb.write(s)
    
    if fileName: fb.close()
    return pg


def executeSQL(pg, db = 'resolve', user = 'postgres', password = '', 
                host = '192.168.2.151'):
    """
    Connects to a postgres database and executes a list of SQL statements.

    pg -- the list of statements to execute
    db -- the name of the database to connect to (default = resolve)
    user -- the name of the user to connect with (default = postgres)
    password -- the password to use (default = )
    host -- the host to connect to (default = 192.168.2.151)

    """
    conn = psycopg2.connect(database = db, user = user, password = password, 
                            host = host)
    cur = conn.cursor()
    
    for i in range(len(pg)):
        print pg[i]
        cur.execute(pg[i])
    
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()

