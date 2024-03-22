# import base libs
from PyQt5 import QtGui as QT_GUI
from PyQt5 import QtWidgets as QT_WIDGETS
from PyQt5 import QtCore as QT_CORE
from PyQt5.QtWidgets import QPushButton, QLabel, QMessageBox

# import custom libs
import AppSwManagerDBHandler
import ApplicationSwManager
#import matplotlib
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from SoftwareComponents import SoftwareComponentListModel

# create global stylesheet
qss_file = open('../AppQss/styles.qss').read()


#########################################################################################################
# Widget for macro Browsing: MODEL + VIEW
#########################################################################################################
class ArchitectureBrowser(QT_WIDGETS.QWidget):
    def __init__(self, parentWidget):
        super(ArchitectureBrowser, self).__init__(parentWidget)

        # global - parent widget object
        self.parentWidget = parentWidget

        # define the layout
        self.layout = QT_WIDGETS.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # set max width
        self.setMaximumWidth(450)

#########################################################################################################
# QWidget to show / edit Macro attributes
#########################################################################################################
class ArchitectureWidget_ORIGINAL(QT_WIDGETS.QWidget):
    def __init__(self, parentWidget):
        super(ArchitectureWidget, self).__init__()

        self.parentWidget = parentWidget

        # define a layout for the widget
        self.layout = QT_WIDGETS.QGridLayout()
        self.layout.setVerticalSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.graphicsView = QT_WIDGETS.QGraphicsView()
        self.scene = GraphicsScene()
        self.graphicsView.setScene(self.scene)
        
        # add widgets to the layout
        self.layout.addWidget(self.graphicsView, 0, 0, 1, 1)
    
        # set the layout for the widget
        self.setLayout(self.layout)

class GraphicsScene(QT_WIDGETS.QGraphicsScene):
    def __init__(self):
        super(GraphicsScene, self).__init__()
        self.image = "samcut_icon.png"
        self.inserted = False

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QT_CORE.Qt.LeftButton and not self.inserted:
            for ii in range(100):
                img = QT_GUI.QPixmap(self.image).scaled(50, 50, QT_CORE.Qt.KeepAspectRatio)
                pixmap = QT_WIDGETS.QGraphicsPixmapItem(img)
                pixmap.setOffset(-pixmap.boundingRect().center())
                pixmap.setShapeMode(QT_WIDGETS.QGraphicsPixmapItem.BoundingRectShape)
                pixmap.setFlag(QT_WIDGETS.QGraphicsItem.ItemIsSelectable, True)
                pixmap.setFlag(QT_WIDGETS.QGraphicsItem.ItemIsMovable, True)
                pixmap.setPos(event.scenePos())
                self.addItem(pixmap)
                self.inserted = True


