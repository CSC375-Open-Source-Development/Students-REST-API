import sqlite3
from sqlite3 import Error

connection = sqlite3.connect('students.db', isolation_level=None)
connection.execute('pragma journal_mode=wal;')

connection.execute('DROP TABLE IF EXISTS Students')
connection.execute('CREATE TABLE "Students" ( "id" INTEGER NOT NULL UNIQUE, "first_name" TEXT NOT NULL, "last_name" TEXT NOT NULL, "email" TEXT NOT NULL UNIQUE, "created_by" TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )')

connection.execute('DROP TABLE IF EXISTS Users')
connection.execute('CREATE TABLE "Users" ( "id" INTEGER NOT NULL UNIQUE, "username" TEXT NOT NULL UNIQUE, "token" TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) )')