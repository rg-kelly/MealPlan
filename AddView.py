from appJar import gui

def addItem(maximumLength, itemGroupName, app, press, rowStart = 0, columnStart = 1, bottomButton = False):
    label = "{} Name ".format(itemGroupName)
    heading = "Add {}s".format(itemGroupName)
    
    headingRow = rowStart
    entryRow = headingRow + 1
    
    if not bottomButton:
        buttonRow = entryRow
        buttonColumn = columnStart + 4
    else:
        buttonRow = entryRow + 6
        buttonColumn = columnStart + 1
    
    #app.startTab(heading)
    app.addLabel(heading, heading, headingRow, columnStart, colspan = 2)
    app.addLabelEntry(label, entryRow, columnStart)
    app.setEntryFocus(label)
    app.setEntryMaxLength(label, maximumLength)
    app.addNamedButton("Add", "Add" + itemGroupName, press, row = buttonRow, column = buttonColumn)
    #app.stopTab()