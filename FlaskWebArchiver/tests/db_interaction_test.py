import sqlite3
import os

list_tables = "SELECT name FROM sqlite_master WHERE type='table';"