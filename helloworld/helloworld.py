# Helloworld plugin

from trac.core import *
from trac.web.chrome import INavigationContributor
from trac.web.main import IRequestHandler
from trac.util import escape, Markup

from mastertickets.model import TicketLinks
class TicketLinksExt(TicketLinks):
		pass
class ISprintChangeListener(Interface):
	def sprint_created(sprint):
		"""
		For sprint created
		"""
	def sprint_changed(sprint):
		"""
		For sprint changed
		"""
	def sprint_deleted(sprint):
		"""
		For sprint deleted
		"""

class SprintChangeListener(Component):
	extension = ExtensionPoint(ISprintChangeListener)
	def __init__(self):
		pass
class PrintSprintChange(Component):
	implements(SprintChangeListener)
	def sprint_created(self, sprint):
		return "sprint created: ###################################"
	def sprint_changed(self, sprint):
		print "sprint changed: ###################################"
	def sprint_deleted(self, sprint):
		print "sprint deleted: ###################################"

class HelloWorldPlugin(Component):
	implements(INavigationContributor, IRequestHandler)

	def get_active_navigation_item(self, req):
		return 'helloworld'
	def get_navigation_items(self,req):
		yield 'mainnav','helloworld',Markup('<a href="%s">Hello</a>' % (
			self.env.href.helloworld()))
	def match_request(self,req):
		return req.path_info == '/helloworld'
	def process_request(self, req):
		req.send_response(200)
		print (TicketLinksExt)
		from trac.core import ComponentManager
		comp_mgr = ComponentManager()
		sprint = PrintSprintChange(comp_mgr)
		st = sprint.sprint_created("testing")
		abuffer = 'Hello world! Sprint created %s' %st
		req.send_header('Content-Type', 'text/plain')
		req.send_header('Content-length', str(len(abuffer)))
		req.end_headers()
		req.write(abuffer)

