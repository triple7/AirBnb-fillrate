import subprocess

# Global variables
DB = './db/db.sqlite3'

def locationExists( location, country):
    sql = f"SELECT id from location WHERE id='{location}' AND country='{country}';"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8').split('\n')
    output = [o for o in output if o != '']
    return True if len(output) > 0 else False

def selectLocations( ):
    sql = f"SELECT * from location;"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8').split('\n')
    output = [o for o in output if o != '']
    if len(output) == 0:
        return output
    else:
        return [o.split('|') for o in output]

def insertLocation( location, country):
    sql = f"INSERT INTO location(id, country) VALUES('{location}', '{country}');"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8')
    output = f'inserted location {location}' if output == '' else output
    print(output)

def roomExists( roomId):
    sql = f"SELECT id from room WHERE id={roomId};"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8').split('\n')
    output = [o for o in output if o != '']
    return True if len(output) > 0 else False

def insertRoom( roomId):
    sql = f"INSERT INTO room(id) VALUES({roomId});"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8')
    output = f'inserted room {roomId}' if output == '' else output
    print(output)

def updateRoom( roomId):
    sql = f"UPDATE room SET WHERE roomId={roomId};"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8')
    output = f'updated room {roomId}' if output == '' else output
    print(output)

def availExists( roomId, timestamp):
    sql = f"SELECT id from availability WHERE roomId={roomId} AND date='{timestamp}';"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8').split('\n')
    output = [o for o in output if o != '']
    return True if len(output) > 0 else False

def insertAvailability( roomId, timestamp, avail):
    sql = f"INSERT INTO availability(roomId, date, available) VALUES({roomId}, '{timestamp}', '{avail}');"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8')
    output = f'inserted availability {roomId} {timestamp} {avail}' if output == '' else output
    print(output)

def updateAvailability( roomId, timestamp, avail):
    sql = f"UPDATE availability SET available='{avail}' WHERE roomId={roomId} AND date='{timestamp}';"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8')
    output = f'updated availability {roomId} {timestamp} {avail}' if output == '' else output
    print(output)

# Start of stats queries

def getAvailableByRange(roomId,  start, end, available='unavailable'):
    sql = f"SELECT * from availability WHERE roomId={roomId} AND date BETWEEN '{start}' AND '{end}' AND available='{available}';"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8').split('\n')
    output = [o for o in output if o != '']
    if len(output) == 0:
        return output
    else:
        return [o.split('|') for o in output]

def getAvailable(roomId, available='unavailable'):
    sql = f"select count(*) FROM availability WHERE roomId={roomId} AND available='{available}';"
    cmd = ['sqlite3', DB, sql]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8')
    output = f'got count {roomId} {timestamp} {avail}' if output == '' else output
    return int(output)

def getGlobalFillRate(roomId):
    u = getAvailable(roomId)
    a = getAvailable(roomId, 'available')
    return float(u)/(u+a)

def getRangedFillRate(roomId, start, end):
    u = getAvailableByRange(roomId, start, end)
    a = getAvailableByRange(roomId, start, end, 'available')
    return float(u)/(u+a)

# Start of map queries

