
import sys

from PyQt5.QtCore import qWarning
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickItem, QQuickWindow
from PyQt5.QtQml import QQmlApplicationEngine

from qmlApp.qmlModel import QmlModel
from model.person import Person

from qmlMaster.qmlMaster import QmlMaster




class QmlApp(object):
  '''
  Contains QApp without reference to a QWidget.
  I.E. all windows defined in qml file.
  Contrast with WidgetApp.
  
  Has event loop (never returns)
  '''
  def __init__(self, qml):
    app = QGuiApplication(sys.argv)
    
    '''
    Register our Python models (classes/types to be registered with QML.)
    '''
    model = QmlModel()
    model.register()
    
    self.qmlMaster = QmlMaster()
    
    engine = QQmlApplicationEngine()
    '''
    Need this if no stdio, i.e. Android, OSX, iOS.
    OW, qWarnings to stdio.
    engine.warnings.connect(self.errors)
    '''
    engine.load(self.qmlMaster.qmlFilenameToQUrl(qml))
    engine.quit.connect(app.quit)
    
    " Keep reference to engine, used by root() "
    self.engine = engine
    
    '''
    Window is shown by default.
    window = self.getWindow()
    window.show()
    '''
    
    '''
    Suggested architecture is for model layer (Python) not to know of UI layer,
    and thus not make connections.
    The model layer can emit signals to UI layer and vice versa,
    but only the UI layer knows what connections to make
    '''
    self.makeConnections()
    
    app.exec_()   # !!! C exec => Python exec_
    print("Application returned")

    
    
  def makeConnections(self):
    '''
    Connections
    Here, make connection on the Python side
    
    Of dubious value
    '''
    # Connect button signal to person handler
    button = self.qmlMaster.findComponentFromRoot(root=self.root(), className=QQuickItem, objectName="button")
    foo = self.qmlMaster.findComponentFromRoot(root=self.root(), className=Person, objectName="foo")
    if button is not None and foo is not None:
      button.activated.connect(foo.activate)
    else:
      print("Can't connect nonexistent button or non-existent model.")

    
  def root(self):
    " QmlApp's root comes from engine."
    try:
      qmlRoot = self.engine.rootObjects()[0]
    except:
      qWarning("Failed to read or parse qml.")
      raise
    
    print(qmlRoot)
    assert isinstance(qmlRoot, QQuickWindow)
    return qmlRoot
    
    
  def getWindow(self):
    " QQuickWindow containing QML app's GUI"
    return self.root()
    
  
    
  def errors(self, warningList):
    for item in warningList:
      # syslog on Android and OSX and iOS
      print(item)
    