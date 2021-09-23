import sys
import global_values as g


def close_all_threads():
	g.run=False
	g.client.s.close()
	g.client.connected=False


g.login_window.show()


g.app.exec_()
sys.exit(close_all_threads())

