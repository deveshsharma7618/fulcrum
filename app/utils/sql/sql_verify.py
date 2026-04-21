def verify_sql_safe(name):
    if any(char in name for char in [";", "--", "/*", "*/", "char", "nchar", "varchar", "nvarchar", "alter", "begin", "cast", "create", "cursor", "declare", "delete", "drop", "end", "exec", "execute", "fetch", "insert", "kill", "select", "sys", "sysobjects", "syscolumns", "table", "update"]):
        print(f"SQL Injection detected in: {name}")
        return False
    
    return True