/*
Dialog containing controls
*/

import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2

import "../dialogs" as MyDialogs

import QmlDelegate 1.0


Item {

	
	DialogDelegate {
		id: dialogDelegate
		objectName: "dialogDelegate"
	}
	
	
	MyDialogs.DialogWSpinBox {
		id: dialog
	}

	 
	 Connections {
    	// target is id of thing emitting signal
    	// control must exist (preceding this in the source file.)
	    target: dialogDelegate
	    onActivated: {
	    	console.log("Dialog activated")
	    	// the id of an object is not accessible except to dereference by its value
	    	console.log("delegate id:", dialogDelegate.id)
	    	console.log("delegate objectName:", dialogDelegate.objectName)
	    	dialog.open()
	    }	
	 }
}
