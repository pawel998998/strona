from pobieranie import *
from napisy import *
import cherrypy

with open("index.html", encoding="utf-8") as template:
    template = template.read()

class main(object):
	@cherrypy.expose
	def index(self):
		return template

	@cherrypy.expose
	def submit(self, link, jezyk):
		try:
			try:
				return napisy(link, jezyk)
			except:
				return rozpoznaj_mowe(link, jezyk)
		except:
			return "Wkleiłeś zły link."

cherrypy.config.update({'server.socket_port': 25565,'engine.autoreload_on': True})
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(main())