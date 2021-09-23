import sys
import global_values as g


def close_all_threads():
  '''
    #退出前关闭所有线程
  '''
	g.run=False
	g.client.s.close()
	g.client.connected=False


g.login_window.show() #显示qt主界面


g.app.exec_()
sys.exit(close_all_threads()) #关闭所有线程后退出
