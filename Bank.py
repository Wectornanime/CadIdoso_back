
import uuid
import json
import sqlite3


with open('envoriments.json') as envoriments:
    env = json.load(envoriments)

def connect():
    return sqlite3.connect(env['db']['database'])


class Elderly():
    def insert(name, birth, cpf):
        db = connect()
        mycursor = db.cursor()
        id = str(uuid.uuid4())
        cmd = f"INSERT INTO {env['db']['tables']['elderly']} (id, name, birth, cpf) VALUES ('{id}', '{name}', '{birth}', '{cpf}')"
        mycursor.execute(cmd)
        db.commit()
        db.close()


    def list(id=''):
        db = connect()
        mycursor = db.cursor()
        ret = list()
        line = dict()

        if (id == ''):
            cmd = f"SELECT id, name, birth, cpf FROM {env['db']['tables']['elderly']} ORDER BY name"
            mycursor.execute(cmd)
            res = mycursor.fetchall()

            for col in res:
                line['id'] = col[0]
                line['name'] = col[1]
                line['birth'] = col[2]
                line['cpf'] = col[3]
                line['remedys'] = ElderlyRemedy.listRemedyByElderly(col[0])

                ret.append(line.copy())
                line.clear()

        else:
            cmd = f"SELECT id, name, birth, cpf FROM {env['db']['tables']['elderly']} WHERE id = '{id}'"
            mycursor.execute(cmd)
            data = mycursor.fetchone()
            line['id'] = data[0]
            line['name'] = data[1]
            line['birth'] = data[2]
            line['cpf'] = data[3]
            line['remedys'] = ElderlyRemedy.listRemedyByElderly(data[0])

            ret.append(line.copy())
            line.clear()

        db.close()
        return ret
    

    def delete(id):
        db = connect()
        mycursor = db.cursor()
        cmd = f"DELETE FROM {env['db']['tables']['elderly']} WHERE id = '{id}'"
        mycursor.execute(cmd)
        
        db.commit()
        db.close()


    def update(id, values):
        db = connect()
        mycursor = db.cursor()
        print(values)
        for key, value in values.items():
            if key == 'name':
                cmd = f"UPDATE {env['db']['tables']['elderly']} SET name = '{value}' WHERE id = '{id}'"
            elif key == 'birth':
                cmd = f"UPDATE {env['db']['tables']['elderly']} SET birth = '{value}' WHERE id = '{id}'"
            elif key == 'cpf':
                cmd = f"UPDATE {env['db']['tables']['elderly']} SET cpf = '{value}' WHERE id = '{id}'"
            
            mycursor.execute(cmd)
            db.commit()

        db.close()


class Remedy():
    def insert(name, isControled = 'nao'):
        db = connect()
        mycursor = db.cursor()
        id = str(uuid.uuid4())
        cmd = f"INSERT INTO {env['db']['tables']['remedy']} (id, name, isControled) VALUES ('{id}', '{name}', '{isControled.lower()}')"
        mycursor.execute(cmd)
        db.commit()
        db.close()


    def list(id=''):
        db = connect()
        mycursor = db.cursor()
        ret = list()
        line = dict()

        if (id == ''):
            cmd = f"SELECT id, name, isControled FROM {env['db']['tables']['remedy']}"
            mycursor.execute(cmd)
            res = mycursor.fetchall()

            for col in res:
                line['id'] = col[0]
                line['name'] = col[1]
                line['isControled'] = col[2]
                ret.append(line.copy())
                line.clear()

        else:
            cmd = f"SELECT id, name, isControled FROM {env['db']['tables']['remedy']} WHERE id = '{id}'"
            mycursor.execute(cmd)
            data = mycursor.fetchone()
            line['id'] = data[0]
            line['name'] = data[1]
            line['isControled'] = data[2]
            ret.append(line.copy())
            line.clear()

        db.close()
        return ret
    

    def delete(id):
        db = connect()
        mycursor = db.cursor()
        cmd = f"DELETE FROM {env['db']['tables']['remedy']} WHERE id = '{id}'"
        mycursor.execute(cmd)
        
        db.commit()
        db.close()


    def update(id, values):
        db = connect()
        mycursor = db.cursor()
        print(values)
        for key, value in values.items():
            if key == 'name':
                cmd = f"UPDATE {env['db']['tables']['remedy']} SET name = '{value}' WHERE id = '{id}'"
            elif key == 'isControled':
                cmd = f"UPDATE {env['db']['tables']['remedy']} SET isControled = '{value}' WHERE id = '{id}'"

            mycursor.execute(cmd)
            db.commit()

        db.close()


class ElderlyRemedy():
    def insert(elderlyID, remedyList):
        db = connect()
        mycursor = db.cursor()
        for remedyID in remedyList:
            id = str(uuid.uuid4())
            cmd = f"INSERT INTO {env['db']['tables']['elderlyRemedy']} (id, elderly_id, remedy_id) VALUES ('{id}', '{elderlyID}', '{remedyID}')"
            mycursor.execute(cmd)
            db.commit()
        db.close()


    def listRemedyByElderly(elderlyID):
        db = connect()
        mycursor = db.cursor()
        ret = list()
        line = dict()
        cmd = f"SELECT remedy.id, remedy.name, remedy.isControled FROM {env['db']['tables']['remedy']} AS remedy INNER JOIN {env['db']['tables']['elderlyRemedy']} AS rel ON remedy.id = rel.remedy_id WHERE rel.elderly_id = '{elderlyID}'"
        # cmd = "SELECT remedy.id, remedy.name FROM remedio_idoso as table INNER JOIN remedios as remedy ON remedy.id = table.remedy_id WHERE remedy.elderly_id = %d"
        mycursor.execute(cmd)
        res = mycursor.fetchall()

        for col in res:
            line['id'] = col[0]
            line['name'] = col[1]
            line['isControled'] = col[2]
            ret.append(line.copy())
            line.clear()

        db.close()
        return ret
    

    def listElderlyByRemedy(remedyID):
        db = connect()
        mycursor = db.cursor()
        ret = list()
        line = dict()
        cmd = F"SELECT elderly.id, elderly.name FROM {env['db']['tables']['elderly']} AS elderly INNER JOIN {env['db']['tables']['elderlyRemedy']} AS rel ON elderly.id = rel.elderly_id WHERE rel.remedy_id = '{remedyID}'"
        # cmd = "SELECT elderly.id, elderly.name FROM remedio_idoso as table INNER JOIN cadastroidoso as elderly ON elderly.id = table.elderly_id WHERE table.remedy_id = %s"
        mycursor.execute(cmd, (remedyID))
        res = mycursor.fetchall()

        for col in res:
            line['id'] = col[0]
            line['name'] = col[1]
            ret.append(line.copy())
            line.clear()

        db.close()
        return ret
    

    def delete(elderlyID, remedyID):
        db = connect()
        mycursor = db.cursor()
        cmd = f"DELETE FROM {env['db']['tables']['elderlyRemedy']} WHERE remedy_id = '{remedyID}' AND elderly_id = '{elderlyID}'"
        mycursor.execute(cmd)
        
        db.commit()
        db.close()
