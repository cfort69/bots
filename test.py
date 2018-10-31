from modulos.modelo import Ticket
from modulos.base import Session

session = Session()

tickets = session.query(Ticket).filter(Ticket.ticket_number == "N090040").first()

if tickets != None:
    print(tickets.ticket_number + " " + tickets.user.user_name +  " " + tickets.user.first_name +  " " + tickets.user.last_name)
else:
    print("no encontre nada")
    
# for ticket in tickets:
#     print(ticket.ticket_number + " " + ticket.user.user_name +  " " + ticket.user.first_name +  " " + ticket.user.last_name)
