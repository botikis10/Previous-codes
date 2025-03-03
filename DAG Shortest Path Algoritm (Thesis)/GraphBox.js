import React, { useState, useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

const GraphBox = () => {
  const cyRef = useRef(null);
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [nodeName, setNodeName] = useState('');
  const [sourceNode, setSourceNode] = useState('');
  const [targetNode, setTargetNode] = useState('');
  const [edgeValue, setEdgeValue] = useState('0');
  const [nodeToRemove, setNodeToRemove] = useState('');
  const [edgeToRemove, setEdgeToRemove] = useState({ from: '', to: '' });
  const [graphRepresentation, setGraphRepresentation] = useState('');
  const [sortedNodes, setSortedNodes] = useState([]);
  const [times, setTimes] = useState({});
  const [resultsVisible, setResultsVisible] = useState(false);
  const [language, setLanguage] = useState('HU');
  const [nextNodeId, setNextNodeId] = useState(1); 

  const translations = {
    EN: {
      title: 'DAG Shortest Path Algorithm',
      addNode: 'Add Node',
      nodeName: 'Node name',
      selectSource: 'Select source node',
      selectTarget: 'Select target node',
      addEdge: 'Add Edge',
      addEdgeAlert1: 'Source and target nodes cannot be the same.',
      addEdgeAlert2: 'This edge already exists.',
      selectRemove: 'Select node to remove',
      removeNode: 'Remove Node',
      graphRepresentation: 'Graph Representation',
      graphVisualization: 'Graph Visualization',
      perfromTopologicalSort: 'Perform Topological Sort and DAG Shortest Path Algorithm',
      nodeStartFinishTimes: 'Node Start/Finish Times',
      dagShortestPath: 'DAG Shortest Path Algorithm',
      alertEmpty: 'The graph is empty. Please add nodes and edges before performing a topological sort.',
      alertCycle: 'The graph is not acyclic. Please remove cycles and try again.',
      alertSameNode: 'Node already exists.',
      alertRemoveEdge: 'There is no edge like that.',
      result: 'Result:',
      legend: 'Base Node',
      TopologySort: 'Topology Sort',
      removeEdge: 'Remove edge',
    },
    HU: {
      title: 'DAG legrövidebb utak egy forrásból algoritmusa',
      addNode: 'Csúcs hozzáadása',
      nodeName: 'Csúcs neve',
      selectSource: 'Forrás csúcs kiválasztása',
      selectTarget: 'Cél csúcs kiválasztása',
      addEdge: 'Él hozzáadása',
      addEdgeAlert1: 'A forrás és cél csúcs nem lehet ugyanaz',
      addEdgeAlert2: 'Ez az él már létezik.',
      selectRemove: 'Eltávolítandó csúcs kiválasztása',
      removeNode: 'Csúcs eltávolítása',
      graphRepresentation: 'Gráf Ábrázolás',
      graphVisualization: 'Gráf Megjelenítés',
      perfromTopologicalSort: 'Topologikus rendezés és DAG legrövidebb út algoritmus végrehajtása',
      nodeStartFinishTimes: 'Csúcs kezdő- és befejezési idők',
      dagShortestPath: 'DAG legrövidebb út algoritmus',
      alertEmpty: 'A gráf üres. Kérjük, adjon hozzá csúcsokat és éleket a topologikus rendezés előtt.',
      alertCycle: 'A gráfban van kör. Kérjük, távolítsa el a ciklusokat, majd próbálja újra.',
      alertSameNode: 'Ez a csúcs már létezik.',
      alertRemoveEdge: 'Nem létezik ilyen él.',
      result: 'Eredmény:',
      legend: 'Kezdő csúcs',
      TopologySort: 'Topológiai rendezés',
      removeEdge: 'Él eltávolítása',
    },
  };

  const handleLanguageToggle = () => {
    setLanguage((prevLang) => (prevLang === 'EN' ? 'HU' : 'EN'));
  };

  const addNode = () => {
    if (nodeName.trim() === '') return;

    const newNode = {
      id: nextNodeId.toString(), 
      name: nodeName,
    };

    if (nodes.some((node) => node.name === newNode.name)) {
      alert(translations[language].alertSameNode);
      return;
    } else {
      setNodes([...nodes, newNode]);
      setNextNodeId((prevId) => prevId + 1); 
    }
    setNodeName('');
  };

  const removeNode = () => {
    if (nodeToRemove === '') return;

    const nodeIdToRemove = nodes.find((node) => node.name === nodeToRemove)?.id;

    if (nodeIdToRemove) {
      const updatedNodes = nodes.filter((node) => node.id !== nodeIdToRemove);
      const updatedEdges = edges.filter(
        (edge) => edge.from !== nodeIdToRemove && edge.to !== nodeIdToRemove
      );
      setNodes(updatedNodes);
      setEdges(updatedEdges);
      setNodeToRemove('');
    }
  };

  const addEdge = () => {
    if (targetNode === '' || edgeValue === '') return;
  
    const targetNodeId = nodes.find((node) => node.name === targetNode)?.id;
    const sourceNodeId = sourceNode === '' ? null : nodes.find((node) => node.name === sourceNode)?.id;
  
    if (sourceNodeId === targetNodeId) {
      alert(translations[language].addEdgeAlert1);
      return;
    }

    const edgeExists = edges.some(
      (edge) => edge.from === sourceNodeId && edge.to === targetNodeId
    );

    if (edgeExists) {
      alert(translations[language].addEdgeAlert2);
      return;
    }
  
    if (targetNodeId) {
      const newEdge = {
        from: sourceNodeId,
        to: targetNodeId,
        value: edgeValue.trim() === '' ? '0' : edgeValue,
      };
  
      setEdges([...edges, newEdge]);
      setSourceNode(''); 
      setTargetNode('');
      setEdgeValue('0');
    }
  };  

  const removeEdge = () => {
    const { from, to } = edgeToRemove;
    if (from === '' || to === '') return;

    const fromNodeId = nodes.find((node) => node.name === from)?.id;
    const toNodeId = nodes.find((node) => node.name === to)?.id;

    if (fromNodeId && toNodeId) {
      const edgeExists = edges.some((edge) => edge.from === fromNodeId && edge.to === toNodeId);
      
      if (edgeExists) {
          setEdges(edges.filter((edge) => edge.from !== fromNodeId || edge.to !== toNodeId));
          setEdgeToRemove({ from: '', to: '' });
      } else {
          alert(translations[language].alertRemoveEdge);
      }
    }
  };
 
  const updateGraphRepresentation = () => {
    const nodeEdgesMap = new Map();
  
    edges.forEach(edge => {
      const fromNode = nodes.find(node => node.id === edge.from);
      const toNode = nodes.find(node => node.id === edge.to);
      const edgeString = `${toNode.name}, ${edge.value}`;
  
      if (nodeEdgesMap.has(fromNode.name)) {
        nodeEdgesMap.get(fromNode.name).push(edgeString);
      } else {
        nodeEdgesMap.set(fromNode.name, [edgeString]);
      }
    });
  
    const sortedGraph = Array.from(nodeEdgesMap)
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([fromNode, edges]) => {
        const sortedEdges = edges.sort((a, b) => {
          const [nodeA, valueA] = a.split(', ');
          const [nodeB, valueB] = b.split(', ');
          return valueA - valueB || nodeA.localeCompare(nodeB);
        });
        return `${fromNode} → ${sortedEdges.join(' ; ')}`;
      })
      .join('\n');
  
    setGraphRepresentation(sortedGraph);
  };

  useEffect(() => {
    updateGraphRepresentation();
  }, [nodes, edges]);

  useEffect(() => {
    if (cyRef.current) {
      const cy = cytoscape({
        container: cyRef.current,
        elements: [
          ...nodes.map((node, index) => {
            const nodeTimes = times[node.name];
            const textMarginY = nodeTimes ? -15 : 0;
  
            return {
              data: { id: node.id, label: node.name },
              style: {
                'background-color': index === 0 ? 'gray' : '#0074D9', 
                'text-margin-y': textMarginY, 
              },
            };
          }),
          ...edges.map(edge => ({
            data: { source: edge.from, target: edge.to, value: edge.value }
          }))
        ],
        style: [
          {
            selector: 'node',
            style: {
              shape: 'ellipse',
              label: 'data(label)',
              'text-valign': 'center',
              'text-halign': 'center',
              'text-wrap': 'wrap',
            }
          },
          {
            selector: 'edge',
            style: {
              width: 2,
              'line-color': '#ccc',
              'target-arrow-color': '#ccc',
              'target-arrow-shape': 'triangle',
              'curve-style': 'bezier',
              label: 'data(value)',
              'text-justification': 'left',
              'text-margin-y': '10px',
            }
          },
        ],
        layout: {
          name: 'cose',
          padding: 10,
        },
      });
  
      nodes.forEach(node => {
        const nodeTimes = times[node.name];
        if (nodeTimes) {
          const nodeElement = cy.getElementById(node.id);
          nodeElement.data('label', `${nodeTimes.start}/${nodeTimes.finish}\n\n${node.name}`);
        }
      });
  
      return () => cy.destroy();
    }
  }, [nodes, edges, times]);

  const topologicalSort = () => {
    let time = 0;
    const visited = {};
    const startFinishTimes = {};
    const nodeGraph = {};
    const inStack = {}; 

    if (nodes.length === 0) {
      alert(translations[language].alertEmpty);
      return; 
    }

    nodes.forEach((node) => {
      nodeGraph[node.name] = [];
      visited[node.name] = false; 
      inStack[node.name] = false; 
    });
    edges.forEach((edge) => {
      const fromNode = nodes.find((node) => node.id === edge.from);
      const toNode = nodes.find((node) => node.id === edge.to);
      nodeGraph[fromNode.name].push(toNode.name);
    });

    const sorted = [];
    let hasCycle = false; 

    const dfs = (node) => {
      visited[node] = true;
      inStack[node] = true; 
      time += 1;
      startFinishTimes[node] = { start: time };

      nodeGraph[node].forEach((neighbor) => {
        if (!visited[neighbor]) {
          dfs(neighbor);
        } else if (inStack[neighbor]) {
          hasCycle = true; 
        }
      });

      time += 1;
      startFinishTimes[node].finish = time;
      inStack[node] = false; 
      sorted.push(node);
    };

    // Start from the base node 
    //dfs(nodes[0]?.name || 'A');
    dfs(nodes[0]?.name);

    if (hasCycle) {
      alert(translations[language].alertCycle);
      return; 
    }

    setSortedNodes(sorted.reverse());
    setTimes(startFinishTimes);
    setResultsVisible(true);
  };

  const dagShortestPath = () => {
    if (sortedNodes.length === 0) {
      return { distances: {}, predecessors: {} }; 
    }
  
    const distances = {};
    const predecessors = {};
    nodes.forEach(node => {
      distances[node.name] = Infinity;
      predecessors[node.name] = '⊗'; 
    });
    distances[nodes[0].name] = 0; 
  
    sortedNodes.forEach(node => {
      edges.forEach(edge => {
        const fromNode = nodes.find(n => n.id === edge.from);
        const toNode = nodes.find(n => n.id === edge.to);
  
        if (fromNode && toNode && fromNode.name === node && distances[fromNode.name] !== Infinity) {
          const newDist = distances[fromNode.name] + parseFloat(edge.value);
          if (newDist < distances[toNode.name]) {
            distances[toNode.name] = newDist;
            predecessors[toNode.name] = fromNode.name; 
          }
        }
      });
    });
  
    return { distances, predecessors };
  };    

  const renderShortestPathTable = () => {
    const { distances, predecessors } = dagShortestPath();

    const edgeMap = {};
    edges.forEach(edge => {
      const fromNode = nodes.find(node => node.id === edge.from);
      const toNode = nodes.find(node => node.id === edge.to);
      if (fromNode && toNode) {
        if (!edgeMap[fromNode.name]) {
          edgeMap[fromNode.name] = [];
        }
        edgeMap[fromNode.name].push({ to: toNode.name, value: edge.value });
      }
    });

    const columnMinimums = {};
    nodes.forEach(node => {
      columnMinimums[node.name] = Infinity; 
    });

    return (
      <table className="table" style={{ fontSize: '24px' }}>
        <thead>
          <tr>
            <th></th>
            {nodes.map(node => (
              <th key={node.name}>{node.name}</th> 
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td> </td> 
            {nodes.map(node => (
              <td key={node.name}>
                {sortedNodes[0] === node.name ? 0 : '∞'}
              </td>
            ))}
          </tr>

          {sortedNodes.slice(0, -1).map(sortedNode => {
            return (
              <tr key={sortedNode}>
                <td>
                  {sortedNode} : {distances[sortedNode] === ' ' ? ' ' : distances[sortedNode]}
                </td> 
                {nodes.map(node => {
                  const edges = edgeMap[sortedNode] || [];
                  const edge = edges.find(e => e.to === node.name);
                  let displayValue = edge ? distances[sortedNode] + Number(edge.value) : ' ';

                  if (edge && distances[sortedNode] !== Infinity) {
                    if (Number(displayValue) < columnMinimums[node.name]) {
                      columnMinimums[node.name] = Number(displayValue);
                    } else {
                      displayValue = ' '; 
                    }
                  }

                  if (displayValue !== ' ') {
                      displayValue = displayValue + ' ' + sortedNode;
                  }

                  return (
                    <td>
                      {displayValue}
                    </td>
                  );
                })}
              </tr>
            );
          })}

          <tr>
            <td>{translations[language].result}</td>
            {nodes.map(node => (
              <td key={node.name}>
                {distances[node.name] === Infinity ? '∞' : distances[node.name] + ' ' + predecessors[node.name]}
              </td>
            ))}
          </tr>

        </tbody>
      </table>
    );
  };

  const getUsedEdges = () => {
    const { predecessors } = dagShortestPath();
    const usedEdges = [];
    
    for (let nodeName in predecessors) {
      if (predecessors[nodeName] !== '⊗') {
        const fromNode = predecessors[nodeName];
        const edgeValue = edges.find(edge => {
          const fromNodeId = nodes.find(node => node.name === fromNode)?.id;
          const toNodeId = nodes.find(node => node.name === nodeName)?.id;
          return edge.from === fromNodeId && edge.to === toNodeId;
        });
        
        if (edgeValue) {
          usedEdges.push(edgeValue);
        }
      }
    }
  
    return usedEdges; 
  };

  const renderShortestPathGraph = () => {
    const { distances } = dagShortestPath();
    const usedEdges = getUsedEdges();

    const nodePositions = {};
    const svgWidth = 800; 
    const svgHeight = 500;
    const radius = 20; 
    const labelOffset = 40; 

    const angleStep = (2 * Math.PI) / nodes.length;
    nodes.forEach((node, index) => {
        const angle = index * angleStep;
        nodePositions[node.name] = {
            x: svgWidth / 2 + (svgWidth / 3) * Math.cos(angle),
            y: svgHeight / 2 + (svgHeight / 3) * Math.sin(angle),
            angle, 
        };
    });

    return (
        <svg width={svgWidth} height={svgHeight} style={{ border: '1px solid #ccc', borderRadius: '15px' }}>
            <defs>
                <marker
                    id="arrowhead"
                    markerWidth="10"
                    markerHeight="7"
                    refX="18"
                    refY="3.5"
                    orient="auto"
                    markerUnits="strokeWidth"
                    strokeLinecap="round"
                >
                    <polygon points="0 0, 10 3.5, 0 7" fill="black" />
                </marker>
            </defs>

            {usedEdges.map((edge, index) => {
                const fromNode = nodes.find((n) => n.id === edge.from)?.name || 'Base Node';
                const toNode = nodes.find((n) => n.id === edge.to)?.name;

                const fromPos = nodePositions[fromNode];
                const toPos = nodePositions[toNode];

                return (
                    <g key={index}>
                        <line
                            x1={fromPos.x}
                            y1={fromPos.y}
                            x2={toPos.x}
                            y2={toPos.y}
                            stroke="black"
                            strokeWidth="2"
                            markerEnd="url(#arrowhead)" 
                        />
                        <text
                            x={(fromPos.x + toPos.x) / 2} 
                            y={(fromPos.y + toPos.y) / 2 + 30}
                            textAnchor="middle"
                            dominantBaseline="middle"
                            fill="black"
                            fontSize="24px"
                        >
                            {edge.value}
                        </text>
                    </g>
                );
            })}

            {nodes.map((node) => {
                const pos = nodePositions[node.name];

                const labelX = pos.x + labelOffset * Math.cos(pos.angle);
                const labelY = pos.y + labelOffset * Math.sin(pos.angle);

                return (
                    <g key={node.id}>
                        <circle cx={pos.x} cy={pos.y} r={radius} fill={node.id === '1' ? 'gray' : '#0074D9'} />

                        <text
                            x={labelX}
                            y={labelY}
                            textAnchor="middle"
                            dominantBaseline="middle"
                            fill="black"
                            fontSize="22px"
                        >
                            {distances[node.name] === Infinity ? '∞' : distances[node.name]}
                        </text>

                        <text
                            x={pos.x}
                            y={pos.y}
                            textAnchor="middle"
                            dominantBaseline="middle"
                            fill="white"
                            fontSize="12px"
                        >
                            {node.name}
                        </text>
                    </g>
                );
            })}
        </svg>
    );
  };

  return (
    <div style={{ maxWidth: '100%', padding: '10px' }}>
      <button
        onClick={handleLanguageToggle}
        style={{
          position: 'fixed',
          top: '10px',
          right: '10px',
          zIndex: 1000,
          padding: '5px 10px',
          border: '1px solid #ccc',
          borderRadius: '5px',
        }}
      >
        {language === 'EN' ? 'Magyar' : 'English'}
      </button>
  
      <h1 style={{ textAlign: 'center' }}>{translations[language].title}</h1>
  
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
        <input
          type="text"
          value={nodeName}
          onChange={(e) => setNodeName(e.target.value)}
          placeholder={translations[language].nodeName}
          style={{ flex: '1 1 auto', minWidth: '200px' }}
        />
        <button onClick={addNode} style={{ flex: '0 1 auto' }}>
          {translations[language].addNode}
        </button>
      </div>
  
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginTop: '10px' }}>
        <select value={sourceNode} onChange={(e) => setSourceNode(e.target.value)} style={{ flex: '1 1 auto', minWidth: '150px' }}>
          <option value="" disabled>{translations[language].selectSource}</option>
          {nodes.map((node) => (
            <option key={node.id} value={node.name}>
              {node.name}
            </option>
          ))}
        </select>
        <select value={targetNode} onChange={(e) => setTargetNode(e.target.value)} style={{ flex: '1 1 auto', minWidth: '150px' }}>
          <option value="" disabled>{translations[language].selectTarget}</option>
          {nodes.map((node) => (
            <option key={node.id} value={node.name}>
              {node.name}
            </option>
          ))}
        </select>
        <input
          type="number"
          value={edgeValue}
          onChange={(e) => setEdgeValue(e.target.value)}
          style={{ flex: '1 1 auto', minWidth: '80px' }}
        />
        <button onClick={addEdge} style={{ flex: '0 1 auto' }}>
          {translations[language].addEdge}
        </button>
      </div>
  
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginTop: '10px' }}>
        <select value={nodeToRemove} onChange={(e) => setNodeToRemove(e.target.value)} style={{ flex: '1 1 auto', minWidth: '200px' }}>
          <option value="" disabled>{translations[language].selectRemove}</option>
          {nodes.map((node) => (
            <option key={node.id} value={node.name}>
              {node.name}
            </option>
          ))}
        </select>
        <button onClick={removeNode} style={{ flex: '0 1 auto' }}>
          {translations[language].removeNode}
        </button>
      </div>

      <select value={edgeToRemove.from} onChange={(e) => setEdgeToRemove({ ...edgeToRemove, from: e.target.value })}>
        <option value="" disabled>{translations[language].selectSource}</option>
        {nodes.map((node) => (
          <option key={node.id} value={node.name}>{node.name}</option>
        ))}
      </select>
      
      <select value={edgeToRemove.to} onChange={(e) => setEdgeToRemove({ ...edgeToRemove, to: e.target.value })}>
        <option value="" disabled>{translations[language].selectTarget}</option>
        {nodes.map((node) => (
          <option key={node.id} value={node.name}>{node.name}</option>
        ))}
      </select>
      <button onClick={removeEdge}>{translations[language].removeEdge}</button>
  
      <h3 style={{ textAlign: 'center' }}>{translations[language].graphRepresentation}</h3>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
        <textarea
          rows={4}
          cols={50}
          value={graphRepresentation}
          readOnly
          style={{ resize: 'none', width: '100%' }}
        />
      </div>
  
      <h3 style={{ textAlign: 'center' }}>{translations[language].graphVisualization}</h3>
      <div ref={cyRef} style={{ width: '100%', height: '500px', maxWidth: '900px', margin: '0 auto' }} />
  
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '10px' }}>
        <div
          style={{
            width: '15px',
            height: '15px',
            backgroundColor: 'gray',
            borderRadius: '50%',
            marginRight: '5px',
          }}
        />
        {translations[language].legend}
      </div>
  
      <button className="buttonTopology" onClick={topologicalSort} style={{ margin: '10px auto', display: 'block' }}>
        {translations[language].perfromTopologicalSort}
      </button>
  
      {resultsVisible && (
        <div>
          <h3>{translations[language].TopologySort}</h3>
          <div style={{ marginTop: '5px' }}>
            <textarea
              rows={4}
              cols={50}
              value={sortedNodes.join(', ')}
              readOnly
              style={{ resize: 'none' }}
            />
          </div>

          <h3>{translations[language].nodeStartFinishTimes}</h3>
          <ul>
            {Object.entries(times).map(([node, { start, finish }]) => (
              <li key={node}>
                {node}: {start}/{finish}
              </li>
            ))}
          </ul>

          <h3>{translations[language].dagShortestPath}</h3>
          {renderShortestPathTable()}

        {renderShortestPathGraph()}

      </div>
      )}
    </div>
  );
};

export default GraphBox;