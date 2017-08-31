from appJar import gui

def addItem(maximumLength, itemGroupName, app, press, rowStart = 0, columnStart = 1):
    label = "{} Name ".format(itemGroupName)
    heading = "Add {}s".format(itemGroupName)
    
    headingRow = rowStart
    entryRow = headingRow + 1
    
    #app.startTab(heading)
    app.addLabel(heading, heading, headingRow, columnStart, colspan = 2)
    app.addLabelEntry(label, entryRow, columnStart)
    app.setEntryFocus(label)
    app.setEntryMaxLength(label, maximumLength)
    app.addNamedButton("Add", "Add" + itemGroupName, press, row = entryRow, column = columnStart + 4)
    #app.stopTab()