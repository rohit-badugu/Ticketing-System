from flask import render_template, request
from classes.queryHandler import QueryHandler
from classes.utils import Utils

'''
The function maintains all the API routes
'''
def configure_routes(app):
    queryHandler = QueryHandler()
    utils = Utils()

    @app.route('/')
    def index():

        try:
            #Extract page number for url args
            page_no = request.args.get("page")
            if page_no == None:
                page_no = 1
            page_no = int(page_no)
            
            jsonResponse = queryHandler.fetchTickets(page_no)
            tickets = jsonResponse["tickets"]

            users = queryHandler.fetchMultipleUsers(tickets)
            groups = queryHandler.fetchGroups()

            #Create a payload from the tickets, users and groups objects
            payload = utils.createPayload(tickets, users, groups, jsonResponse["count"], page_no)
        except TypeError:
            return render_template('internal_error.html'), 500

        return render_template('index.html', payload=payload)


    @app.route('/ticket')
    def detail():
        try:
            #Extract ticket id from url args
            ticket_id = request.args.get("id")
            if ticket_id == None or ticket_id == "":
                return render_template('404.html'), 404

            ticket = queryHandler.fetchSingleTicket(ticket_id)
            comments = queryHandler.fetchComments(ticket_id)
            users = queryHandler.fetchTicketUsers(ticket, comments)

            #Create a payload from the ticket, users and comments objects
            payload = utils.createTicketPayload(ticket, comments, users)
        except TypeError:
            return render_template('internal_error.html'), 500

        return render_template('ticket.html', payload=payload)

    @app.errorhandler(404)
    def page_not_found(e):
        #setting the 404 status explicitly
        return render_template('page_not_found.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        #setting the 500 status explicitly
        return render_template('internal_error.html'), 404