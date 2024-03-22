import sys
import json

if len(sys.argv) >= 2:
    with open(sys.argv[1], "r") as file:
        data = json.load(file)
        counter = 0

        for simulation in data["simulation"]["demands"]:
            simulation["inUse"] = []

        for time in range(1, data["simulation"]["duration"] + 1):
            for simulation in data["simulation"]["demands"]:
                if simulation["end-time"] == time:
                    if not simulation["success"]:
                        break
                    for i in simulation["inUse"]:
                        data["links"][i]["capacity"] += simulation["demand"]
                    counter += 1
                    print("%d. igény felszabadítás: %s<->%s st:%d" % (
                    counter, simulation["end-points"][0], simulation["end-points"][1], time))
                elif simulation["start-time"] == time:
                    possible_circuits = [circ for circ in data["possible-circuits"] if
                                         (circ[0] == simulation["end-points"][0] and circ[-1] == simulation["end-points"][1])]
                    simulation["success"] = False
                    for circuit in possible_circuits:
                        if simulation["success"]:
                            break
                        simulation["success"] = True
                        for ep_from, ep_to in zip(circuit, circuit[1:]):
                            for link_index, link in enumerate(data["links"]):
                                if link["points"] in [[ep_from, ep_to], [ep_to, ep_from]]:
                                    if link["capacity"] < simulation["demand"]:
                                        simulation["success"] = False
                                    else:
                                        simulation["inUse"].append(link_index)
                        if simulation["success"]:
                            for i in simulation["inUse"]:
                                data["links"][i]["capacity"] -= simulation["demand"]
                    counter += 1
                    print("%d. igény foglalás: %s<->%s st:%d - %s" % (
                    counter, simulation["end-points"][0], simulation["end-points"][1], time,
                    "sikeres" if simulation["success"] else "sikertelen"))