#########################################################################################################
# QWidget to show / edit Macro attributes
#########################################################################################################
class ArchitectureWidget(QT_WIDGETS.QWidget):
    def __init__(self, parentWidget):
        super(ArchitectureWidget, self).__init__()

        self.parentWidget = parentWidget

        # define a layout for the widget
        self.layout = QT_WIDGETS.QGridLayout()
        self.layout.setVerticalSpacing(1)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.figure = plt.figure(dpi=50)
        self.canvas = FigureCanvas(self.figure)    
        self.canvas.setSizePolicy( QT_WIDGETS.QSizePolicy.Expanding, QT_WIDGETS.QSizePolicy.Expanding)

        self.toolbar = MyNavigationToolbar(self.canvas, self) 
        
        self.label = QLabel(self)
        self.label.setText(AppSwManagerDBHandler.getLabelText())

        self.label2 = QLabel(self)
        self.label2.setText("")
        
        # add widgets to the layout
        self.layout.addWidget(self.label, 0, 0, 1, 1)
        self.layout.addWidget(self.label2, 0, 1, 1, 1)
        self.layout.addWidget(self.canvas, 1, 0, 1, 2)
        self.layout.addWidget(self.toolbar, 2, 0, 1, 2)

        # block the click/move handlers if pan/zoom is used
        self.isBlocked = False

        # save the coordinates of the moved nodes
        self.movedNodesCoord = []

        # save the removed nodes
        self.removedNodes = []

        self.baseColor = 'white'
        self.movingNode = None

        # set the layout for the widget
        self.setLayout(self.layout)
    
    def plot(self):
        self.figure.clf()
        # create a directed graph
        self.G = nx.DiGraph()
        self.G.add_nodes_from(AppSwManagerDBHandler.getAllSoftwareComponents(), node_color="lightblue", node_size=500, font_size=64)
        self.data = AppSwManagerDBHandler.getDataForArchitecture()
        #[print(d) for d in self.data]

        # add edges as directed edges:
        for d in self.data:
            self.G.add_edge(d[0], d[1], arrows=True, edge_color="grey", font_size=32, arrowsize=20)

        # set main attributes label
        self.setMainAttributesLabel(AppSwManagerDBHandler.getMainComponent())
        
        # non isolated nodes
        self.GFiltered = self.G.subgraph([n for n, d in self.G.degree() if d > 0])
        if AppSwManagerDBHandler.getPartitionFilter() != "None" or AppSwManagerDBHandler.getTaskFilter() != "None":
            self.getFilteredNodes()

        # making sure that the removed nodes stay removed after level/color change
        self.G.remove_nodes_from(self.removedNodes)

        # creating labels for the edges
        self.labels = self.getLabels()

        # remove excluded nodes
        excludeComponents = ["CtApCANMapperSWP1", "CtApCANMapperSWP4", "CtApLINMapperSWP1", "CtApLINMapperSWP4", "CtMVMapperEPB", "CtMVMapperEAC", "CtMVMapper"]
        self.G.remove_nodes_from(excludeComponents)

        self.pos = nx.spring_layout(self.GFiltered, seed = 10, k=1.8)

        # get weights/level of the nodes from data
        self.weightsForData = self.getWeightsForData()

        # get edge colors
        self.edgeColors = self.getASILLevelForEdges()

        # set the color and the position of the nodes
        self.nodeColors = self.getNodeColors()

        # get frequency
        self.getFrequency(self.GFiltered)

        # create legend
        self.label2.setText(self.createLegend())

        # handling click / move events
        self.figure.canvas.mpl_connect('button_press_event', self.handleClick) 

        nx.draw(self.GFiltered, pos=self.pos, with_labels=True, node_color=self.nodeColors, edge_color=self.edgeColors)
        nx.draw_networkx_edge_labels(self.GFiltered, pos=self.pos, edge_labels=self.labels,font_size=12)
        self.canvas.draw_idle()

    #
    def setMainAttributesLabel(self, node):
        swCompInfo = AppSwManagerDBHandler.getDataFromSQL("SELECT" + " Name, BasicInfo_Description AS Description, BasicInfo_Partition AS Partition, BasicInfo_EstimatedAsilLevel AS AsilLevel "
                                                    "FROM " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_ARCH)
                            
        self.text = ""
        for item in swCompInfo:
            if item['Name'] == node:
                self.text += "Name of the Software Component: " + item['Name']
                if item['Description'] is not None:
                    self.text += "\nDescription of the Software Component: " + item['Description']
                if item['Partition'] is not None:
                    self.text += "\nPartition of the Software Component: " + item['Partition']
                if item['AsilLevel'] is not None:
                    self.text += "\nEstimated ASIL Level of the Software Component: " + item['AsilLevel']  
        AppSwManagerDBHandler.setLabelText(self.text)  
        self.label.setText(self.text)

    #
    def createLegend(self):
        if AppSwManagerDBHandler.getColor() == 0:
            return ""
        elif AppSwManagerDBHandler.getColor() == 1:
            # Define labels for edge colors
            colorLabels = {
                'lightblue': 'Main',
                'red': 'QM',
                'brown': 'A',
                'lightgreen': 'B',
                'purple': 'C',
                'black': 'None',
                'pink': 'D',
                'yellow': 'Selected node'
            }

            # Define the desired order of labels
            desiredOrder = ['Main', 'Selected node', 'QM', 'A', 'B', 'C', 'D', 'None']

            colors = self.nodeColors + self.edgeColors

            # Sort the colors and labels based on the desired order
            sortedColors = sorted(set(colors), key=lambda x: desiredOrder.index(colorLabels[x]))
            sortedLabels = [colorLabels[color] for color in sortedColors]

            legendText = ""
            for color, label in zip(sortedColors, sortedLabels):
                line = ""
                if legendText != "":
                    line ="<br>"
                line += "<font color='" + color + "'>" + color + ": " + label + "</font>" 
                legendText += line
            return legendText

        else:
            # Define labels for edge colors
            colorLabels = {
                'lightblue': 'Main',
                'red': 'Appl_50ms',
                'brown': 'Appl_1ms',
                'lightgreen': 'Appl_10ms',
                'black': 'None',
                'yellow': 'Selected node'
            }

            # Define the desired order of labels
            desiredOrder = ['Main', 'Selected node', 'Appl_1ms', 'Appl_10ms', 'Appl_50ms', 'None']

            # Sort the colors and labels based on the desired order
            sortedColors = sorted(set(self.nodeColors), key=lambda x: desiredOrder.index(colorLabels[x]))
            sortedLabels = [colorLabels[color] for color in sortedColors]

            legendText = ""
            for color, label in zip(sortedColors, sortedLabels):
                line = ""
                if legendText != "":
                    line ="<br>"
                line += "<font color='" + color + "'>" + color + ": " + label + "</font>" 
                legendText += line
            return legendText

    #
    def getNodeColors(self):
        nodeColors = []
        for node in self.GFiltered.nodes:
            weight = next(map(lambda x: x[1], filter(lambda x: x[0] == node, self.weightsForData)), None)
            yCoord = next(map(lambda x: x[2], filter(lambda x: x[0] == node, self.weightsForData)), None) 

            if weight is not None:
                # set color for basic
                if AppSwManagerDBHandler.getColor() == 0:
                    if node == AppSwManagerDBHandler.getMainComponent():
                        nodeColors.append('lightblue')
                        self.pos[node][0] = 0.0
                    elif weight < 0:
                        nodeColors.append('red')
                    elif weight > 0:
                        nodeColors.append('green')

                # set color for ASILLevel
                elif AppSwManagerDBHandler.getColor() == 1:
                    if node == AppSwManagerDBHandler.getMainComponent():
                        nodeColors.append('lightblue')
                        self.pos[node][0] = 0.0
                    else:
                        ASILLevel = self.getASILLevelForNodes(node)
                        if ASILLevel == "QM":
                            nodeColors.append('red')
                        elif ASILLevel == "A":
                            nodeColors.append('brown')
                        elif ASILLevel == "B":
                            nodeColors.append('lightgreen')
                        elif ASILLevel == "C":
                            nodeColors.append('purple')
                        elif ASILLevel == "D":
                            nodeColors.append('pink')
                        else:
                            nodeColors.append('black')

                # set color for frequency
                else:
                    if node == AppSwManagerDBHandler.getMainComponent():
                        nodeColors.append('lightblue')
                        self.pos[node][0] = 0.0
                    else:
                        frequency = self.getFrequency(node)
                        if frequency == "Appl_50ms":
                            nodeColors.append('red')
                        elif frequency == "Appl_1ms":
                            nodeColors.append('brown')
                        elif frequency == "Appl_10ms":
                            nodeColors.append('lightgreen')
                        else:
                            nodeColors.append('black')
            
                if self.pos[node][0] != 0.0:
                    self.pos[node] = [weight, yCoord]
                    
        for item in self.movedNodesCoord:
            name = item[0]
            for node in self.GFiltered.nodes:
                if name == node:
                    self.pos[node] = [item[1], item[2]]
        return nodeColors

    #
    def getWeightsForData(self):
        weightsForData = []
        for d in sorted(self.data, key=lambda x: abs(x[2]['weight'])):
            if d[2]['weight'] >= 0:
                weightsForData.append((d[1], d[2]['weight']-1))

            elif d[2]['weight'] <= 0: 
                weightsForData.append((d[1], d[2]['weight']+1))
        
        for d in sorted(self.data, key=lambda x: abs(x[2]['weight'])):
            if d[0] not in weightsForData:
                if d[2]['weight'] >= 0:
                    weightsForData.append((d[0], d[2]['weight']-1))
                elif d[2]['weight'] <= 0: 
                    weightsForData.append((d[0], d[2]['weight']+1))

        weightsForData = list(set(item for item in weightsForData))
        weightsForData = sorted(weightsForData, key=lambda x: abs(x[1]))

        # making a unique list of weightsForData 
        uniqueDict = {}
        result = []

        for item in weightsForData:
            key = item[0]  
            if key not in uniqueDict:
                uniqueDict[key] = item
                result.append(item)

        # sorting the weightForData in ascending order
        weightsForData = []
        result = sorted(result, key=lambda x: x[1])

        # setting y coordinate for the nodes
        prevX = None
        yCoord = 0
        for d in result:
            if prevX == None:
                prevX = d[1]
            else:
                if d[1] != prevX:
                    yCoord = 0
                    prevX = d[1]
                else:
                    yCoord += 1  
            weightsForData.append((d[0], d[1], yCoord))

        return weightsForData

    # 
    def getLabels(self):
        allEdgesWithInterfaceName = AppSwManagerDBHandler.getDataFromSQL("SELECT" + " t1.parent_table_ref AS node1, t2.parent_table_ref AS node2, t1.Name "
                                                   "FROM " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_ARCH_SENDER_IF_REFERENCE + " t1 "
                                                   "JOIN " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_ARCH_RECEIVER_IF_REFERENCE + " t2 "
                                                   "ON t1.Name = t2.Name")
        allEdgesWithInterfaceName = list(map(lambda d: (d.values()), allEdgesWithInterfaceName))
        #[print(d) for d in allEdgesWithInterfaceName]
        
        filteredEdgesWithInterfaceName = []
        for edge in self.G.edges:
            for e in allEdgesWithInterfaceName:
                eList = list(e)
                if edge[0] == eList[0] and edge[1] == eList[1]:
                    filteredEdgesWithInterfaceName.append(e)
        filteredEdgesWithInterfaceName = list(map(lambda x: list(x), filteredEdgesWithInterfaceName))
        #[print(d) for d in filteredEdgesWithInterfaceName]

        labels = {}
        for item in filteredEdgesWithInterfaceName:
            key = (item[0], item[1])
            value = item[2]
            if key in labels:
                labels[key].append(value) 
            else:
                labels[key] = [value]

        return labels

    #
    def deleteGraph(self):
        self.figure.clf()
        self.canvas.draw_idle()
  
    #
    def handleClick(self, event):
        if self.isBlocked is False:
            if event.button == 1:
                # handle double click, change main component to the clicked node
                if event.dblclick: 
                    for node, coords in self.pos.items():
                        distance = np.sqrt((event.xdata - coords[0]) ** 2 + (event.ydata - coords[1]) ** 2)
                        if distance < 0.05:
                            if node is not None:
                                AppSwManagerDBHandler.setMainComponent(node)
                                self.parentWidget.architectureBrowser.changeBrowserElement(node)
                            break
                
                    #clear / draw
                    self.deleteGraph()
                    self.plot()

                # handle node movement, first click: select node, second click: click where to move the node 
                else:
                    if event.inaxes is not None:
                        x, y = event.xdata, event.ydata
                        if self.movingNode is None:
                            minDist = float('inf')
                            #minDist = 0.05
                            for n, pos in self.pos.items():
                                dist = (pos[0] - x) ** 2 + (pos[1] - y) ** 2
                                if dist < minDist:
                                    self.movingNode = n
                                    minDist = dist

                            list = [{key: value} for key, value in zip(self.GFiltered.nodes, self.nodeColors)]
                            colorOfNode = [item[self.movingNode] for item in list if self.movingNode in item]
                            index = [index for index, item in enumerate(list) if self.movingNode in item]

                            self.baseColor = colorOfNode[0]
                            self.nodeColors[index[0]] = 'yellow'

                            self.setMainAttributesLabel(self.movingNode)

                            self.updateGraph()
                        else:
                            if 'yellow' in self.nodeColors:
                                index = self.nodeColors.index('yellow')                          
                                self.nodeColors[index] = self.baseColor

                            self.setMainAttributesLabel(self.movingNode)

                            self.movedNodesCoord.append((self.movingNode, x, y))

                            self.pos[self.movingNode] = (x, y)
                            self.updateGraph()
                            self.movingNode = None
            elif event.button == 3:  # Right-click
                # unfreezing the graph
                self.GFiltered = nx.Graph(self.GFiltered) 

                for node, coords in self.pos.items():
                    distance = np.sqrt((event.xdata - coords[0]) ** 2 + (event.ydata - coords[1]) ** 2)
                    if distance < 0.05:
                        if node == AppSwManagerDBHandler.getMainComponent():
                            pass
                        else:
                            reply = QMessageBox.question(self, 'Confirmation', f"Do you really want to remove node {node}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if reply == QMessageBox.Yes:
                                # Remove the node from the graph
                                self.GFiltered.remove_node(node)
                                self.G.remove_node(node)
                                self.removedNodes.append(node)
                                
                                # Remove isolated and not connected nodes
                                isolatedNodes = [n for n, d in self.GFiltered.degree() if d == 0]
                                mainNode = AppSwManagerDBHandler.getMainComponent() 
                                connectedNodes = nx.node_connected_component(self.GFiltered, mainNode)
                                unconnectedNodes = set(self.GFiltered.nodes) - connectedNodes

                                if mainNode not in isolatedNodes and mainNode not in unconnectedNodes: 
                                    self.GFiltered.remove_nodes_from(isolatedNodes)
                                    self.G.remove_nodes_from(isolatedNodes)
                                    self.removedNodes.extend(isolatedNodes)

                                    self.GFiltered.remove_nodes_from(unconnectedNodes)
                                    self.G.remove_nodes_from(unconnectedNodes)
                                    self.removedNodes.extend(unconnectedNodes)

                                # Update positions dictionary
                                self.pos.pop(node, None)

                                # Update node colors / edge colors
                                self.nodeColors = self.getNodeColors()
                                self.labels = self.getLabels()
                                self.edgeColors = self.getASILLevelForEdges()

                                # Redraw the graph
                                self.updateGraph()
                            break
    
    #
    def updateGraph(self):
        self.figure.clf()

        # setting label texts
        self.label.setText(AppSwManagerDBHandler.getLabelText())
        self.label2.setText(self.createLegend())

        # draw graph
        nx.draw(self.GFiltered, pos=self.pos, with_labels=True, node_color=self.nodeColors, edge_color=self.edgeColors)
        nx.draw_networkx_edge_labels(self.GFiltered, pos=self.pos, edge_labels=self.labels,font_size=12)
        self.canvas.draw_idle()

    #
    def getASILLevelForNodes(self, componentName):
        interfacesASILLevel = AppSwManagerDBHandler.getDataFromSQL("SELECT" + " Name, BasicInfo_EstimatedAsilLevel AS ASILLevel "
                                                   "FROM " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_ARCH)
        #print(interfacesASILLevel)

        ASILLevel = None
        for item in interfacesASILLevel:
            if item['Name'] == componentName:
                ASILLevel = item['ASILLevel']
        if ASILLevel == "A(B)" or ASILLevel == "A(C)" or ASILLevel == "A(D)":
            return "A"
        elif ASILLevel == "C(C)" or ASILLevel == "B(D)":
            return "B"
        elif ASILLevel == "C(D)":
            return "C"
        else:
            return ASILLevel

    #
    def getASILLevelForEdges(self):
        if AppSwManagerDBHandler.getColor() == 1:
            allEdgesWithInterfaceName = AppSwManagerDBHandler.getDataFromSQL("SELECT" + " t1.parent_table_ref AS node1, t2.parent_table_ref AS node2, t1.Name "
                                                    "FROM " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_ARCH_SENDER_IF_REFERENCE + " t1 "
                                                    "JOIN " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_ARCH_RECEIVER_IF_REFERENCE + " t2 "
                                                    "ON t1.Name = t2.Name")
            allEdgesWithInterfaceName = list(map(lambda d: (d.values()), allEdgesWithInterfaceName))
            #[print(d) for d in allEdgesWithInterfaceName]

            filteredEdgesWithInterfaceName = []
            for edge in self.G.edges:
                for e in allEdgesWithInterfaceName:
                    eList = list(e)
                    if edge[0] == eList[0] and edge[1] == eList[1]:
                        filteredEdgesWithInterfaceName.append(e)
            filteredEdgesWithInterfaceName = list(map(lambda x: list(x), filteredEdgesWithInterfaceName))
            #print(filteredEdgesWithInterfaceName)

            interfacesASILLevel = AppSwManagerDBHandler.getDataFromSQL("SELECT" + " Name, ASILLevel "
                                                    "FROM " + AppSwManagerDBHandler.TABLE_SR_INTERFACE_DEFINITIONS)
            
            interfacesASILLevel = [item for item in interfacesASILLevel if item['Name'] in [elem[2] for elem in filteredEdgesWithInterfaceName]]
            #print(interfacesASILLevel)

            labels = self.getLabels()

            # sort labels in the way GFiltered.edges are sorted
            #labels = {edge: labels[edge] for edge in self.GFiltered.edges}
            labels = {edge: labels[edge] for edge in self.GFiltered.edges if edge in labels}

            edgeColors = []
            for key, values in labels.items():
                valueResult = -1
                for value in values:
                    for element in interfacesASILLevel:
                        if value == element['Name']:
                            result = element['ASILLevel']
                            if result == 'QM':
                                valueResult = 5
                            if result == 'ASIL_A' and valueResult < 5:
                                valueResult = 4
                            if result == 'ASIL_B' and valueResult < 4:
                                valueResult = 3
                            if result == 'ASIL_C' and valueResult < 3:
                                valueResult = 2
                            if result == 'ASIL_D' and valueResult < 2:
                                valueResult = 1
                            if result == None and valueResult < 1:
                                valueResult = 0
                if valueResult == 0:
                    edgeColors.append("black")
                elif valueResult == 1:
                    edgeColors.append("pink")
                elif valueResult == 2:
                    edgeColors.append("purple")
                elif valueResult == 3:
                    edgeColors.append("lightgreen")
                elif valueResult == 4:
                    edgeColors.append("brown")
                else:
                    edgeColors.append("red")

            return edgeColors

    #
    def getFrequency(self, node):
        frequencies = AppSwManagerDBHandler.getDataFromSQL("SELECT" + " RunnableRef AS Name, TaskRef AS frequency "
                                                   "FROM " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_RUNNABLE_ORDER)
        #print(frequencies)

        # filter the ones with _step on the end of there name and then remove it
        for item in frequencies:
            if item['Name'].endswith('_step'):
                item['Name'] = item['Name'][:-5] 
                if item['Name'] == node:
                    return item['frequency']

    #
    def getFilteredNodes(self):
        excludeComponents = []
        if AppSwManagerDBHandler.getPartitionFilter() != "None":
            # Partition
            for node in self.GFiltered.nodes:
                #
                nodeObj = AppSwManagerDBHandler.getSoftwareComponentByName(node)
                #
                if nodeObj.getSwCompPartition() != AppSwManagerDBHandler.getPartitionFilter():
                    if node != AppSwManagerDBHandler.getMainComponent():
                        excludeComponents.append(node)
                pass
            if AppSwManagerDBHandler.getTaskFilter() != "None":
                # Both
                for node in self.GFiltered.nodes:
                    task = AppSwManagerDBHandler.getDataFromSQL("SELECT TaskRef FROM " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_RUNNABLE_ORDER + " WHERE RunnableRef = ?", (node + "_step",))
                    if task:
                        if task[0]["TaskRef"] != AppSwManagerDBHandler.getTaskFilter():
                            if node != AppSwManagerDBHandler.getMainComponent():
                                excludeComponents.append(node)
        elif AppSwManagerDBHandler.getTaskFilter() != "None":
            # Task
            for node in self.GFiltered.nodes:
                task = AppSwManagerDBHandler.getDataFromSQL("SELECT TaskRef FROM " + AppSwManagerDBHandler.TABLE_SOFTWARE_COMPONENT_RUNNABLE_ORDER + " WHERE RunnableRef = ?", (node + "_step",))
                if task:
                    if task[0]["TaskRef"] != AppSwManagerDBHandler.getTaskFilter():
                        if node != AppSwManagerDBHandler.getMainComponent():
                            excludeComponents.append(node)

        # remove the excluded nodes
        self.G.remove_nodes_from(excludeComponents)

        # Check and remove nodes not in relation with the main component
        nodes_to_remove = []
        for node in self.G.nodes:
            if not (nx.has_path(self.G, node, AppSwManagerDBHandler.getMainComponent()) or nx.has_path(self.G, AppSwManagerDBHandler.getMainComponent(), node)):
                nodes_to_remove.append(node)
        self.G.remove_nodes_from(nodes_to_remove)


#########################################################################################################
# QWidget for software component browsing: MODEL + VIEW
#########################################################################################################
class SoftwareComponentBrowserForArchitecture(QT_WIDGETS.QWidget):
    def __init__(self, parentWidget):
        super(SoftwareComponentBrowserForArchitecture, self).__init__(parentWidget)

        # global - parent widget object
        self.parentWidget = parentWidget

        # define the layout
        self.layout = QT_WIDGETS.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # set max width
        self.setMaximumWidth(300)

        # define model for the view
        self.originalModel = None

        # define filter proxy
        self.filterProxyModel = QT_CORE.QSortFilterProxyModel()
        self.filterProxyModel.setFilterCaseSensitivity(QT_CORE.Qt.CaseInsensitive)
        self.filterProxyModel.setDynamicSortFilter(True)

        # define the main browser tree widget
        self.SoftwareComponentBrowserForArchitecture = QT_WIDGETS.QListView()
        self.SoftwareComponentBrowserForArchitecture.setStyleSheet(qss_file)
        # create an empty list for the Sender - Receiver interfaces
        self.SoftwareComponentBrowserForArchitecture.softwareComponentNameList = list()
        # set tree widget enabled
        self.SoftwareComponentBrowserForArchitecture.setEnabled(True)
        # selected object
        self.SoftwareComponentBrowserForArchitecture.selectedSoftwareComponentObj = None

        self.button1 = QPushButton('Color for ASIL Level')
        self.button2 = QPushButton('Color for Frequency')
        self.button1.setCheckable(True)
        self.button2.setCheckable(True)

        self.button1.clicked.connect(self.button1Clicked)
        self.button2.clicked.connect(self.button2Clicked)

        # create integer input fields
        self.receiverLevelInput = QT_WIDGETS.QSpinBox(self)
        self.receiverLevelInput.setFont(QT_GUI.QFont('Calibri', 9))
        self.receiverLevelInput.setRange(0, 5)
        self.receiverLevelInput.setSpecialValueText("Receiver level: ")

        self.senderLevelInput = QT_WIDGETS.QSpinBox(self)
        self.senderLevelInput.setFont(QT_GUI.QFont('Calibri', 9))
        self.senderLevelInput.setRange(0, 5)
        self.senderLevelInput.setSpecialValueText("Sender level: ")

        self.receiverLevelInput.valueChanged.connect(self.changedHandler)
        self.senderLevelInput.valueChanged.connect(self.changedHandler)

        #
        self.Partition_Label = QPushButton("Filter by Partition:")
        self.Partition_Label.setCheckable(False)
        self.Partition_combo_box = QT_WIDGETS.QComboBox()
        options = ["None", "SWP1_QM", "SWP2_MAIN", "SWP3_CHECK", "SWP4_D"]
        self.Partition_combo_box.addItems(options)
        self.Partition_combo_box.currentIndexChanged.connect(self.partitionFilterChanged)

        self.Task_Label = QPushButton("Filter by Frequency:")
        self.Task_Label.setCheckable(False)
        self.Task_combo_box = QT_WIDGETS.QComboBox()
        options = ["None", "Appl_1ms", "Appl_10ms", "Appl_50ms"]
        self.Task_combo_box.addItems(options)
        self.Task_combo_box.currentIndexChanged.connect(self.taskFilterChanged)

        # add to widget
        self.layout.addWidget(self.button1, 0,0,1,10)
        self.layout.addWidget(self.button2, 1,0,1,10)
        self.layout.addWidget(self.receiverLevelInput, 2,0,1,10)
        self.layout.addWidget(self.senderLevelInput, 3,0,1,10)
        self.layout.addWidget(self.Partition_Label, 4,0,1,10)
        self.layout.addWidget(self.Partition_combo_box, 5,0,1,10)
        self.layout.addWidget(self.Task_Label, 6,0,1,10)
        self.layout.addWidget(self.Task_combo_box, 7,0,1,10)

        # define toolbar for search Sender - Receiver interfaces
        self.searchToolBar = QT_WIDGETS.QToolBar()
        self.searchToolBar.setFont(QT_GUI.QFont('Calibri', 12))
        self.searchSoftwareComponentWidget = QT_WIDGETS.QLineEdit()
        self.searchSoftwareComponentWidget.setClearButtonEnabled(True)
        self.searchSoftwareComponentWidget.addAction(QT_GUI.QIcon("../AppIcons/search_icon.png"),QT_WIDGETS.QLineEdit.LeadingPosition)
        self.searchSoftwareComponentWidget.setPlaceholderText("Search...")
        self.searchSoftwareComponentWidget.textEdited.connect(self.setProxyFilterByText)
        # add actions to toolbar
        self.searchToolBar.addWidget(self.searchSoftwareComponentWidget)

        # add widgets to the layout
        self.layout.addWidget(self.searchToolBar, 8, 0, 1, 1)
        self.layout.addWidget(self.SoftwareComponentBrowserForArchitecture, 9, 0, 9, 1)

        # initialize the global Sender - Receiver interface tree widget
        self.initializeSoftwareComponentTree()
        # connect tree item clicked function after model is added to list view
        self.SoftwareComponentBrowserForArchitecture.selectionModel().currentChanged.connect(self.itemClickedHandler)

        # set the layout of the widget
        self.setLayout(self.layout)

    # read all Sender - Receiver interfaces from the database and initialize the browser
    def initializeSoftwareComponentTree(self):
        # parse the database, collect all Sender - Receiver interfaces (returning a list of Sender - Receiver interface names)
        self.SoftwareComponentBrowserForArchitecture.softwareComponentNameList = AppSwManagerDBHandler.getAllSoftwareComponents()
        self.originalModel = SoftwareComponentListModel(self.SoftwareComponentBrowserForArchitecture.softwareComponentNameList)
        self.filterProxyModel.setSourceModel(self.originalModel)
        self.SoftwareComponentBrowserForArchitecture.setModel(self.filterProxyModel)
    
    # proxy filter for search bar
    def setProxyFilterByText(self):
        filterText = self.searchSoftwareComponentWidget.text()
        self.filterProxyModel.setFilterFixedString(filterText)

    # view item clicked function call definition
    def itemClickedHandler(self, currentSelection):
        # get item name from QModelIndex
        itemName = self.filterProxyModel.data(currentSelection)
        if itemName != None:
            AppSwManagerDBHandler.setMainComponent(itemName)

        #clear / draw
        self.parentWidget.selectedItem.movedNodesCoord = []
        self.parentWidget.selectedItem.removedNodes = []
        self.parentWidget.selectedItem.deleteGraph()
        self.parentWidget.selectedItem.plot()
    
    def button1Clicked(self):
        if self.button1.isChecked():
            AppSwManagerDBHandler.setColor(1)
            self.button2.setChecked(False)
        else:
            if not self.button2.isChecked():
                AppSwManagerDBHandler.setColor(0)
            else:
                AppSwManagerDBHandler.setColor(2)

        #clear / draw
        self.parentWidget.selectedItem.deleteGraph()
        if AppSwManagerDBHandler.getMainComponent():
            self.parentWidget.selectedItem.plot()

    def button2Clicked(self):
        if self.button2.isChecked():
            AppSwManagerDBHandler.setColor(2)
            self.button1.setChecked(False)
        else:
            if not self.button1.isChecked():
                AppSwManagerDBHandler.setColor(0)
            else:
                AppSwManagerDBHandler.setColor(1)

        #clear / draw
        self.parentWidget.selectedItem.deleteGraph()
        if AppSwManagerDBHandler.getMainComponent():
            self.parentWidget.selectedItem.plot()
    
    def partitionFilterChanged(self):
        AppSwManagerDBHandler.setPartitionFilter(self.Partition_combo_box.currentText())

        #clear / draw
        self.parentWidget.selectedItem.deleteGraph()
        if AppSwManagerDBHandler.getMainComponent():
            self.parentWidget.selectedItem.plot()

    def taskFilterChanged(self):
        AppSwManagerDBHandler.setTaskFilter(self.Task_combo_box.currentText())

        #clear / draw
        self.parentWidget.selectedItem.deleteGraph()
        if AppSwManagerDBHandler.getMainComponent():
            self.parentWidget.selectedItem.plot()

    def changedHandler(self):
        # set receiver/sender levels
        AppSwManagerDBHandler.setRecevierLevel(self.receiverLevelInput.value()-1)
        AppSwManagerDBHandler.setSenderLevel(self.senderLevelInput.value()-1)

        #clear / draw
        self.parentWidget.selectedItem.deleteGraph()
        if AppSwManagerDBHandler.getMainComponent():
            self.parentWidget.selectedItem.plot()
        
    def changeBrowserElement(self, node):
        index = self.filterProxyModel.index(0, 0)
        while index.isValid():
            item = self.filterProxyModel.data(index)
            if item == node:
                break
            index = index.sibling(index.row() + 1, 0)

        if index.isValid():
            self.SoftwareComponentBrowserForArchitecture.setCurrentIndex(index)


#########################################################################################################
# Custom NavigationToolbar: blocking handleClick function when pan/zoom is active
#########################################################################################################
class MyNavigationToolbar(NavigationToolbar):
    def __init__(self, canvas, parent=None):
        super(MyNavigationToolbar, self).__init__(canvas, parent)
        self.architecture_widget = parent

    def pan(self):
        if self._active == 'PAN':
            super().pan()
            self.architecture_widget.isBlocked = False
        else:
            super().pan()
            self.architecture_widget.isBlocked = True

    def zoom(self):
        if self._active == 'ZOOM':
            super().zoom()
            self.architecture_widget.isBlocked = False
        else:
            super().zoom()
            self.architecture_widget.isBlocked = True