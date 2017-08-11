from appJar import gui

def addItem(maximumLength, itemGroupName, app, press):
    label = "{} Name".format(itemGroupName)
    heading = "Add {}s".format(itemGroupName)
    
    #app.startTab(heading)
    app.addLabel(heading, heading, 0, 1, colspan = 2)
    app.addLabelEntry(label, 1, 1)
    app.setEntryFocus(label)
    app.setEntryMaxLength(label, maximumLength)
    app.addButton("Add", press, row = 3, column = 1, colspan = 2)
    #app.stopTab()