from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from sqlite3 import Error

app = FastAPI()

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("tickets_conciertos.db")
    except Error as e:
        print(e)
    return conn

class TicketRequest(BaseModel):
    usuario_id: int
    concierto_id: int

@app.post("/ticket")
async def buy_ticket(ticket: TicketRequest):
    try:
        usuario_id = ticket.usuario_id
        concierto_id = ticket.concierto_id

        conn = create_connection()
        c = conn.cursor()

        c.execute("SELECT tickets_disponibles FROM Concerts WHERE id = ?", (concierto_id,))
        available_tickets = c.fetchone()

        if not available_tickets:
            raise HTTPException(status_code=404, detail="Concert not found")

        if available_tickets[0] <= 0:
            raise HTTPException(status_code=400, detail="No tickets available")

        c.execute('''
            UPDATE Tickets 
            SET estado = 'comprado', fecha_reserva = CURRENT_TIMESTAMP 
            WHERE usuario_id = ? AND concierto_id = ? AND estado = 'reservado'
        ''', (usuario_id, concierto_id))

        c.execute('''
            UPDATE Concerts 
            SET tickets_disponibles = tickets_disponibles - 1 
            WHERE id = ?
        ''', (concierto_id,))

        conn.commit()
        conn.close()

        return {"message": "Ticket purchased successfully."}

    except sqlite3.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@app.post("/reservation")
async def reserve_ticket(ticket: TicketRequest):
    try:
        usuario_id = ticket.usuario_id
        concierto_id = ticket.concierto_id

        conn = create_connection()
        c = conn.cursor()

        c.execute("SELECT tickets_disponibles FROM Concerts WHERE id = ?", (concierto_id,))
        available_tickets = c.fetchone()

        if not available_tickets:
            raise HTTPException(status_code=404, detail="Concert not found")

        if available_tickets[0] <= 0:
            raise HTTPException(status_code=400, detail="No tickets available for reservation")

        c.execute('''
            INSERT INTO Tickets (estado, usuario_id, concierto_id)
            VALUES ('reservado', ?, ?)
        ''', (usuario_id, concierto_id))

        c.execute('''
            UPDATE Concerts 
            SET tickets_disponibles = tickets_disponibles - 1 
            WHERE id = ?
        ''', (concierto_id,))

        conn.commit()
        conn.close()

        return {"message": "Ticket reserved successfully."}

    except sqlite3.DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))


@app.post("/cancelation")
async def cancel_ticket(ticket: TicketRequest):
    try:
        usuario_id = ticket.usuario_id
        concierto_id = ticket.concierto_id

        conn = create_connection()
        c = conn.cursor()

        c.execute('''
            SELECT estado FROM Tickets 
            WHERE usuario_id = ? AND concierto_id = ?
        ''', (usuario_id, concierto_id))

        ticket = c.fetchone()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        if ticket[0] == 'cancelado':
            raise HTTPException(status_code=400, detail="The ticket is already canceled")

        c.execute('''
            UPDATE Tickets 
            SET estado = 'cancelado', fecha_cancelacion = CURRENT_TIMESTAMP 
            WHERE usuario_id = ? AND concierto_id = ?
        ''', (usuario_id, concierto_id))

        c.execute('''
            UPDATE Concerts 
            SET tickets_disponibles = tickets_disponibles + 1 
            WHERE id = ?
        ''', (concierto_id,))

        conn.commit()
        conn.close()

        return {"message": "Ticket canceled successfully."}

    except sqlite3.DatabaseError as e:
        raise HTTPException(status_code=500, detail="error: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
